"""
EDFlow AI - Web Dashboard Server
Real-time chat interface with agents and metrics monitoring
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, List, Any
import asyncio
import json
from pydantic import BaseModel

from src.agents import EDCoordinatorAgent, create_agent
from src.models import PatientArrivalNotification
from src.ai import ClaudeEngine


# Initialize FastAPI app
app = FastAPI(title="EDFlow AI Dashboard")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
active_connections: List[WebSocket] = []
system_metrics = {
    "total_patients": 0,
    "active_patients": 0,
    "protocols_activated": 0,
    "avg_response_time": 0.0,
    "agent_messages": 0,
}
message_history: List[Dict[str, Any]] = []
agent_status = {
    "ed_coordinator": {"status": "initializing", "address": None},
    "resource_manager": {"status": "initializing", "address": None},
    "specialist_coordinator": {"status": "initializing", "address": None},
    "lab_service": {"status": "initializing", "address": None},
    "pharmacy": {"status": "initializing", "address": None},
    "bed_management": {"status": "initializing", "address": None},
}


class ChatMessage(BaseModel):
    """Chat message model"""
    user: str
    message: str
    timestamp: str


class PatientData(BaseModel):
    """Patient data for processing"""
    patient_id: str
    complaint: str
    vitals: Dict[str, Any]


# Initialize AI engine
ai_engine = ClaudeEngine()


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


# API Endpoints

@app.get("/")
async def get_dashboard():
    """Serve the main dashboard"""
    return HTMLResponse(content=open("web/dashboard.html").read())


@app.get("/api/metrics")
async def get_metrics():
    """Get current system metrics"""
    return {
        "metrics": system_metrics,
        "agent_status": agent_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/agents")
async def get_agents():
    """Get all agent statuses"""
    return {"agents": agent_status}


@app.get("/api/messages")
async def get_messages():
    """Get message history"""
    return {"messages": message_history[-50:]}  # Last 50 messages


@app.post("/api/patient")
async def process_patient(patient: PatientData):
    """Process a new patient arrival"""
    
    try:
        # Analyze with AI
        start_time = datetime.utcnow()
        analysis = await ai_engine.analyze_patient_acuity(
            vitals=patient.vitals,
            symptoms=patient.complaint
        )
        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds()
        
        # Update metrics
        system_metrics["total_patients"] += 1
        system_metrics["active_patients"] += 1
        
        # Update average response time
        old_avg = system_metrics["avg_response_time"]
        n = system_metrics["total_patients"]
        system_metrics["avg_response_time"] = (old_avg * (n-1) + response_time) / n
        
        if analysis.get("protocol") in ["stemi", "stroke", "trauma", "pediatric"]:
            system_metrics["protocols_activated"] += 1
        
        # Log message
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "patient_arrival",
            "patient_id": patient.patient_id,
            "complaint": patient.complaint,
            "analysis": analysis,
            "response_time": response_time
        }
        message_history.append(message)
        
        # Broadcast to connected clients
        await manager.broadcast({
            "type": "patient_processed",
            "data": message
        })
        
        return {
            "success": True,
            "patient_id": patient.patient_id,
            "analysis": analysis,
            "response_time": response_time
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    
    try:
        # Send initial status
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to EDFlow AI",
            "metrics": system_metrics,
            "agents": agent_status
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "chat":
                # Process chat message
                user_message = message_data.get("message", "")
                
                # Log chat
                chat_log = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "type": "chat",
                    "user": "operator",
                    "message": user_message
                }
                message_history.append(chat_log)
                
                # Broadcast to all clients
                await manager.broadcast({
                    "type": "chat_message",
                    "data": chat_log
                })
                
                # Simple AI response
                if "patient" in user_message.lower():
                    response = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "type": "system_response",
                        "message": f"Received: {user_message}. System ready to process patients."
                    }
                    await manager.broadcast({
                        "type": "system_message",
                        "data": response
                    })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Background task to update metrics
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    print("=" * 60)
    print("EDFlow AI Web Dashboard Starting...")
    print("=" * 60)
    print("\n✅ FastAPI server initialized")
    print("✅ WebSocket endpoint ready")
    print("✅ Claude AI engine loaded")
    print("\n🌐 Dashboard URL: http://localhost:8080")
    print("📊 API Docs: http://localhost:8080/docs")
    print("\nPress Ctrl+C to stop")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)