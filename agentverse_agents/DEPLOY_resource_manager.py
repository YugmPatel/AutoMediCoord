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

AGENT_SEED = "resource_manager_phrase_001"
JSONBIN_ID = "68fd4c71ae596e708f2c8fb0"
JSONBIN_KEY = "$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa"
ANTHROPIC_KEY = "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"

agent = Agent(name="resource_manager", seed=AGENT_SEED, port=8001)
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

async def get_overall_capacity():
    """Tool: Get overall ED capacity and resource status"""
    data = await get_hospital_data()
    if "error" in data:
        return None
    
    beds = data.get("beds", {})
    total_beds = sum(len(bed_list) for bed_list in beds.values())
    available_beds = sum(
        len([b for b in bed_list if b.get("status") == "available"])
        for bed_list in beds.values()
    )
    
    staff = data.get("staff", {})
    equipment = data.get("lab_equipment", {}).get("diagnostic", {})
    
    return {
        "beds": {"available": available_beds, "total": total_beds},
        "staff": staff,
        "equipment": equipment,
        "current_status": data.get("current_status", {})
    }

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("resources_allocated", 0)
    ctx.logger.info(f"📊 Resource Manager Agent Started")
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
        
        ctx.logger.info("🔧 Tool Call: Fetching overall capacity from JSONBin...")
        capacity = await get_overall_capacity()
        
        if capacity:
            ctx.logger.info(f"📊 Tool Result: {capacity['beds']['available']}/{capacity['beds']['total']} beds available")
            ctx.logger.info(f"📊 Staff: {capacity['staff']['nurses']['available']} nurses, {capacity['staff']['physicians']['available']} physicians available")
        
        if claude_client and capacity:
            ctx.logger.info("🤖 Calling Claude AI for resource allocation...")
            
            prompt = f"""You are a Resource Manager AI agent in an emergency department.

Ambulance Report: {text}

Current Resources:
- Beds: {capacity['beds']['available']}/{capacity['beds']['total']} available
- Nurses: {capacity['staff']['nurses']['available']}/{capacity['staff']['nurses']['on_duty']} available
- Physicians: {capacity['staff']['physicians']['available']}/{capacity['staff']['physicians']['on_duty']} available
- Technicians: {capacity['staff']['technicians']['available']}/{capacity['staff']['technicians']['on_duty']} available
- ED Capacity: {capacity['current_status'].get('ed_capacity_percent', 0)}%
- System Load: {capacity['current_status'].get('system_load', 'unknown')}

Analyze the report and:
1. Identify the protocol (STEMI/Stroke/Trauma)
2. Allocate appropriate resources (bed, staff, equipment)
3. Confirm availability
4. Provide resource allocation summary
5. Flag any resource constraints

Be specific about which resources are allocated."""

            response = await claude_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response.content[0].text
            ctx.logger.info("✅ Claude AI response generated")
            
            allocated = ctx.storage.get("resources_allocated") + 1
            ctx.storage.set("resources_allocated", allocated)
        else:
            response_text = "📊 RESOURCE MANAGER RESPONSE\n\nResources allocated"
    
    else:
        ctx.logger.info("📊 Standard query - Using Claude AI + Tools...")
        
        ctx.logger.info("🔧 Tool Call: get_overall_capacity() - Fetching overall ED capacity from JSONBin...")
        capacity = await get_overall_capacity()
        
        if capacity is None:
            ctx.logger.error("❌ Tool Error: Failed to fetch capacity data")
            response_text = "❌ Error fetching hospital data"
        else:
            beds_available = capacity['beds']['available']
            beds_total = capacity['beds']['total']
            ed_capacity = capacity['current_status'].get('ed_capacity_percent', 0)
            
            ctx.logger.info(f"📊 Tool Result: {beds_available}/{beds_total} beds available, {ed_capacity}% ED capacity")
            
            if claude_client:
                ctx.logger.info("🤖 Calling Claude AI for response generation...")
                prompt = f"""You are a Resource Manager AI agent.

Query: {text}

Current capacity: {beds_available} beds available, {ed_capacity}% capacity

Provide a helpful, professional response about resource management."""

                response = await claude_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.content[0].text
                ctx.logger.info("✅ Claude AI response generated")
            else:
                ctx.logger.warning("⚠️ Claude AI not configured - using fallback")
                response_text = f"""📊 Resource Manager Status

• Beds Available: {beds_available}/{beds_total}
• ED Capacity: {ed_capacity}%

How can I help you with resource management?"""
    
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
    allocated = ctx.storage.get("resources_allocated")
    ctx.logger.info(f"💓 Health: {allocated} resource allocations")

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()