"""
Quick test of the visualization system
"""

import asyncio
from datetime import datetime
from src.visualization.event_tracker import EventTracker, AgentEvent, EventType
from src.visualization.terminal_logger import TerminalLogger


def test_terminal_logger():
    """Test the terminal logger display"""
    print("Testing Terminal Logger...")
    
    # Create event tracker and logger
    tracker = EventTracker()
    logger = TerminalLogger(event_tracker=tracker)
    
    # Test banner
    logger.print_banner("🏥 EDFlow AI Test", "cyan")
    
    # Test section
    logger.print_section(
        "Test Agents:",
        ["🏥 ED Coordinator", "📊 Resource Manager", "👨‍⚕️ Specialist"]
    )
    
    # Test patient details
    patient_data = {
        "patient_id": "TEST_001",
        "priority": 1,
        "chief_complaint": "Test complaint",
        "vitals": {
            "hr": 110,
            "bp_sys": 160,
            "bp_dia": 95,
            "spo2": 94
        }
    }
    logger.print_patient_details(patient_data)
    
    # Test protocol info
    logger.print_protocol_info("stemi")
    
    # Add some test events
    tracker.track_event(AgentEvent(
        timestamp=datetime.utcnow(),
        event_type=EventType.AGENT_STARTED,
        agent_name="ed_coordinator",
        description="ED Coordinator started"
    ))
    
    tracker.track_event(AgentEvent(
        timestamp=datetime.utcnow(),
        event_type=EventType.MESSAGE_SENT,
        agent_name="ed_coordinator",
        from_agent="ed_coordinator",
        to_agent="resource_manager",
        message_type="ResourceRequest",
        description="Requesting bed for patient"
    ))
    
    tracker.track_event(AgentEvent(
        timestamp=datetime.utcnow(),
        event_type=EventType.PROTOCOL_ACTIVATED,
        agent_name="ed_coordinator",
        description="STEMI protocol activated",
        protocol="stemi",
        patient_id="TEST_001"
    ))
    
    print("\n✅ Terminal logger test complete!")
    print("✅ All visualization components loaded successfully!")
    print("\n🎯 Ready to run: python demo.py")


if __name__ == "__main__":
    test_terminal_logger()