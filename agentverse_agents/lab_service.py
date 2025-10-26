"""
Lab Service Agent - ASI:One Compatible
Laboratory test coordination with Chat Protocol
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

AGENT_SEED = os.getenv("LAB_SERVICE_SEED", "lab_service_phrase_001")

agent = Agent(name="lab_service", seed=AGENT_SEED, port=8002)
protocol = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("pending_orders", 0)
    ctx.storage.set("completed_today", 0)
    ctx.storage.set("average_turnaround", 25.5)
    ctx.storage.set("critical_pending", 0)
    ctx.logger.info(f"🧪 Lab Service started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
    response_text = await process_lab_query(ctx, text.lower())
    await ctx.send(sender, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), 
                                       content=[TextContent(type="text", text=response_text)]))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

async def process_lab_query(ctx: Context, query: str) -> str:
    # 🚑 AMBULANCE REPORT RESPONSE
    if any(word in query for word in ["ambulance", "incoming", "protocol", "action required"]):
        protocol = "General"
        if "STEMI" in query or "chest pain" in query.lower():
            protocol = "STEMI"
            tests = "Troponin, ECG, CBC, BMP, PT/INR"
        elif "Stroke" in query or "stroke" in query.lower():
            protocol = "Stroke"
            tests = "CT Head, CBC, BMP, PT/INR, Glucose"
        elif "Trauma" in query or "trauma" in query.lower():
            protocol = "Trauma"
            tests = "Type & Cross, CBC, BMP, Lactate, ABG"
        else:
            tests = "CBC, BMP, Troponin"
        
        return f"""✅ LAB SERVICE RESPONSE - {protocol} Protocol

🧪 LABS PREPARED:
• STAT Orders: {tests}
• Priority: CRITICAL
• Turnaround: <15 minutes
• Phlebotomy: Standing by

📊 Lab Status:
• Equipment: Calibrated and ready
• Reagents: Stocked
• Staff: Alerted for STAT processing

⏱️ Ready for immediate sample processing
🎯 Results will be expedited"""
    
    elif any(word in query for word in ["status", "pending", "queue"]):
        return f"""🧪 Lab Status:
• Pending Orders: {ctx.storage.get('pending_orders')}
• Completed Today: {ctx.storage.get('completed_today')}
• Average Turnaround: {ctx.storage.get('average_turnaround'):.1f} min
• Critical Pending: {ctx.storage.get('critical_pending')}
• Status: {'Operational' if ctx.storage.get('pending_orders') < 5 else 'Busy'}"""
    elif any(word in query for word in ["test", "available", "can you"]):
        return """🧪 Available Tests:
• CBC (Complete Blood Count)
• BMP (Basic Metabolic Panel)
• Troponin • D-Dimer • PT/INR
• Glucose • Lactate
• ABG (Arterial Blood Gas)
• Urinalysis • Blood Culture"""
    else:
        return """🧪 Lab Service

I coordinate laboratory tests:
• Blood work (CBC, BMP, Troponin)
• Urgent/STAT processing  
• Result reporting

Ask: "Lab status?" or "What tests available?"?"""

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()