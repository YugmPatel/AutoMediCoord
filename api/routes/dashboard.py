"""
Dashboard API Routes
Endpoints for dashboard metrics, cases, and activity data
"""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from ..models.api_models import (
    DashboardMetrics, PatientCase, ActivityEntry, ApiResponse,
    FilterParams, PaginationParams
)
from src.utils import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Dependency to get agents (will be imported from main)
def get_ed_coordinator():
    from api.main import get_ed_coordinator
    return get_ed_coordinator()

def get_all_agents():
    from api.main import get_all_agents
    return get_all_agents()

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics():
    """
    Get current ED dashboard metrics
    
    Returns:
        DashboardMetrics: Current metrics including active cases, lab ETA, etc.
    """
    try:
        ed_coordinator = get_ed_coordinator()
        all_agents = get_all_agents()
        
        # Get active cases count from ED Coordinator
        active_cases = len(ed_coordinator.active_patients) if hasattr(ed_coordinator, 'active_patients') else 0
        
        # Calculate average lab ETA from lab service agent
        lab_agent = all_agents.get("lab_service")
        avg_lab_eta = 9  # Default value, can be calculated from lab agent data
        
        # Get ICU beds held from resource manager
        resource_manager = all_agents.get("resource_manager")
        icu_beds_held = 2  # Default value, can be calculated from resource manager
        
        # Get doctors paged from specialist coordinator
        specialist_coordinator = all_agents.get("specialist_coordinator")
        doctors_paged = 2  # Default value, can be calculated from specialist coordinator
        
        metrics = DashboardMetrics(
            active_cases=active_cases,
            avg_lab_eta=avg_lab_eta,
            icu_beds_held=icu_beds_held,
            doctors_paged=doctors_paged,
            last_updated=datetime.utcnow()
        )
        
        logger.info(f"Dashboard metrics retrieved: {active_cases} active cases")
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")

@router.get("/cases", response_model=List[PatientCase])
async def get_active_cases(
    filters: FilterParams = Depends(),
    pagination: PaginationParams = Depends()
):
    """
    Get all active patient cases
    
    Args:
        filters: Filter parameters for cases
        pagination: Pagination parameters
        
    Returns:
        List[PatientCase]: List of active patient cases
    """
    try:
        ed_coordinator = get_ed_coordinator()
        
        cases = []
        
        # Get cases from ED Coordinator
        if hasattr(ed_coordinator, 'active_patients'):
            for patient_id, patient_data in ed_coordinator.active_patients.items():
                # Calculate duration since arrival
                arrival_time = patient_data.get('arrival_time', datetime.utcnow())
                if isinstance(arrival_time, str):
                    arrival_time = datetime.fromisoformat(arrival_time.replace('Z', '+00:00'))
                duration = int((datetime.utcnow() - arrival_time).total_seconds() / 60)
                
                # Create case object
                case = PatientCase(
                    id=patient_id,
                    type=patient_data.get("protocol", "General").upper(),
                    duration=max(duration, 1),  # Ensure at least 1 minute
                    vitals={
                        "hr": patient_data.get("vitals", {}).get("hr", 80),
                        "bp_sys": patient_data.get("vitals", {}).get("bp_sys", 120),
                        "bp_dia": patient_data.get("vitals", {}).get("bp_dia", 80),
                        "spo2": patient_data.get("vitals", {}).get("spo2", 98),
                        "temp": patient_data.get("vitals", {}).get("temp", 37.0)
                    },
                    status=patient_data.get("status", "Pending"),
                    location=f"ED-{len(cases) + 1}",
                    lab_eta=patient_data.get("lab_eta", 10),
                    assigned_bed=patient_data.get("assigned_bed", f"Bed-{len(cases) + 1}"),
                    priority=1 if patient_data.get("acuity") == "1" else 3,
                    timestamp=arrival_time,
                    chief_complaint=patient_data.get("chief_complaint", ""),
                    ems_report=patient_data.get("ems_report", "")
                )
                cases.append(case)
        
        # Apply filters
        if filters.case_type:
            cases = [case for case in cases if case.type == filters.case_type]
        if filters.status:
            cases = [case for case in cases if case.status == filters.status]
        if filters.priority:
            cases = [case for case in cases if case.priority == filters.priority]
        
        # Apply pagination
        start_idx = (pagination.page - 1) * pagination.limit
        end_idx = start_idx + pagination.limit
        cases = cases[start_idx:end_idx]
        
        logger.info(f"Retrieved {len(cases)} active cases")
        return cases
        
    except Exception as e:
        logger.error(f"Error retrieving active cases: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve cases: {str(e)}")

@router.get("/activity", response_model=List[ActivityEntry])
async def get_recent_activity(
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    limit: int = Query(20, description="Maximum number of entries", ge=1, le=100)
):
    """
    Get recent activity log entries
    
    Args:
        activity_type: Optional filter by activity type (Lab, Pharm, System, etc.)
        limit: Maximum number of entries to return
        
    Returns:
        List[ActivityEntry]: List of recent activity entries
    """
    try:
        all_agents = get_all_agents()
        
        # Generate activity entries based on agent states
        activities = []
        
        # Lab activities
        lab_agent = all_agents.get("lab_service")
        if lab_agent:
            activities.append(ActivityEntry(
                id="lab_1",
                timestamp=datetime.utcnow() - timedelta(minutes=2),
                type="Lab",
                message="Lab ETA 12m",
                status="Pending",
                agent_name="Lab Service"
            ))
        
        # Pharmacy activities
        pharmacy_agent = all_agents.get("pharmacy")
        if pharmacy_agent:
            activities.append(ActivityEntry(
                id="pharm_1",
                timestamp=datetime.utcnow() - timedelta(minutes=3),
                type="Pharm",
                message="STEMI kit ready",
                status="Ready",
                agent_name="Pharmacy"
            ))
        
        # Bed management activities
        bed_agent = all_agents.get("bed_management")
        if bed_agent:
            activities.append(ActivityEntry(
                id="bed_1",
                timestamp=datetime.utcnow() - timedelta(minutes=4),
                type="Bed",
                message="ICU-3 held",
                status="Pending",
                agent_name="Bed Management"
            ))
        
        # Doctor activities
        specialist_agent = all_agents.get("specialist_coordinator")
        if specialist_agent:
            activities.extend([
                ActivityEntry(
                    id="doctor_1",
                    timestamp=datetime.utcnow() - timedelta(minutes=5),
                    type="Doctor",
                    message="Dr. Lee paged",
                    status="Complete",
                    agent_name="Specialist Coordinator"
                ),
                ActivityEntry(
                    id="doctor_2",
                    timestamp=datetime.utcnow() - timedelta(minutes=6),
                    type="Doctor",
                    message="Dr. Patel paged",
                    status="Complete",
                    agent_name="Specialist Coordinator"
                )
            ])
        
        # System activities
        activities.extend([
            ActivityEntry(
                id="system_1",
                timestamp=datetime.utcnow() - timedelta(minutes=1),
                type="System",
                message="STEMI kit ready",
                status="Ready"
            ),
            ActivityEntry(
                id="system_2",
                timestamp=datetime.utcnow() - timedelta(seconds=30),
                type="System",
                message="ED-Bed2 assigned",
                status="Complete"
            )
        ])
        
        # Filter by activity type if specified
        if activity_type:
            activities = [a for a in activities if a.type.lower() == activity_type.lower()]
        
        # Sort by timestamp (most recent first)
        activities.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply limit
        activities = activities[:limit]
        
        logger.info(f"Retrieved {len(activities)} activity entries")
        return activities
        
    except Exception as e:
        logger.error(f"Error retrieving activity log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve activity: {str(e)}")

@router.get("/status", response_model=ApiResponse)
async def get_dashboard_status():
    """
    Get overall dashboard status
    
    Returns:
        ApiResponse: Dashboard status information
    """
    try:
        all_agents = get_all_agents()
        ed_coordinator = get_ed_coordinator()
        
        # Count active agents
        active_agents = len([agent for agent in all_agents.values() if agent is not None])
        
        # Get active cases count
        active_cases = len(ed_coordinator.active_patients) if hasattr(ed_coordinator, 'active_patients') else 0
        
        status_data = {
            "agents_active": active_agents,
            "total_agents": 6,
            "active_cases": active_cases,
            "system_status": "operational",
            "last_update": datetime.utcnow().isoformat()
        }
        
        return ApiResponse(
            success=True,
            message="Dashboard status retrieved successfully",
            data=status_data
        )
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve status: {str(e)}")