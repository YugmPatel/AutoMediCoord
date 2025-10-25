"""
Event tracking system for agent communication
Captures all messages and events for visualization
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from collections import defaultdict


class EventType(str, Enum):
    """Types of events to track"""
    AGENT_STARTED = "agent_started"
    AGENT_STOPPED = "agent_stopped"
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    PROTOCOL_ACTIVATED = "protocol_activated"
    PROTOCOL_STEP = "protocol_step"
    RESOURCE_ALLOCATED = "resource_allocated"
    TEAM_ACTIVATED = "team_activated"
    LAB_ORDER = "lab_order"
    LAB_RESULT = "lab_result"
    MEDICATION_ORDER = "medication_order"
    BED_ASSIGNED = "bed_assigned"
    ERROR = "error"
    METRIC = "metric"


@dataclass
class AgentEvent:
    """Represents a single event in the system"""
    timestamp: datetime
    event_type: EventType
    agent_name: str
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    from_agent: Optional[str] = None
    to_agent: Optional[str] = None
    message_type: Optional[str] = None
    latency_ms: Optional[float] = None
    patient_id: Optional[str] = None
    protocol: Optional[str] = None


class EventTracker:
    """Central event tracking system for all agent communications"""
    
    # Agent emoji mapping for visual identification
    AGENT_EMOJIS = {
        "ed_coordinator": "🏥",
        "resource_manager": "📊",
        "specialist_coordinator": "👨‍⚕️",
        "lab_service": "🧪",
        "pharmacy": "💊",
        "bed_management": "🛏️"
    }
    
    # Color scheme for agents
    AGENT_COLORS = {
        "ed_coordinator": "cyan",
        "resource_manager": "green",
        "specialist_coordinator": "yellow",
        "lab_service": "magenta",
        "pharmacy": "blue",
        "bed_management": "red"
    }
    
    def __init__(self):
        self.events: List[AgentEvent] = []
        self.agent_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "messages_sent": 0,
            "messages_received": 0,
            "avg_latency_ms": 0,
            "total_latency_ms": 0,
            "latency_count": 0,
            "status": "idle",
            "last_activity": None
        })
        self.protocol_timings: Dict[str, Dict[str, Any]] = {}
        self.start_time = datetime.utcnow()
        self._callbacks: List[callable] = []
    
    def register_callback(self, callback: callable):
        """Register a callback to be called when events occur"""
        self._callbacks.append(callback)
    
    async def _notify_callbacks(self, event: AgentEvent):
        """Notify all registered callbacks of a new event"""
        for callback in self._callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                print(f"Error in event callback: {e}")
    
    def track_event(self, event: AgentEvent):
        """Track a new event"""
        self.events.append(event)
        
        # Update agent stats
        if event.agent_name:
            stats = self.agent_stats[event.agent_name]
            stats["last_activity"] = event.timestamp
            stats["status"] = "active"
            
            if event.event_type == EventType.MESSAGE_SENT:
                stats["messages_sent"] += 1
            elif event.event_type == EventType.MESSAGE_RECEIVED:
                stats["messages_received"] += 1
            
            if event.latency_ms is not None:
                stats["total_latency_ms"] += event.latency_ms
                stats["latency_count"] += 1
                stats["avg_latency_ms"] = stats["total_latency_ms"] / stats["latency_count"]
        
        # Track protocol timings
        if event.protocol and event.patient_id:
            key = f"{event.patient_id}_{event.protocol}"
            if key not in self.protocol_timings:
                self.protocol_timings[key] = {
                    "patient_id": event.patient_id,
                    "protocol": event.protocol,
                    "start_time": event.timestamp,
                    "steps": [],
                    "completed": False
                }
            
            if event.event_type == EventType.PROTOCOL_STEP:
                self.protocol_timings[key]["steps"].append({
                    "step": event.description,
                    "timestamp": event.timestamp,
                    "details": event.details
                })
    
    async def track_event_async(self, event: AgentEvent):
        """Track event and notify callbacks asynchronously"""
        self.track_event(event)
        await self._notify_callbacks(event)
    
    def get_agent_emoji(self, agent_name: str) -> str:
        """Get emoji for agent"""
        return self.AGENT_EMOJIS.get(agent_name, "🤖")
    
    def get_agent_color(self, agent_name: str) -> str:
        """Get color for agent"""
        return self.AGENT_COLORS.get(agent_name, "white")
    
    def get_uptime_seconds(self) -> float:
        """Get system uptime in seconds"""
        return (datetime.utcnow() - self.start_time).total_seconds()
    
    def get_message_rate(self) -> float:
        """Get messages per second"""
        uptime = self.get_uptime_seconds()
        if uptime == 0:
            return 0
        total_messages = sum(
            stats["messages_sent"] + stats["messages_received"] 
            for stats in self.agent_stats.values()
        ) / 2  # Divide by 2 since each message counts for both sender and receiver
        return total_messages / uptime
    
    def get_recent_events(self, limit: int = 10) -> List[AgentEvent]:
        """Get most recent events"""
        return self.events[-limit:] if self.events else []
    
    def get_agent_stats(self, agent_name: str) -> Dict[str, Any]:
        """Get statistics for a specific agent"""
        return self.agent_stats.get(agent_name, {})
    
    def get_all_agent_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all agents"""
        return dict(self.agent_stats)
    
    def get_protocol_status(self, patient_id: str, protocol: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific protocol"""
        key = f"{patient_id}_{protocol}"
        return self.protocol_timings.get(key)
    
    def format_message_flow(self, event: AgentEvent) -> str:
        """Format a message flow for display"""
        if event.from_agent and event.to_agent:
            from_emoji = self.get_agent_emoji(event.from_agent)
            to_emoji = self.get_agent_emoji(event.to_agent)
            msg_type = event.message_type or "Message"
            return f"{from_emoji}→{to_emoji}  {msg_type:<25} | {event.description}"
        return f"{self.get_agent_emoji(event.agent_name)}  {event.description}"
    
    def clear_events(self):
        """Clear all tracked events (useful for testing)"""
        self.events.clear()
        self.agent_stats.clear()
        self.protocol_timings.clear()
        self.start_time = datetime.utcnow()


# Global event tracker instance
_global_tracker: Optional[EventTracker] = None


def get_event_tracker() -> EventTracker:
    """Get or create the global event tracker"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = EventTracker()
    return _global_tracker


def reset_event_tracker():
    """Reset the global event tracker"""
    global _global_tracker
    _global_tracker = EventTracker()