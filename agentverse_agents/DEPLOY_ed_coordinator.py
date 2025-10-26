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
        "resource_manager": "REPLACE_WITH_RESOURCE_MANAGER_ADDRESS",
        "specialist_coordinator": "REPLACE_WITH_SPECIALIST_COORDINATOR_ADDRESS",
        "lab_service": "REPLACE_WITH_LAB_SERVICE_ADDRESS",
        "pharmacy": "REPLACE_WITH_PHARMACY_ADDRESS",
        "bed_management": "REPLACE_WITH_BED_MANAGEMENT_ADDRESS"
    })
    
    ctx.logger.info(f"🏥 ED Coordinator Agent Started")
    ctx.logger.info(f"📍 Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"🔧 Tools: JSONBin + Claude AI enabled")
    ctx.logger.info(f"📊 JSONBin ID: {JSONBIN_ID[:20]}...")
    ctx.logger.info(f"🚑 Ambulance broadcast system enabled")

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"📨 Message received from {sender[:16]}...")
    
    # LOOP PREVENTION: Ignore responses from other agents
    agent_addresses = ctx.storage.get("agent_addresses")
    if agent_addresses and sender in agent_addresses.values():
        ctx.logger.info(f"📥 Response from agent (ignoring to prevent loop)")
        await ctx.send(sender, ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        ))
        return
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(),
        acknowledged_msg_id=msg.msg_id
    ))
    
    text = ''.join(item.text for item in msg.content if isinstance(item, TextContent))
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
            broadcast_message = f"""🚑 AMBULANCE REPORT - {protocol_name.upper()} PROTOCOL

{text}

AI ANALYSIS:
{analysis}

⚡ ACTION REQUIRED: Prepare for incoming patient
Coordinator: ED Coordinator

Please respond with your preparation status."""
            
            ctx.logger.info("📡 Broadcasting to all 5 agents...")
            agents_to_notify = [
                ("Resource Manager", agent_addresses.get("resource_manager")),
                ("Specialist Coordinator", agent_addresses.get("specialist_coordinator")),
                ("Lab Service", agent_addresses.get("lab_service")),
                ("Pharmacy", agent_addresses.get("pharmacy")),
                ("Bed Management", agent_addresses.get("bed_management"))
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
            
            response_prompt = f"""You are the ED Coordinator responding to ambulance crew.

Protocol: {protocol_name}
Agents Coordinated: {broadcast_count}/5
Analysis: {analysis}

Create a BRIEF, ACTIONABLE response for ambulance crew that includes:
1. Confirmation we're ready (1 sentence)
2. What bay/room to bring patient to
3. What we've prepared (bullets, max 4 items)
4. ETA for specialist team
5. Any special instructions for transport

Keep it under 150 words. Be direct and practical for EMS crew."""

            final_response = await claude_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=300,
                messages=[{"role": "user", "content": response_prompt}]
            )
            response_text = final_response.content[0].text
            ctx.logger.info("✅ Final response generated")
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

@agent.on_interval(period=120.0)
async def health_check(ctx: Context):
    cases = ctx.storage.get("total_cases")
    protocols = ctx.storage.get("protocols_activated")
    ctx.logger.info(f"💓 Health: {cases} cases, {protocols} protocols activated")

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()