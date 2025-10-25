# Agent Communication Flows - EDFlow AI

## 🔄 Communication Architecture

### Communication Protocols

EDFlow AI uses Fetch.ai's uAgents framework with the following communication patterns:

1. **Chat Protocol** - All agents use standardized chat protocol for structured communication
2. **Request-Response** - Synchronous communication for critical operations
3. **Event Broadcasting** - One-to-many notifications for state changes
4. **State Synchronization** - Shared state management through LangGraph

---

## 📨 Message Types

### Core Message Models

```python
# Patient-related messages
class PatientArrivalNotification(Model):
    patient_id: str
    timestamp: datetime
    vitals: Dict[str, Any]
    chief_complaint: str
    ems_report: str
    priority: int  # 1-5 (ESI scale)

class PatientUpdate(Model):
    patient_id: str
    status: str  # "triaged", "in_treatment", "admitted", "discharged"
    location: str
    timestamp: datetime

# Resource-related messages
class ResourceRequest(Model):
    request_id: str
    resource_type: str  # "bed", "equipment", "room"
    requirements: Dict[str, Any]
    priority: int
    patient_id: str

class ResourceAllocation(Model):
    request_id: str
    resource_id: str
    resource_type: str
    allocated: bool
    location: str
    expires_at: datetime

class ResourceConflict(Model):
    conflict_id: str
    competing_requests: List[str]
    resource_type: str
    resolution_required: bool

# Team activation messages
class TeamActivationRequest(Model):
    activation_id: str
    protocol: str  # "STEMI", "Stroke", "Trauma", "Pediatric"
    patient_id: str
    urgency: str  # "immediate", "urgent", "routine"
    required_specialists: List[str]

class TeamStatus(Model):
    activation_id: str
    team_members: List[Dict[str, str]]
    assembly_time: float  # seconds
    ready: bool
    location: str

# Lab and Pharmacy messages
class LabOrder(Model):
    order_id: str
    patient_id: str
    tests: List[str]
    priority: str  # "stat", "asap", "routine"
    ordered_by: str

class LabResult(Model):
    order_id: str
    patient_id: str
    test: str
    result: Dict[str, Any]
    critical: bool
    timestamp: datetime

class MedicationOrder(Model):
    order_id: str
    patient_id: str
    medication: str
    dose: str
    route: str
    frequency: str
    priority: str  # "stat", "urgent", "routine"

# Protocol activation messages
class ProtocolActivation(Model):
    activation_id: str
    protocol_type: str
    patient_id: str
    activation_time: datetime
    target_completion: datetime
    checklist: List[Dict[str, Any]]
```

---

## 🎬 Scenario 1: STEMI Patient Workflow

### Timeline: 0-5 Minutes (Target: <5 min)

```
Time    Agent               Message                      Action
────────────────────────────────────────────────────────────────────
00:00   Ambulance          → ED Coordinator             Pre-arrival alert
        (External)           PatientArrivalNotification  "76yo M, Chest pain,
                                                         ECG shows STEMI"

00:15   ED Coordinator     → LangGraph Engine           Process patient data
                            ChatMessage                  Initiate STEMI protocol

00:30   LangGraph Engine   → Claude AI                  Analyze patient acuity
                            AnalysisRequest              Confirm STEMI, Priority 1

00:45   Claude AI          → LangGraph Engine           STEMI confirmed
                            AnalysisResponse             Recommend immediate
                                                         cath lab activation

01:00   LangGraph Engine   → ED Coordinator             Protocol decision
                            ProtocolActivation           "Activate STEMI protocol"

01:05   ED Coordinator     ⟿ Parallel Broadcasts ⟿
        ├─→ Specialist Coordinator   TeamActivationRequest    "Activate cath lab team"
        ├─→ Resource Manager         ResourceRequest          "Reserve cath lab"
        ├─→ Lab Service             LabOrder                  "Stat: Troponin, CBC"
        └─→ Bed Management          BedRequest                "Prep cath lab bed"

01:30   Specialist Coord   → ED Coordinator             Team status update
                            TeamStatus                   "Interventional card
                                                         team activated"

02:00   Resource Manager   → ED Coordinator             Resource confirmed
                            ResourceAllocation           "Cath lab 2 reserved"

02:15   Lab Service        → ED Coordinator             Labs ordered
                            ChatAcknowledgement         "Stat labs processing"

02:30   Bed Management     → ED Coordinator             Bed ready
                            BedAssignment               "Cath lab 2 bed ready"

03:00   ED Coordinator     → All Agents                 Status broadcast
                            ChatMessage                  "All resources ready"

03:30   Specialist Coord   → ED Coordinator             Team assembled
                            TeamStatus                   "Cath team in position
                                                         ETA: 1 min"

04:00   Lab Service        → ED Coordinator             Critical result
                            LabResult                    "Troponin: elevated"

04:30   ED Coordinator     → Ambulance                  Ready confirmation
                            ChatMessage                  "Hospital ready,
                                                         direct to cath lab"

05:00   ✅ PROTOCOL COMPLETE - All agents coordinated
        Total activation time: 4 min 30 sec
        Target: <5 min ✅
```

### Message Flow Diagram

```
Ambulance                ED Coordinator         LangGraph              Claude AI
    │                           │                    │                     │
    ├─ PatientArrival ─────────>│                    │                     │
    │                           ├─ ProcessData ─────>│                     │
    │                           │                    ├─ AnalyzeAcuity ────>│
    │                           │                    │<─ STEMIConfirmed ───┤
    │                           │<─ ProtocolStart ───┤                     │
    │                           │                    │                     │
    │                           ├──────────┬─────────┴─────────┬──────────┤
    │                           │          ▼                   ▼          ▼
    │                    Specialist    Resource           Lab         Bed Mgmt
    │                       Coord        Manager         Service
    │                           │          │               │              │
    │                           ├─ Activate Team          │              │
    │                           ├──────────> Reserve Resources            │
    │                           ├─────────────────────> Order Labs        │
    │                           ├────────────────────────────────> Prep Bed
    │                           │          │               │              │
    │                           │<─ Team Ready             │              │
    │                           │<─────────┼ Allocated     │              │
    │                           │<────────────────────── Labs OK           │
    │                           │<──────────────────────────────── Bed Ready
    │                           │          │               │              │
    │<─ Ready for Patient ──────┤          │               │              │
    │                           │          │               │              │
```

---

## 🎬 Scenario 2: Multi-Patient Coordination

### Concurrent Patients: STEMI + Stroke + Trauma

```
Time    Event                                    Agent Actions
─────────────────────────────────────────────────────────────────────
00:00   3 Patients Arrive Simultaneously
        ├─ Patient A: STEMI (Chest pain)
        ├─ Patient B: Stroke (Facial droop)
        └─ Patient C: Trauma (MVA, GCS 8)

00:15   ED Coordinator receives all alerts      → Send to Claude AI
                                                 for prioritization

00:30   Claude AI analyzes and sequences:
        Priority 1: Trauma (immediate threat)
        Priority 2: STEMI (time-sensitive)
        Priority 3: Stroke (time-sensitive)

00:45   LangGraph activates 3 parallel workflows
        ├─ Trauma Protocol    (Target: <3 min)
        ├─ STEMI Protocol     (Target: <5 min)
        └─ Stroke Protocol    (Target: <7 min)

01:00   Resource Manager orchestrates allocation
        ├─ Trauma Bay 1  → Patient C
        ├─ Cath Lab 2    → Patient A
        └─ CT Scanner 1  → Patient B

01:30   All teams activated in parallel
        ├─ Trauma Team    → Bay 1 (ETA: 2 min)
        ├─ Cath Lab Team  → Lab 2 (ETA: 3 min)
        └─ Stroke Team    → CT area (ETA: 4 min)

03:00   Trauma Bay Ready    ✅ (2:45 - Target: <3 min)
04:30   Cath Lab Ready      ✅ (4:15 - Target: <5 min)
06:00   Stroke Team Ready   ✅ (5:45 - Target: <7 min)

Result: All 3 critical patients handled concurrently
        No resource conflicts
        All protocols met time targets
```

### Parallel Communication Pattern

```
                    ED Coordinator
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    Patient A         Patient B         Patient C
    (STEMI)          (Stroke)          (Trauma)
        │                 │                 │
        ├─ Workflow A     ├─ Workflow B     ├─ Workflow C
        │                 │                 │
    ┌───┴───┐         ┌───┴───┐         ┌───┴───┐
    │       │         │       │         │       │
  Cath    Labs       CT    Neuro      Trauma  Surgery
  Lab              Scanner  Team        Team    Team
```

---

## 🎬 Scenario 3: Resource Conflict Resolution

### ED at Capacity - Intelligent Resolution

```
Time    Event                               Agent Communication
─────────────────────────────────────────────────────────────────────
00:00   ED Status: All beds occupied
        ├─ Trauma Bay 1: Stable patient
        ├─ Trauma Bay 2: Moderate trauma
        └─ No available critical beds

00:30   New STEMI Patient Alert            Ambulance → ED Coordinator
                                           "Critical patient incoming"

01:00   Resource Request                   ED Coordinator → Resource Mgr
                                          "Need critical bed IMMEDIATELY"

01:15   Resource Check                     Resource Mgr → Bed Management
                                          "Query all bed status"

01:30   Conflict Detected                  Bed Management → Resource Mgr
                                          ResourceConflict:
                                          - No critical beds available
                                          - STEMI requires immediate bed
                                          - 2 stable patients in trauma

02:00   AI Conflict Resolution             Resource Mgr → Claude AI
                                          "Resolve: Need critical bed,
                                          all occupied, stable patients
                                          in trauma bays"

02:30   Resolution Strategy                Claude AI → Resource Mgr
                                          AnalysisResponse:
                                          Option 1: Transfer stable
                                                    patient to floor
                                          Option 2: Use alternative space
                                          Option 3: Expedite DC planning
                                          Recommendation: Option 1
                                          Confidence: 0.95

03:00   Execute Resolution                 Resource Mgr → Bed Management
                                          "Transfer Patient in Bay 1 to
                                          floor, prep Bay 1 for STEMI"

03:30   Coordination                       Bed Management → Floor Units
                                          "Accept stable trauma patient"

04:00   Confirmation                       Floor Units → Bed Management
                                          "Ready to accept"

04:30   Transfer Initiated                 Bed Management → Resource Mgr
                                          "Bay 1 will be available in
                                          10 minutes"

05:00   Resource Allocated                 Resource Mgr → ED Coordinator
                                          ResourceAllocation:
                                          - Trauma Bay 1 allocated
                                          - Available: 10 minutes
                                          - Patient transfer in progress

05:30   Ready Status                       ED Coordinator → Ambulance
                                          "Hospital ready, trauma bay
                                          available on arrival"

10:00   ✅ CONFLICT RESOLVED
        Stable patient safely transferred
        Critical bed available for STEMI
        Total resolution time: 10 minutes
```

### Conflict Resolution Flow

```
    Resource Request
          │
          ▼
    [Check Availability]
          │
          ├─ Available? ──> Allocate
          │
          ▼
    [Conflict Detected]
          │
          ▼
    [Claude AI Analysis]
          │
          ├─ Option 1: Transfer patient
          ├─ Option 2: Alternative space
          └─ Option 3: Expedite discharge
          │
          ▼
    [Select Best Option]
          │
          ▼
    [Execute Resolution]
          │
          ▼
    [Verify Success]
          │
          ▼
    [Allocate Resource]
```

---

## 🔧 Agent Interaction Patterns

### Pattern 1: Request-Response

Used for: Resource allocation, lab orders, bed requests

```python
# Sender (ED Coordinator)
@agent.on_interval(period=10.0)
async def check_patient_status(ctx: Context):
    response, status = await ctx.send_and_receive(
        resource_manager_address,
        ResourceRequest(
            request_id=str(uuid4()),
            resource_type="bed",
            requirements={"type": "critical", "isolation": False},
            priority=1,
            patient_id="P12345"
        ),
        response_type=ResourceAllocation
    )
    
    if isinstance(response, ResourceAllocation):
        if response.allocated:
            ctx.logger.info(f"Bed allocated: {response.resource_id}")
        else:
            ctx.logger.warning("No beds available - escalate")

# Receiver (Resource Manager)
@protocol.on_message(ResourceRequest)
async def handle_resource_request(ctx: Context, sender: str, msg: ResourceRequest):
    # Check availability
    available = check_resource_availability(msg.resource_type, msg.requirements)
    
    if available:
        allocation = allocate_resource(msg)
        await ctx.send(sender, ResourceAllocation(
            request_id=msg.request_id,
            resource_id=allocation.id,
            resource_type=msg.resource_type,
            allocated=True,
            location=allocation.location,
            expires_at=datetime.now() + timedelta(hours=1)
        ))
    else:
        # Trigger conflict resolution
        await handle_conflict(ctx, msg)
```

---

### Pattern 2: Broadcast Notification

Used for: Protocol activation, status updates, alerts

```python
# ED Coordinator broadcasts protocol activation
@agent.on_message(model=ProtocolActivation)
async def broadcast_activation(ctx: Context, sender: str, msg: ProtocolActivation):
    # Broadcast to all relevant agents
    agents = [
        specialist_coordinator_address,
        resource_manager_address,
        lab_service_address,
        pharmacy_address,
        bed_management_address
    ]
    
    activation_msg = ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[
            TextContent(
                type="text",
                text=f"ACTIVATE {msg.protocol_type} PROTOCOL - Patient {msg.patient_id}"
            )
        ]
    )
    
    for agent_addr in agents:
        await ctx.send(agent_addr, activation_msg)
        ctx.logger.info(f"Protocol activation sent to {agent_addr}")
```

---

### Pattern 3: Chat Protocol Communication

Used for: General communication, acknowledgments, session management

```python
# Agent 1: Initiator
@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    # Send acknowledgment
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )
    
    # Process message
    for item in msg.content:
        if isinstance(item, TextContent):
            ctx.logger.info(f"Received: {item.text}")
            
            # Process and respond
            response_text = process_message(item.text)
            
            # Send response
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

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Message {msg.acknowledged_msg_id} acknowledged by {sender}")
```

---

### Pattern 4: State Synchronization

Used for: LangGraph state updates, workflow coordination

```python
# LangGraph updates patient state
async def update_patient_state(state: PatientState, action: str):
    """Update patient state and notify all agents"""
    
    # Update state
    state.current_stage = action
    state.last_updated = datetime.utcnow()
    
    # Broadcast state change
    state_update = PatientUpdate(
        patient_id=state.patient_id,
        status=state.current_stage,
        location=state.location,
        timestamp=state.last_updated
    )
    
    # Notify all subscribed agents
    await broadcast_state_update(state_update)
    
    return state

# Agents receive state updates
@agent.on_message(model=PatientUpdate)
async def handle_state_update(ctx: Context, sender: str, msg: PatientUpdate):
    ctx.logger.info(f"Patient {msg.patient_id} status: {msg.status}")
    
    # Update local cache
    update_local_patient_state(msg)
    
    # React to state changes
    if msg.status == "ready_for_procedure":
        await prepare_for_procedure(ctx, msg.patient_id)
```

---

## 📊 Message Metrics

### Communication Performance

| Metric | Target | Typical |
|--------|--------|---------|
| Message Latency | <500ms | 200-300ms |
| Ack Response Time | <100ms | 50-80ms |
| Broadcast Fanout | <1s | 400-600ms |
| Request-Response | <2s | 1-1.5s |

### Message Volume (per patient workflow)

| Workflow | Messages Exchanged | Agents Involved |
|----------|-------------------|-----------------|
| STEMI Protocol | 25-30 | 6 |
| Stroke Protocol | 20-25 | 5 |
| Trauma Protocol | 30-35 | 6 |
| Routine Patient | 10-15 | 3-4 |

---

## 🔍 Debugging Communication

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# In agent code
@agent.on_message(model=Message)
async def debug_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.debug(f"Received from {sender}")
    ctx.logger.debug(f"Message: {msg.json()}")
```

### Monitor Message Flow

```bash
# View agent logs
tail -f logs/ed_coordinator.log
tail -f logs/resource_manager.log

# Check Agentverse dashboard
# https://agentverse.ai → My Agents → Logs
```

---

## ✅ Best Practices

1. **Always Acknowledge Messages**
   - Send `ChatAcknowledgement` for all chat messages
   - Confirms receipt and processing

2. **Use Appropriate Patterns**
   - Request-Response for critical operations
   - Broadcast for notifications
   - Chat protocol for general communication

3. **Handle Failures Gracefully**
   - Implement retry logic
   - Timeout mechanisms
   - Fallback strategies

4. **Log All Communications**
   - Debug message content
   - Track message flow
   - Audit trail for compliance

5. **Optimize Message Size**
   - Keep messages concise
   - Use references instead of full data
   - Batch when possible

---

**Communication flows designed for speed, reliability, and scalability! 🚀**