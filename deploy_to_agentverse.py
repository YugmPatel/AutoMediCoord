"""
Deploy EDFlow AI agents to Agentverse
"""

import os
from dotenv import load_dotenv
from uagents import Identity
from uagents.registration import register_with_agentverse

load_dotenv()


def deploy_agent(agent_name: str, seed: str, port: int, readme: str):
    """
    Deploy a single agent to Agentverse
    
    Args:
        agent_name: Name of the agent
        seed: Agent seed phrase
        port: Local port
        readme: Agent README content
    """
    print(f"\nDeploying {agent_name}...")
    
    # Get API key
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print(f"❌ AGENTVERSE_API_KEY not set in .env")
        return False
    
    try:
        # Create identity from seed
        identity = Identity.from_seed(seed, 0)
        
        # Register with Agentverse
        register_with_agentverse(
            identity=identity,
            url=f"http://localhost:{port}/webhook",
            agentverse_token=api_key,
            agent_title=agent_name.replace("_", " ").title(),
            readme=readme
        )
        
        print(f"✅ {agent_name} registered successfully")
        print(f"   Address: {identity.address}")
        return True
        
    except Exception as e:
        print(f"❌ Error deploying {agent_name}: {str(e)}")
        return False


def deploy_all_agents():
    """Deploy all 6 EDFlow AI agents to Agentverse"""
    
    print("=" * 60)
    print("EDFlow AI - Agentverse Deployment")
    print("=" * 60)
    
    agents = [
        {
            "name": "ed_coordinator",
            "seed": os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_seed"),
            "port": int(os.getenv("ED_COORDINATOR_PORT", "8000")),
            "readme": """
# ED Coordinator Agent

Central orchestrator for Emergency Department operations.

**Features:**
- Patient arrival processing
- AI-powered triage using Claude
- Protocol activation (STEMI, Stroke, Trauma, Pediatric)
- Coordination with all ED agents

**Chat Protocol:** Enabled
**AI Integration:** Claude 3.5 Sonnet
            """
        },
        {
            "name": "resource_manager",
            "seed": os.getenv("RESOURCE_MANAGER_SEED", "resource_manager_seed"),
            "port": int(os.getenv("RESOURCE_MANAGER_PORT", "8001")),
            "readme": """
# Resource Manager Agent

Manages all ED resources in real-time.

**Features:**
- Bed availability tracking
- Equipment allocation
- Resource conflict detection
- Utilization optimization

**Chat Protocol:** Enabled
**Performance:** <500ms allocation response
            """
        },
        {
            "name": "specialist_coordinator",
            "seed": os.getenv("SPECIALIST_COORDINATOR_SEED", "specialist_coordinator_seed"),
            "port": int(os.getenv("SPECIALIST_COORDINATOR_PORT", "8002")),
            "readme": """
# Specialist Coordinator Agent

Coordinates emergency specialist teams.

**Features:**
- Team activation (STEMI, Stroke, Trauma, Pediatric)
- Specialist notification
- Response time tracking
- Escalation handling

**Chat Protocol:** Enabled
**Teams:** 4 emergency response teams
            """
        },
        {
            "name": "lab_service",
            "seed": os.getenv("LAB_SERVICE_SEED", "lab_service_seed"),
            "port": int(os.getenv("LAB_SERVICE_PORT", "8003")),
            "readme": """
# Lab Service Agent

Manages laboratory test ordering and results.

**Features:**
- Test ordering with priority routing
- Real-time result management
- Critical value alerts
- Capacity tracking

**Chat Protocol:** Enabled
**Priority Levels:** Stat, ASAP, Urgent, Routine
            """
        },
        {
            "name": "pharmacy",
            "seed": os.getenv("PHARMACY_SEED", "pharmacy_seed"),
            "port": int(os.getenv("PHARMACY_PORT", "8004")),
            "readme": """
# Pharmacy Agent

Manages medication orders and delivery.

**Features:**
- Medication order processing
- Delivery status tracking
- Priority handling
- Stock management

**Chat Protocol:** Enabled
**Delivery Tracking:** Real-time updates
            """
        },
        {
            "name": "bed_management",
            "seed": os.getenv("BED_MANAGEMENT_SEED", "bed_management_seed"),
            "port": int(os.getenv("BED_MANAGEMENT_PORT", "8005")),
            "readme": """
# Bed Management Agent

Optimizes bed assignments and turnover.

**Features:**
- Real-time bed status tracking
- Intelligent bed assignment
- Turnover coordination
- Overflow management

**Chat Protocol:** Enabled
**Target:** 30% improved bed turnover
            """
        }
    ]
    
    print("\nDeploying 6 EDFlow AI agents...")
    print("-" * 60)
    
    successful = 0
    failed = 0
    
    for agent in agents:
        if deploy_agent(agent["name"], agent["seed"], agent["port"], agent["readme"]):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Deployment Complete: {successful} successful, {failed} failed")
    print("=" * 60)
    
    if successful == 6:
        print("\n✅ All agents deployed successfully!")
        print("\nNext steps:")
        print("1. Go to https://agentverse.ai")
        print("2. Check 'My Agents' to see all 6 agents")
        print("3. Test communication between agents")
        print("4. Enable chat protocol if not already enabled")
    else:
        print("\n⚠️  Some agents failed to deploy")
        print("Check the errors above and retry")


if __name__ == "__main__":
    deploy_all_agents()