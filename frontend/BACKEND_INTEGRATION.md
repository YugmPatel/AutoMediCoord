# Backend Integration Plan

## Overview

This document outlines how to integrate the React frontend with the existing AutoMediCoord uAgents backend system.

## Integration Architecture

### Current Backend Structure

```
AutoMediCoord/
├── app.py                 # Main uAgents application
├── src/
│   ├── agents.py         # 6 specialized agents
│   ├── models.py         # Data models
│   ├── ai.py            # Claude AI engine
│   └── utils.py         # Configuration and utilities
```

### New Integration Layer

```
AutoMediCoord/
├── api/                  # New FastAPI wrapper
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── dashboard.py  # Dashboard endpoints
│   │   ├── cases.py     # Patient case endpoints
│   │   ├── agents.py    # Agent status endpoints
│   │   └── simulation.py # Simulation triggers
│   ├── websocket/
│   │   ├── __init__.py
│   │   ├── manager.py   # WebSocket connection manager
│   │   └── events.py    # Event handlers
│   └── models/
│       ├── __init__.py
│       ├── api_models.py # API response models
│       └── websocket_models.py # WebSocket event models
```

## FastAPI Wrapper Implementation

### main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from api.routes import dashboard, cases, agents, simulation
from api.websocket.manager import WebSocketManager
from src.agents import create_agent
from src.utils import get_config

# Create FastAPI app
app = FastAPI(title="EDFlow AI API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://localhost:3000"]
)

# Combine FastAPI and Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# WebSocket manager
ws_manager = WebSocketManager(sio)

# Include routers
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(cases.router, prefix="/api/cases", tags=["cases"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])

# Global variables for agents
ed_coordinator = None
all_agents = {}

@app.on_event("startup")
async def startup_event():
    global ed_coordinator, all_agents

    # Create all agents
    ed_coordinator = create_agent("ed_coordinator")
    all_agents = {
        "ed_coordinator": ed_coordinator,
        "resource_manager": create_agent("resource_manager"),
        "specialist_coordinator": create_agent("specialist_coordinator"),
        "lab_service": create_agent("lab_service"),
        "pharmacy": create_agent("pharmacy"),
        "bed_management": create_agent("bed_management"),
    }

    # Setup agent communication with WebSocket
    await ws_manager.setup_agent_listeners(all_agents)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8080)
```

### Dashboard Routes (api/routes/dashboard.py)

```python
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from api.models.api_models import DashboardMetrics, PatientCase, ActivityEntry

router = APIRouter()

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics():
    """Get current ED dashboard metrics"""
    # Get data from agents
    active_cases = len(ed_coordinator.active_patients) if ed_coordinator else 0

    return DashboardMetrics(
        active_cases=active_cases,
        avg_lab_eta=9,  # Calculate from lab agent
        icu_beds_held=2,  # Get from bed management agent
        doctors_paged=2,  # Get from specialist coordinator
        last_updated=datetime.utcnow()
    )

@router.get("/cases", response_model=List[PatientCase])
async def get_active_cases():
    """Get all active patient cases"""
    if not ed_coordinator:
        return []

    cases = []
    for patient_id, patient_data in ed_coordinator.active_patients.items():
        case = PatientCase(
            id=patient_id,
            type=patient_data.get("protocol", "General").upper(),
            duration=5,  # Calculate actual duration
            vitals={
                "hr": 110,
                "bp_sys": 160,
                "bp_dia": 95,
                "spo2": 94
            },
            status=patient_data.get("status", "Pending"),
            location="ED-1",
            priority=1 if patient_data.get("acuity") == "1" else 3
        )
        cases.append(case)

    return cases

@router.get("/activity", response_model=List[ActivityEntry])
async def get_recent_activity():
    """Get recent activity log entries"""
    # This would be populated by agent activities
    return [
        ActivityEntry(
            id="1",
            timestamp=datetime.utcnow(),
            type="Lab",
            message="Lab ETA 12m",
            status="Pending"
        ),
        ActivityEntry(
            id="2",
            timestamp=datetime.utcnow(),
            type="Pharm",
            message="STEMI kit ready",
            status="Ready"
        )
    ]
```

### Simulation Routes (api/routes/simulation.py)

```python
from fastapi import APIRouter
from datetime import datetime
from src.models import PatientArrivalNotification

router = APIRouter()

@router.post("/stemi")
async def simulate_stemi():
    """Trigger STEMI patient simulation"""
    if not ed_coordinator:
        raise HTTPException(status_code=503, detail="ED Coordinator not available")

    # Create STEMI patient
    patient = PatientArrivalNotification(
        patient_id=f"STEMI_{datetime.utcnow().strftime('%H%M%S')}",
        arrival_time=datetime.utcnow(),
        vitals={
            "hr": 110,
            "bp_sys": 160,
            "bp_dia": 95,
            "spo2": 94,
            "temp": 37.2
        },
        chief_complaint="Severe chest pain radiating to left arm",
        ems_report="ST elevation on ECG, suspected STEMI",
        priority=1
    )

    # Process through ED Coordinator
    await ed_coordinator._process_arrival(None, patient)

    return {"message": "STEMI simulation triggered", "patient_id": patient.patient_id}

@router.post("/stroke")
async def simulate_stroke():
    """Trigger stroke patient simulation"""
    if not ed_coordinator:
        raise HTTPException(status_code=503, detail="ED Coordinator not available")

    # Create stroke patient
    patient = PatientArrivalNotification(
        patient_id=f"STROKE_{datetime.utcnow().strftime('%H%M%S')}",
        arrival_time=datetime.utcnow(),
        vitals={
            "hr": 80,
            "bp_sys": 195,
            "bp_dia": 118,
            "spo2": 96,
            "temp": 36.8
        },
        chief_complaint="Sudden onset weakness and speech difficulty",
        ems_report="Left-sided weakness, NIHSS 8, suspected stroke",
        priority=1
    )

    # Process through ED Coordinator
    await ed_coordinator._process_arrival(None, patient)

    return {"message": "Stroke simulation triggered", "patient_id": patient.patient_id}
```

### WebSocket Manager (api/websocket/manager.py)

```python
import socketio
from typing import Dict, Any
from datetime import datetime

class WebSocketManager:
    def __init__(self, sio: socketio.AsyncServer):
        self.sio = sio
        self.connected_clients = set()

        # Setup Socket.IO event handlers
        @sio.event
        async def connect(sid, environ):
            self.connected_clients.add(sid)
            await sio.emit('connection_status', {'connected': True}, room=sid)
            print(f"Client {sid} connected")

        @sio.event
        async def disconnect(sid):
            self.connected_clients.discard(sid)
            print(f"Client {sid} disconnected")

        @sio.event
        async def send_message(sid, data):
            # Handle chat messages from frontend
            message = {
                'id': f"msg_{datetime.utcnow().timestamp()}",
                'content': data.get('message', ''),
                'timestamp': datetime.utcnow().isoformat(),
                'sender': 'User',
                'type': 'user'
            }
            await sio.emit('chat_message', message)

    async def broadcast_patient_arrival(self, patient_data: Dict[str, Any]):
        """Broadcast new patient arrival to all connected clients"""
        await self.sio.emit('patient_arrival', {
            'type': 'patient_arrival',
            'data': patient_data,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def broadcast_protocol_activation(self, protocol_data: Dict[str, Any]):
        """Broadcast protocol activation to all connected clients"""
        await self.sio.emit('protocol_activation', {
            'type': 'protocol_activation',
            'data': protocol_data,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def broadcast_case_update(self, case_data: Dict[str, Any]):
        """Broadcast case status update to all connected clients"""
        await self.sio.emit('case_update', {
            'type': 'case_update',
            'data': case_data,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def broadcast_agent_message(self, message_data: Dict[str, Any]):
        """Broadcast agent communication to all connected clients"""
        await self.sio.emit('agent_message', {
            'type': 'agent_message',
            'data': message_data,
            'timestamp': datetime.utcnow().isoformat()
        })

    async def setup_agent_listeners(self, agents: Dict[str, Any]):
        """Setup listeners for agent events"""
        # This would integrate with the existing agent message handlers
        # to forward events to WebSocket clients
        pass
```

### API Models (api/models/api_models.py)

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class DashboardMetrics(BaseModel):
    active_cases: int
    avg_lab_eta: int  # minutes
    icu_beds_held: int
    doctors_paged: int
    last_updated: datetime

class PatientVitals(BaseModel):
    hr: int  # heart rate
    bp_sys: int  # systolic BP
    bp_dia: int  # diastolic BP
    spo2: int  # oxygen saturation

class PatientCase(BaseModel):
    id: str
    type: str  # STEMI, Stroke, Trauma, etc.
    duration: int  # minutes since arrival
    vitals: PatientVitals
    status: str
    location: str
    lab_eta: Optional[int] = None
    assigned_bed: Optional[str] = None
    priority: int

class ActivityEntry(BaseModel):
    id: str
    timestamp: datetime
    type: str  # Lab, Pharm, Bed, Doctor, System
    message: str
    status: str  # Ready, Pending, Complete, Failed
    case_id: Optional[str] = None

class ChatMessage(BaseModel):
    id: str
    content: str
    timestamp: datetime
    sender: str
    type: str  # user, agent, system

class SimulationResponse(BaseModel):
    message: str
    patient_id: str
    timestamp: datetime
```

## Frontend Integration Points

### API Service (frontend/src/services/api.ts)

```typescript
const API_BASE_URL = "http://localhost:8080/api";

export const api = {
  // Dashboard endpoints
  getDashboardMetrics: () =>
    fetch(`${API_BASE_URL}/dashboard/metrics`).then((res) => res.json()),

  getActiveCases: () =>
    fetch(`${API_BASE_URL}/dashboard/cases`).then((res) => res.json()),

  getRecentActivity: () =>
    fetch(`${API_BASE_URL}/dashboard/activity`).then((res) => res.json()),

  // Simulation endpoints
  simulateSTEMI: () =>
    fetch(`${API_BASE_URL}/simulation/stemi`, { method: "POST" }).then((res) =>
      res.json()
    ),

  simulateStroke: () =>
    fetch(`${API_BASE_URL}/simulation/stroke`, { method: "POST" }).then((res) =>
      res.json()
    ),
};
```

### Socket Service (frontend/src/services/socket.ts)

```typescript
import { io, Socket } from "socket.io-client";

class SocketService {
  private socket: Socket | null = null;

  connect() {
    this.socket = io("http://localhost:8080", {
      transports: ["websocket"],
    });

    this.socket.on("connect", () => {
      console.log("Connected to WebSocket server");
    });

    this.socket.on("disconnect", () => {
      console.log("Disconnected from WebSocket server");
    });

    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  on(event: string, callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  emit(event: string, data: any) {
    if (this.socket) {
      this.socket.emit(event, data);
    }
  }
}

export const socketService = new SocketService();
```

## Deployment Configuration

### Docker Compose (docker-compose.yml)

```yaml
version: "3.8"

services:
  backend:
    build: ./AutoMediCoord
    ports:
      - "8080:8080"
    environment:
      - DEPLOYMENT_MODE=local
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./AutoMediCoord:/app
    command: python api/main.py

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://localhost:8080
    volumes:
      - ./frontend:/app
      - /app/node_modules
```

## Integration Steps

1. **Create API Layer**: Add FastAPI wrapper to AutoMediCoord
2. **Setup WebSocket**: Implement Socket.IO server for real-time events
3. **Agent Integration**: Connect existing agents to WebSocket events
4. **Frontend Services**: Implement API and Socket services in React
5. **Real-time Updates**: Connect frontend components to WebSocket events
6. **Testing**: Test end-to-end communication
7. **Deployment**: Configure production deployment

This integration plan provides a complete bridge between the existing uAgents backend and the new React frontend, enabling real-time communication and seamless user experience.
