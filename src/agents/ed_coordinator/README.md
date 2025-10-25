# ED Coordinator Agent

## Overview

The ED Coordinator Agent serves as the central orchestrator for all Emergency Department operations in the EDFlow AI system.

## Responsibilities

- **Patient Arrival Processing**: Receives and processes patient arrival notifications from ambulances/EMS
- **AI-Powered Triage**: Uses Claude AI engine to analyze patient acuity and recommend appropriate protocols
- **Protocol Activation**: Activates emergency protocols (STEMI, Stroke, Trauma, Pediatric) when needed
- **Agent Coordination**: Coordinates with all other agents in the system
- **Status Monitoring**: Tracks status of all active patients
- **Metrics Tracking**: Monitors ED performance metrics and KPIs

## Key Features

### Protocol Activation Targets
- **STEMI Protocol**: < 5 minutes
- **Stroke Protocol**: < 7 minutes
- **Trauma Protocol**: < 3 minutes
- **Pediatric Protocol**: < 4 minutes

### AI Integration
- Patient acuity analysis using Claude AI
- Real-time decision making with < 2 second response time
- Fallback to rule-based logic if AI unavailable

### Communication
- Chat protocol enabled for all agent communication
- Broadcasts protocol activations to all agents
- Receives status updates from other agents
- Sends alerts for critical situations

## Message Types Handled

### Incoming
- [`PatientArrivalNotification`](../../models/patient.py:39) - New patient arrivals
- [`StatusUpdate`](../../models/messages.py:125) - Status updates from other agents
- Chat messages from all agents

### Outgoing
- [`ProtocolActivation`](../../models/messages.py:26) - Emergency protocol triggers
- [`Alert`](../../models/messages.py:136) - System alerts
- Chat messages to coordinate agents

## Usage

### Running Locally
```python
from src.agents.ed_coordinator import EDCoordinatorAgent

agent = EDCoordinatorAgent()
agent.run()
```

### Configuration
Set in `.env`:
```
ED_COORDINATOR_SEED=your_seed_here
ED_COORDINATOR_PORT=8000
```

### Agentverse Deployment
Agent automatically uses mailbox when `DEPLOYMENT_MODE=agentverse`

## API

### Public Methods

#### `register_agent_address(agent_name: str, address: str)`
Register another agent's address for communication.

#### `get_patient_count() -> int`
Get current number of active patients.

#### `get_patient_status(patient_id: str) -> Dict`
Get status of a specific patient.

## Agent Address

After startup, check logs for agent address:
```
Agent address: agent1q...
```

Use this address for other agents to communicate with ED Coordinator.

## Monitoring

The agent logs:
- Patient arrivals and processing
- Protocol activations
- AI analysis results
- Status updates
- Errors and alerts

Log level configured via `LOG_LEVEL` in `.env`