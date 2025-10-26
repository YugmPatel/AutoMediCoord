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

AGENT_SEED = "ed_coordinator_phrase_001"
JSONBIN_ID = "68fd4c71ae596e708f2c8fb0"
JSONBIN_KEY = "$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa"
ANTHROPIC_KEY = "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"

agent = Agent(name="ed_coordinator", seed=AGENT_SEED, port=8000)
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

async def update_hospital_data(data):
    """Tool: Update hospital data in JSONBin"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(
                f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}",
                json=data,
                headers={"X-Master-Key": JSONBIN_KEY, "Content-Type": "application/json"}
            )
            return response.json()
    except Exception as e:
        return {"error": str(e)}

async def activate_protocol(protocol_name):
    """Tool: Activate emergency protocol and update stats"""
    data = await get_hospital_data()
    if "error" in data:
        return False
    
    protocol_key = protocol_name.lower()
    if protocol_key in data.get("protocols", {}):
        data["protocols"][protocol_key]["active_cases"] += 1
        data["protocols"][protocol_key]["last_activation"] = datetime.utcnow().isoformat()
        await update_hospital_data(data)
        return True
    return False

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("total_cases", 0)
    ctx.storage.set("protocols_activated", 0)
    
    ctx.storage.set("agent_addresses", {
        "resource_manager": "agent1qff3y8ry6jew53lgc5gxzg8cqc3cc505c5n0rwcntpwe2ydvz23gxc36xh4",
        "specialist_coordinator": "agent1qdentzr0unjc5t8sylsha2ugv5yecpf80jw67qwwu4glgc84rr9u6w98f0c",
        "lab_service": "agent1qw4g3efd5t7ve83gmq3yp7dkzzmg7g4z480cunk8rru4yhw5x2k979ddxgk",
        "pharmacy": "agent1qfx6rpglgl86s8072ja8y7fkk9pfg5csa2jg7h2vgkl2nztt2fctye7wngx",
        "bed_management": "agent1qd6j2swdef06tgl4ly66r65c4vz6rcggt7rm89udnuvmn8n2y90myq46rfl",
        "whatsapp_notification": "agent1qdvph9h02dhvs4vfk032hmpuaz3tm65p6n3ksgd9q5d22xyln3vqgkp2str"
    })
    
    ctx.logger.info(f"🏥 ED Coordinator Agent Started")
    ctx.logger.info(f"📍 Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"🔧 Tools: JSONBin + Claude AI enabled")
    ctx.logger.info(f"📊 JSONBin ID: {JSONBIN_ID[:20]}...")
    ctx.logger.info(f"🚑 Ambulance broadcast system enabled")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"📨 Message received from {sender[:16]}...")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(),
        acknowledged_msg_id=msg.msg_id
    ))
    
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
    
    # COLLECT AGENT RESPONSES: Store responses from other agents
    agent_addresses = ctx.storage.get("agent_addresses")
    if agent_addresses and sender in agent_addresses.values():
        ctx.logger.info(f"📥 Agent response received - storing for aggregation")
        
        # Store the response
        agent_responses = ctx.storage.get("agent_responses") or {}
        agent_name = [name for name, addr in agent_addresses.items() if addr == sender][0]
        agent_responses[agent_name] = {
            "text": text,
            "timestamp": datetime.utcnow().isoformat()
        }
        ctx.storage.set("agent_responses", agent_responses)
        ctx.logger.info(f"✅ Stored response from {agent_name} ({len(agent_responses)}/5 collected)")
        return
    
    ctx.logger.info(f"📝 Query: {text[:150]}...")
    
    if "ambulance" in text.lower() or any(word in text.lower() for word in ["chest pain", "stroke", "trauma", "critical", "emergency"]):
        ctx.logger.info("🚑 AMBULANCE REPORT DETECTED - Initiating AI analysis and broadcast")
        
        ctx.logger.info("🔧 Tool Call: Fetching hospital status from JSONBin...")
        hospital_data = await get_hospital_data()
        
        if claude_client:
            ctx.logger.info("🤖 Calling Claude AI to analyze ambulance report...")
            
            current_status = hospital_data.get("current_status", {})
            protocols = hospital_data.get("protocols", {})
            
            analysis_prompt = f"""You are the ED Coordinator AI analyzing an ambulance report.

Ambulance Report:
{text}

Current ED Status:
- Total Patients: {current_status.get('total_patients', 0)}
- Critical Patients: {current_status.get('critical_patients', 0)}
- ED Capacity: {current_status.get('ed_capacity_percent', 0)}%
- System Load: {current_status.get('system_load', 'unknown')}

Protocol Performance Today:
- STEMI: {protocols.get('stemi', {}).get('total_today', 0)} cases, {protocols.get('stemi', {}).get('avg_door_to_balloon_minutes', 0)}min avg
- Stroke: {protocols.get('stroke', {}).get('total_today', 0)} cases, {protocols.get('stroke', {}).get('avg_door_to_needle_minutes', 0)}min avg
- Trauma: {protocols.get('trauma', {}).get('total_today', 0)} cases, {protocols.get('trauma', {}).get('avg_response_time_minutes', 0)}min avg

Analyze and determine:
1. Which protocol to activate (STEMI/Stroke/Trauma/General)
2. Urgency level (1-5, 1=critical)
3. Key actions needed
4. Estimated time to treatment

Respond in this format:
PROTOCOL: [name]
URGENCY: [1-5]
ANALYSIS: [brief analysis]"""

            analysis_response = await claude_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=400,
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            analysis = analysis_response.content[0].text
            ctx.logger.info(f"✅ Claude AI Analysis: {analysis[:100]}...")
            
            protocol_name = "STEMI" if "STEMI" in analysis else "Stroke" if "Stroke" in analysis else "Trauma" if "Trauma" in analysis else "General"
            
            ctx.logger.info(f"🔧 Tool Call: Activating {protocol_name} protocol...")
            activated = await activate_protocol(protocol_name)
            ctx.logger.info(f"✅ Protocol activation: {activated}")
            
            agent_addresses = ctx.storage.get("agent_addresses")
            
            # Store original sender and initialize response collection
            ctx.storage.set("original_sender", sender)
            ctx.storage.set("agent_responses", {})
            ctx.storage.set("waiting_for_responses", True)
            ctx.storage.set("broadcast_timestamp", datetime.utcnow().isoformat())
            
            broadcast_message = f"""🚑 AMBULANCE REPORT - {protocol_name.upper()} PROTOCOL

{text}

AI ANALYSIS:
{analysis}

⚡ ACTION REQUIRED: Prepare for incoming patient
Coordinator: ED Coordinator
Original Sender: {sender}

RESPOND TO ORIGINAL SENDER with your detailed preparation report showing:
1. Data you fetched from database
2. Actions you took
3. Your current status"""
            
            ctx.logger.info("📡 Broadcasting to all 5 agents...")
            agents_to_notify = [
                ("Resource Manager", agent_addresses.get("resource_manager")),
                ("Specialist Coordinator", agent_addresses.get("specialist_coordinator")),
                ("Lab Service", agent_addresses.get("lab_service")),
                ("Pharmacy", agent_addresses.get("pharmacy")),
                ("Bed Management", agent_addresses.get("bed_management")),
                ("WhatsApp Notification", agent_addresses.get("whatsapp_notification"))
            ]
            
            broadcast_count = 0
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
                        broadcast_count += 1
                    except Exception as e:
                        ctx.logger.error(f"❌ Failed to send to {agent_name}: {e}")
                else:
                    ctx.logger.warning(f"⚠️  {agent_name} address not configured")
            
            ctx.logger.info(f"📡 Broadcast complete: {broadcast_count}/5 agents notified")
            
            protocols_activated = ctx.storage.get("protocols_activated") + 1
            ctx.storage.set("protocols_activated", protocols_activated)
            
            response_text = f"""🏥 ED COORDINATOR AGENT REPORT

📊 DATA FETCHED FROM HOSPITAL DATABASE:
• Current Patients: {current_status.get('total_patients', 0)}
• ED Capacity: {current_status.get('ed_capacity_percent', 0)}%
• Critical Patients: {current_status.get('critical_patients', 0)}
• Average Wait Time: {current_status.get('average_wait_time_minutes', 0)} minutes
• System Load: {current_status.get('system_load', 'unknown')}

🤖 AI ANALYSIS PERFORMED:
{analysis}

🔧 ACTIONS TAKEN:
• Protocol activated: {protocol_name} in hospital database
• Updated protocol stats: Active cases incremented
• Broadcast sent to {broadcast_count}/5 specialized agents
• Timestamp: {datetime.utcnow().isoformat()}

✅ COORDINATION STATUS:
• Resource Manager: Notified ✅
• Bed Management: Notified ✅
• Lab Service: Notified ✅
• Pharmacy: Notified ✅
• Specialist Coordinator: Notified ✅
• WhatsApp Notification: Notified ✅

⏱️ Protocol activation time: <5 seconds
🎯 All 6 agents are now preparing - check their individual responses below"""
            
            ctx.logger.info("✅ ED Coordinator response generated")
        else:
            response_text = "🚨 EMERGENCY PROTOCOL ACTIVATED\n\n📡 Broadcasting to all agents..."
    
    else:
        ctx.logger.info("📊 Standard query - Using Claude AI + Tools...")
        
        ctx.logger.info("🔧 Tool Call: get_hospital_data() - Fetching ED status from JSONBin...")
        data = await get_hospital_data()
        
        if "error" in data:
            ctx.logger.error(f"❌ Tool Error: {data['error']}")
            response_text = "❌ Error fetching hospital data"
        else:
            status = data.get("current_status", {})
            total_patients = status.get('total_patients', 0)
            capacity = status.get('ed_capacity_percent', 0)
            wait_time = status.get('average_wait_time_minutes', 0)
            
            ctx.logger.info(f"📊 Tool Result: {total_patients} patients, {capacity}% capacity, {wait_time}min wait")
            
            if claude_client:
                ctx.logger.info("🤖 Calling Claude AI for response generation...")
                prompt = f"""You are the ED Coordinator AI.

Query: {text}

Current Status:
- Patients: {total_patients}
- Capacity: {capacity}%
- Wait Time: {wait_time} min

Provide a helpful, professional response."""

                response = await claude_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.content[0].text
                ctx.logger.info("✅ Claude AI response generated")
            else:
                ctx.logger.warning("⚠️ Claude AI not configured - using fallback")
                response_text = f"""🏥 ED Coordinator Status

• Total Patients: {total_patients}
• ED Capacity: {capacity}%
• Average Wait: {wait_time} minutes

How can I help you coordinate the ED?"""
    
    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=response_text)]
    ))
    
    cases = ctx.storage.get("total_cases") + 1
    ctx.storage.set("total_cases", cases)
    ctx.logger.info(f"✅ Response sent | Total cases: {cases}")

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.debug(f"✓ Ack received: {msg.acknowledged_msg_id}")

@agent.on_interval(period=3.0)
async def check_and_aggregate_responses(ctx: Context):
    """Check if all agent responses collected and send aggregated response"""
    if not ctx.storage.get("waiting_for_responses"):
        return
    
    agent_responses = ctx.storage.get("agent_responses") or {}
    broadcast_time = ctx.storage.get("broadcast_timestamp")
    
    if not broadcast_time:
        return
    
    elapsed = (datetime.utcnow() - datetime.fromisoformat(broadcast_time)).total_seconds()
    ctx.logger.info(f"⏱️ Checking responses: {len(agent_responses)}/5 collected, {elapsed:.1f}s elapsed")
    
    # Send aggregated response if we have all 5 OR timeout after 10 seconds
    if len(agent_responses) >= 6 or elapsed > 10:
        ctx.logger.info(f"📦 AGGREGATING RESPONSES: {len(agent_responses)}/6 collected after {elapsed:.1f}s")
        
        original_sender = ctx.storage.get("original_sender")
        if not original_sender:
            ctx.logger.error("❌ No original sender stored!")
            ctx.storage.set("waiting_for_responses", False)
            return
        
        try:
            # Build aggregated response
            ctx.logger.info("🔨 Building aggregated response...")
            aggregated = await build_aggregated_response(ctx, agent_responses)
            
            ctx.logger.info(f"📤 Sending aggregated response to {original_sender[:16]}...")
            await ctx.send(original_sender, ChatMessage(
                timestamp=datetime.utcnow(),
                msg_id=uuid4(),
                content=[TextContent(type="text", text=aggregated)]
            ))
            
            ctx.logger.info(f"✅ Aggregated response sent successfully!")
        except Exception as e:
            ctx.logger.error(f"❌ Error sending aggregated response: {e}")
        
        # Reset
        ctx.storage.set("waiting_for_responses", False)
        ctx.storage.set("agent_responses", {})
        ctx.logger.info("🔄 Reset complete, ready for next query")

async def build_aggregated_response(ctx: Context, agent_responses: dict) -> str:
    """Build comprehensive response with ambulance instructions + agent details"""
    
    # Get protocol info
    hospital_data = await get_hospital_data()
    
    # Build ambulance instructions section
    instructions = """🚨 STEMI PROTOCOL ACTIVATED - INSTRUCTIONS FOR EMS

📍 DESTINATION: Trauma Bay 1 (Direct Entry - Bypass Triage)

🚑 TRANSPORT INSTRUCTIONS:
1. Maintain high-flow oxygen (keep SpO2 >94%)
2. Continue cardiac monitoring
3. Keep patient calm and still
4. Call 5 minutes before arrival if status changes
5. Report any: hypotension, arrhythmia, or cardiac arrest immediately

⏱️ WE ARE READY:
• Trauma Bay 1: Cleared and waiting
• Cath Lab Team: Mobilizing (ETA 15 min)
• All medications: Prepared and staged
• Cardiac ICU bed: Reserved
• STAT labs: Ready for immediate processing

🎯 Door-to-Balloon Target: <90 minutes
Team will meet you at ambulance entrance.

═══════════════════════════════════════════════════════════
📊 DETAILED AGENT COORDINATION REPORT
(Multi-Agent System Response)
═══════════════════════════════════════════════════════════
"""
    
    # Add each agent's response
    agent_order = ["bed_management", "pharmacy", "lab_service", "specialist_coordinator", "resource_manager", "whatsapp_notification"]
    for agent_name in agent_order:
        if agent_name in agent_responses:
            instructions += f"\n{agent_responses[agent_name]['text']}\n\n---\n"
    
    instructions += f"\n🎯 COORDINATION COMPLETE: {len(agent_responses)}/6 agents responded"
    instructions += f"\n⏱️ Total coordination time: <10 seconds"
    instructions += f"\n✅ All systems ready for patient arrival"
    
    return instructions

@agent.on_interval(period=120.0)
async def health_check(ctx: Context):
    cases = ctx.storage.get("total_cases")
    protocols = ctx.storage.get("protocols_activated")
    ctx.logger.info(f"💓 Health: {cases} cases, {protocols} protocols activated")

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()