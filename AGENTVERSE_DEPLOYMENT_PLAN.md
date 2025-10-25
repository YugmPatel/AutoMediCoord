# 🚀 Agentverse Deployment Plan - EDFlow AI Agents

## Overview
Complete implementation plan for deploying EDFlow AI agents to Fetch.ai Agentverse platform, enabling ASI-1 agent integration and inter-agent communication.

---

## 📚 Research Summary - Official Documentation

### Key Resources:
- Fetch.ai uAgents Documentation: https://docs.fetch.ai/guides/agents/
- Agentverse Platform: https://agentverse.ai
- Agent Mailbox Protocol: https://docs.fetch.ai/guides/agents/intermediate/mailbox
- Agent Communication: https://docs.fetch.ai/guides/agents/intermediate/communicating-with-other-agents

### Key Concepts:
1. **Local Agents**: Run on your machine, require port forwarding
2. **Agentverse Hosted**: Cloud-hosted agents with built-in mailbox
3. **Mailbox**: Communication relay for agents that can't receive direct messages
4. **Agent Address**: Unique identifier (format: `agent1q...`)
5. **Almanac**: Agent registry for discovery

---

## 🎯 Deployment Architecture

```
┌────────────────────────────────────────────────────┐
│              Agentverse Cloud Platform             │
│  ┌──────────────────────────────────────────────┐ │
│  │  Hosted Agent 1: ED Coordinator              │ │
│  │  - Mailbox: enabled                          │ │
│  │  - Address: agent1q...                       │ │
│  └──────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────┐ │
│  │  Hosted Agent 2: Resource Manager            │ │
│  └──────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────┐ │
│  │  Hosted Agent 3-6: Lab, Pharmacy, etc.       │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
         ↓ Communication via Almanac ↓
┌────────────────────────────────────────────────────┐
│            External Agents (ASI-1, etc.)           │
└────────────────────────────────────────────────────┘
```

---

## 📋 Implementation Plan

---

## PHASE 1: Agentverse Account Setup (30 minutes)

### Step 1.1: Create Agentverse Account
1. Visit https://agentverse.ai
2. Click "Sign Up" or "Get Started"
3. Register with email or GitHub
4. Verify email address
5. Complete profile setup

### Step 1.2: Understand Dashboard
- **My Agents**: View and manage hosted agents
- **Agents**: Discover other agents on network
- **Services**: Find available agent services
- **Mailroom**: Check agent messages
- **Settings**: API keys and configuration

### Step 1.3: Generate API Key (if needed)
1. Go to Settings → API Keys
2. Click "Create New API Key"
3. Copy and save securely
4. Add to `.env` file

**Deliverable:** ✅ Agentverse account ready

---

## PHASE 2: Prepare Agent Code for Agentverse (2-3 hours)

### Step 2.1: Understand Agent Requirements

**For Agentverse Deployment, agents must:**
- Be written in Python using uAgents framework
- Have a single agent per file
- Use `agent.run()` at the end
- Not use `Bureau` (multi-agent runner)
- Keep dependencies minimal

### Step 2.2: Create Standalone Agent Files

Currently, our agents are in `src/agents.py` as a bureau. We need to split them.

**Create these files:**

1. `agentverse_agents/ed_coordinator.py`
2. `agentverse_agents/resource_manager.py`
3. `agentverse_agents/lab_service.py`
4. `agentverse_agents/pharmacy.py`
5. `agentverse_agents/specialist_coordinator.py`
6. `agentverse_agents/bed_management.py`

### Step 2.3: Agent Code Template

Each agent file should follow this structure:

```python
# agentverse_agents/ed_coordinator.py

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import os

# Define message models
class PatientArrival(Model):
    patient_id: str
    symptoms: str
    acuity: int

class SystemStatusQuery(Model):
    query_id: str
    requester: str

class SystemStatusResponse(Model):
    query_id: str
    active_cases: int
    available_beds: int
    system_load: str

# Create agent
agent = Agent(
    name="ed_coordinator",
    seed=os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_recovery_phrase"),
    port=8000,  # Not used in Agentverse but required
)

# Storage for agent state
@agent.on_event("startup")
async def initialize(ctx: Context):
    ctx.storage.set("active_cases", [])
    ctx.storage.set("available_beds", 10)
    ctx.logger.info(f"ED Coordinator started: {ctx.agent.address}")

# Message handlers
@agent.on_message(model=PatientArrival)
async def handle_patient(ctx: Context, sender: str, msg: PatientArrival):
    ctx.logger.info(f"Patient arrived: {msg.patient_id}")
    
    cases = ctx.storage.get("active_cases")
    cases.append({
        "id": msg.patient_id,
        "symptoms": msg.symptoms,
        "acuity": msg.acuity
    })
    ctx.storage.set("active_cases", cases)

@agent.on_message(model=SystemStatusQuery)
async def handle_status_query(ctx: Context, sender: str, msg: SystemStatusQuery):
    """Handle external queries from ASI-1 or other agents"""
    ctx.logger.info(f"Status query from: {sender}")
    
    response = SystemStatusResponse(
        query_id=msg.query_id,
        active_cases=len(ctx.storage.get("active_cases")),
        available_beds=ctx.storage.get("available_beds"),
        system_load="medium"
    )
    
    await ctx.send(sender, response)

# Interval tasks
@agent.on_interval(period=60.0)
async def periodic_check(ctx: Context):
    """Check system health every minute"""
    cases = ctx.storage.get("active_cases")
    ctx.logger.info(f"System check: {len(cases)} active cases")

# Required for Agentverse
if __name__ == "__main__":
    agent.run()
```

### Step 2.4: Create requirements.txt for Agentverse

```txt
# agentverse_agents/requirements.txt
uagents>=1.0.0
pydantic>=2.0.0
```

**Deliverable:** ✅ 6 standalone agent files ready for Agentverse

---

## PHASE 3: Deploy First Agent to Agentverse (1 hour)

### Step 3.1: Login to Agentverse

1. Go to https://agentverse.ai
2. Login with your credentials
3. Navigate to "My Agents" section

### Step 3.2: Create New Hosted Agent

1. Click "**+ New Agent**" or "**Create Agent**"
2. Choose "**Hosted Agent**" (not local)
3. Agent creation wizard will open

### Step 3.3: Configure Agent

**Agent Configuration:**

- **Name**: `ed_coordinator`
- **Description**: "Emergency Department Coordinator - Main orchestration agent for EDFlow AI"
- **Agent Code**: Copy-paste content from `agentverse_agents/ed_coordinator.py`
- **Requirements**: Copy from requirements.txt (if prompted)

### Step 3.4: Deploy Agent

1. Click "**Deploy**" or "**Create & Deploy**"
2. Wait for deployment (30-60 seconds)
3. Agent status should show "**Running**" or "**Active**"

### Step 3.5: Get Agent Details

After deployment, you'll see:

- **Agent Address**: `agent1q...` (40+ characters)
- **Mailbox**: Automatically enabled for hosted agents
- **Status**: Running
- **Logs**: View real-time logs

**Copy and save the agent address!**

### Step 3.6: Test Agent Locally

Create a test script to send message:

```python
# test_agentverse_agent.py

from uagents import Agent, Context, Model

class SystemStatusQuery(Model):
    query_id: str
    requester: str

test_agent = Agent(name="test", seed="test_seed", port=8001)

ED_COORDINATOR_ADDRESS = "agent1q..."  # Your deployed agent address

@test_agent.on_interval(period=10.0)
async def send_query(ctx: Context):
    await ctx.send(
        ED_COORDINATOR_ADDRESS,
        SystemStatusQuery(
            query_id="test-001",
            requester=ctx.agent.address
        )
    )
    ctx.logger.info("Query sent to ED Coordinator")

if __name__ == "__main__":
    test_agent.run()
```

Run test:
```bash
python test_agentverse_agent.py
```

Check logs on Agentverse dashboard to verify message received.

**Deliverable:** ✅ ED Coordinator deployed and tested

---

## PHASE 4: Deploy Remaining Agents (2-3 hours)

### Repeat for Each Agent:

1. **Resource Manager**
   - File: `agentverse_agents/resource_manager.py`
   - Name: `resource_manager`
   - Description: "Manages beds, equipment, and resources"

2. **Lab Service**
   - File: `agentverse_agents/lab_service.py`
   - Name: `lab_service`
   - Description: "Laboratory test coordination"

3. **Pharmacy**
   - File: `agentverse_agents/pharmacy.py`
   - Name: `pharmacy`
   - Description: "Medication dispensing"

4. **Specialist Coordinator**
   - File: `agentverse_agents/specialist_coordinator.py`
   - Name: `specialist_coordinator`
   - Description: "Specialist doctor coordination"

5. **Bed Management**
   - File: `agentverse_agents/bed_management.py`
   - Name: `bed_management`
   - Description: "ICU and regular bed allocation"

### Document All Addresses:

Create `AGENT_ADDRESSES.txt`:

```txt
EDFlow AI - Agentverse Deployed Agents
======================================

ED Coordinator:
Address: agent1q...
Role: Main orchestrator
Protocols: SystemStatusQuery, PatientArrival

Resource Manager:
Address: agent1q...
Role: Resource allocation
Protocols: ResourceQuery

Lab Service:
Address: agent1q...
Role: Laboratory coordination
Protocols: LabTestRequest

Pharmacy:
Address: agent1q...
Role: Medication management
Protocols: MedicationRequest

Specialist Coordinator:
Address: agent1q...
Role: Doctor coordination
Protocols: SpecialistRequest

Bed Management:
Address: agent1q...
Role: Bed assignment
Protocols: BedRequest
```

**Deliverable:** ✅ All 6 agents deployed to Agentverse

---

## PHASE 5: Enable Agent-to-Agent Communication (1-2 hours)

### Step 5.1: Update Agent Code with Peer Addresses

Each agent needs to know other agents' addresses.

**Option 1: Hardcode addresses in agent code**

```python
# In ed_coordinator.py after deployment

RESOURCE_MANAGER_ADDRESS = "agent1q..."
LAB_SERVICE_ADDRESS = "agent1q..."
PHARMACY_ADDRESS = "agent1q..."
# etc.

@agent.on_message(model=PatientArrival)
async def handle_patient(ctx: Context, sender: str, msg: PatientArrival):
    # Forward to resource manager
    await ctx.send(RESOURCE_MANAGER_ADDRESS, ResourceRequest(...))
```

**Option 2: Use environment variables (recommended)**

Update agent code to read from environment:

```python
import os

RESOURCE_MANAGER = os.getenv("RESOURCE_MANAGER_ADDRESS")
```

Then set in Agentverse:
1. Go to agent settings
2. Find "Environment Variables" section
3. Add: `RESOURCE_MANAGER_ADDRESS = agent1q...`

### Step 5.2: Update and Redeploy Agents

For each agent:
1. Update code with peer addresses
2. Click "**Edit**" on Agentverse
3. Paste updated code
4. Click "**Save & Redeploy**"
5. Wait for redeployment

### Step 5.3: Test Inter-Agent Communication

Send a test patient arrival:

```python
# test_patient_flow.py

from uagents import Agent, Context
from your_models import PatientArrival

test_agent = Agent(name="test", seed="test", port=9000)

ED_COORDINATOR_ADDRESS = "agent1q..."

@test_agent.on_interval(period=30.0)
async def send_patient(ctx: Context):
    await ctx.send(
        ED_COORDINATOR_ADDRESS,
        PatientArrival(
            patient_id="TEST001",
            symptoms="Chest pain",
            acuity=1
        )
    )
    ctx.logger.info("Patient sent to ED")

if __name__ == "__main__":
    test_agent.run()
```

Check logs on all agents to verify message propagation.

**Deliverable:** ✅ Agents communicating on Agentverse

---

## PHASE 6: Enable ASI-1 Integration (1 hour)

### Step 6.1: Define Query Protocol

Create standardized query interface:

```python
# In ed_coordinator.py

class QuerySystemStatus(Model):
    query_id: str
    requested_by: str  # ASI-1 agent address

class SystemStatusResponse(Model):
    query_id: str
    active_cases: int
    available_beds: int
    staff_on_duty: int
    system_load: str  # "low", "medium", "high"
    timestamp: str

@agent.on_message(model=QuerySystemStatus)
async def handle_external_query(ctx: Context, sender: str, msg: QuerySystemStatus):
    """Handle queries from ASI-1 or other external agents"""
    
    ctx.logger.info(f"External query from: {sender}")
    
    # Prepare response
    response = SystemStatusResponse(
        query_id=msg.query_id,
        active_cases=len(ctx.storage.get("active_cases", [])),
        available_beds=ctx.storage.get("available_beds", 10),
        staff_on_duty=25,
        system_load="medium",
        timestamp=datetime.utcnow().isoformat()
    )
    
    # Send back to requester
    await ctx.send(sender, response)
    ctx.logger.info(f"Response sent to: {sender}")
```

### Step 6.2: Share Agent Address with Mentor

Create integration document:

```markdown
# EDFlow AI - ASI-1 Integration

## ED Coordinator Agent

**Address:** `agent1q...`
**Network:** Fetch.ai Mainnet
**Mailbox:** Enabled (hosted on Agentverse)

## How to Query

```python
from uagents import Agent, Context, Model

class QuerySystemStatus(Model):
    query_id: str
    requested_by: str

# Your ASI-1 agent
asi1_agent = Agent(...)

ED_COORDINATOR = "agent1q..."  # Our ED Coordinator address

@asi1_agent.on_interval(period=60.0)
async def query_edflow(ctx: Context):
    query = QuerySystemStatus(
        query_id="unique-id",
        requested_by=ctx.agent.address
    )
    await ctx.send(ED_COORDINATOR, query)

@asi1_agent.on_message(model=SystemStatusResponse)
async def handle_response(ctx: Context, sender: str, msg: SystemStatusResponse):
    ctx.logger.info(f"EDFlow Status: {msg.active_cases} cases")
```

## Response Format

```json
{
  "query_id": "unique-id",
  "active_cases": 5,
  "available_beds": 8,
  "staff_on_duty": 25,
  "system_load": "medium",
  "timestamp": "2024-10-25T19:00:00Z"
}
```

## Rate Limits
- 100 queries per hour per agent
- Response time: < 2 seconds

## Support
Contact: [your email]
```

**Deliverable:** ✅ Integration ready for ASI-1

---

## PHASE 7: Monitoring & Debugging (Ongoing)

### Step 7.1: Use Agentverse Dashboard

**View Logs:**
1. Go to "My Agents"
2. Click on agent name
3. View "Logs" tab
4. Filter by timestamp, level

**Monitor Activity:**
- Message count
- CPU/Memory usage
- Uptime
- Error rate

### Step 7.2: Add Logging to Agents

```python
@agent.on_message(model=QuerySystemStatus)
async def handle_query(ctx: Context, sender: str, msg: QuerySystemStatus):
    # Log all queries
    ctx.logger.info(f"📨 Query from: {sender[:8]}...")
    ctx.logger.info(f"   Query ID: {msg.query_id}")
    
    # Process...
    
    ctx.logger.info(f"✅ Response sent")
```

### Step 7.3: Handle Errors Gracefully

```python
@agent.on_message(model=QuerySystemStatus)
async def handle_query(ctx: Context, sender: str, msg: QuerySystemStatus):
    try:
        # Process query
        response = create_response(ctx, msg)
        await ctx.send(sender, response)
    except Exception as e:
        ctx.logger.error(f"Error handling query: {e}")
        # Send error response
        error_response = ErrorResponse(
            query_id=msg.query_id,
            error=str(e)
        )
        await ctx.send(sender, error_response)
```

**Deliverable:** ✅ Robust monitoring in place

---

## 📊 Success Checklist

- [ ] Agentverse account created
- [ ] All 6 agents deployed to Agentverse
- [ ] Agent addresses documented
- [ ] Inter-agent communication working
- [ ] Query protocol implemented
- [ ] ASI-1 can send queries
- [ ] Responses received successfully
- [ ] Logs visible on dashboard
- [ ] Error handling implemented
- [ ] Integration documentation shared

---

## 🔧 Troubleshooting Guide

### Issue: Agent won't deploy

**Solution:**
- Check syntax errors in code
- Verify all imports are available
- Ensure `agent.run()` is at the end
- Check requirements.txt is valid

### Issue: Messages not received

**Solution:**
- Verify recipient address is correct
- Check both agents are running
- Ensure message model matches on both sides
- Check Agentverse mailbox status

### Issue: Slow response times

**Solution:**
- Reduce computation in message handlers
- Use async operations
- Check Agentverse platform status
- Optimize data storage

### Issue: Agent keeps restarting

**Solution:**
- Check for infinite loops
- Reduce interval periods
- Fix any exceptions in startup
- Review logs for error messages

---

## 📚 Additional Resources

- uAgents GitHub: https://github.com/fetchai/uAgents
- Fetch.ai Discord: https://discord.gg/fetchai
- Documentation: https://docs.fetch.ai
- Examples: https://github.com/fetchai/uAgents-examples

---

## 🎯 Timeline Estimate

| Phase | Time | Cumulative |
|-------|------|------------|
| 1. Account Setup | 30 min | 0.5h |
| 2. Prepare Code | 3h | 3.5h |
| 3. Deploy First Agent | 1h | 4.5h |
| 4. Deploy Remaining | 2h | 6.5h |
| 5. Enable Communication | 2h | 8.5h |
| 6. ASI-1 Integration | 1h | 9.5h |
| 7. Testing & Refinement | 2h | 11.5h |

**Total: ~12 hours (1.5 days)**

---

## 🚀 Quick Start (Next Steps)

1. **Today**: Create Agentverse account
2. **Today**: Prepare ed_coordinator.py standalone file
3. **Tomorrow**: Deploy first agent
4. **Tomorrow**: Test agent communication
5. **Day 3**: Deploy all agents and enable ASI-1 integration

---

**Ready to start? Begin with Phase 1!**