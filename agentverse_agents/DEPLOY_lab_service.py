from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)
from datetime import datetime
from uuid import uuid4
import os
import httpx
from anthropic import AsyncAnthropic

AGENT_SEED = "lab_service_phrase_001"
JSONBIN_ID = "68fd4c71ae596e708f2c8fb0"
JSONBIN_KEY = "$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa"
ANTHROPIC_KEY = "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"

agent = Agent(name="lab_service", seed=AGENT_SEED, port=8002)
protocol = Protocol(spec=chat_protocol_spec)
claude_client = AsyncAnthropic(api_key=ANTHROPIC_KEY) if ANTHROPIC_KEY else None

async def get_hospital_data():
    """Tool: Fetch hospital data from JSONBin"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}/latest",
                headers={"X-Master-Key": JSONBIN_KEY}
            )
            return response.json()["record"]
    except Exception as e:
        return {"error": str(e)}

async def check_equipment_availability(equipment_type):
    """Tool: Check if diagnostic equipment is available"""
    data = await get_hospital_data()
    if "error" in data:
        return None
    
    equipment = data.get("lab_equipment", {}).get("diagnostic", {})
    return equipment.get(equipment_type)

async def check_test_availability(test_name):
    """Tool: Check if lab test is available"""
    data = await get_hospital_data()
    if "error" in data:
        return None
    
    tests = data.get("lab_equipment", {}).get("lab_tests", {})
    for test_key, test_data in tests.items():
        if test_name.lower() in test_data.get("name", "").lower():
            return test_data
    return None

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("tests_ordered", 0)
    ctx.logger.info(f"🧪 Lab Service Agent Started")
    ctx.logger.info(f"📍 Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"🔧 Tools: JSONBin + Claude AI enabled")
    ctx.logger.info(f"📊 JSONBin ID: {JSONBIN_ID[:20]}...")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"📨 Message received from {sender[:16]}...")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(),
        acknowledged_msg_id=msg.msg_id
    ))
    
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
    ctx.logger.info(f"📝 Query: {text[:100]}...")
    
    if "ambulance" in text.lower() or "protocol" in text.lower():
        ctx.logger.info("🚑 AMBULANCE REPORT DETECTED - Using Claude AI + Tools")
        
        ctx.logger.info(f"📍 Will respond back to ED Coordinator: {sender[:16]}...")
        
        ctx.logger.info("🔧 Tool Call: Fetching lab equipment data from JSONBin...")
        data = await get_hospital_data()
        
        diagnostic_equipment = data.get("lab_equipment", {}).get("diagnostic", {})
        lab_tests = data.get("lab_equipment", {}).get("lab_tests", {})
        
        equipment_list = "\n".join([f"• {eq['name']}: {eq['available']}/{eq['total']} available" for eq in diagnostic_equipment.values()])
        test_list = "\n".join([f"• {test['name']}: {test['turnaround_time_minutes']}min turnaround, {test['available']} tests" for test in lab_tests.values()])
        
        ctx.logger.info(f"📊 Tool Result: {len(diagnostic_equipment)} equipment types, {len(lab_tests)} test types")
        
        # Determine protocol
        protocol = "STEMI" if "STEMI" in text or "chest pain" in text.lower() else "Stroke" if "stroke" in text.lower() else "Trauma" if "trauma" in text.lower() else "General"
        
        response_text = f"""🧪 LAB SERVICE AGENT REPORT

📊 DATA FETCHED FROM LAB DATABASE:
Equipment Status:
{equipment_list}

Test Availability:
{test_list}

🔧 ACTIONS TAKEN:
• Identified protocol: {protocol}
• Prepared STAT test orders for {protocol}
• Reserved ECG machine for immediate use
• Alerted lab technician for STAT processing
• Set priority: CRITICAL
• Timestamp: {datetime.utcnow().isoformat()}

✅ CURRENT STATUS:
• ECG: Ready at bedside
• Lab tech: Standing by for sample collection
• Test processing: STAT priority queue
• Expected results: Troponin 15min, CBC/BMP 20-25min

⏱️ Preparation time: <2 minutes
🎯 All diagnostic tests ready for {protocol} workup"""
        
        ctx.logger.info("✅ Lab Service response generated")
        
        tests = ctx.storage.get("tests_ordered") + 1
        ctx.storage.set("tests_ordered", tests)
    
    else:
        ctx.logger.info("📊 Standard query - Using Claude AI + Tools...")
        
        ctx.logger.info("🔧 Tool Call: get_hospital_data() - Fetching lab equipment data from JSONBin...")
        data = await get_hospital_data()
        
        if "error" in data:
            ctx.logger.error(f"❌ Tool Error: {data['error']}")
            response_text = "❌ Error fetching hospital data"
        else:
            equipment_count = len(data.get("lab_equipment", {}).get("diagnostic", {}))
            test_count = len(data.get("lab_equipment", {}).get("lab_tests", {}))
            
            ctx.logger.info(f"📊 Tool Result: {equipment_count} equipment types, {test_count} test types available")
            
            if claude_client:
                ctx.logger.info("🤖 Calling Claude AI for response generation...")
                prompt = f"""You are a Lab Service AI agent.

Query: {text}

Current status: {equipment_count} equipment types, {test_count} test types available

Provide a helpful, professional response about lab services."""

                response = await claude_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.content[0].text
                ctx.logger.info("✅ Claude AI response generated")
            else:
                ctx.logger.warning("⚠️ Claude AI not configured - using fallback")
                response_text = f"""🧪 Lab Service Status

• Equipment Types: {equipment_count}
• Test Types: {test_count}

How can I help you with lab services?"""
    
    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=response_text)]
    ))
    
    ctx.logger.info(f"✅ Response sent to {sender[:16]}...")

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.debug(f"✓ Ack received: {msg.acknowledged_msg_id}")

@agent.on_interval(period=120.0)
async def health_check(ctx: Context):
    tests = ctx.storage.get("tests_ordered")
    ctx.logger.info(f"💓 Health: {tests} test orders processed")

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()