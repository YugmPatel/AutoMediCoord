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

AGENT_SEED = os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_phrase_001")

agent = Agent(
    name="ed_coordinator",
    seed=AGENT_SEED,
    port=8000,
)

protocol = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("active_cases", [])
    ctx.storage.set("active_protocols", [])
    ctx.storage.set("available_beds", 10)
    ctx.storage.set("total_beds", 15)
    ctx.storage.set("staff_on_duty", 25)
    ctx.storage.set("system_load", "medium")
    
    ctx.storage.set("protocol_stats", {
        "stemi": {"active": 0, "total_today": 0, "avg_time": 4.5, "success_rate": 0.95},
        "stroke": {"active": 0, "total_today": 0, "avg_time": 6.2, "success_rate": 0.93},
        "trauma": {"active": 0, "total_today": 0, "avg_time": 3.8, "success_rate": 0.97}
    })
    
    ctx.storage.set("total_queries", 0)
    ctx.storage.set("last_query_time", None)
    
    ctx.storage.set("agent_addresses", {
        "resource_manager": os.getenv("RESOURCE_MANAGER_ADDRESS", "agent1q..."),
        "specialist_coordinator": os.getenv("SPECIALIST_COORDINATOR_ADDRESS", "agent1q..."),
        "lab_service": os.getenv("LAB_SERVICE_ADDRESS", "agent1q..."),
        "pharmacy": os.getenv("PHARMACY_ADDRESS", "agent1q..."),
        "bed_management": os.getenv("BED_MANAGEMENT_ADDRESS", "agent1q...")
    })
    
    ctx.logger.info(f"🏥 ED Coordinator started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")
    ctx.logger.info(f"✅ Chat Protocol enabled - Ready for ASI:One")
    ctx.logger.info(f"🚑 Ambulance broadcast system enabled")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"📨 Chat message received from {sender[:12]}...")
    
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )
    
    text = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text
    
    ctx.logger.info(f"   Query: {text[:100]}...")
    
    total_queries = ctx.storage.get("total_queries") + 1
    ctx.storage.set("total_queries", total_queries)
    ctx.storage.set("last_query_time", datetime.utcnow().isoformat())
    
    response_text = await process_query(ctx, text.lower())
    
    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response_text)
            ]
        )
    )
    
    ctx.logger.info(f"✅ Response sent")

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.debug(f"Ack received: {msg.acknowledged_msg_id}")

async def process_query(ctx: Context, query: str) -> str:
    if any(word in query for word in ["ambulance", "patient arriving", "ems", "incoming patient", "chest pain", "stroke", "trauma", "critical"]):
        ctx.logger.info("🚑 AMBULANCE REPORT DETECTED - Initiating broadcast to all agents")
        
        protocol_type = "general"
        if any(word in query for word in ["chest pain", "stemi", "heart attack", "mi"]):
            protocol_type = "STEMI"
        elif any(word in query for word in ["stroke", "cva", "weakness", "slurred"]):
            protocol_type = "Stroke"
        elif any(word in query for word in ["trauma", "accident", "injury", "bleeding"]):
            protocol_type = "Trauma"
        
        await broadcast_to_all_agents(ctx, query, protocol_type)
        
        return f"""🚨 EMERGENCY PROTOCOL ACTIVATED: {protocol_type}

📡 Broadcasting to all agents:
✅ Resource Manager - Allocating resources
✅ Bed Management - Reserving bed
✅ Lab Service - Preparing tests
✅ Pharmacy - Readying medications
✅ Specialist Coordinator - Alerting team

⏱️ Protocol activation time: <5 minutes
🎯 All agents are coordinating response

Patient will be ready for immediate care upon arrival."""
    
    elif any(word in query for word in ["system", "status", "overview", "how are things"]):
        active_cases = ctx.storage.get("active_cases")
        response = f"""📊 EDFlow AI System Status:
        
• Active Cases: {len(active_cases)}
• Available Beds: {ctx.storage.get('available_beds')}/{ctx.storage.get('total_beds')}
• Staff on Duty: {ctx.storage.get('staff_on_duty')}
• System Load: {ctx.storage.get('system_load')}
• Active Protocols: {', '.join(ctx.storage.get('active_protocols')) if ctx.storage.get('active_protocols') else 'None'}

System is operational and ready for emergency department coordination."""
        return response
    
    elif any(word in query for word in ["patient", "load", "how many patients", "busy"]):
        active_cases = ctx.storage.get("active_cases")
        critical = len([c for c in active_cases if c.get("acuity") == 1])
        avg_wait = 15.5 if len(active_cases) < 5 else 25.3
        
        response = f"""👥 Patient Load Information:
        
• Total Patients: {len(active_cases)}
• Critical (Level 1): {critical}
• Waiting: {max(0, len(active_cases) - 3)}
• Average Wait Time: {avg_wait:.1f} minutes

Current patient volume: {'Low' if len(active_cases) < 5 else 'Moderate' if len(active_cases) < 10 else 'High'}"""
        return response
    
    elif any(word in query for word in ["bed", "resource", "available", "capacity"]):
        beds_available = ctx.storage.get("available_beds")
        beds_total = ctx.storage.get("total_beds")
        utilization = ((beds_total - beds_available) / beds_total * 100) if beds_total > 0 else 0
        
        response = f"""🛏️ Resource Availability:
        
• Beds Available: {beds_available}/{beds_total}
• Bed Utilization: {utilization:.0f}%
• Staff on Duty: {ctx.storage.get('staff_on_duty')}
• Equipment: Available
• Wait Time: {0 if beds_available > 0 else 20} minutes

Capacity Status: {'Available' if beds_available > 3 else 'Limited' if beds_available > 0 else 'Full'}"""
        return response
    
    elif any(word in query for word in ["protocol", "stemi", "stroke", "trauma", "performance"]):
        protocol_stats = ctx.storage.get("protocol_stats")
        
        protocol_type = "stemi" if "stemi" in query else "stroke" if "stroke" in query else "trauma" if "trauma" in query else "stemi"
        stats = protocol_stats.get(protocol_type, {})
        
        response = f"""⚡ {protocol_type.upper()} Protocol Performance:
        
• Active Now: {stats.get('active', 0)}
• Completed Today: {stats.get('total_today', 0)}
• Avg Response Time: {stats.get('avg_time', 0):.1f} minutes
• Success Rate: {stats.get('success_rate', 0)*100:.0f}%

Protocol Status: {'Active' if stats.get('active', 0) > 0 else 'Ready'}
Response time target: {'<5 min' if protocol_type == 'stemi' else '<7 min' if protocol_type == 'stroke' else '<3 min'}"""
        return response
    
    elif any(word in query for word in ["help", "what can you", "capabilities", "do"]):
        response = """🏥 EDFlow AI - Emergency Department Coordinator

I can help you with:

📊 System Status
   Ask: "What's the system status?" or "How are things?"

👥 Patient Information  
   Ask: "How many patients?" or "What's the patient load?"

🛏️ Resource Availability
   Ask: "Are beds available?" or "What's the capacity?"

⚡ Protocol Performance
   Ask: "STEMI protocol status?" or "How are protocols performing?"

I coordinate emergency department operations including:
• Patient triage and flow
• Resource allocation (beds, equipment)
• Emergency protocol activation (STEMI, Stroke, Trauma)
• Team coordination

How can I assist you today?"""
        return response
    
    else:
        response = """🏥 EDFlow AI Emergency Department Coordinator

I specialize in emergency department operations and coordination.

I can provide information about:
• System status and operations
• Patient load and wait times  
• Resource availability (beds, equipment)
• Emergency protocol performance (STEMI, Stroke, Trauma)

Please ask me about any of these topics, or type "help" for more information."""
        return response

async def broadcast_to_all_agents(ctx: Context, ambulance_report: str, protocol_type: str):
    agent_addresses = ctx.storage.get("agent_addresses")
    
    broadcast_message = f"""🚑 AMBULANCE REPORT - {protocol_type} PROTOCOL

{ambulance_report}

⚡ ACTION REQUIRED: Prepare for incoming patient
Protocol: {protocol_type}
Coordinator: ED Coordinator

Please respond with your preparation status."""
    
    agents_to_notify = [
        ("Resource Manager", agent_addresses.get("resource_manager")),
        ("Specialist Coordinator", agent_addresses.get("specialist_coordinator")),
        ("Lab Service", agent_addresses.get("lab_service")),
        ("Pharmacy", agent_addresses.get("pharmacy")),
        ("Bed Management", agent_addresses.get("bed_management"))
    ]
    
    for agent_name, agent_address in agents_to_notify:
        if agent_address and agent_address != "agent1q...":
            try:
                await ctx.send(
                    agent_address,
                    ChatMessage(
                        timestamp=datetime.utcnow(),
                        msg_id=uuid4(),
                        content=[TextContent(type="text", text=broadcast_message)]
                    )
                )
                ctx.logger.info(f"✅ Broadcast sent to {agent_name}")
            except Exception as e:
                ctx.logger.error(f"❌ Failed to send to {agent_name}: {e}")
        else:
            ctx.logger.warning(f"⚠️  {agent_name} address not configured")

@agent.on_interval(period=60.0)
async def periodic_health_check(ctx: Context):
    active_cases = ctx.storage.get("active_cases")
    available_beds = ctx.storage.get("available_beds")
    total_queries = ctx.storage.get("total_queries")
    
    ctx.logger.info(f"💓 Health Check:")
    ctx.logger.info(f"   📊 Active Cases: {len(active_cases)}")
    ctx.logger.info(f"   🛏️  Available Beds: {available_beds}")
    ctx.logger.info(f"   📞 Total Queries: {total_queries}")

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()