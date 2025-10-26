"""
Bed Management Agent - ASI:One Compatible
Manages bed assignments with Chat Protocol
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

AGENT_SEED = os.getenv("BED_MANAGEMENT_SEED", "bed_management_phrase_001")

agent = Agent(name="bed_management", seed=AGENT_SEED, port=8005)
protocol = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("icu_total", 10)
    ctx.storage.set("icu_available", 3)
    ctx.storage.set("step_down_total", 8)
    ctx.storage.set("step_down_available", 4)
    ctx.storage.set("med_surg_total", 20)
    ctx.storage.set("med_surg_available", 12)
    ctx.storage.set("observation_total", 5)
    ctx.storage.set("observation_available", 3)
    ctx.logger.info(f"🛏️ Bed Management started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
    response_text = await process_bed_query(ctx, text.lower())
    await ctx.send(sender, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(),
                                       content=[TextContent(type="text", text=response_text)]))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

async def process_bed_query(ctx: Context, query: str) -> str:
    # 🚑 AMBULANCE REPORT RESPONSE
    if any(word in query for word in ["ambulance", "incoming", "protocol", "action required"]):
        protocol = "General"
        if "STEMI" in query or "chest pain" in query.lower():
            protocol = "STEMI"
            bed = "Cardiac ICU Bed 3"
            prep = "Cardiac monitoring, defibrillator"
        elif "Stroke" in query or "stroke" in query.lower():
            protocol = "Stroke"
            bed = "Neuro ICU Bed 2"
            prep = "Neuro monitoring, CT access"
        elif "Trauma" in query or "trauma" in query.lower():
            protocol = "Trauma"
            bed = "Trauma Bay 1"
            prep = "Full trauma setup, OR ready"
        else:
            bed = "ED Bed 5"
            prep = "Standard monitoring"
        
        icu_available = ctx.storage.get("icu_available")
        if icu_available > 0:
            ctx.storage.set("icu_available", icu_available - 1)
        
        return f"""✅ BED MANAGEMENT RESPONSE - {protocol} Protocol

🛏️ BED ASSIGNED:
• Bed: {bed} (RESERVED)
• Location: Critical care area
• Equipment: {prep}
• Status: Cleaned and ready

📊 Bed Status:
• ICU Beds: {ctx.storage.get('icu_available')}/{ctx.storage.get('icu_total')}
• Step-Down: {ctx.storage.get('step_down_available')}/{ctx.storage.get('step_down_total')}
• Turnover: Complete
• Housekeeping: Notified for post-care

⏱️ Bed ready for immediate occupancy
🎯 Direct admit pathway activated"""
    
    elif any(word in query for word in ["icu", "intensive"]):
        available = ctx.storage.get("icu_available")
        total = ctx.storage.get("icu_total")
        return f"""🛏️ ICU Beds:
• Available: {available}/{total}
• Utilization: {((total-available)/total*100):.0f}%
• Status: {'Available' if available > 1 else 'Critical'}"""
    elif any(word in query for word in ["status", "all", "summary"]):
        return f"""🛏️ Bed Status Summary:
• ICU: {ctx.storage.get('icu_available')}/{ctx.storage.get('icu_total')}
• Step-Down: {ctx.storage.get('step_down_available')}/{ctx.storage.get('step_down_total')}
• Med-Surg: {ctx.storage.get('med_surg_available')}/{ctx.storage.get('med_surg_total')}
• Observation: {ctx.storage.get('observation_available')}/{ctx.storage.get('observation_total')}
• Total Available: {ctx.storage.get('icu_available') + ctx.storage.get('step_down_available') + ctx.storage.get('med_surg_available') + ctx.storage.get('observation_available')}"""
    else:
        return """🛏️ Bed Management

I manage bed assignments:
• ICU beds
• Step-down unit
• Medical-surgical beds
• Observation beds

Ask: "ICU availability?" or "Bed status?"?"""

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()