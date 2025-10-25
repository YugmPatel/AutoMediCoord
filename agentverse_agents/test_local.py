"""
Local Test Script for ED Coordinator Agent
Test before deploying to Agentverse
"""

from uagents import Agent, Context
from protocols import QuerySystemStatus, SystemStatusResponse
from datetime import datetime
import asyncio

# Test agent that simulates ASI-1
test_agent = Agent(
    name="test_asi1",
    seed="test_asi1_seed_12345",
    port=9000
)

# ED Coordinator address (will be set after first run)
ED_COORDINATOR_ADDRESS = None

@test_agent.on_event("startup")
async def startup(ctx: Context):
    """Print test agent info on startup"""
    ctx.logger.info(f"🧪 Test Agent Started")
    ctx.logger.info(f"📍 Test Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"")
    ctx.logger.info(f"⚠️  INSTRUCTIONS:")
    ctx.logger.info(f"1. Run ED Coordinator in another terminal:")
    ctx.logger.info(f"   python ed_coordinator.py")
    ctx.logger.info(f"2. Copy the ED Coordinator address from its startup log")
    ctx.logger.info(f"3. Paste it in this file as ED_COORDINATOR_ADDRESS")
    ctx.logger.info(f"4. Restart this test agent")
    ctx.logger.info(f"")


@test_agent.on_interval(period=15.0)
async def send_test_query(ctx: Context):
    """Send test queries to ED Coordinator every 15 seconds"""
    
    if not ED_COORDINATOR_ADDRESS:
        ctx.logger.warning("⚠️  ED_COORDINATOR_ADDRESS not set. Please update test_local.py")
        return
    
    ctx.logger.info(f"")
    ctx.logger.info(f"📨 Sending System Status Query to ED Coordinator...")
    
    query = QuerySystemStatus(
        query_id=f"test-{datetime.utcnow().timestamp()}",
        requested_by=ctx.agent.address
    )
    
    try:
        await ctx.send(ED_COORDINATOR_ADDRESS, query)
        ctx.logger.info(f"✅ Query sent successfully")
    except Exception as e:
        ctx.logger.error(f"❌ Error sending query: {e}")


@test_agent.on_message(model=SystemStatusResponse)
async def handle_response(ctx: Context, sender: str, msg: SystemStatusResponse):
    """Handle response from ED Coordinator"""
    ctx.logger.info(f"")
    ctx.logger.info(f"✅ RESPONSE RECEIVED from ED Coordinator:")
    ctx.logger.info(f"   Query ID: {msg.query_id}")
    ctx.logger.info(f"   Active Cases: {msg.active_cases}")
    ctx.logger.info(f"   Available Beds: {msg.available_beds}")
    ctx.logger.info(f"   Staff on Duty: {msg.staff_on_duty}")
    ctx.logger.info(f"   System Load: {msg.system_load}")
    ctx.logger.info(f"   Active Protocols: {msg.active_protocols}")
    ctx.logger.info(f"   Timestamp: {msg.timestamp}")
    ctx.logger.info(f"")


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 ED COORDINATOR - LOCAL TEST")
    print("=" * 70)
    print("")
    print("This script tests the ED Coordinator agent locally before")
    print("deploying to Agentverse.")
    print("")
    print("STEPS:")
    print("1. Open two terminals")
    print("2. Terminal 1: python ed_coordinator.py")
    print("3. Terminal 2: python test_local.py")
    print("4. Copy ED Coordinator address and update ED_COORDINATOR_ADDRESS")
    print("")
    print("=" * 70)
    print("")
    
    test_agent.run()