"""
WebSocket Manager for EDFlow AI
Handles real-time communication between uAgents and React frontend
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
import socketio

from ..models.api_models import (
    WebSocketEvent, PatientArrivalEvent, ProtocolActivationEvent,
    CaseUpdateEvent, AgentMessageEvent, ChatMessage, MessageType
)
from src.utils import get_logger

logger = get_logger(__name__)

class WebSocketManager:
    """Manages WebSocket connections and real-time events"""
    
    def __init__(self, sio: socketio.AsyncServer):
        self.sio = sio
        self.connected_clients: Set[str] = set()
        self.agent_listeners: Dict[str, Any] = {}
        self.message_history: List[ChatMessage] = []
        self.setup_socket_handlers()
        
    def setup_socket_handlers(self):
        """Setup Socket.IO event handlers"""
        
        @self.sio.event
        async def connect(sid, environ):
            """Handle client connection"""
            self.connected_clients.add(sid)
            logger.info(f"Client {sid} connected. Total clients: {len(self.connected_clients)}")
            
            # Send connection confirmation
            await self.sio.emit('connection_status', {
                'connected': True,
                'timestamp': datetime.utcnow().isoformat(),
                'client_id': sid
            }, room=sid)
            
            # Send recent message history
            if self.message_history:
                recent_messages = self.message_history[-10:]  # Last 10 messages
                await self.sio.emit('message_history', {
                    'messages': [self._serialize_message(msg) for msg in recent_messages]
                }, room=sid)
        
        @self.sio.event
        async def disconnect(sid):
            """Handle client disconnection"""
            self.connected_clients.discard(sid)
            logger.info(f"Client {sid} disconnected. Total clients: {len(self.connected_clients)}")
        
        @self.sio.event
        async def send_message(sid, data):
            """Handle chat messages from frontend"""
            try:
                message_content = data.get('message', '').strip()
                sender = data.get('sender', 'User')
                
                if not message_content:
                    await self.sio.emit('error', {
                        'message': 'Message content cannot be empty'
                    }, room=sid)
                    return
                
                # Create chat message
                chat_message = ChatMessage(
                    id=f"msg_{datetime.utcnow().timestamp()}",
                    content=message_content,
                    timestamp=datetime.utcnow(),
                    sender=sender,
                    type=MessageType.USER
                )
                
                # Add to history
                self.message_history.append(chat_message)
                
                # Broadcast to all clients
                await self.broadcast_chat_message(chat_message)
                
                # Simulate agent response after a delay
                asyncio.create_task(self._simulate_agent_response(message_content))
                
                logger.info(f"Chat message from {sender}: {message_content[:50]}...")
                
            except Exception as e:
                logger.error(f"Error handling chat message: {str(e)}")
                await self.sio.emit('error', {
                    'message': f'Failed to process message: {str(e)}'
                }, room=sid)
        
        @self.sio.event
        async def request_dashboard_update(sid):
            """Handle dashboard update requests"""
            try:
                # Trigger dashboard data refresh
                await self.sio.emit('dashboard_refresh', {
                    'timestamp': datetime.utcnow().isoformat()
                }, room=sid)
                
            except Exception as e:
                logger.error(f"Error handling dashboard update request: {str(e)}")
        
        @self.sio.event
        async def join_room(sid, data):
            """Handle room joining for targeted updates"""
            try:
                room = data.get('room', 'general')
                await self.sio.enter_room(sid, room)
                logger.info(f"Client {sid} joined room {room}")
                
            except Exception as e:
                logger.error(f"Error joining room: {str(e)}")
        
        @self.sio.event
        async def leave_room(sid, data):
            """Handle room leaving"""
            try:
                room = data.get('room', 'general')
                await self.sio.leave_room(sid, room)
                logger.info(f"Client {sid} left room {room}")
                
            except Exception as e:
                logger.error(f"Error leaving room: {str(e)}")
    
    async def setup_agent_listeners(self, agents: Dict[str, Any]):
        """Setup listeners for agent events"""
        self.agent_listeners = agents
        logger.info(f"Setup listeners for {len(agents)} agents")
        
        # In a real implementation, you would setup actual listeners
        # to the uAgent message handlers here
        # For now, we'll simulate this with periodic updates
        asyncio.create_task(self._periodic_agent_updates())
    
    async def _periodic_agent_updates(self):
        """Simulate periodic agent updates"""
        while True:
            try:
                await asyncio.sleep(30)  # Update every 30 seconds
                
                if self.connected_clients:
                    # Simulate agent activity
                    await self.broadcast_agent_activity({
                        'agent': 'system',
                        'message': 'System health check',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    
            except Exception as e:
                logger.error(f"Error in periodic updates: {str(e)}")
    
    async def _simulate_agent_response(self, user_message: str):
        """Simulate agent response to user messages"""
        await asyncio.sleep(2)  # Simulate processing delay
        
        try:
            # Determine which agent should respond based on message content
            agent_name = "ED Coordinator"
            agent_type = "ed_coordinator"
            
            if "lab" in user_message.lower():
                agent_name = "Lab Service"
                agent_type = "lab_service"
            elif "medication" in user_message.lower() or "drug" in user_message.lower():
                agent_name = "Pharmacy"
                agent_type = "pharmacy"
            elif "bed" in user_message.lower():
                agent_name = "Bed Management"
                agent_type = "bed_management"
            elif "doctor" in user_message.lower() or "specialist" in user_message.lower():
                agent_name = "Specialist Coordinator"
                agent_type = "specialist_coordinator"
            
            # Generate appropriate response
            responses = [
                "Message received. Processing request...",
                "Acknowledged. Coordinating with relevant departments.",
                "Request understood. Initiating appropriate protocols.",
                "Confirmed. Updating patient status and notifying team.",
                "Received. Checking resource availability and scheduling."
            ]
            
            import random
            response_content = random.choice(responses)
            
            # Create agent response message
            agent_message = ChatMessage(
                id=f"agent_{datetime.utcnow().timestamp()}",
                content=response_content,
                timestamp=datetime.utcnow(),
                sender=agent_name,
                type=MessageType.AGENT,
                agent_type=agent_type
            )
            
            # Add to history
            self.message_history.append(agent_message)
            
            # Broadcast to all clients
            await self.broadcast_chat_message(agent_message)
            
        except Exception as e:
            logger.error(f"Error simulating agent response: {str(e)}")
    
    def _serialize_message(self, message: ChatMessage) -> Dict[str, Any]:
        """Serialize chat message for transmission"""
        return {
            'id': message.id,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
            'sender': message.sender,
            'type': message.type,
            'agent_type': message.agent_type
        }
    
    async def broadcast_patient_arrival(self, patient_data: Dict[str, Any]):
        """Broadcast new patient arrival to all connected clients"""
        try:
            event = PatientArrivalEvent(
                data=patient_data
            )
            
            await self.sio.emit('patient_arrival', {
                'type': 'patient_arrival',
                'data': patient_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            logger.info(f"Broadcasted patient arrival: {patient_data.get('patient_id')}")
            
        except Exception as e:
            logger.error(f"Error broadcasting patient arrival: {str(e)}")
    
    async def broadcast_protocol_activation(self, protocol_data: Dict[str, Any]):
        """Broadcast protocol activation to all connected clients"""
        try:
            event = ProtocolActivationEvent(
                data=protocol_data
            )
            
            await self.sio.emit('protocol_activation', {
                'type': 'protocol_activation',
                'data': protocol_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            logger.info(f"Broadcasted protocol activation: {protocol_data.get('protocol')}")
            
        except Exception as e:
            logger.error(f"Error broadcasting protocol activation: {str(e)}")
    
    async def broadcast_case_update(self, case_data: Dict[str, Any]):
        """Broadcast case status update to all connected clients"""
        try:
            event = CaseUpdateEvent(
                data=case_data
            )
            
            await self.sio.emit('case_update', {
                'type': 'case_update',
                'data': case_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            logger.info(f"Broadcasted case update: {case_data.get('case_id')}")
            
        except Exception as e:
            logger.error(f"Error broadcasting case update: {str(e)}")
    
    async def broadcast_agent_message(self, message_data: Dict[str, Any]):
        """Broadcast agent communication to all connected clients"""
        try:
            event = AgentMessageEvent(
                data=message_data
            )
            
            await self.sio.emit('agent_message', {
                'type': 'agent_message',
                'data': message_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            logger.info(f"Broadcasted agent message from: {message_data.get('agent')}")
            
        except Exception as e:
            logger.error(f"Error broadcasting agent message: {str(e)}")
    
    async def broadcast_chat_message(self, message: ChatMessage):
        """Broadcast chat message to all connected clients"""
        try:
            await self.sio.emit('chat_message', self._serialize_message(message))
            logger.info(f"Broadcasted chat message from {message.sender}")
            
        except Exception as e:
            logger.error(f"Error broadcasting chat message: {str(e)}")
    
    async def broadcast_agent_activity(self, activity_data: Dict[str, Any]):
        """Broadcast general agent activity"""
        try:
            await self.sio.emit('agent_activity', {
                'type': 'agent_activity',
                'data': activity_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error broadcasting agent activity: {str(e)}")
    
    async def broadcast_dashboard_update(self, update_data: Dict[str, Any]):
        """Broadcast dashboard data updates"""
        try:
            await self.sio.emit('dashboard_update', {
                'type': 'dashboard_update',
                'data': update_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            logger.info("Broadcasted dashboard update")
            
        except Exception as e:
            logger.error(f"Error broadcasting dashboard update: {str(e)}")
    
    async def send_to_client(self, client_id: str, event: str, data: Dict[str, Any]):
        """Send event to specific client"""
        try:
            if client_id in self.connected_clients:
                await self.sio.emit(event, data, room=client_id)
                logger.info(f"Sent {event} to client {client_id}")
            else:
                logger.warning(f"Client {client_id} not connected")
                
        except Exception as e:
            logger.error(f"Error sending to client {client_id}: {str(e)}")
    
    def get_connected_clients_count(self) -> int:
        """Get number of connected clients"""
        return len(self.connected_clients)
    
    def get_message_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent message history"""
        recent_messages = self.message_history[-limit:] if self.message_history else []
        return [self._serialize_message(msg) for msg in recent_messages]