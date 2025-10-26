"""
WhatsApp Notification Agent - ASI:One Compatible
Sends WhatsApp notifications to medical staff during emergency protocols
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

AGENT_SEED = os.getenv("WHATSAPP_NOTIFICATION_SEED", "whatsapp_notification_phrase_001")

agent = Agent(
    name="whatsapp_notification",
    seed=AGENT_SEED,
    port=8006,
)

# Create protocol compatible with chat_protocol_spec for ASI:One
protocol = Protocol(spec=chat_protocol_spec)

# ============================================================================
# AGENT STATE INITIALIZATION
# ============================================================================

@agent.on_event("startup")
async def initialize(ctx: Context):
    """Initialize WhatsApp notification agent state"""
    
    # Initialize medical staff contacts (real numbers)
    ctx.storage.set("medical_staff_contacts", {
        "cardiologist": "+14082109942",      # Dr. Martinez
        "neurologist": "+16693409734",       # Dr. Chen
        "trauma_surgeon": "+14082109942",    # Dr. Smith
        "pediatrician": "+16693409734",      # Dr. Wilson
        "on_call_doctor": "+14082109942",    # General on-call
        "charge_nurse": "+16693409734",      # Charge nurse
        "family_contact": "+14082109942"     # Patient family
    })
    
    # Initialize notification tracking
    ctx.storage.set("notifications_sent_today", 0)
    ctx.storage.set("notification_history", [])
    ctx.storage.set("failed_notifications", 0)
    ctx.storage.set("last_notification_time", None)
    
    # WhatsApp API status (simulated for demo)
    ctx.storage.set("whatsapp_api_status", "connected")
    ctx.storage.set("twilio_status", "sandbox_mode")
    
    ctx.logger.info(f"📱 WhatsApp Notification Agent started (ASI:One Compatible)")
    ctx.logger.info(f"📍 Agent address: {ctx.agent.address}")
    ctx.logger.info(f"✅ Chat Protocol enabled - Ready for ASI:One")
    ctx.logger.info(f"📞 Medical staff contacts configured: 7 contacts")


# ============================================================================
# CHAT PROTOCOL HANDLERS (ASI:One Compatible)
# ============================================================================

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle chat messages from ASI:One or other agents
    Processes WhatsApp notification requests and status queries
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
    total_queries = ctx.storage.get("total_queries", 0) + 1
    ctx.storage.set("total_queries", total_queries)
    ctx.storage.set("last_query_time", datetime.utcnow().isoformat())
    
    # Process query and generate response
    response_text = await process_whatsapp_query(ctx, text.lower())
    
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
    
    ctx.logger.info(f"✅ WhatsApp response sent")


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements"""
    ctx.logger.debug(f"Ack received: {msg.acknowledged_msg_id}")


# ============================================================================
# WHATSAPP QUERY PROCESSING
# ============================================================================

async def process_whatsapp_query(ctx: Context, query: str) -> str:
    """
    Process WhatsApp-related queries and return appropriate response
    Handles: notification status, contact management, alert history
    """
    
    # Notification status query
    if any(word in query for word in ["status", "notifications", "how many", "sent"]):
        notifications_sent = ctx.storage.get("notifications_sent_today", 0)
        failed_notifications = ctx.storage.get("failed_notifications", 0)
        last_notification = ctx.storage.get("last_notification_time")
        
        response = f"""📱 WhatsApp Notification Status:
        
• Notifications Sent Today: {notifications_sent}
• Failed Notifications: {failed_notifications}
• Success Rate: {((notifications_sent - failed_notifications) / max(notifications_sent, 1) * 100):.1f}%
• Last Notification: {last_notification or 'None'}
• API Status: {ctx.storage.get('whatsapp_api_status', 'unknown')}

Ready to send emergency alerts to medical staff."""
        return response
    
    # Contact management query
    elif any(word in query for word in ["contact", "staff", "phone", "number"]):
        contacts = ctx.storage.get("medical_staff_contacts", {})
        
        response = f"""📞 Medical Staff Contacts:
        
• Cardiologist: {contacts.get('cardiologist', 'Not set')}
• Neurologist: {contacts.get('neurologist', 'Not set')}
• Trauma Surgeon: {contacts.get('trauma_surgeon', 'Not set')}
• Pediatrician: {contacts.get('pediatrician', 'Not set')}
• On-Call Doctor: {contacts.get('on_call_doctor', 'Not set')}
• Charge Nurse: {contacts.get('charge_nurse', 'Not set')}

Total contacts configured: {len(contacts)}"""
        return response
    
    # Protocol notification query
    elif any(word in query for word in ["stemi", "stroke", "trauma", "protocol", "alert"]):
        protocol_type = "stemi" if "stemi" in query else "stroke" if "stroke" in query else "trauma" if "trauma" in query else "general"
        
        response = f"""🚨 {protocol_type.upper()} Protocol Notifications:
        
When {protocol_type.upper()} protocol is activated, I automatically send WhatsApp alerts to:

"""
        
        if protocol_type == "stemi":
            response += """• Interventional Cardiologist (Dr. Martinez)
• Charge Nurse
• Cath Lab Team
• Blood Bank

Message includes: Patient ID, activation time, target completion (<5 min)"""
        
        elif protocol_type == "stroke":
            response += """• Neurologist (Dr. Chen)
• Charge Nurse
• CT Scan Team
• Pharmacy (tPA preparation)

Message includes: Patient ID, activation time, NIHSS score, target completion (<7 min)"""
        
        elif protocol_type == "trauma":
            response += """• Trauma Surgeon (Dr. Smith)
• Orthopedic Surgeon (Dr. Johnson)
• Charge Nurse
• Blood Bank
• OR Team

Message includes: Patient ID, activation time, injury mechanism, target completion (<3 min)"""
        
        return response
    
    # Help/capabilities query
    elif any(word in query for word in ["help", "what can you", "capabilities"]):
        response = """📱 WhatsApp Notification Agent
        
I automatically send WhatsApp alerts to medical staff during emergencies.

🚨 Emergency Protocols:
   • STEMI: Cardiologist + Cath Lab team
   • Stroke: Neurologist + CT team
   • Trauma: Trauma surgeon + OR team
   • Pediatric: Pediatrician + specialized equipment

📞 Contact Management:
   Ask: "Show contacts" or "Staff phone numbers"

📊 Notification Status:
   Ask: "Notification status" or "How many sent?"

⚡ Protocol Alerts:
   Ask: "STEMI notifications" or "Stroke alerts"

I ensure critical medical staff are instantly notified via WhatsApp when emergency protocols are activated."""
        return response
    
    # General/unknown query
    else:
        response = """📱 WhatsApp Notification Agent

I specialize in sending emergency alerts to medical staff via WhatsApp.

I can provide information about:
• Notification status and statistics
• Medical staff contact management
• Protocol-specific alert procedures
• WhatsApp API connectivity status

Ask me about notifications, contacts, or specific protocols (STEMI, Stroke, Trauma)."""
        return response


# ============================================================================
# WHATSAPP NOTIFICATION FUNCTIONS
# ============================================================================

async def send_protocol_notification(ctx: Context, protocol_type: str, patient_id: str):
    """Send WhatsApp notifications for protocol activation"""
    
    contacts = ctx.storage.get("medical_staff_contacts", {})
    notifications_sent = ctx.storage.get("notifications_sent_today", 0)
    
    # Simulate sending notifications based on protocol
    if protocol_type == "stemi":
        # Send to cardiologist and charge nurse
        await simulate_whatsapp_send(ctx, contacts.get("cardiologist"), 
            f"🚨 STEMI ALERT\n\nPatient: {patient_id}\nCath lab activation required\nETA: 5 minutes\n\nPlease respond immediately.")
        
        await simulate_whatsapp_send(ctx, contacts.get("charge_nurse"),
            f"🏥 STEMI Protocol Active\n\nPatient: {patient_id}\nPrepare cardiac medications\nCath lab team needed")
        
        notifications_sent += 2
    
    elif protocol_type == "stroke":
        # Send to neurologist and charge nurse
        await simulate_whatsapp_send(ctx, contacts.get("neurologist"),
            f"🧠 STROKE ALERT\n\nPatient: {patient_id}\nCT scan ordered\ntPA ready\nETA: 7 minutes\n\nPlease respond immediately.")
        
        await simulate_whatsapp_send(ctx, contacts.get("charge_nurse"),
            f"🏥 Stroke Protocol Active\n\nPatient: {patient_id}\nNeurology team needed\nCT priority")
        
        notifications_sent += 2
    
    elif protocol_type == "trauma":
        # Send to trauma surgeon and charge nurse
        await simulate_whatsapp_send(ctx, contacts.get("trauma_surgeon"),
            f"🚑 TRAUMA ALERT\n\nPatient: {patient_id}\nTrauma bay ready\nBlood bank notified\nETA: 3 minutes\n\nPlease respond immediately.")
        
        await simulate_whatsapp_send(ctx, contacts.get("charge_nurse"),
            f"🏥 Trauma Protocol Active\n\nPatient: {patient_id}\nTrauma team needed\nBlood products ready")
        
        notifications_sent += 2
    
    # Update notification count
    ctx.storage.set("notifications_sent_today", notifications_sent)
    ctx.storage.set("last_notification_time", datetime.utcnow().isoformat())
    
    ctx.logger.info(f"📱 WhatsApp notifications sent for {protocol_type.upper()} protocol")


async def simulate_whatsapp_send(ctx: Context, phone_number: str, message: str):
    """Simulate sending WhatsApp message (for demo purposes)"""
    
    # In production, this would use Twilio WhatsApp API:
    # from twilio.rest import Client
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     from_='whatsapp:+14155238886',
    #     body=message,
    #     to=f'whatsapp:{phone_number}'
    # )
    
    # For demo, just log the notification
    ctx.logger.info(f"📱 WhatsApp sent to {phone_number[-4:]}: {message[:50]}...")
    
    # Add to history
    history = ctx.storage.get("notification_history", [])
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "phone_number": phone_number,
        "message": message[:100],
        "status": "delivered"
    })
    ctx.storage.set("notification_history", history[-50:])  # Keep last 50


# ============================================================================
# PERIODIC TASKS
# ============================================================================

@agent.on_interval(period=300.0)  # Every 5 minutes
async def periodic_status_check(ctx: Context):
    """Check WhatsApp API status and notification queue"""
    notifications_sent = ctx.storage.get("notifications_sent_today", 0)
    failed_notifications = ctx.storage.get("failed_notifications", 0)
    
    ctx.logger.info(f"📱 WhatsApp Status Check:")
    ctx.logger.info(f"   📊 Notifications sent today: {notifications_sent}")
    ctx.logger.info(f"   ❌ Failed notifications: {failed_notifications}")
    ctx.logger.info(f"   📡 API Status: {ctx.storage.get('whatsapp_api_status', 'unknown')}")


# ============================================================================
# ATTACH PROTOCOL AND RUN
# ============================================================================

# Attach the chat protocol to the agent with manifest publishing
# This makes the agent discoverable on ASI:One
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()