"""
Resource Manager Agent - ASI:One Compatible
Manages beds, equipment, and ED resources with Chat Protocol
"""

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

AGENT_SEED = os.getenv("RESOURCE_MANAGER_SEED", "resource_manager_phrase_001")

agent = Agent(name="resource_manager", seed=AGENT_SEED, port=8001)
protocol = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("beds_total", 15)
    ctx.storage.set("beds_available", 10)
    ctx.storage.set("equipment_total", 25)
    ctx.storage.set("equipment_available", 18)
    ctx.storage.set("rooms_total", 8)
    ctx.storage.set("rooms_available", 5)
    ctx.logger.info(f"🛏️ Resource Manager started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
    response_text = await process_resource_query(ctx, text.lower())
    await ctx.send(sender, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), 
                                       content=[TextContent(type="text", text=response_text)]))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

async def process_resource_query(ctx: Context, query: str) -> str:
    if any(word in query for word in ["bed", "beds"]):
        available = ctx.storage.get("beds_available")
        total = ctx.storage.get("beds_total")
        return f"""🛏️ Bed Availability:
• Available: {available}/{total} beds
• Utilization: {((total-available)/total*100):.0f}%
• Status: {'Available' if available > 3 else 'Limited'}"""
    elif any(word in query for word in ["equipment"]):
        available = ctx.storage.get("equipment_available")
        total = ctx.storage.get("equipment_total")
        return f"""🔧 Equipment Status:
• Available: {available}/{total}
• Status: {'Ready' if available > 10 else 'Limited'}"""
    elif any(word in query for word in ["room", "rooms"]):
        available = ctx.storage.get("rooms_available")
        total = ctx.storage.get("rooms_total")
        return f"""🚪 Room Availability:
• Available: {available}/{total}
• Status: {'Available' if available > 2 else 'Limited'}"""
    else:
        return """🛏️ Resource Manager

I manage ED resources:
• Beds (ICU, regular, observation)  
• Equipment
• Exam rooms

Ask: "Are beds available?" or "Equipment status?"""

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()