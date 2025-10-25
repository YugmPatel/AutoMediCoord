"""
All EDFlow AI Data Models - Consolidated
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from uagents import Model


# ============================================================================
# ENUMS
# ============================================================================

class AcuityLevel(str, Enum):
    LEVEL_1 = "1"  # Immediate life threat
    LEVEL_2 = "2"  # High risk
    LEVEL_3 = "3"  # Moderate risk
    LEVEL_4 = "4"  # Low risk
    LEVEL_5 = "5"  # Minimal risk


class PatientStatus(str, Enum):
    ARRIVING = "arriving"
    TRIAGED = "triaged"
    PROTOCOL_ACTIVATED = "protocol_activated"
    IN_TREATMENT = "in_treatment"
    ADMITTED = "admitted"
    DISCHARGED = "discharged"


class ResourceType(str, Enum):
    BED = "bed"
    EQUIPMENT = "equipment"
    ROOM = "room"
    STAFF = "staff"


class ResourceStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    CLEANING = "cleaning"


class ProtocolType(str, Enum):
    STEMI = "stemi"
    STROKE = "stroke"
    TRAUMA = "trauma"
    PEDIATRIC = "pediatric"
    GENERAL = "general"


class Priority(str, Enum):
    STAT = "stat"
    ASAP = "asap"
    URGENT = "urgent"
    ROUTINE = "routine"


# ============================================================================
# PATIENT MODELS
# ============================================================================

class PatientArrivalNotification(Model):
    patient_id: str
    arrival_time: datetime
    vitals: Dict[str, Any]
    chief_complaint: str
    ems_report: str
    estimated_arrival_minutes: Optional[int] = None
    priority: int
    demographics: Optional[Dict[str, Any]] = None


class PatientUpdate(Model):
    patient_id: str
    status: str
    location: str
    timestamp: datetime
    additional_info: Optional[Dict[str, Any]] = None


# ============================================================================
# RESOURCE MODELS
# ============================================================================

class ResourceRequest(Model):
    request_id: str
    resource_type: str
    requirements: Dict[str, Any]
    priority: int
    patient_id: str
    requesting_agent: str
    timestamp: datetime


class ResourceAllocation(Model):
    request_id: str
    resource_id: Optional[str] = None
    resource_type: str
    allocated: bool
    location: Optional[str] = None
    expires_at: Optional[datetime] = None
    timestamp: datetime


class ResourceConflict(Model):
    conflict_id: str
    competing_requests: List[str]
    resource_type: str
    resolution_required: bool
    timestamp: datetime


# ============================================================================
# TEAM MODELS
# ============================================================================

class TeamActivationRequest(Model):
    activation_id: str
    team_type: str
    patient_id: str
    urgency: str
    required_specialists: List[str]
    location: str
    reason: str
    requesting_agent: str
    timestamp: datetime


class TeamStatus(Model):
    activation_id: str
    team_type: str
    team_members: List[Dict[str, str]]
    assembly_time_seconds: Optional[float] = None
    ready: bool
    location: str
    timestamp: datetime


# ============================================================================
# MESSAGE MODELS
# ============================================================================

class ProtocolActivation(Model):
    activation_id: str
    protocol_type: str
    patient_id: str
    activation_time: datetime
    target_completion: datetime
    checklist: List[Dict[str, Any]]
    activating_agent: str
    metadata: Optional[Dict[str, Any]] = None


class LabOrder(Model):
    order_id: str
    patient_id: str
    tests: List[str]
    priority: str
    ordered_by: str
    order_time: datetime


class LabResult(Model):
    result_id: str
    order_id: str
    patient_id: str
    test_name: str
    result_value: str
    result_unit: Optional[str] = None
    critical: bool
    result_time: datetime
    reported_by: str


class MedicationOrder(Model):
    order_id: str
    patient_id: str
    medication_name: str
    dose: str
    route: str
    frequency: str
    priority: str
    ordered_by: str
    order_time: datetime


class MedicationDelivery(Model):
    delivery_id: str
    order_id: str
    patient_id: str
    medication_name: str
    status: str
    delivered_by: Optional[str] = None
    delivery_time: Optional[datetime] = None


class BedRequest(Model):
    request_id: str
    patient_id: str
    bed_type: str
    priority: int
    requesting_agent: str
    request_time: datetime
    isolation_needed: bool = False


class BedAssignment(Model):
    assignment_id: str
    request_id: str
    patient_id: str
    bed_id: Optional[str] = None
    bed_location: Optional[str] = None
    assigned: bool
    assignment_time: Optional[datetime] = None


class StatusUpdate(Model):
    update_id: str
    entity_type: str
    entity_id: str
    status: str
    timestamp: datetime
    updated_by: str
    details: Optional[Dict[str, Any]] = None


class Alert(Model):
    alert_id: str
    alert_type: str
    title: str
    message: str
    timestamp: datetime
    source_agent: str
    target_agents: Optional[List[str]] = None
    requires_action: bool = False


__all__ = [
    # Enums
    "AcuityLevel", "PatientStatus", "ResourceType", "ResourceStatus",
    "ProtocolType", "Priority",
    # Patient Models
    "PatientArrivalNotification", "PatientUpdate",
    # Resource Models
    "ResourceRequest", "ResourceAllocation", "ResourceConflict",
    # Team Models
    "TeamActivationRequest", "TeamStatus",
    # Message Models
    "ProtocolActivation", "LabOrder", "LabResult",
    "MedicationOrder", "MedicationDelivery",
    "BedRequest", "BedAssignment",
    "StatusUpdate", "Alert",
]