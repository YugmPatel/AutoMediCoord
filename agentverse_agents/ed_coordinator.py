"""
ED Coordinator Agent - ASI:One Compatible
Emergency Department Coordinator with Chat Protocol for ASI:One integration
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

# ============================================================================
# CREATE AGENT
# ============================================================================

AGENT_SEED = os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_phrase_001")

agent = Agent(
    name="ed_coordinator",
    seed=AGENT_SEED,
    port=8000,
)

# Create protocol compatible with chat_protocol_spec for ASI:One
protocol = Protocol(spec=chat_protocol_spec)

# ============================================================================
# AGENT STATE INITIALIZATION
# ============================================================================

@agent.on_event("startup")
async def initialize(ctx: Context):
    """Initialize agent state on startup"""
    
    # Initialize storage
    ctx.storage.set("active_cases", [])
    ctx.storage.set("active_protocols", [])
    ctx.storage.set("available_beds", 10)
    ctx.storage.set("total_beds", 15)
    ctx.storage.set("staff_on_duty", 25)
    ctx.storage.set("system_load", "medium")
    
    # Protocol statistics
    ctx.storage.set("protocol_stats", {
        "stemi": {"active": 0, "total_today": 0, "avg_time": 4.5, "success_rate": 0.95},
        "stroke": {"active": 0, "total_today": 0, "avg_time": 6.2, "success_rate": 0.93},
        "trauma": {"active": 0, "total_today": 0, "avg_time": 3.8, "success_rate": 0.97}
    })
    
    # Query tracking
    ctx.storage.set("total_queries", 0)
    ctx.storage.set("last_query_time", None)
    
    ctx.logger.info(f"🏥 ED Coordinator started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")
    ctx.logger.info(f"✅ Chat Protocol enabled - Ready for ASI:One")


# ============================================================================
# CHAT PROTOCOL HANDLERS (ASI:One Compatible)
# ============================================================================

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle chat messages from ASI:One or other agents
    Processes queries about ED status, patient load, resources, protocols
    """
    ctx.logger.info(f"📨 Chat message received from {sender[:12]}...")
    
    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )
    
    # Collect text from message
    text = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text
    
    ctx.logger.info(f"   Query: {text[:100]}...")
    
    # Track query
    total_queries = ctx.storage.get("total_queries") + 1
    ctx.storage.set("total_queries", total_queries)
    ctx.storage.set("last_query_time", datetime.utcnow().isoformat())
    
    # Process query and generate response
    response_text = await process_query(ctx, text.lower())
    
    # Send response using ChatMessage
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
    """Handle acknowledgements"""
    ctx.logger.debug(f"Ack received: {msg.acknowledged_msg_id}")


# ============================================================================
# QUERY PROCESSING
# ============================================================================

async def process_query(ctx: Context, query: str) -> str:
    """
    Process incoming queries and return appropriate response
    Handles: system status, patient load, resources, protocols
    """
    
    # System status query
    if any(word in query for word in ["system", "status", "overview", "how are things"]):
        active_cases = ctx.storage.get("active_cases")
        response = f"""📊 EDFlow AI System Status:
        
• Active Cases: {len(active_cases)}
• Available Beds: {ctx.storage.get('available_beds')}/{ctx.storage.get('total_beds')}
• Staff on Duty: {ctx.storage.get('staff_on_duty')}
• System Load: {ctx.storage.get('system_load')}
• Active Protocols: {', '.join(ctx.storage.get('active_protocols')) if ctx.storage.get('active_protocols') else 'None'}

System is operational and ready for emergency department coordination."""
        return response
    
    # Patient load query
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
    
    # Resource availability query
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
    
    # Protocol performance query
    elif any(word in query for word in ["protocol", "stemi", "stroke", "trauma", "performance"]):
        protocol_stats = ctx.storage.get("protocol_stats")
        
        # Determine which protocol
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
    
    # Help/capabilities query
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
    
    # General/unknown query
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


# ============================================================================
# PERIODIC TASKS
# ============================================================================

@agent.on_interval(period=60.0)
async def periodic_health_check(ctx: Context):
    """Perform system health check every minute"""
    active_cases = ctx.storage.get("active_cases")
    available_beds = ctx.storage.get("available_beds")
    total_queries = ctx.storage.get("total_queries")
    
    ctx.logger.info(f"💓 Health Check:")
    ctx.logger.info(f"   📊 Active Cases: {len(active_cases)}")
    ctx.logger.info(f"   🛏️  Available Beds: {available_beds}")
    ctx.logger.info(f"   📞 Total Queries: {total_queries}")


# ============================================================================
# ATTACH PROTOCOL AND RUN
# ============================================================================

# Attach the chat protocol to the agent with manifest publishing
# This makes the agent discoverable on ASI:One
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()