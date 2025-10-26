"""
Specialist Coordinator Agent - ASI:One Compatible
Coordinates specialist teams with Chat Protocol
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

AGENT_SEED = os.getenv("SPECIALIST_COORDINATOR_SEED", "specialist_coordinator_phrase_001")

agent = Agent(name="specialist_coordinator", seed=AGENT_SEED, port=8004)
protocol = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("active_teams", 0)
    ctx.storage.set("completed_activations_today", 0)
    ctx.storage.set("avg_response_stemi", 4.5)
    ctx.storage.set("avg_response_stroke", 6.2)
    ctx.storage.set("avg_response_trauma", 3.8)
    ctx.logger.info(f"👨‍⚕️ Specialist Coordinator started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
    response_text = await process_specialist_query(ctx, text.lower())
    await ctx.send(sender, ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(),
                                       content=[TextContent(type="text", text=response_text)]))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

async def process_specialist_query(ctx: Context, query: str) -> str:
    # 🚑 AMBULANCE REPORT RESPONSE
    if any(word in query for word in ["ambulance", "incoming", "protocol", "action required"]):
        protocol = "General"
        if "STEMI" in query or "chest pain" in query.lower():
            protocol = "STEMI"
            team = "Cardiology team (Dr. Smith, Cath Lab ready)"
            eta = "3 minutes"
        elif "Stroke" in query or "stroke" in query.lower():
            protocol = "Stroke"
            team = "Neurology team (Dr. Johnson, CT ready)"
            eta = "4 minutes"
        elif "Trauma" in query or "trauma" in query.lower():
            protocol = "Trauma"
            team = "Trauma surgery team (Dr. Williams, OR alerted)"
            eta = "2 minutes"
        else:
            team = "ED attending physician"
            eta = "5 minutes"
        
        return f"""✅ SPECIALIST COORDINATOR RESPONSE - {protocol} Protocol

👨‍⚕️ TEAM ACTIVATED:
• Team: {team}
• ETA: {eta}
• Status: Paged and responding
• Backup: On standby

📊 Team Status:
• Primary team: En route
• Support staff: Alerted
• Equipment: Prepared
• Procedure room: Reserved

⏱️ Team assembling now
🎯 Ready for immediate intervention"""
    
    elif any(word in query for word in ["status", "active", "teams"]):
        return f"""👨‍⚕️ Specialist Status:
• Active Teams: {ctx.storage.get('active_teams')}
• Activations Today: {ctx.storage.get('completed_activations_today')}
• STEMI Response: {ctx.storage.get('avg_response_stemi'):.1f} min
• Stroke Response: {ctx.storage.get('avg_response_stroke'):.1f} min
• Trauma Response: {ctx.storage.get('avg_response_trauma'):.1f} min
• Status: {'Available' if ctx.storage.get('active_teams') < 3 else 'Busy'}"""
    elif any(word in query for word in ["specialist", "available", "doctor"]):
        return """👨‍⚕️ Available Specialists:
• Cardiologists (3 available)
• Neurologists (2 available)
• Trauma Surgeons (2 available)
• Pediatricians (3 available)
• Radiologists (4 available)"""
    else:
        return """👨‍⚕️ Specialist Coordinator

I coordinate specialist teams:
• STEMI (Cardiology) teams
• Stroke (Neurology) teams
• Trauma surgery teams
• Pediatric teams

Ask: "Specialist status?" or "Who is available?"?"""

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()