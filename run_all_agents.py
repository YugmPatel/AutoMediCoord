"""
Run all 6 AutoMediCoord agents simultaneously using Bureau
"""

from uagents import Bureau
from src.agents import (
    EDCoordinatorAgent,
    ResourceManagerAgent,
    SpecialistCoordinatorAgent,
    LabServiceAgent,
    PharmacyAgent,
    BedManagementAgent
)

def main():
    """Run all 6 agents in a single process"""
    print("=" * 60)
    print("AutoMediCoord - Starting All 6 Agents")
    print("=" * 60)
    print("\nInitializing agents...")
    
    # Create all agents
    ed_coordinator = EDCoordinatorAgent()
    resource_manager = ResourceManagerAgent()
    specialist_coordinator = SpecialistCoordinatorAgent()
    lab_service = LabServiceAgent()
    pharmacy = PharmacyAgent()
    bed_management = BedManagementAgent()
    
    print("\n✅ All agents created successfully")
    print("\nAdding agents to bureau...")
    
    # Create bureau and add all agents
    bureau = Bureau()
    bureau.add(ed_coordinator.agent)
    bureau.add(resource_manager.agent)
    bureau.add(specialist_coordinator.agent)
    bureau.add(lab_service.agent)
    bureau.add(pharmacy.agent)
    bureau.add(bed_management.agent)
    
    print("\n✅ Bureau configured with 6 agents")
    print("\n" + "=" * 60)
    print("Starting AutoMediCoord Multi-Agent System")
    print("=" * 60)
    print("\nAgents running... (Ctrl+C to stop)\n")
    
    # Run the bureau
    bureau.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutting down all agents...")
        print("AutoMediCoord stopped.")