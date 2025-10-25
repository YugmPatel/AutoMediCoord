"""
EDFlow AI - FastAPI Backend
Main application that bridges uAgents with React frontend
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socketio
import uvicorn

from .routes import dashboard, cases, agents, simulation
from .websocket.manager import WebSocketManager
from .models.api_models import *
from src.agents import create_agent
from src.utils import get_config, get_logger

# Setup logging
logger = get_logger(__name__)
config = get_config()

# Global variables for agents
ed_coordinator = None
all_agents = {}
ws_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global ed_coordinator, all_agents, ws_manager
    
    logger.info("🚀 Starting EDFlow AI API Server...")
    
    try:
        # Create all 6 uAgents
        logger.info("Creating uAgents...")
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
        if ws_manager:
            await ws_manager.setup_agent_listeners(all_agents)
        
        logger.info("✅ All agents created and configured")
        api_port = getattr(config, 'API_PORT', 8080)
        logger.info(f"🏥 EDFlow AI API Server ready on port {api_port}")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize agents: {str(e)}")
        raise
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down EDFlow AI API Server...")

# Create FastAPI app
app = FastAPI(
    title="EDFlow AI API",
    description="Emergency Department Flow Optimization API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    logger=True,
    engineio_logger=True
)

# Combine FastAPI and Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# Initialize WebSocket manager
ws_manager = WebSocketManager(sio)

# Include API routes
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(cases.router, prefix="/api/cases", tags=["cases"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_active": len(all_agents),
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "EDFlow AI - Emergency Department Flow Optimization API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "agents": len(all_agents) if all_agents else 0
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Utility functions to access agents from routes
def get_ed_coordinator():
    """Get ED Coordinator agent"""
    if not ed_coordinator:
        raise HTTPException(status_code=503, detail="ED Coordinator not available")
    return ed_coordinator

def get_all_agents():
    """Get all agents"""
    if not all_agents:
        raise HTTPException(status_code=503, detail="Agents not available")
    return all_agents

def get_websocket_manager():
    """Get WebSocket manager"""
    if not ws_manager:
        raise HTTPException(status_code=503, detail="WebSocket manager not available")
    return ws_manager

if __name__ == "__main__":
    # Run the server
    port = getattr(config, 'API_PORT', 8080)
    uvicorn.run(
        "api.main:socket_app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )