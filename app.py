"""
EDFlow AI Agents - Agentverse Deployment via Render
All 6 agents running with mailbox enabled for Agentverse integration
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from uagents import Bureau
from src.agents import create_agent
from src.utils import get_logger, get_config

# Load environment variables
load_dotenv()

logger = get_logger(__name__)
config = get_config()

def main():
    """Deploy all 6 EDFlow AI agents to Agentverse via Render"""
    
    logger.info("=" * 70)
    logger.info("EDFlow AI - Agentverse Deployment")
    logger.info("=" * 70)
    
    # Verify Agentverse mode
    if not config.is_agentverse_mode():
        logger.error("❌ DEPLOYMENT_MODE must be set to 'agentverse' in .env")
        logger.error("Please update your .env file:")
        logger.error("DEPLOYMENT_MODE=agentverse")
        return
    
    logger.info("✅ Running in AGENTVERSE mode")
    logger.info("Creating all 6 agents with mailbox enabled...")
    
    # Create all 6 agents
    try:
        ed_coord = create_agent("ed_coordinator")
        resource_mgr = create_agent("resource_manager")
        specialist = create_agent("specialist_coordinator")
        lab = create_agent("lab_service")
        pharmacy = create_agent("pharmacy")
        bed_mgmt = create_agent("bed_management")
        
        logger.info("✅ All 6 agents created successfully!")
        
        # Print agent addresses
        logger.info("-" * 70)
        logger.info("Agent Addresses (Register these in Agentverse):")
        logger.info(f"  1. ED Coordinator:          {ed_coord.agent.address}")
        logger.info(f"  2. Resource Manager:        {resource_mgr.agent.address}")
        logger.info(f"  3. Specialist Coordinator:  {specialist.agent.address}")
        logger.info(f"  4. Lab Service:             {lab.agent.address}")
        logger.info(f"  5. Pharmacy:                {pharmacy.agent.address}")
        logger.info(f"  6. Bed Management:          {bed_mgmt.agent.address}")
        logger.info("-" * 70)
        
        # Register agent addresses with ED Coordinator
        ed_coord.agents = {
            "resource_manager": resource_mgr.agent.address,
            "specialist_coordinator": specialist.agent.address,
            "lab_service": lab.agent.address,
            "pharmacy": pharmacy.agent.address,
            "bed_management": bed_mgmt.agent.address,
        }
        
        logger.info("✅ Agent addresses registered with ED Coordinator")
        
        # Create bureau and add all agents
        bureau = Bureau()
        bureau.add(ed_coord.agent)
        bureau.add(resource_mgr.agent)
        bureau.add(specialist.agent)
        bureau.add(lab.agent)
        bureau.add(pharmacy.agent)
        bureau.add(bed_mgmt.agent)
        
        logger.info("=" * 70)
        logger.info("🚀 Starting Bureau - All Agents Running")
        logger.info("=" * 70)
        logger.info("")
        logger.info("📋 Next Steps:")
        logger.info("  1. Check logs for Agent Inspector links")
        logger.info("  2. Open each link to register agents with Agentverse")
        logger.info("  3. Update agent profiles in Agentverse dashboard")
        logger.info("  4. Test agent communication via Agentverse chat")
        logger.info("")
        logger.info("🎯 EDFlow AI Multi-Agent System Ready!")
        logger.info("=" * 70)
        
        # Run bureau (this will block)
        bureau.run()
        
    except Exception as e:
        logger.error(f"❌ Error starting agents: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()