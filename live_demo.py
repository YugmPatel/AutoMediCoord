"""
AutoMediCoord - LIVE Demo with Real Agentverse Agents
Sends actual messages to deployed agents and shows real responses
"""

import asyncio
from datetime import datetime
from uagents import Agent, Context
from src.models import PatientArrivalNotification
from src.utils import get_config

config = get_config()

# Your deployed agent addresses (update these with your actual addresses!)
AGENT_ADDRESSES = {
    "ed_coordinator": "agent1qvdyt84sumpq2g9d5cfekt7v4uwcfv93gx24n8lulr8g7xfp3hwasv93dne",
    "resource_manager": "agent1q200nyuurr9ft547p25tchcfw7twrx5sdrt5kj8l3zcs584zg7yw5uptxt4",
    "specialist_coordinator": "agent1qgg5d4nft907tu7mj0fkj59czjmzsce3576gd0arfz7fllcxqypnv55x20w",
    "lab_service": "agent1qf0ymt6hkyy9vek7yrqshzmuaa6fkt06c6a96ttmlhrunacwdpgzgxz2hxx",
    # Add pharmacy and bed_management if you deployed them
}


async def run_live_stemi_demo():
    """
    Send REAL patient to REAL agents on Agentverse
    Shows live agent communication and responses
    """
    
    print("=" * 70)
    print("AutoMediCoord - LIVE AGENT DEMO")
    print("=" * 70)
    print("\n🔴 LIVE MODE: Sending real messages to Agentverse agents")
    print("=" * 70)
    
    # Create a demo client agent to send messages
    demo_client = Agent(
        name="demo_client",
        seed="demo_client_seed_12345",
        mailbox=True
    )
    
    print(f"\n📱 Demo Client Address: {demo_client.address}")
    print(f"🎯 Target: ED Coordinator at {AGENT_ADDRESSES['ed_coordinator'][:20]}...")
    
    # Create real patient data
    patient = PatientArrivalNotification(
        patient_id=f"LIVE_STEMI_{int(datetime.utcnow().timestamp())}",
        arrival_time=datetime.utcnow(),
        vitals={
            "blood_pressure_systolic": 145,
            "blood_pressure_diastolic": 90,
            "heart_rate": 95,
            "respiratory_rate": 18,
            "oxygen_saturation": 96,
            "temperature": 98.6
        },
        chief_complaint="Severe crushing chest pain radiating to left arm and jaw",
        ems_report="76yo M with acute onset chest pain 45 min ago. ECG shows ST elevation in V2-V4. Aspirin given.",
        estimated_arrival_minutes=5,
        priority=1,
        demographics={
            "age": 76,
            "gender": "M",
            "medical_history": {"hypertension": True}
        }
    )
    
    print("\n" + "=" * 70)
    print("📞 SENDING PATIENT TO ED COORDINATOR")
    print("=" * 70)
    print(f"\nPatient ID: {patient.patient_id}")
    print(f"Chief Complaint: {patient.chief_complaint}")
    print(f"Vitals: HR {patient.vitals['heart_rate']}, BP {patient.vitals['blood_pressure_systolic']}/{patient.vitals['blood_pressure_diastolic']}")
    print(f"Priority: ESI Level {patient.priority}")
    print(f"\n⏳ Sending to ED Coordinator...")
    
    message_sent = False
    
    @demo_client.on_event("startup")
    async def send_patient(ctx: Context):
        nonlocal message_sent
        if not message_sent:
            print(f"📤 Sending PatientArrivalNotification...")
            await ctx.send(AGENT_ADDRESSES["ed_coordinator"], patient)
            message_sent = True
            print(f"✅ Message sent to ED Coordinator!")
            print(f"\n💬 Check Agentverse dashboard to see:")
            print(f"   1. Go to https://agentverse.ai")
            print(f"   2. Click your ed_coordinator agent")
            print(f"   3. Go to 'Logs' tab")
            print(f"   4. See the patient arrival being processed!")
            print(f"\n🧠 ED Coordinator will:")
            print(f"   - Analyze patient with Claude AI")
            print(f"   - Identify STEMI protocol")
            print(f"   - Send messages to other 4 agents")
            print(f"   - Coordinate response")
            
            # Give time for processing
            await asyncio.sleep(5)
            print(f"\n✅ Demo complete! Check agent logs on Agentverse.")
    
    print(f"\n🚀 Starting demo client...")
    print(f"\n⏰ Demo will run for 10 seconds then exit...")
    
    # Schedule shutdown
    async def shutdown_after_delay(ctx: Context):
        await asyncio.sleep(10)
        print(f"\n✅ Demo complete! Check Agentverse logs to see agent activity.")
        ctx.agent.stop()
    
    @demo_client.on_event("startup")
    async def schedule_shutdown(ctx: Context):
        asyncio.create_task(shutdown_after_delay(ctx))
    
    demo_client.run()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AutoMediCoord - Live Agent Communication Demo")
    print("=" * 70)
    print("\n⚠️  REQUIREMENTS:")
    print("   1. Your 4 agents must be running on Agentverse")
    print("   2. Have Agentverse dashboard open in browser")
    print("   3. Ready to check logs in real-time")
    print("\n🎬 This will send a REAL patient to your REAL agents!")
    print("=" * 70)
    
    input("\nPress Enter to start live demo...")
    
    try:
        run_live_stemi_demo()
    except KeyboardInterrupt:
        print("\n\nDemo stopped.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure your agents are running on Agentverse!")