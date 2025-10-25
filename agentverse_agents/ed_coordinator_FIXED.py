"""
ED Coordinator Orchestrator - FINAL FIXED VERSION
Following Agentverse reference patterns for proper message handling
With Claude AI + LangChain for intelligent routing
"""

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    StartSessionContent,
    MetadataContent,
    chat_protocol_spec,
)
from datetime import datetime
from uuid import uuid4
import os
import asyncio

# LangChain imports
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

# ============================================================================
# CONFIGURATION
# ============================================================================

AGENT_ADDRESSES = {
    "bed_manager": "agent1qf785dg24awwrwvmwn0djpm5jwhpmfp6lysv7da0d9g68c7aa5p7z4lcxg",
    "specialist_hub": "agent1qvy05wjeh6jrvs3dchznr6jqwpytzcrt5679ye98na4wqlursy7j26seanx",
    "pharmacy": "agent1qd5uf5ttptlgaknuhl7ws8ff08qrzjavzvv8krc40e03zrxhckx45lxzn2s",
    "lab_service": "agent1q275vgl4wczlscdnprv4fr9sw3r7hsemrpx8cxuhs7jj3pgt40yyq6p3vz4",
    "resource_manager": "agent1qfdy6crsyuek6dxym68pxsw8tz0esmr0qxn0rpgf8qst5y6w7sawyfqm0tj",
}

PROTOCOL_WORKFLOWS = {
    "stemi": {
        "name": "STEMI (Heart Attack)",
        "emoji": "❤️",
        "agents": ["resource_manager", "bed_manager", "lab_service", "pharmacy", "specialist_hub"],
        "queries": {
            "resource_manager": "Allocate bed for STEMI patient urgently",
            "bed_manager": "Reserve ICU bed for STEMI patient",
            "lab_service": "Order STAT troponin, ECG, and cardiac panel",
            "pharmacy": "Prepare aspirin 325mg and heparin for STEMI",
            "specialist_hub": "Page cardiology STEMI team immediately",
        },
        "target_time": 5.0,
        "description": "Cardiac emergency - door to balloon <5 min"
    },
    "stroke": {
        "name": "Stroke (CVA)",
        "emoji": "🧠",
        "agents": ["resource_manager", "lab_service", "pharmacy", "specialist_hub"],
        "queries": {
            "resource_manager": "Allocate bed for stroke patient urgently",
            "lab_service": "Order STAT CT scan and coagulation panel",
            "pharmacy": "Prepare tPA if eligible",
            "specialist_hub": "Page neurology stroke team",
        },
        "target_time": 7.0,
        "description": "Cerebrovascular emergency - door to needle <7 min"
    },
    "trauma": {
        "name": "Trauma",
        "emoji": "🚑",
        "agents": ["resource_manager", "bed_manager", "lab_service", "pharmacy", "specialist_hub"],
        "queries": {
            "resource_manager": "Allocate trauma bay immediately",
            "bed_manager": "Reserve ICU bed for trauma",
            "lab_service": "Order type & cross, trauma panel STAT",
            "pharmacy": "Prepare blood products",
            "specialist_hub": "Activate trauma surgery team",
        },
        "target_time": 3.0,
        "description": "Multi-trauma emergency - activation <3 min"
    },
}

# ============================================================================
# AI SETUP
# ============================================================================

def get_claude_llm():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        anthropic_api_key=api_key,
        temperature=0.1,
        max_tokens=500
    )

INTENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Classify ED query as: protocol (emergency), route (specific agent), or local (general).
Respond with JSON: {{"type": "protocol|route|local", "protocol": "stemi|stroke|trauma", "agents": ["name"], "reasoning": "why", "confidence": 0-1}}"""),
    ("human", "{query}")
])

def create_intent_chain():
    return ({"query": RunnablePassthrough()} | INTENT_PROMPT | get_claude_llm() | JsonOutputParser())

async def parse_intent_with_ai(ctx: Context, query: str) -> dict:
    if not ctx.storage.get("ai_enabled"):
        return fallback_intent_parse(query)
    
    try:
        ctx.logger.info(f"🤖 Using Claude AI...")
        intent_chain = create_intent_chain()
        result = await asyncio.get_event_loop().run_in_executor(None, lambda: intent_chain.invoke(query))
        ctx.logger.info(f"   AI: {result['type']} (confidence: {result.get('confidence', 0):.2f})")
        ctx.logger.info(f"   Reasoning: {result.get('reasoning', '')[:100]}")
        return result
    except Exception as e:
        ctx.logger.error(f"❌ AI failed: {e}")
        return fallback_intent_parse(query)

def fallback_intent_parse(query: str) -> dict:
    q = query.lower()
    if "stemi" in q or "heart attack" in q:
        return {"type": "protocol", "protocol": "stemi", "confidence": 0.9}
    elif "stroke" in q or "cva" in q:
        return {"type": "protocol", "protocol": "stroke", "confidence": 0.9}
    elif "trauma" in q:
        return {"type": "protocol", "protocol": "trauma", "confidence": 0.9}
    elif "bed" in q or "icu" in q:
        return {"type": "route", "agents": ["bed_manager"], "confidence": 0.8}
    elif "lab" in q:
        return {"type": "route", "agents": ["lab_service"], "confidence": 0.8}
    elif "pharmacy" in q or "medication" in q:
        return {"type": "route", "agents": ["pharmacy"], "confidence": 0.8}
    return {"type": "local", "confidence": 0.7}

# ============================================================================
# AGENT COORDINATION
# ============================================================================

async def coordinate_agents(ctx: Context, agents: list, queries: dict) -> str:
    ctx.logger.info(f"🔄 Coordinating {len(agents)} agents...")
    success = 0
    for agent_name in agents:
        agent_address = AGENT_ADDRESSES.get(agent_name)
        if agent_address:
            query_text = queries.get(agent_name, "Status?")
            try:
                msg = ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(),
                                content=[TextContent(type="text", text=query_text)])
                await ctx.send(agent_address, msg)
                ctx.logger.info(f"  ✓ {agent_name}")
                success += 1
            except Exception as e:
                ctx.logger.error(f"  ✗ {agent_name}: {e}")
    
    return f"{success}/{len(agents)} agents coordinated"

async def execute_protocol(ctx: Context, protocol_name: str) -> str:
    protocol = PROTOCOL_WORKFLOWS.get(protocol_name)
    if not protocol:
        return f"❌ Unknown protocol: {protocol_name}"
    
    ctx.logger.info(f"🚨 Executing {protocol_name.upper()} Protocol")
    
    coordination_result = await coordinate_agents(ctx, protocol["agents"], protocol["queries"])
    
    emoji = protocol["emoji"]
    name = protocol["name"]
    target = protocol["target_time"]
    desc = protocol["description"]
    
    output = f"{emoji} {name} PROTOCOL ACTIVATED\n\n"
    output += f"📋 {desc}\n\n"
    output += f"✅ Coordination: {coordination_result}\n"
    output += f"⏱️  Target: <{target} min\n"
    output += f"🤖 AI: {'Enabled' if ctx.storage.get('ai_enabled') else 'Fallback'}\n\n"
    
    output += "Actions Initiated:\n"
    for agent_name, query in protocol["queries"].items():
        output += f"• {query}\n"
    
    return output

# ============================================================================
# AGENT SETUP
# ============================================================================

AGENT_SEED = os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_phrase_001")
agent = Agent(name="ed_coordinator", seed=AGENT_SEED, port=8000)
protocol = Protocol(spec=chat_protocol_spec)

# ============================================================================
# STARTUP
# ============================================================================

@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.logger.info("=" * 70)
    ctx.logger.info("🏥 ED COORDINATOR - AI ORCHESTRATOR")
    ctx.logger.info("=" * 70)
    
    # Initialize storage
    ctx.storage.set("active_cases", [])
    ctx.storage.set("total_queries", 0)
    
    # Check AI
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        ctx.logger.error("❌ ANTHROPIC_API_KEY NOT SET!")
        ctx.logger.error("   Add to Agentverse Secrets: ANTHROPIC_API_KEY")
        ctx.logger.warning("⚠️  AI DISABLED - Using keyword fallback")
        ctx.storage.set("ai_enabled", False)
    else:
        try:
            ctx.logger.info(f"✅ API Key: {api_key[:15]}...{api_key[-4:]}")
            llm = get_claude_llm()
            ctx.logger.info("✅ Claude AI: Connected")
            ctx.logger.info("🤖 AI Routing: ENABLED")
            ctx.storage.set("ai_enabled", True)
        except Exception as e:
            ctx.logger.error(f"❌ AI Init failed: {e}")
            ctx.storage.set("ai_enabled", False)
    
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🔄 Agents: {len(AGENT_ADDRESSES)}")
    ctx.logger.info("=" * 70)

# ============================================================================
# MESSAGE HANDLER (Following Reference Pattern)
# ============================================================================

@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle messages following Agentverse reference pattern"""
    ctx.logger.info(f"📨 Message from {sender[:16]}...")
    
    # Always send acknowledgement first
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    
    # Process content items (following reference pattern)
    text_content = []
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            # Handle session start (ASI:One compatibility)
            ctx.logger.info("   🔄 Session started")
            await ctx.send(sender, ChatMessage(
                timestamp=datetime.utcnow(),
                msg_id=uuid4(),
                content=[MetadataContent(type="metadata", metadata={"ready": "true"})]
            ))
            return  # Don't process StartSession as a query
            
        elif isinstance(item, TextContent):
            text_content.append(item.text)
    
    # CRITICAL: Only process if we have actual text content
    if not text_content:
        ctx.logger.info("   ℹ️  No text content - skipping")
        return  # Don't respond to empty messages
    
    # Join all text content
    text = ''.join(text_content)
    
    # CRITICAL: Ignore messages FROM our coordinated agents (prevent loop)
    if sender in AGENT_ADDRESSES.values():
        agent_name = [name for name, addr in AGENT_ADDRESSES.items() if addr == sender]
        ctx.logger.info(f"   ℹ️  From agent '{agent_name[0] if agent_name else 'unknown'}' - ignoring")
        return  # Don't process agent responses
    
    ctx.logger.info(f"   ✅ User query: {text[:60]}...")
    
    # Update tracking
    total = (ctx.storage.get("total_queries") or 0) + 1
    ctx.storage.set("total_queries", total)
    
    # Parse intent with AI
    intent = await parse_intent_with_ai(ctx, text)
    
    # Generate response based on intent
    if intent["type"] == "protocol":
        ctx.logger.info(f"🚨 Protocol: {intent.get('protocol', '').upper()}")
        response_text = await execute_protocol(ctx, intent.get("protocol", "stemi"))
    
    elif intent["type"] == "route":
        agents_list = intent.get("agents", [])
        ctx.logger.info(f"🔀 Routing to: {', '.join(agents_list)}")
        
        # Send to target agents
        for agent_name in agents_list:
            agent_addr = AGENT_ADDRESSES.get(agent_name)
            if agent_addr:
                try:
                    await ctx.send(agent_addr, ChatMessage(
                        timestamp=datetime.utcnow(), msg_id=uuid4(),
                        content=[TextContent(type="text", text=text)]
                    ))
                    ctx.logger.info(f"  ✓ Routed to {agent_name}")
                except Exception as e:
                    ctx.logger.error(f"  ✗ {agent_name}: {e}")
        
        response_text = f"🔀 Routed to: {', '.join([a.replace('_', ' ').title() for a in agents_list])}\nThey will respond shortly."
    
    else:
        # Local processing
        ctx.logger.info("💬 Local processing")
        response_text = f"""🏥 EDFlow AI Orchestrator

Query: "{text[:100]}"

AI Status: {'✅ Enabled' if ctx.storage.get('ai_enabled') else '⚠️  Fallback Mode'}

Emergency Protocols:
• "activate stemi protocol" or "chest pain patient"
• "activate stroke protocol" or "stroke symptoms"
• "activate trauma protocol" or "trauma patient"

Queries processed: {total}"""
    
    # Send response (ONLY if we have text content)
    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=response_text)]
    ))
    
    ctx.logger.info("✅ Response sent to user")


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.debug(f"Ack from {sender[:16]}")

# ============================================================================
# RUN
# ============================================================================

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()