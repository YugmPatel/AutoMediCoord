"""
Resource-related data models for EDFlow AI
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from uagents import Model


class ResourceType(str, Enum):
    """Types of ED resources"""
    BED = "bed"
    EQUIPMENT = "equipment"
    ROOM = "room"
    STAFF = "staff"


class ResourceStatus(str, Enum):
    """Resource availability status"""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    CLEANING = "cleaning"
    MAINTENANCE = "maintenance"
    UNAVAILABLE = "unavailable"


class BedType(str, Enum):
    """Types of beds"""
    TRAUMA_BAY = "trauma_bay"
    CARDIAC_MONITORING = "cardiac_monitoring"
    ISOLATION = "isolation"
    GENERAL = "general"
    PEDIATRIC = "pediatric"


class Resource(Model):
    """Resource entity"""
    resource_id: str
    resource_type: str  # ResourceType enum value
    resource_subtype: Optional[str] = None  # e.g., BedType
    status: str  # ResourceStatus enum value
    location: str
    capabilities: list[str] = []
    metadata: Optional[Dict[str, Any]] = None
    last_updated: datetime


class ResourceRequest(Model):
    """Request for resource allocation"""
    request_id: str
    resource_type: str  # ResourceType enum value
    requirements: Dict[str, Any]  # Specific requirements
    priority: int  # 1-5 (1 is highest)
    patient_id: str
    requesting_agent: str
    timestamp: datetime
    deadline: Optional[datetime] = None


class ResourceAllocation(Model):
    """Resource allocation response"""
    request_id: str
    resource_id: Optional[str] = None
    resource_type: str
    allocated: bool
    location: Optional[str] = None
    expires_at: Optional[datetime] = None
    timestamp: datetime
    allocation_metadata: Optional[Dict[str, Any]] = None


class ResourceConflict(Model):
    """Resource conflict notification"""
    conflict_id: str
    competing_requests: list[str]
    resource_type: str
    resource_id: Optional[str] = None
    resolution_required: bool
    priority_order: Optional[list[str]] = None  # Suggested resolution order
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None


class ResourceUtilization(Model):
    """Resource utilization metrics"""
    resource_type: str
    total_resources: int
    available: int
    occupied: int
    reserved: int
    utilization_percentage: float
    timestamp: datetime