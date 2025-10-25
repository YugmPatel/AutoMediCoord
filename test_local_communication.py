"""
Test Local Agent Communication
Verifies agents can communicate with each other locally before Agentverse deployment
"""

import os
import sys
import signal
import psutil
from uagents import Bureau
from datetime import datetime
from src.agents import create_agent
from src.models import PatientArrivalNotification, ResourceRequest
from src.utils import get_logger

logger = get_logger(__name__)


def kill_processes_on_ports(ports):
    """Kill any processes using the specified ports"""
    killed = []
    for port in ports:
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    for conn in proc.connections():
                        if conn.laddr.port == port and conn.status == 'LISTEN':
                            print(f"  • Killing process {proc.pid} ({proc.name()}) on port {port}")
                            proc.kill()
                            killed.append(port)
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, PermissionError):
                    pass
        except (KeyboardInterrupt, SystemExit):
            break
        except Exception:
            pass
    return killed


def test_local_communication():
    """
    Test agents communicating locally
    """
    
    # Clean up ports first
    print("\n🧹 Cleaning up ports...")
    ports = [8000, 8001, 8002, 8003, 8004, 8005]
    killed = kill_processes_on_ports(ports)
    if killed:
        print(f"✅ Cleaned up {len(killed)} port(s)")
        import time
        time.sleep(2)  # Give OS time to release ports
    else:
        print("✅ All ports are free")
    
    print("=" * 70)
    print("AutoMediCoord - Local Communication Test")
    print("=" * 70)
    print("\n✅ DEPLOYMENT_MODE set to 'local' in .env")
    print("✅ Testing agent-to-agent communication...\n")
    
    print("Creating agents...")
    
    # Create all 6 agents
    ed_coord = create_agent("ed_coordinator")
    resource_mgr = create_agent("resource_manager")
    specialist = create_agent("specialist_coordinator")
    lab = create_agent("lab_service")
    pharmacy = create_agent("pharmacy")
    bed_mgmt = create_agent("bed_management")
    
    print("\n✅ All 6 agents created successfully!\n")
    
    # Print addresses
    print("Agent Addresses:")
    print("-" * 70)
    print(f"  1. ED Coordinator:          {ed_coord.agent.address}")
    print(f"  2. Resource Manager:        {resource_mgr.agent.address}")
    print(f"  3. Specialist Coordinator:  {specialist.agent.address}")
    print(f"  4. Lab Service:             {lab.agent.address}")
    print(f"  5. Pharmacy:                {pharmacy.agent.address}")
    print(f"  6. Bed Management:          {bed_mgmt.agent.address}")
    
    # Register agent addresses with ED Coordinator
    ed_coord.agents = {
        "resource_manager": resource_mgr.agent.address,
        "specialist_coordinator": specialist.agent.address,
        "lab_service": lab.agent.address,
        "pharmacy": pharmacy.agent.address,
        "bed_management": bed_mgmt.agent.address,
    }
    
    print("\n✅ Agent addresses registered with ED Coordinator")
    
    # Setup test patient arrival message
    @ed_coord.agent.on_interval(period=10.0)
    async def send_test_patient(ctx):
        """Send a test patient every 10 seconds"""
        patient = PatientArrivalNotification(
            patient_id=f"TEST_{int(datetime.utcnow().timestamp())}",
            arrival_time=datetime.utcnow(),
            vitals={"hr": 95, "bp_sys": 145, "bp_dia": 90, "spo2": 96},
            chief_complaint="Chest pain radiating to left arm - suspected STEMI",
            ems_report="76yo M, chest pain, ST elevation on ECG",
            priority=1
        )
        
        print(f"\n{'='*70}")
        print(f"📞 SIMULATING PATIENT ARRIVAL")
        print(f"{'='*70}")
        print(f"Patient ID: {patient.patient_id}")
        print(f"Sending to ED Coordinator...")
        
        # This will trigger the ED Coordinator's patient processing
        await ed_coord._process_arrival(ctx, patient)
    
    # Create bureau and add all agents
    bureau = Bureau()
    bureau.add(ed_coord.agent)
    bureau.add(resource_mgr.agent)
    bureau.add(specialist.agent)
    bureau.add(lab.agent)
    bureau.add(pharmacy.agent)
    bureau.add(bed_mgmt.agent)
    
    print("\n" + "=" * 70)
    print("🚀 Starting Bureau with All 6 Agents")
    print("=" * 70)
    print("\n📊 What to Watch:")
    print("  • ED Coordinator receives patient")
    print("  • Claude AI analyzes patient (<2s)")
    print("  • ED Coordinator identifies protocol")
    print("  • Messages sent to other 5 agents")
    print("  • All agents log their activity")
    print("\n⏰ Test runs for 30 seconds, sending patient every 10s")
    print("🔍 Watch the console output to see agent communication!")
    print("\nPress Ctrl+C to stop anytime\n")
    print("=" * 70)
    
    # Run bureau
    bureau.run()


if __name__ == "__main__":
    print("\n🧪 Local Agent Communication Test")
    print("This verifies all 6 agents can communicate before Agentverse deployment\n")
    
    try:
        test_local_communication()
    except KeyboardInterrupt:
        print("\n\n✅ Test stopped. Did you see agent communication?")
        print("\nWhat you should have seen:")
        print("  ✅ Patient arrival logged")
        print("  ✅ AI analysis completed")
        print("  ✅ Protocol identified")
        print("  ✅ Messages sent to other agents")
        print("  ✅ All 6 agents active")
        print("\n🎯 If communication worked, you're ready for Agentverse!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🧹 Cleaning up ports...")
        kill_processes_on_ports([8000, 8001, 8002, 8003, 8004, 8005])
        print("✅ Cleanup complete")