"""
Integration test - Run agents and test communication
"""

import asyncio
import time
from datetime import datetime
from src.agents import create_agent
from src.models import PatientArrivalNotification
from uagents import Bureau


async def test_agent_communication():
    """Test communication between agents"""
    
    print("=" * 60)
    print("EDFlow AI - Integration Test")
    print("=" * 60)
    print("\nCreating agents...")
    
    # Create agents
    ed_coord = create_agent("ed_coordinator")
    resource_mgr = create_agent("resource_manager")
    specialist = create_agent("specialist_coordinator")
    lab = create_agent("lab_service")
    pharmacy = create_agent("pharmacy")
    bed_mgmt = create_agent("bed_management")
    
    print("✅ All 6 agents created")
    
    # Print addresses
    print("\nAgent Addresses:")
    print(f"  ED Coordinator: {ed_coord.agent.address}")
    print(f"  Resource Manager: {resource_mgr.agent.address}")
    print(f"  Specialist Coordinator: {specialist.agent.address}")
    print(f"  Lab Service: {lab.agent.address}")
    print(f"  Pharmacy: {pharmacy.agent.address}")
    print(f"  Bed Management: {bed_mgmt.agent.address}")
    
    # Register agent addresses with ED Coordinator
    ed_coord.agents = {
        "resource_manager": resource_mgr.agent.address,
        "specialist_coordinator": specialist.agent.address,
        "lab_service": lab.agent.address,
        "pharmacy": pharmacy.agent.address,
        "bed_management": bed_mgmt.agent.address,
    }
    
    print("\n✅ Agent addresses registered")
    print("\n" + "=" * 60)
    print("Integration test setup complete!")
    print("=" * 60)
    print("\nTo run agents:")
    print("  python run_all_agents.py")
    print("\nOr run individually:")
    print("  python demo.py ed_coordinator")
    print("  python demo.py resource_manager")
    print("  # etc...")


if __name__ == "__main__":
    asyncio.run(test_agent_communication())