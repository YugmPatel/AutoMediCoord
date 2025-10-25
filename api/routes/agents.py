"""
Agents API Routes
Endpoints for agent status, communication, and management
"""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from ..models.api_models import (
    AgentStatus, ChatMessage, ApiResponse, AgentType
)
from src.utils import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Dependency to get agents
def get_all_agents():
    from api.main import get_all_agents
    return get_all_agents()

def get_websocket_manager():
    from api.main import get_websocket_manager
    return get_websocket_manager()

@router.get("/status", response_model=List[AgentStatus])
async def get_agents_status():
    """
    Get status of all agents
    
    Returns:
        List[AgentStatus]: Status of all 6 agents
    """
    try:
        all_agents = get_all_agents()
        
        agent_statuses = []
        
        # Define agent information
        agent_info = {
            "ed_coordinator": {
                "name": "ED Coordinator",
                "type": AgentType.ED_COORDINATOR,
                "description": "Central orchestrator for ED operations"
            },
            "resource_manager": {
                "name": "Resource Manager",
                "type": AgentType.RESOURCE_MANAGER,
                "description": "Manages beds, equipment, and resources"
            },
            "specialist_coordinator": {
                "name": "Specialist Coordinator",
                "type": AgentType.SPECIALIST_COORDINATOR,
                "description": "Coordinates specialist teams and doctors"
            },
            "lab_service": {
                "name": "Lab Service",
                "type": AgentType.LAB_SERVICE,
                "description": "Manages laboratory tests and results"
            },
            "pharmacy": {
                "name": "Pharmacy",
                "type": AgentType.PHARMACY,
                "description": "Handles medication orders and delivery"
            },
            "bed_management": {
                "name": "Bed Management",
                "type": AgentType.BED_MANAGEMENT,
                "description": "Manages bed assignments and turnover"
            }
        }
        
        # Create status for each agent
        for agent_key, agent in all_agents.items():
            if agent_key in agent_info:
                info = agent_info[agent_key]
                
                # Determine agent status
                status = "online" if agent is not None else "offline"
                
                # Get agent address
                address = getattr(agent.agent, 'address', f"agent_{agent_key}") if agent else f"agent_{agent_key}_offline"
                
                agent_status = AgentStatus(
                    name=info["name"],
                    type=info["type"],
                    status=status,
                    last_seen=datetime.utcnow() if status == "online" else datetime.utcnow() - timedelta(minutes=5),
                    address=str(address),
                    message_count=0  # Could be tracked in real implementation
                )
                
                agent_statuses.append(agent_status)
        
        logger.info(f"Retrieved status for {len(agent_statuses)} agents")
        return agent_statuses
        
    except Exception as e:
        logger.error(f"Error retrieving agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve agent status: {str(e)}")

@router.get("/messages", response_model=List[ChatMessage])
async def get_agent_messages(
    agent_type: Optional[AgentType] = Query(None, description="Filter by agent type"),
    limit: int = Query(50, description="Maximum number of messages", ge=1, le=100)
):
    """
    Get recent agent messages
    
    Args:
        agent_type: Optional filter by agent type
        limit: Maximum number of messages to return
        
    Returns:
        List[ChatMessage]: Recent agent messages
    """
    try:
        ws_manager = get_websocket_manager()
        
        # Get message history from WebSocket manager
        messages = ws_manager.get_message_history(limit)
        
        # Convert to ChatMessage objects
        chat_messages = []
        for msg_data in messages:
            try:
                chat_message = ChatMessage(
                    id=msg_data['id'],
                    content=msg_data['content'],
                    timestamp=datetime.fromisoformat(msg_data['timestamp'].replace('Z', '+00:00')),
                    sender=msg_data['sender'],
                    type=msg_data['type'],
                    agent_type=msg_data.get('agent_type')
                )
                chat_messages.append(chat_message)
            except Exception as e:
                logger.warning(f"Error parsing message: {str(e)}")
                continue
        
        # Filter by agent type if specified
        if agent_type:
            chat_messages = [msg for msg in chat_messages if msg.agent_type == agent_type]
        
        logger.info(f"Retrieved {len(chat_messages)} agent messages")
        return chat_messages
        
    except Exception as e:
        logger.error(f"Error retrieving agent messages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve messages: {str(e)}")

@router.get("/health", response_model=ApiResponse)
async def get_agents_health():
    """
    Get overall agent system health
    
    Returns:
        ApiResponse: Agent system health information
    """
    try:
        all_agents = get_all_agents()
        
        # Count online agents
        online_agents = len([agent for agent in all_agents.values() if agent is not None])
        total_agents = len(all_agents)
        
        # Calculate health percentage
        health_percentage = (online_agents / total_agents) * 100 if total_agents > 0 else 0
        
        # Determine overall status
        if health_percentage == 100:
            overall_status = "healthy"
        elif health_percentage >= 80:
            overall_status = "degraded"
        elif health_percentage >= 50:
            overall_status = "warning"
        else:
            overall_status = "critical"
        
        health_data = {
            "overall_status": overall_status,
            "health_percentage": health_percentage,
            "agents_online": online_agents,
            "agents_total": total_agents,
            "agents_offline": total_agents - online_agents,
            "last_check": datetime.utcnow().isoformat(),
            "system_uptime": "operational"
        }
        
        return ApiResponse(
            success=True,
            message=f"Agent system health: {overall_status}",
            data=health_data
        )
        
    except Exception as e:
        logger.error(f"Error checking agent health: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to check agent health: {str(e)}")

@router.get("/{agent_type}/status", response_model=AgentStatus)
async def get_specific_agent_status(agent_type: AgentType):
    """
    Get status of a specific agent
    
    Args:
        agent_type: The type of agent to get status for
        
    Returns:
        AgentStatus: Status of the specified agent
    """
    try:
        all_agents = get_all_agents()
        
        # Map agent types to keys
        agent_key_map = {
            AgentType.ED_COORDINATOR: "ed_coordinator",
            AgentType.RESOURCE_MANAGER: "resource_manager",
            AgentType.SPECIALIST_COORDINATOR: "specialist_coordinator",
            AgentType.LAB_SERVICE: "lab_service",
            AgentType.PHARMACY: "pharmacy",
            AgentType.BED_MANAGEMENT: "bed_management"
        }
        
        agent_key = agent_key_map.get(agent_type)
        if not agent_key:
            raise HTTPException(status_code=404, detail=f"Agent type {agent_type} not found")
        
        agent = all_agents.get(agent_key)
        
        # Agent names
        agent_names = {
            AgentType.ED_COORDINATOR: "ED Coordinator",
            AgentType.RESOURCE_MANAGER: "Resource Manager",
            AgentType.SPECIALIST_COORDINATOR: "Specialist Coordinator",
            AgentType.LAB_SERVICE: "Lab Service",
            AgentType.PHARMACY: "Pharmacy",
            AgentType.BED_MANAGEMENT: "Bed Management"
        }
        
        status = "online" if agent is not None else "offline"
        address = getattr(agent.agent, 'address', f"agent_{agent_key}") if agent else f"agent_{agent_key}_offline"
        
        agent_status = AgentStatus(
            name=agent_names[agent_type],
            type=agent_type,
            status=status,
            last_seen=datetime.utcnow() if status == "online" else datetime.utcnow() - timedelta(minutes=5),
            address=str(address),
            message_count=0
        )
        
        logger.info(f"Retrieved status for {agent_type} agent: {status}")
        return agent_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving {agent_type} agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve {agent_type} status: {str(e)}")

@router.post("/{agent_type}/restart", response_model=ApiResponse)
async def restart_agent(agent_type: AgentType):
    """
    Restart a specific agent (simulation)
    
    Args:
        agent_type: The type of agent to restart
        
    Returns:
        ApiResponse: Restart operation result
    """
    try:
        # In a real implementation, this would restart the actual agent
        # For now, we'll simulate the restart operation
        
        agent_names = {
            AgentType.ED_COORDINATOR: "ED Coordinator",
            AgentType.RESOURCE_MANAGER: "Resource Manager",
            AgentType.SPECIALIST_COORDINATOR: "Specialist Coordinator",
            AgentType.LAB_SERVICE: "Lab Service",
            AgentType.PHARMACY: "Pharmacy",
            AgentType.BED_MANAGEMENT: "Bed Management"
        }
        
        agent_name = agent_names.get(agent_type, str(agent_type))
        
        # Simulate restart delay
        import asyncio
        await asyncio.sleep(1)
        
        logger.info(f"Simulated restart for {agent_type} agent")
        
        return ApiResponse(
            success=True,
            message=f"{agent_name} agent restarted successfully",
            data={
                "agent_type": agent_type,
                "agent_name": agent_name,
                "restart_time": datetime.utcnow().isoformat(),
                "status": "online"
            }
        )
        
    except Exception as e:
        logger.error(f"Error restarting {agent_type} agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to restart {agent_type}: {str(e)}")

@router.get("/communication/stats", response_model=ApiResponse)
async def get_communication_stats():
    """
    Get agent communication statistics
    
    Returns:
        ApiResponse: Communication statistics
    """
    try:
        ws_manager = get_websocket_manager()
        all_agents = get_all_agents()
        
        # Get basic stats
        connected_clients = ws_manager.get_connected_clients_count()
        message_history = ws_manager.get_message_history(100)
        
        # Calculate message stats
        total_messages = len(message_history)
        agent_messages = len([msg for msg in message_history if msg.get('type') == 'agent'])
        user_messages = len([msg for msg in message_history if msg.get('type') == 'user'])
        
        stats_data = {
            "connected_clients": connected_clients,
            "total_messages": total_messages,
            "agent_messages": agent_messages,
            "user_messages": user_messages,
            "active_agents": len([agent for agent in all_agents.values() if agent is not None]),
            "last_message_time": message_history[-1].get('timestamp') if message_history else None,
            "communication_status": "active" if connected_clients > 0 else "idle"
        }
        
        return ApiResponse(
            success=True,
            message="Communication statistics retrieved successfully",
            data=stats_data
        )
        
    except Exception as e:
        logger.error(f"Error retrieving communication stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve communication stats: {str(e)}")