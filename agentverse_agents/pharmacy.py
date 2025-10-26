"""
Pharmacy Agent - ASI:One Compatible
Medication management with Chat Protocol
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

AGENT_SEED = os.getenv("PHARMACY_SEED", "pharmacy_phrase_001")

agent = Agent(name="pharmacy", seed=AGENT_SEED, port=8003)
protocol = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("pending_orders", 0)
    ctx.storage.set("delivered_today", 0)
    ctx.storage.set("average_prep_time", 12.5)
    ctx.storage.set("stat_pending", 0)
    ctx.logger.info(f"💊 Pharmacy started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
    response_text = await process_pharmacy_query(ctx, text.lower())
    await ctx.send(sender, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(),
                                       content=[TextContent(type="text", text=response_text)]))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

async def process_pharmacy_query(ctx: Context, query: str) -> str:
    # 🚑 AMBULANCE REPORT RESPONSE
    if any(word in query for word in ["ambulance", "incoming", "protocol", "action required"]):
        protocol = "General"
        if "STEMI" in query or "chest pain" in query.lower():
            protocol = "STEMI"
            meds = "Aspirin 325mg, Heparin, Nitroglycerin, Morphine"
        elif "Stroke" in query or "stroke" in query.lower():
            protocol = "Stroke"
            meds = "Alteplase (tPA), Labetalol, Mannitol"
        elif "Trauma" in query or "trauma" in query.lower():
            protocol = "Trauma"
            meds = "Tranexamic acid, Morphine, Ceftriaxone, Tetanus"
        else:
            meds = "Standard emergency medications"
        
        return f"""✅ PHARMACY RESPONSE - {protocol} Protocol

💊 MEDICATIONS PREPARED:
• STAT Meds: {meds}
• Priority: IMMEDIATE
• Delivery: <5 minutes
• Dosing: Pre-calculated

📊 Pharmacy Status:
• Medications: Drawn and labeled
• IV Solutions: Prepared
• Crash Cart: Stocked and checked

⏱️ Ready for immediate administration
🎯 Pharmacist standing by for consult"""
    
    elif any(word in query for word in ["status", "pending", "queue"]):
        return f"""💊 Pharmacy Status:
• Pending Orders: {ctx.storage.get('pending_orders')}
• Delivered Today: {ctx.storage.get('delivered_today')}
• Average Prep Time: {ctx.storage.get('average_prep_time'):.1f} min
• STAT Pending: {ctx.storage.get('stat_pending')}
• Status: {'Operational' if ctx.storage.get('pending_orders') < 3 else 'Busy'}"""
    elif any(word in query for word in ["medication", "drug", "available"]):
        return """💊 Available Medications:
• Aspirin • Heparin • Nitroglycerin
• Morphine • Epinephrine • Alteplase  
• Ceftriaxone • Ondansetron
Plus full ED formulary"""
    else:
        return """💊 Pharmacy Service

I manage medication orders:
• ED formulary medications
• STAT/urgent processing
• Delivery tracking

Ask: "Pharmacy status?" or "What medications available?"?"""

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()