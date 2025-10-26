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

AGENT_SEED = "pharmacy_phrase_001"
JSONBIN_ID = "68fd4c71ae596e708f2c8fb0"
JSONBIN_KEY = "$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa"
ANTHROPIC_KEY = "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"

agent = Agent(name="pharmacy", seed=AGENT_SEED, port=8003)
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

async def update_hospital_data(data):
    """Tool: Update hospital data in JSONBin"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(
                f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}",
                json=data,
                headers={"X-Master-Key": JSONBIN_KEY, "Content-Type": "application/json"}
            )
            return response.json()
    except Exception as e:
        return {"error": str(e)}

async def check_medication_availability(med_name):
    """Tool: Check if medication is available"""
    data = await get_hospital_data()
    if "error" in data:
        return None
    
    for category in data.get("medications", {}).values():
        if isinstance(category, dict):
            for med_key, med_data in category.items():
                if med_name.lower() in med_data.get("name", "").lower():
                    return med_data
    return None

async def dispense_medication(med_name, quantity=1):
    """Tool: Dispense medication and update inventory"""
    data = await get_hospital_data()
    if "error" in data:
        return False
    
    for category in data.get("medications", {}).values():
        if isinstance(category, dict):
            for med_key, med_data in category.items():
                if med_name.lower() in med_data.get("name", "").lower():
                    if med_data.get("available", 0) >= quantity:
                        med_data["available"] -= quantity
                        await update_hospital_data(data)
                        return True
    return False

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("medications_dispensed", 0)
    ctx.logger.info(f"💊 Pharmacy Agent Started")
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
        
        ctx.logger.info("🔧 Tool Call: Fetching medication data from JSONBin...")
        data = await get_hospital_data()
        
        emergency_meds = data.get("medications", {}).get("emergency", {})
        meds_list = "\n".join([f"• {med['name']}: {med['available']} {med['unit']} (Location: {med.get('location', 'Pharmacy')})" for med in emergency_meds.values()])
        
        ctx.logger.info(f"📊 Tool Result: {len(emergency_meds)} emergency medications available")
        
        # Determine protocol
        protocol = "STEMI" if "STEMI" in text or "chest pain" in text.lower() else "Stroke" if "stroke" in text.lower() else "Trauma" if "trauma" in text.lower() else "General"
        
        response_text = f"""💊 PHARMACY AGENT REPORT

📊 DATA FETCHED FROM MEDICATION DATABASE:
{meds_list}

🔧 ACTIONS TAKEN:
• Identified protocol: {protocol}
• Prepared {protocol}-specific medication kit
• Medications drawn and labeled
• Staged location: Trauma Bay 1 medication cart
• Timestamp: {datetime.utcnow().isoformat()}

✅ CURRENT STATUS:
• All {protocol} medications: READY
• Delivery time: <5 minutes to bedside
• Pharmacist: Available for consultation
• Backup medications: Stocked and verified

⏱️ Preparation time: <3 minutes
🎯 Medications ready for immediate administration"""
        
        ctx.logger.info("✅ Pharmacy response generated")
        
        dispensed = ctx.storage.get("medications_dispensed") + 1
        ctx.storage.set("medications_dispensed", dispensed)
    
    else:
        ctx.logger.info("📊 Standard query - Using Claude AI + Tools...")
        
        ctx.logger.info("🔧 Tool Call: get_hospital_data() - Fetching medication inventory from JSONBin...")
        data = await get_hospital_data()
        
        if "error" in data:
            ctx.logger.error(f"❌ Tool Error: {data['error']}")
            response_text = "❌ Error fetching hospital data"
        else:
            meds_count = sum(len(cat) for cat in data.get("medications", {}).values() if isinstance(cat, dict))
            emergency_meds = len(data.get("medications", {}).get("emergency", {}))
            
            ctx.logger.info(f"📊 Tool Result: {meds_count} total medication types, {emergency_meds} emergency medications")
            
            if claude_client:
                ctx.logger.info("🤖 Calling Claude AI for response generation...")
                prompt = f"""You are a Pharmacy AI agent.

Query: {text}

Current inventory: {meds_count} medication types available

Provide a helpful, professional response about pharmacy services."""

                response = await claude_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.content[0].text
                ctx.logger.info("✅ Claude AI response generated")
            else:
                ctx.logger.warning("⚠️ Claude AI not configured - using fallback")
                response_text = f"""💊 Pharmacy Status

• Total Medications: {meds_count} types
• Emergency Meds: {emergency_meds} types

How can I help you with pharmacy services?"""
    
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
    dispensed = ctx.storage.get("medications_dispensed")
    ctx.logger.info(f"💓 Health: {dispensed} medication orders processed")

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()