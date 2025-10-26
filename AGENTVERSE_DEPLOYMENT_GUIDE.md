# Agentverse Deployment Guide - Single File Implementation

## 🎯 Important Constraint

**Agentverse Build Section accepts ONLY ONE FILE**: `agent.py`

This means we CANNOT use multiple files like:
- ❌ `agent_config.py`
- ❌ `orchestrator_utils.py`
- ❌ Multiple Python modules

## ✅ Solution: Single Self-Contained File

We will create **ONE complete Python file** that contains:
1. **Configuration section** (agent addresses, protocols) at the top
2. **Helper functions** (intent parsing, coordination)
3. **Agent creation** and setup
4. **Protocol handlers** and orchestration logic
5. **Message handlers** (existing + new orchestration)
6. **Agent startup** and run code

## 📁 File Structure (All in ONE file)

```python
"""
ED Coordinator Agent - Orchestrator Version
Single file for Agentverse deployment
"""

# ============================================================================
# SECTION 1: IMPORTS
# ============================================================================
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (...)
import asyncio
from datetime import datetime
from uuid import uuid4
import os

# ============================================================================
# SECTION 2: CONFIGURATION (Embedded)
# ============================================================================
AGENT_ADDRESSES = {
    "bed_manager": "agent1qf785dg24awwrwvmwwn0djpm5jwhpmfp6lysv7da0d9g68c7aa5p7z4lcxg",
    "specialist_hub": "agent1qvy05wjeh6jrvs3dchznr6jqwpytzcrt5679ye98na4wqlursy7j26seanx",
    # ... etc
}

PROTOCOL_WORKFLOWS = {
    "stemi": {
        "agents": [...],
        "queries": {...},
        # ... etc
    }
}

ROUTING_RULES = {...}

# ============================================================================
# SECTION 3: HELPER FUNCTIONS
# ============================================================================
async def parse_intent(query: str) -> dict:
    """Determine query type"""
    # Intent parsing logic here
    pass

async def coordinate_agents(ctx: Context, agents: list, queries: dict) -> dict:
    """Multi-agent coordination"""
    # Coordination logic here
    pass

async def execute_protocol(ctx: Context, protocol_name: str) -> str:
    """Execute emergency protocol"""
    # Protocol execution logic here
    pass

# ... other helper functions

# ============================================================================
# SECTION 4: AGENT CREATION
# ============================================================================
AGENT_SEED = os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_phrase_001")
agent = Agent(name="ed_coordinator", seed=AGENT_SEED, port=8000)
protocol = Protocol(spec=chat_protocol_spec)

# ============================================================================
# SECTION 5: EVENT HANDLERS
# ============================================================================
@agent.on_event("startup")
async def initialize(ctx: Context):
    """Initialize agent state"""
    # Startup logic
    pass

# ============================================================================
# SECTION 6: MESSAGE HANDLERS (Original + Orchestrator)
# ============================================================================
@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat with orchestration"""
    # Parse intent
    intent = await parse_intent(text)
    
    # Route based on type:
    if intent["type"] == "protocol":
        response = await execute_protocol(ctx, intent["protocol"])
    elif intent["type"] == "route":
        response = await route_query(ctx, intent["agents"], text)
    else:
        response = await process_query(ctx, text)  # Original functionality
    
    # Send response
    pass

# ============================================================================
# SECTION 7: RUN AGENT
# ============================================================================
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
```

## 📋 Deployment Process

### Step 1: Backup Current Code
1. Go to Agentverse → Your ED Coordinator agent
2. Open "Build" section
3. **Copy ALL existing code**
4. Save it locally as `ed_coordinator_backup.py`

### Step 2: Prepare New Code
1. I'll create the complete orchestrator as ONE file
2. The file will be: `agentverse_agents/ed_coordinator_orchestrator.py`
3. This file contains EVERYTHING needed

### Step 3: Deploy to Agentverse
1. Open your ED Coordinator in Agentverse
2. Go to "Build" section
3. **Select all existing code** (Ctrl+A / Cmd+A)
4. **Delete it**
5. **Paste the new orchestrator code** (entire file)
6. Click "Deploy" button
7. Wait for successful deployment

### Step 4: Verify Deployment
1. Check agent logs for startup messages
2. Look for: "🏥 ED Coordinator Orchestrator started"
3. Test with simple query: "system status"
4. Test protocol: "activate stemi"

### Step 5: Rollback (if needed)
If something goes wrong:
1. Go back to Build section
2. Delete new code
3. Paste your backup code
4. Re-deploy
5. Debug offline

## 🎨 Single File Design Pattern

The orchestrator file will follow this structure:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  agent.py (Single File)                         │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 1. IMPORTS                               │  │
│  │    All dependencies                      │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 2. CONFIGURATION (Embedded)              │  │
│  │    • AGENT_ADDRESSES                     │  │
│  │    • PROTOCOL_WORKFLOWS                  │  │
│  │    • ROUTING_RULES                       │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 3. HELPER FUNCTIONS                      │  │
│  │    • parse_intent()                      │  │
│  │    • send_agent_query()                  │  │
│  │    • coordinate_agents()                 │  │
│  │    • execute_protocol()                  │  │
│  │    • format_response()                   │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 4. AGENT SETUP                           │  │
│  │    agent = Agent(...)                    │  │
│  │    protocol = Protocol(...)              │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 5. EVENT HANDLERS                        │  │
│  │    @agent.on_event("startup")            │  │
│  │    @agent.on_interval(...)               │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 6. MESSAGE HANDLERS                      │  │
│  │    @protocol.on_message(ChatMessage)     │  │
│  │    Enhanced with orchestration           │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 7. RUN                                   │  │
│  │    agent.include(protocol)               │  │
│  │    if __name__ == "__main__": run()      │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

## ⚙️ Configuration Management

Since we can't use separate config files, configuration is embedded in the code:

```python
# Agent Registry - Update these with your actual addresses
AGENT_ADDRESSES = {
    "bed_manager": "agent1qf785dg24awwrwvmwwn0djpm5jwhpmfp6lysv7da0d9g68c7aa5p7z4lcxg",
    "specialist_hub": "agent1qvy05wjeh6jrvs3dchznr6jqwpytzcrt5679ye98na4wqlursy7j26seanx",
    "pharmacy": "agent1qd5uf5ttptlgaknuhl7ws8ff08qrzjavzvv8krc40e03zrxhckx45lxzn2s",
    "lab_service": "agent1q275vgl4wczlscdnprv4fr9sw3r7hsemrpx8cxuhs7jj3pgt40yyq6p3vz4",
    "resource_manager": "agent1qfdy6crsyuek6dxym68pxsw8tz0esmr0qxn0rpgf8qst5y6w7sawyfqm0tj",
}

# Protocol Workflows
PROTOCOL_WORKFLOWS = {
    "stemi": {
        "agents": ["resource_manager", "bed_manager", "lab_service", "pharmacy", "specialist_hub"],
        "queries": {
            "resource_manager": "Allocate bed for STEMI patient",
            "bed_manager": "ICU bed availability?",
            "lab_service": "Order STAT troponin and ECG",
            "pharmacy": "Prepare aspirin 325mg and heparin",
            "specialist_hub": "Page cardiology STEMI team",
        },
        "timeout": 30.0,
        "target_time": 5.0,
    },
    # ... other protocols
}

# Query Routing
ROUTING_RULES = {
    "bed": ["bed_manager"],
    "icu": ["bed_manager"],
    "lab": ["lab_service"],
    # ... etc
}
```

## 📝 Code Organization Best Practices

### Clear Section Headers
```python
# ============================================================================
# SECTION NAME
# ============================================================================
```

### Inline Documentation
```python
async def execute_protocol(ctx: Context, protocol_name: str) -> str:
    """
    Execute emergency protocol workflow
    
    Args:
        ctx: Agent context
        protocol_name: Protocol to execute (stemi, stroke, trauma)
    
    Returns:
        Formatted response string
    """
    # Implementation
```

### Logical Grouping
Group related functions together:
- Configuration (top)
- Utilities (intent parsing, formatting)
- Coordination (multi-agent calling)
- Protocols (emergency workflows)
- Handlers (message, events)

## 🧪 Testing Strategy

### Local Testing (Optional)
Before deploying to Agentverse:
1. Save the file locally as `test_orchestrator.py`
2. Run: `python test_orchestrator.py`
3. Check for syntax errors
4. Verify imports work

### Agentverse Testing
After deployment:
1. **Test 1**: Simple query
   - Send: "system status"
   - Should work (existing functionality)

2. **Test 2**: Protocol activation
   - Send: "activate stemi"
   - Should coordinate all 5 agents

3. **Test 3**: Query routing
   - Send: "ICU beds available?"
   - Should route to bed manager

4. **Test 4**: Error handling
   - Send query with timeout scenario
   - Should handle gracefully

## ⚡ Quick Deployment Checklist

- [ ] Backup current ED Coordinator code from Agentverse
- [ ] Review the new orchestrator code
- [ ] Verify agent addresses are correct
- [ ] Go to Agentverse Build section
- [ ] Select all existing code (Ctrl+A)
- [ ] Delete existing code
- [ ] Paste new orchestrator code
- [ ] Click Deploy button
- [ ] Wait for "Deploy successful" message
- [ ] Check agent logs for startup
- [ ] Test with "system status"
- [ ] Test with "activate stemi"
- [ ] Verify orchestration works

## 🔄 Update Process

If you need to update configuration later:
1. Go to Agentverse Build section
2. Find the configuration section (near top of file)
3. Update values (e.g., agent addresses)
4. Click Deploy
5. Wait for redeployment

## 🚨 Troubleshooting

### Issue: "Import Error"
- Check all imports are at the top
- Verify uagents version compatibility

### Issue: "Agent doesn't start"
- Check logs for syntax errors
- Verify AGENT_SEED is correct

### Issue: "Can't reach other agents"
- Verify agent addresses are correct
- Check agents are deployed and running
- Test individual agent addresses

### Issue: "Timeout errors"
- Increase timeout values in PROTOCOL_WORKFLOWS
- Check network connectivity
- Verify agent mailbox addresses

## 📊 Advantages of Single File

✅ **Simple Deployment**: One copy-paste operation  
✅ **No Import Issues**: Everything in one file  
✅ **Easy to Update**: Edit configuration in one place  
✅ **Agentverse Compatible**: Matches platform constraints  
✅ **Version Control**: Single file to track changes  

## 🎯 Next Steps

Now that we understand the single-file constraint:

1. **Switch to Code Mode** when ready
2. I'll create the complete orchestrator as ONE self-contained file
3. You copy-paste it into Agentverse Build section
4. Deploy and test

The file will be created as:
`agentverse_agents/ed_coordinator_orchestrator.py`

This file will contain ALL orchestration logic, configuration, and helper functions in a single, deployable unit.

---

**Ready**: Single-file architecture designed for Agentverse deployment  
**Format**: One complete Python file with embedded configuration  
**Compatibility**: 100% compatible with Agentverse Build section