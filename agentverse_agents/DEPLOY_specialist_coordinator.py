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

AGENT_SEED = "specialist_coordinator_phrase_001"
JSONBIN_ID = "68fd4c71ae596e708f2c8fb0"
JSONBIN_KEY = "$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa"
ANTHROPIC_KEY = "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"

agent = Agent(name="specialist_coordinator", seed=AGENT_SEED, port=8004)
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

async def get_available_specialists(specialty):
    """Tool: Get available specialists by specialty"""
    data = await get_hospital_data()
    if "error" in data:
        return []
    
    specialists = data.get("specialists", {}).get(specialty, [])
    return [s for s in specialists if s.get("status") == "available"]

async def get_all_specialists_status():
    """Tool: Get status of all specialists"""
    data = await get_hospital_data()
    if "error" in data:
        return {}
    
    return data.get("specialists", {})

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("teams_activated", 0)
    ctx.logger.info(f"👨‍⚕️ Specialist Coordinator Agent Started")
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
        
        ctx.logger.info("🔧 Tool Call: Fetching specialist data from JSONBin...")
        all_specialists = await get_all_specialists_status()
        
        total_specialists = sum(len(specs) for specs in all_specialists.values())
        ctx.logger.info(f"📊 Tool Result: {total_specialists} specialists in database")
        
        if claude_client:
            ctx.logger.info("🤖 Calling Claude AI for specialist team activation...")
            
            specialist_summary = []
            for specialty, doctors in all_specialists.items():
                available = [d for d in doctors if d.get("status") == "available"]
                specialist_summary.append(
                    f"{specialty.title()}: {len(available)}/{len(doctors)} available"
                )
                if available:
                    for doc in available:
                        specialist_summary.append(
                            f"  - {doc['name']} ({doc['specialty']}) - Response time: {doc['response_time_minutes']}min"
                        )
            
            prompt = f"""You are a Specialist Coordinator AI agent in an emergency department.

Ambulance Report: {text}

Available Specialists:
{chr(10).join(specialist_summary)}

Analyze the report and:
1. Identify the protocol (STEMI/Stroke/Trauma)
2. Determine which specialist team to activate
3. Select the best available specialist
4. Provide estimated response time
5. Confirm team activation status

Be specific with doctor names and response times."""

            response = await claude_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response.content[0].text
            ctx.logger.info("✅ Claude AI response generated")
            
            teams = ctx.storage.get("teams_activated") + 1
            ctx.storage.set("teams_activated", teams)
        else:
            response_text = "👨‍⚕️ SPECIALIST COORDINATOR RESPONSE\n\nTeam activated"
    
    else:
        ctx.logger.info("📊 Standard query - Using Claude AI + Tools...")
        
        ctx.logger.info("🔧 Tool Call: get_hospital_data() - Fetching specialist data from JSONBin...")
        data = await get_hospital_data()
        
        if "error" in data:
            ctx.logger.error(f"❌ Tool Error: {data['error']}")
            response_text = "❌ Error fetching hospital data"
        else:
            specialists = data.get("specialists", {})
            total = sum(len(s) for s in specialists.values())
            available = sum(len([d for d in s if d.get("status") == "available"]) for s in specialists.values())
            
            ctx.logger.info(f"📊 Tool Result: {available}/{total} specialists available")
            
            if claude_client:
                ctx.logger.info("🤖 Calling Claude AI for response generation...")
                prompt = f"""You are a Specialist Coordinator AI agent.

Query: {text}

Current status: {available}/{total} specialists available

Provide a helpful, professional response about specialist services."""

                response = await claude_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.content[0].text
                ctx.logger.info("✅ Claude AI response generated")
            else:
                ctx.logger.warning("⚠️ Claude AI not configured - using fallback")
                response_text = f"""👨‍⚕️ Specialist Coordinator Status

• Available Specialists: {available}/{total}

How can I help you with specialist coordination?"""
    
    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=response_text)]
    ))
    
    ctx.logger.info(f"✅ Response sent")

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.debug(f"✓ Ack received: {msg.acknowledged_msg_id}")

@agent.on_interval(period=120.0)
async def health_check(ctx: Context):
    teams = ctx.storage.get("teams_activated")
    ctx.logger.info(f"💓 Health: {teams} teams activated")

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()