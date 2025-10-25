"""
Team and specialist-related data models for EDFlow AI
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from uagents import Model


class SpecialistType(str, Enum):
    """Types of medical specialists"""
    INTERVENTIONAL_CARDIOLOGY = "interventional_cardiology"
    NEUROLOGY = "neurology"
    NEUROSURGERY = "neurosurgery"
    TRAUMA_SURGERY = "trauma_surgery"
    ORTHOPEDIC_SURGERY = "orthopedic_surgery"
    PEDIATRICS = "pediatrics"
    ANESTHESIOLOGY = "anesthesiology"
    RADIOLOGY = "radiology"
    EMERGENCY_MEDICINE = "emergency_medicine"


class TeamType(str, Enum):
    """Types of emergency response teams"""
    STEMI_TEAM = "stemi_team"
    STROKE_TEAM = "stroke_team"
    TRAUMA_TEAM = "trauma_team"
    PEDIATRIC_TEAM = "pediatric_team"
    RAPID_RESPONSE = "rapid_response"


class MemberStatus(str, Enum):
    """Team member availability status"""
    AVAILABLE = "available"
    ACTIVATED = "activated"
    EN_ROUTE = "en_route"
    ON_SITE = "on_site"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"


class TeamMember(Model):
    """Individual team member"""
    member_id: str
    name: str
    role: str  # SpecialistType or other role
    status: str  # MemberStatus enum value
    location: Optional[str] = None
    contact_info: Optional[Dict[str, str]] = None
    estimated_arrival_minutes: Optional[int] = None


class TeamActivationRequest(Model):
    """Request to activate an emergency team"""
    activation_id: str
    team_type: str  # TeamType enum value
    patient_id: str
    urgency: str  # "immediate", "urgent", "routine"
    required_specialists: list[str]  # SpecialistType enum values
    location: str
    reason: str
    requesting_agent: str
    timestamp: datetime
    additional_info: Optional[Dict[str, Any]] = None


class TeamStatus(Model):
    """Status of activated team"""
    activation_id: str
    team_type: str
    team_members: list[Dict[str, str]]  # List of team member info
    assembly_time_seconds: Optional[float] = None
    ready: bool
    location: str
    timestamp: datetime
    notes: Optional[str] = None


class TeamAssembly(Model):
    """Team assembly progress tracking"""
    activation_id: str
    team_type: str
    members_activated: int
    members_en_route: int
    members_on_site: int
    total_required: int
    assembly_complete: bool
    assembly_start_time: datetime
    assembly_complete_time: Optional[datetime] = None
    bottlenecks: Optional[list[str]] = None