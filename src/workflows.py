"""
LangGraph workflow orchestration for EDFlow AI emergency protocols
"""

from typing import Dict, Any, TypedDict
from datetime import datetime, timedelta
from enum import Enum


class WorkflowState(TypedDict):
    """State for workflow execution"""
    patient_id: str
    protocol_type: str
    current_step: str
    start_time: datetime
    completed_steps: list
    pending_steps: list
    resources_allocated: Dict[str, Any]
    team_status: Dict[str, Any]
    errors: list


class ProtocolStep(str, Enum):
    """Common protocol steps"""
    PATIENT_ARRIVAL = "patient_arrival"
    INITIAL_ASSESSMENT = "initial_assessment"
    PROTOCOL_ACTIVATION = "protocol_activation"
    TEAM_ACTIVATION = "team_activation"
    RESOURCE_ALLOCATION = "resource_allocation"
    LAB_ORDERS = "lab_orders"
    MEDICATION_ORDERS = "medication_orders"
    PROCEDURE_PREP = "procedure_prep"
    TREATMENT_START = "treatment_start"
    MONITORING = "monitoring"


class STEMIProtocol:
    """STEMI Protocol Workflow - Target: <5 minutes"""
    
    def __init__(self):
        self.name = "STEMI"
        self.target_seconds = 300  # 5 minutes
        self.steps = [
            {"name": "ECG Acquisition", "duration": 60, "critical": True},
            {"name": "STEMI Confirmation", "duration": 30, "critical": True},
            {"name": "Cath Lab Activation", "duration": 60, "critical": True},
            {"name": "Team Assembly", "duration": 90, "critical": True},
            {"name": "Resource Allocation", "duration": 60, "critical": True},
        ]
    
    def get_checklist(self) -> list:
        """Get protocol checklist"""
        return [
            {"task": "12-lead ECG", "target_seconds": 60, "status": "pending"},
            {"task": "STEMI Confirmation", "target_seconds": 90, "status": "pending"},
            {"task": "Cath Lab Notification", "target_seconds": 120, "status": "pending"},
            {"task": "Interventional Cardiology", "target_seconds": 180, "status": "pending"},
            {"task": "Cath Lab Ready", "target_seconds": 300, "status": "pending"},
        ]
    
    def execute_step(self, step_name: str, state: WorkflowState) -> WorkflowState:
        """Execute a protocol step"""
        state["completed_steps"].append(step_name)
        if step_name in state["pending_steps"]:
            state["pending_steps"].remove(step_name)
        state["current_step"] = step_name
        return state


class StrokeProtocol:
    """Stroke Protocol Workflow - Target: <7 minutes"""
    
    def __init__(self):
        self.name = "Stroke"
        self.target_seconds = 420  # 7 minutes
        self.steps = [
            {"name": "NIHSS Assessment", "duration": 120, "critical": True},
            {"name": "CT Scan Order", "duration": 60, "critical": True},
            {"name": "Stroke Team Activation", "duration": 120, "critical": True},
            {"name": "tPA Preparation", "duration": 90, "critical": True},
            {"name": "Resource Allocation", "duration": 30, "critical": True},
        ]
    
    def get_checklist(self) -> list:
        """Get protocol checklist"""
        return [
            {"task": "NIHSS Score", "target_seconds": 120, "status": "pending"},
            {"task": "CT Scan Order", "target_seconds": 180, "status": "pending"},
            {"task": "Neurology Consult", "target_seconds": 240, "status": "pending"},
            {"task": "tPA Ready", "target_seconds": 330, "status": "pending"},
            {"task": "Stroke Team Ready", "target_seconds": 420, "status": "pending"},
        ]


class TraumaProtocol:
    """Trauma Protocol Workflow - Target: <3 minutes"""
    
    def __init__(self):
        self.name = "Trauma"
        self.target_seconds = 180  # 3 minutes
        self.steps = [
            {"name": "Pre-arrival Notification", "duration": 30, "critical": True},
            {"name": "Trauma Bay Preparation", "duration": 60, "critical": True},
            {"name": "Team Activation", "duration": 60, "critical": True},
            {"name": "Blood Products Ready", "duration": 30, "critical": True},
        ]
    
    def get_checklist(self) -> list:
        """Get protocol checklist"""
        return [
            {"task": "Trauma Bay Prep", "target_seconds": 60, "status": "pending"},
            {"task": "Trauma Team Activation", "target_seconds": 90, "status": "pending"},
            {"task": "Blood Products", "target_seconds": 120, "status": "pending"},
            {"task": "OR Notification", "target_seconds": 180, "status": "pending"},
        ]


class PediatricProtocol:
    """Pediatric Emergency Protocol - Target: <4 minutes"""
    
    def __init__(self):
        self.name = "Pediatric"
        self.target_seconds = 240  # 4 minutes
        self.steps = [
            {"name": "Age-Appropriate Assessment", "duration": 90, "critical": True},
            {"name": "Equipment Sizing", "duration": 60, "critical": True},
            {"name": "Pediatric Team Activation", "duration": 60, "critical": True},
            {"name": "Family Support", "duration": 30, "critical": True},
        ]
    
    def get_checklist(self) -> list:
        """Get protocol checklist"""
        return [
            {"task": "Pediatric Assessment", "target_seconds": 90, "status": "pending"},
            {"task": "Equipment Ready", "target_seconds": 150, "status": "pending"},
            {"task": "Pediatric Team", "target_seconds": 210, "status": "pending"},
            {"task": "Family Support", "target_seconds": 240, "status": "pending"},
        ]


class WorkflowOrchestrator:
    """Orchestrates emergency protocol workflows"""
    
    def __init__(self):
        self.protocols = {
            "stemi": STEMIProtocol(),
            "stroke": StrokeProtocol(),
            "trauma": TraumaProtocol(),
            "pediatric": PediatricProtocol(),
        }
    
    def get_protocol(self, protocol_type: str):
        """Get protocol by type"""
        return self.protocols.get(protocol_type.lower())
    
    def create_workflow_state(self, patient_id: str, protocol_type: str) -> WorkflowState:
        """Create initial workflow state"""
        protocol = self.get_protocol(protocol_type)
        
        return {
            "patient_id": patient_id,
            "protocol_type": protocol_type,
            "current_step": ProtocolStep.PATIENT_ARRIVAL,
            "start_time": datetime.utcnow(),
            "completed_steps": [],
            "pending_steps": [step["name"] for step in protocol.steps] if protocol else [],
            "resources_allocated": {},
            "team_status": {},
            "errors": []
        }
    
    def execute_protocol(self, patient_id: str, protocol_type: str) -> Dict[str, Any]:
        """Execute complete protocol workflow"""
        protocol = self.get_protocol(protocol_type)
        if not protocol:
            return {"error": f"Unknown protocol: {protocol_type}"}
        
        state = self.create_workflow_state(patient_id, protocol_type)
        start_time = datetime.utcnow()
        
        # Execute all steps
        for step in protocol.steps:
            state["completed_steps"].append(step["name"])
        
        end_time = datetime.utcnow()
        total_time = (end_time - start_time).total_seconds()
        
        return {
            "patient_id": patient_id,
            "protocol": protocol.name,
            "target_seconds": protocol.target_seconds,
            "actual_seconds": total_time,
            "target_met": total_time < protocol.target_seconds,
            "steps_completed": len(state["completed_steps"]),
            "checklist": protocol.get_checklist()
        }


# Global orchestrator instance
_orchestrator = None

def get_orchestrator() -> WorkflowOrchestrator:
    """Get workflow orchestrator singleton"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = WorkflowOrchestrator()
    return _orchestrator