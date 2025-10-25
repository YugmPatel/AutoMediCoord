"""
Simulation API Routes
Endpoints for triggering patient simulations (STEMI, Stroke, etc.)
"""

from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from ..models.api_models import (
    SimulationRequest, SimulationResponse, CaseType, ApiResponse
)
from src.models import PatientArrivalNotification
from src.utils import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Dependency to get agents and websocket manager
def get_ed_coordinator():
    from api.main import get_ed_coordinator
    return get_ed_coordinator()

def get_websocket_manager():
    from api.main import get_websocket_manager
    return get_websocket_manager()

@router.post("/stemi", response_model=SimulationResponse)
async def simulate_stemi(background_tasks: BackgroundTasks):
    """
    Trigger STEMI patient simulation
    
    Returns:
        SimulationResponse: Simulation result with patient details
    """
    try:
        ed_coordinator = get_ed_coordinator()
        ws_manager = get_websocket_manager()
        
        # Generate unique patient ID
        patient_id = f"STEMI_{datetime.utcnow().strftime('%H%M%S')}"
        
        # Create STEMI patient data
        patient_data = PatientArrivalNotification(
            patient_id=patient_id,
            arrival_time=datetime.utcnow(),
            vitals={
                "hr": 110,
                "bp_sys": 160,
                "bp_dia": 95,
                "spo2": 94,
                "temp": 37.2
            },
            chief_complaint="Severe chest pain radiating to left arm and jaw",
            ems_report="72-year-old male with crushing chest pain, ST elevation on ECG, suspected STEMI",
            priority=1,
            demographics={
                "age": 72,
                "gender": "male",
                "weight": 80
            }
        )
        
        # Process through ED Coordinator
        logger.info(f"Processing STEMI simulation for patient {patient_id}")
        
        # Add to ED Coordinator's active patients
        if not hasattr(ed_coordinator, 'active_patients'):
            ed_coordinator.active_patients = {}
        
        ed_coordinator.active_patients[patient_id] = {
            "acuity": "1",
            "protocol": "stemi",
            "status": "Triaged",
            "arrival_time": datetime.utcnow(),
            "vitals": patient_data.vitals,
            "chief_complaint": patient_data.chief_complaint,
            "ems_report": patient_data.ems_report,
            "lab_eta": 8,
            "assigned_bed": f"ED-{len(ed_coordinator.active_patients) + 1}"
        }
        
        # Broadcast patient arrival via WebSocket
        background_tasks.add_task(
            ws_manager.broadcast_patient_arrival,
            {
                "patient_id": patient_id,
                "type": "STEMI",
                "vitals": patient_data.vitals,
                "status": "Triaged",
                "protocol": "stemi"
            }
        )
        
        # Broadcast protocol activation
        background_tasks.add_task(
            ws_manager.broadcast_protocol_activation,
            {
                "patient_id": patient_id,
                "protocol": "STEMI",
                "activation_time": datetime.utcnow().isoformat(),
                "target_completion": (datetime.utcnow().timestamp() + 300),  # 5 minutes
                "priority": 1
            }
        )
        
        response = SimulationResponse(
            message="STEMI simulation triggered successfully",
            patient_id=patient_id,
            case_type=CaseType.STEMI,
            timestamp=datetime.utcnow(),
            success=True
        )
        
        logger.info(f"STEMI simulation completed for patient {patient_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error in STEMI simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"STEMI simulation failed: {str(e)}")

@router.post("/stroke", response_model=SimulationResponse)
async def simulate_stroke(background_tasks: BackgroundTasks):
    """
    Trigger Stroke patient simulation
    
    Returns:
        SimulationResponse: Simulation result with patient details
    """
    try:
        ed_coordinator = get_ed_coordinator()
        ws_manager = get_websocket_manager()
        
        # Generate unique patient ID
        patient_id = f"STROKE_{datetime.utcnow().strftime('%H%M%S')}"
        
        # Create Stroke patient data
        patient_data = PatientArrivalNotification(
            patient_id=patient_id,
            arrival_time=datetime.utcnow(),
            vitals={
                "hr": 80,
                "bp_sys": 195,
                "bp_dia": 118,
                "spo2": 96,
                "temp": 36.8
            },
            chief_complaint="Sudden onset weakness and speech difficulty",
            ems_report="68-year-old female with left-sided weakness, NIHSS 8, suspected stroke",
            priority=1,
            demographics={
                "age": 68,
                "gender": "female",
                "weight": 65
            }
        )
        
        # Process through ED Coordinator
        logger.info(f"Processing Stroke simulation for patient {patient_id}")
        
        # Add to ED Coordinator's active patients
        if not hasattr(ed_coordinator, 'active_patients'):
            ed_coordinator.active_patients = {}
        
        ed_coordinator.active_patients[patient_id] = {
            "acuity": "1",
            "protocol": "stroke",
            "status": "Triaged",
            "arrival_time": datetime.utcnow(),
            "vitals": patient_data.vitals,
            "chief_complaint": patient_data.chief_complaint,
            "ems_report": patient_data.ems_report,
            "lab_eta": 6,
            "assigned_bed": f"ED-{len(ed_coordinator.active_patients) + 1}"
        }
        
        # Broadcast patient arrival via WebSocket
        background_tasks.add_task(
            ws_manager.broadcast_patient_arrival,
            {
                "patient_id": patient_id,
                "type": "Stroke",
                "vitals": patient_data.vitals,
                "status": "Triaged",
                "protocol": "stroke"
            }
        )
        
        # Broadcast protocol activation
        background_tasks.add_task(
            ws_manager.broadcast_protocol_activation,
            {
                "patient_id": patient_id,
                "protocol": "Stroke",
                "activation_time": datetime.utcnow().isoformat(),
                "target_completion": (datetime.utcnow().timestamp() + 420),  # 7 minutes
                "priority": 1
            }
        )
        
        response = SimulationResponse(
            message="Stroke simulation triggered successfully",
            patient_id=patient_id,
            case_type=CaseType.STROKE,
            timestamp=datetime.utcnow(),
            success=True
        )
        
        logger.info(f"Stroke simulation completed for patient {patient_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error in Stroke simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stroke simulation failed: {str(e)}")

@router.post("/trauma", response_model=SimulationResponse)
async def simulate_trauma(background_tasks: BackgroundTasks):
    """
    Trigger Trauma patient simulation
    
    Returns:
        SimulationResponse: Simulation result with patient details
    """
    try:
        ed_coordinator = get_ed_coordinator()
        ws_manager = get_websocket_manager()
        
        # Generate unique patient ID
        patient_id = f"TRAUMA_{datetime.utcnow().strftime('%H%M%S')}"
        
        # Create Trauma patient data
        patient_data = PatientArrivalNotification(
            patient_id=patient_id,
            arrival_time=datetime.utcnow(),
            vitals={
                "hr": 120,
                "bp_sys": 90,
                "bp_dia": 60,
                "spo2": 92,
                "temp": 36.5
            },
            chief_complaint="Multiple injuries from motor vehicle accident",
            ems_report="25-year-old male, high-speed MVA, multiple trauma, GCS 14",
            priority=1,
            demographics={
                "age": 25,
                "gender": "male",
                "weight": 75
            }
        )
        
        # Process through ED Coordinator
        logger.info(f"Processing Trauma simulation for patient {patient_id}")
        
        # Add to ED Coordinator's active patients
        if not hasattr(ed_coordinator, 'active_patients'):
            ed_coordinator.active_patients = {}
        
        ed_coordinator.active_patients[patient_id] = {
            "acuity": "1",
            "protocol": "trauma",
            "status": "Triaged",
            "arrival_time": datetime.utcnow(),
            "vitals": patient_data.vitals,
            "chief_complaint": patient_data.chief_complaint,
            "ems_report": patient_data.ems_report,
            "lab_eta": 5,
            "assigned_bed": f"Trauma-{len(ed_coordinator.active_patients) + 1}"
        }
        
        # Broadcast patient arrival via WebSocket
        background_tasks.add_task(
            ws_manager.broadcast_patient_arrival,
            {
                "patient_id": patient_id,
                "type": "Trauma",
                "vitals": patient_data.vitals,
                "status": "Triaged",
                "protocol": "trauma"
            }
        )
        
        # Broadcast protocol activation
        background_tasks.add_task(
            ws_manager.broadcast_protocol_activation,
            {
                "patient_id": patient_id,
                "protocol": "Trauma",
                "activation_time": datetime.utcnow().isoformat(),
                "target_completion": (datetime.utcnow().timestamp() + 180),  # 3 minutes
                "priority": 1
            }
        )
        
        response = SimulationResponse(
            message="Trauma simulation triggered successfully",
            patient_id=patient_id,
            case_type=CaseType.TRAUMA,
            timestamp=datetime.utcnow(),
            success=True
        )
        
        logger.info(f"Trauma simulation completed for patient {patient_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error in Trauma simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Trauma simulation failed: {str(e)}")

@router.post("/custom", response_model=SimulationResponse)
async def simulate_custom_case(
    request: SimulationRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger custom patient simulation
    
    Args:
        request: Custom simulation parameters
        
    Returns:
        SimulationResponse: Simulation result with patient details
    """
    try:
        ed_coordinator = get_ed_coordinator()
        ws_manager = get_websocket_manager()
        
        # Generate unique patient ID
        patient_id = f"{request.case_type.upper()}_{datetime.utcnow().strftime('%H%M%S')}"
        
        # Use provided patient data or defaults
        patient_data = request.patient_data or {}
        
        # Create patient notification
        patient_notification = PatientArrivalNotification(
            patient_id=patient_id,
            arrival_time=datetime.utcnow(),
            vitals=patient_data.get("vitals", {
                "hr": 85,
                "bp_sys": 120,
                "bp_dia": 80,
                "spo2": 98,
                "temp": 37.0
            }),
            chief_complaint=patient_data.get("chief_complaint", f"{request.case_type} patient"),
            ems_report=patient_data.get("ems_report", f"Custom {request.case_type} simulation"),
            priority=patient_data.get("priority", 2)
        )
        
        # Add to ED Coordinator's active patients
        if not hasattr(ed_coordinator, 'active_patients'):
            ed_coordinator.active_patients = {}
        
        ed_coordinator.active_patients[patient_id] = {
            "acuity": str(patient_notification.priority),
            "protocol": request.case_type.lower(),
            "status": "Triaged",
            "arrival_time": datetime.utcnow(),
            "vitals": patient_notification.vitals,
            "chief_complaint": patient_notification.chief_complaint,
            "ems_report": patient_notification.ems_report,
            "lab_eta": patient_data.get("lab_eta", 10),
            "assigned_bed": f"ED-{len(ed_coordinator.active_patients) + 1}"
        }
        
        # Broadcast via WebSocket
        background_tasks.add_task(
            ws_manager.broadcast_patient_arrival,
            {
                "patient_id": patient_id,
                "type": request.case_type,
                "vitals": patient_notification.vitals,
                "status": "Triaged",
                "protocol": request.case_type.lower()
            }
        )
        
        response = SimulationResponse(
            message=f"{request.case_type} simulation triggered successfully",
            patient_id=patient_id,
            case_type=request.case_type,
            timestamp=datetime.utcnow(),
            success=True
        )
        
        logger.info(f"Custom {request.case_type} simulation completed for patient {patient_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error in custom simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Custom simulation failed: {str(e)}")

@router.get("/status", response_model=ApiResponse)
async def get_simulation_status():
    """
    Get simulation system status
    
    Returns:
        ApiResponse: Simulation system status
    """
    try:
        ed_coordinator = get_ed_coordinator()
        
        # Get simulation statistics
        active_simulations = len(ed_coordinator.active_patients) if hasattr(ed_coordinator, 'active_patients') else 0
        
        status_data = {
            "simulation_system": "operational",
            "active_simulations": active_simulations,
            "available_types": ["STEMI", "Stroke", "Trauma", "General", "Pediatric"],
            "last_simulation": datetime.utcnow().isoformat()
        }
        
        return ApiResponse(
            success=True,
            message="Simulation status retrieved successfully",
            data=status_data
        )
        
    except Exception as e:
        logger.error(f"Error retrieving simulation status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve simulation status: {str(e)}")