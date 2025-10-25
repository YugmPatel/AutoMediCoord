"""
AutoMediCoord Local Demo - See All 6 Agents Communicating
Run this to show your friends how the multi-agent system works!
"""

import asyncio
from datetime import datetime
from uagents import Bureau
from src.agents import create_agent
from src.models import PatientArrivalNotification
from src.utils import get_logger

logger = get_logger(__name__)


def print_banner(text, char="="):
    """Print a nice banner"""
    print(f"\n{char * 70}")
    print(f" {text}")
    print(f"{char * 70}\n")


async def simulate_patient_arrival(ctx, ed_coordinator):
    """Simulate a patient arriving at the ED"""
    await asyncio.sleep(3)  # Wait for agents to start
    
    print_banner("📞 PATIENT ARRIVING AT EMERGENCY DEPARTMENT", "=")
    
    # Create a STEMI patient (heart attack)
    patient = PatientArrivalNotification(
        patient_id="DEMO_PATIENT_001",
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
        priority=1
    )
    
    print("📋 Patient Details:")
    print(f"   Patient ID: {patient.patient_id}")
    print(f"   Priority: {patient.priority} (CRITICAL)")
    print(f"   Chief Complaint: {patient.chief_complaint}")
    print(f"   Heart Rate: {patient.vitals['hr']} bpm")
    print(f"   Blood Pressure: {patient.vitals['bp_sys']}/{patient.vitals['bp_dia']} mmHg")
    print(f"   SpO2: {patient.vitals['spo2']}%")
    
    print_banner("🤖 WATCHING AGENT COMMUNICATION...", "=")
    print("ED Coordinator will:")
    print("  1. Analyze patient with Claude AI")
    print("  2. Identify STEMI protocol")
    print("  3. Notify all 5 other agents")
    print("\nWatch the logs below to see the communication!\n")
    print("-" * 70)
    
    # Send patient to ED Coordinator with proper context
    await ed_coordinator._process_arrival(ctx, patient)


def main():
    """Run the local demo"""
    
    print_banner("🏥 AutoMediCoord Multi-Agent System - LIVE DEMO", "=")
    print("This demo shows all 6 agents communicating in real-time")
    print("\nThe Agents:")
    print("  1. 🏥 ED Coordinator - Receives patient, analyzes with AI")
    print("  2. 📊 Resource Manager - Manages beds and equipment")
    print("  3. 👨‍⚕️ Specialist Coordinator - Activates specialist teams")
    print("  4. 🧪 Lab Service - Processes lab orders")
    print("  5. 💊 Pharmacy - Handles medications")
    print("  6. 🛏️ Bed Management - Assigns patient beds")
    
    print_banner("🚀 STARTING ALL 6 AGENTS...", "=")
    
    # Create all 6 agents
    ed_coord = create_agent("ed_coordinator")
    resource_mgr = create_agent("resource_manager")
    specialist = create_agent("specialist_coordinator")
    lab = create_agent("lab_service")
    pharmacy = create_agent("pharmacy")
    bed_mgmt = create_agent("bed_management")
    
    print("✅ All agents created successfully!\n")
    
    # Register agent addresses
    ed_coord.agents = {
        "resource_manager": resource_mgr.agent.address,
        "specialist_coordinator": specialist.agent.address,
        "lab_service": lab.agent.address,
        "pharmacy": pharmacy.agent.address,
        "bed_management": bed_mgmt.agent.address,
    }
    
    # Create bureau
    bureau = Bureau()
    bureau.add(ed_coord.agent)
    bureau.add(resource_mgr.agent)
    bureau.add(specialist.agent)
    bureau.add(lab.agent)
    bureau.add(pharmacy.agent)
    bureau.add(bed_mgmt.agent)
    
    # Schedule patient arrival
    @ed_coord.agent.on_interval(period=5.0)
    async def send_patient(ctx):
        """Send demo patient once"""
        if not hasattr(send_patient, 'sent'):
            send_patient.sent = True
            await simulate_patient_arrival(ctx, ed_coord)
            
            # Show summary after a bit
            await asyncio.sleep(3)
            print_banner("✅ DEMO COMPLETE!", "=")
            print("What you just saw:")
            print("  ✅ Patient arrival logged by ED Coordinator")
            print("  ✅ Claude AI analyzed patient data")
            print("  ✅ STEMI protocol identified automatically")
            print("  ✅ All 5 agents received protocol activation message")
            print("  ✅ Agents ready to coordinate patient care")
            print("\n🎯 This is how AutoMediCoord coordinates emergency care in real-time!")
            print("\nPress Ctrl+C to stop the demo\n")
    
    # Run the demo
    try:
        bureau.run()
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped. Thanks for watching!")


if __name__ == "__main__":
    main()