"""
Message-related data models for EDFlow AI agent communication
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from uagents import Model


class ProtocolType(str, Enum):
    """Types of emergency protocols"""
    STEMI = "stemi"
    STROKE = "stroke"
    TRAUMA = "trauma"
    PEDIATRIC = "pediatric"
    SEPSIS = "sepsis"
    GENERAL = "general"


class Priority(str, Enum):
    """Priority levels for orders and requests"""
    STAT = "stat"  # Immediate
    ASAP = "asap"  # As soon as possible
    URGENT = "urgent"  # Within 1 hour
    ROUTINE = "routine"  # Standard timing


class ProtocolActivation(Model):
    """Protocol activation message"""
    activation_id: str
    protocol_type: str  # ProtocolType enum value
    patient_id: str
    activation_time: datetime
    target_completion: datetime
    checklist: list[Dict[str, Any]]
    activating_agent: str
    metadata: Optional[Dict[str, Any]] = None


class LabOrder(Model):
    """Laboratory test order"""
    order_id: str
    patient_id: str
    tests: list[str]  # List of test names
    priority: str  # Priority enum value
    ordered_by: str
    order_time: datetime
    collection_location: Optional[str] = None
    special_instructions: Optional[str] = None


class LabResult(Model):
    """Laboratory test result"""
    result_id: str
    order_id: str
    patient_id: str
    test_name: str
    result_value: str
    result_unit: Optional[str] = None
    reference_range: Optional[str] = None
    critical: bool
    result_time: datetime
    reported_by: str
    notes: Optional[str] = None


class MedicationOrder(Model):
    """Medication order"""
    order_id: str
    patient_id: str
    medication_name: str
    dose: str
    route: str  # "IV", "PO", "IM", etc.
    frequency: str
    duration: Optional[str] = None
    priority: str  # Priority enum value
    ordered_by: str
    order_time: datetime
    indications: Optional[str] = None
    special_instructions: Optional[str] = None


class MedicationDelivery(Model):
    """Medication delivery status"""
    delivery_id: str
    order_id: str
    patient_id: str
    medication_name: str
    status: str  # "preparing", "ready", "delivered", "administered"
    delivered_by: Optional[str] = None
    delivery_time: Optional[datetime] = None
    administration_time: Optional[datetime] = None
    notes: Optional[str] = None


class BedRequest(Model):
    """Bed assignment request"""
    request_id: str
    patient_id: str
    bed_type: str  # BedType enum value
    priority: int  # 1-5
    special_requirements: Optional[list[str]] = None
    requesting_agent: str
    request_time: datetime
    isolation_needed: bool = False


class BedAssignment(Model):
    """Bed assignment response"""
    assignment_id: str
    request_id: str
    patient_id: str
    bed_id: Optional[str] = None
    bed_location: Optional[str] = None
    assigned: bool
    assignment_time: Optional[datetime] = None
    estimated_ready_time: Optional[datetime] = None
    notes: Optional[str] = None


class StatusUpdate(Model):
    """General status update message"""
    update_id: str
    entity_type: str  # "patient", "resource", "team", etc.
    entity_id: str
    status: str
    timestamp: datetime
    updated_by: str
    details: Optional[Dict[str, Any]] = None


class Alert(Model):
    """Alert/notification message"""
    alert_id: str
    alert_type: str  # "critical", "warning", "info"
    title: str
    message: str
    timestamp: datetime
    source_agent: str
    target_agents: Optional[list[str]] = None
    requires_action: bool = False
    context: Optional[Dict[str, Any]] = None