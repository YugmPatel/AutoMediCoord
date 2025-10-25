"""
AutoMediCoord - Simple Demo
Run individual agents or test the system
"""

import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.agents import create_agent
from src.models import PatientArrivalNotification


def run_agent(agent_type: str):
    """Run a single agent"""
    print(f"Starting {agent_type} agent...")
    agent = create_agent(agent_type)
    agent.run()


def print_usage():
    """Print usage instructions"""
    print("""
AutoMediCoord - Emergency Department Flow Optimizer

Usage:
    python demo.py <agent_type>

Available agents:
    ed_coordinator          - Central ED orchestrator
    resource_manager        - Resource allocation
    specialist_coordinator  - Team coordination
    lab_service            - Laboratory services
    pharmacy               - Medication management
    bed_management         - Bed assignments

Example:
    python demo.py ed_coordinator

To run all agents, open 6 separate terminals and run each agent.

For Agentverse deployment:
    1. Set DEPLOYMENT_MODE=agentverse in .env
    2. Run agents - they will use mailbox
    3. Connect via Agent Inspector link in logs
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    agent_type = sys.argv[1].lower()
    
    valid_agents = [
        "ed_coordinator",
        "resource_manager",
        "specialist_coordinator",
        "lab_service",
        "pharmacy",
        "bed_management"
    ]
    
    if agent_type not in valid_agents:
        print(f"Error: Unknown agent type '{agent_type}'")
        print_usage()
        sys.exit(1)
    
    run_agent(agent_type)