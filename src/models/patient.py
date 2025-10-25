"""
Patient-related data models for EDFlow AI
"""

from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from uagents import Model


class AcuityLevel(str, Enum):
    """Emergency Severity Index (ESI) - 1 is most critical"""
    LEVEL_1 = "1"  # Immediate life threat
    LEVEL_2 = "2"  # High risk
    LEVEL_3 = "3"  # Moderate risk
    LEVEL_4 = "4"  # Low risk
    LEVEL_5 = "5"  # Minimal risk


class PatientStatus(str, Enum):
    """Patient status in ED workflow"""
    ARRIVING = "arriving"
    TRIAGED = "triaged"
    PROTOCOL_ACTIVATED = "protocol_activated"
    IN_TREATMENT = "in_treatment"
    AWAITING_ADMISSION = "awaiting_admission"
    ADMITTED = "admitted"
    DISCHARGED = "discharged"


class PatientVitals(Model):
    """Patient vital signs"""
    blood_pressure_systolic: int  # mmHg
    blood_pressure_diastolic: int  # mmHg
    heart_rate: int  # beats per minute
    respiratory_rate: int  # breaths per minute
    oxygen_saturation: int  # percentage
    temperature: float  # Fahrenheit
    timestamp: datetime


class PatientDemographics(Model):
    """Patient demographic information"""
    patient_id: str
    age: int
    gender: str  # "M", "F", "Other"
    weight_kg: Optional[float] = None
    medical_history: Optional[Dict[str, Any]] = None


class PatientArrivalNotification(Model):
    """Notification of patient arrival from ambulance/EMS"""
    patient_id: str
    arrival_time: datetime
    vitals: Dict[str, Any]  # Vital signs
    chief_complaint: str
    ems_report: str
    estimated_arrival_minutes: Optional[int] = None
    priority: int  # 1-5 (ESI scale)
    demographics: Optional[Dict[str, Any]] = None


class PatientUpdate(Model):
    """Update on patient status"""
    patient_id: str
    status: str  # PatientStatus enum value
    location: str
    timestamp: datetime
    additional_info: Optional[Dict[str, Any]] = None


class PatientState(Model):
    """Complete patient state for LangGraph workflow"""
    patient_id: str
    arrival_time: datetime
    demographics: Dict[str, Any]
    vitals: Dict[str, Any]
    chief_complaint: str
    ems_report: str
    
    # Workflow state
    current_status: str  # PatientStatus enum value
    acuity_level: str  # AcuityLevel enum value
    assigned_protocol: Optional[str] = None  # ProtocolType enum value
    
    # Resource tracking
    assigned_bed: Optional[str] = None
    assigned_room: Optional[str] = None
    equipment_allocated: list[str] = []
    
    # Team tracking
    activated_teams: list[str] = []
    attending_staff: list[Dict[str, str]] = []
    
    # Clinical tracking
    lab_orders: list[str] = []
    medication_orders: list[str] = []
    procedures_ordered: list[str] = []
    
    # Timing
    triage_time: Optional[datetime] = None
    protocol_activation_time: Optional[datetime] = None
    treatment_start_time: Optional[datetime] = None
    disposition_time: Optional[datetime] = None
    
    # Metadata
    last_updated: datetime
    notes: Optional[str] = None