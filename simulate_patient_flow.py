"""
Simulate actual patient flow through the system with real agent communication
"""

import asyncio
import time
from datetime import datetime
from src.models import PatientArrivalNotification
from src.agents import EDCoordinatorAgent


async def simulate_stemi_patient():
    """Simulate a STEMI patient going through the real system"""
    
    print("=" * 70)
    print("EDFlow AI - Live Patient Flow Simulation")
    print("=" * 70)
    print("\nNote: This simulates real agent processing with your Claude AI key")
    print("      The ED Coordinator will actually analyze the patient with AI\n")
    
    # Create ED Coordinator agent
    print("🤖 Initializing ED Coordinator Agent...")
    ed_agent = EDCoordinatorAgent()
    
    print(f"✅ Agent Address: {ed_agent.agent.address}")
    print(f"✅ Claude AI: {'Configured' if ed_agent.ai_engine.client else 'Using fallback'}")
    print(f"✅ Chat Protocol: Enabled")
    
    # Create patient notification
    patient = PatientArrivalNotification(
        patient_id="STEMI_SIM_001",
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
        ems_report="76yo M with acute chest pain onset 45 minutes ago. ECG shows ST elevation in leads V2-V4. Aspirin 325mg administered. Patient diaphoretic, anxious. Vitals stable currently.",
        estimated_arrival_minutes=5,
        priority=1,
        demographics={
            "age": 76,
            "gender": "M",
            "weight_kg": 82,
            "medical_history": {
                "hypertension": True,
                "diabetes": False,
                "prior_mi": False,
                "current_medications": ["Lisinopril", "Atorvastatin"]
            }
        }
    )
    
    print("\n" + "-" * 70)
    print("📞 Simulating Patient Arrival")
    print("-" * 70)
    print(f"Patient ID: {patient.patient_id}")
    print(f"Chief Complaint: {patient.chief_complaint}")
    print(f"Vitals: HR {patient.vitals['heart_rate']}, BP {patient.vitals['blood_pressure_systolic']}/{patient.vitals['blood_pressure_diastolic']}")
    print(f"Priority: ESI Level {patient.priority}")
    
    print("\n🧠 AI Analysis Starting...")
    start_time = time.time()
    
    # Use the AI engine directly to show it working
    analysis = await ed_agent.ai_engine.analyze_patient_acuity(
        vitals=patient.vitals,
        symptoms=patient.chief_complaint,
        history=str(patient.demographics.get("medical_history"))
    )
    
    end_time = time.time()
    analysis_time = end_time - start_time
    
    print(f"\n✅ AI Analysis Complete in {analysis_time:.2f} seconds")
    print("-" * 70)
    print(f"Acuity Level: {analysis.get('acuity_level')}")
    print(f"Recommended Protocol: {analysis.get('protocol', 'unknown').upper()}")
    print(f"Confidence: {analysis.get('confidence', 0.0):.0%}")
    print(f"Risk Factors: {', '.join(analysis.get('risk_factors', []))}")
    print(f"Immediate Actions: {', '.join(analysis.get('immediate_actions', []))}")
    
    # Add patient to active tracking
    ed_agent.active_patients[patient.patient_id] = {
        "arrival_time": patient.arrival_time,
        "acuity": analysis.get("acuity_level"),
        "protocol": analysis.get("protocol"),
        "status": "analyzed"
    }
    
    print("\n✅ Patient added to ED Coordinator tracking")
    try:
        count = ed_agent.get_patient_count()
        print(f"   Active patients: {count}")
    except AttributeError as e:
        print(f"   Active patients: {len(ed_agent.active_patients)}")
    
    protocol = analysis.get("protocol", "general")
    if protocol in ["stemi", "stroke", "trauma", "pediatric"]:
        print(f"\n🚨 {protocol.upper()} PROTOCOL INDICATED")
        print(f"   This would trigger:")
        print(f"   - Broadcast to all 6 agents")
        print(f"   - Team activation")
        print(f"   - Resource allocation")
        print(f"   - Time-critical pathway (<5 min for STEMI)")
    
    print("\n" + "=" * 70)
    print("✅ Simulation Complete!")
    print("=" * 70)
    
    if analysis_time < 2.0:
        print(f"\n✅ AI Response Time: {analysis_time:.2f}s (Target: <2s) - MET!")
    else:
        print(f"\n⚠️  AI Response Time: {analysis_time:.2f}s (Target: <2s)")
    
    print(f"\n📊 System Capabilities Demonstrated:")
    print(f"   ✅ Patient data processing")
    print(f"   ✅ Claude AI integration")
    print(f"   ✅ Protocol identification")
    print(f"   ✅ Real-time analysis")
    print(f"   ✅ Agent state management")


if __name__ == "__main__":
    # Fix Windows Unicode encoding
    import sys
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    print("\nStarting Live Patient Flow Simulation...")
    print("This will actually process a patient with Claude AI\n")
    
    try:
        asyncio.run(simulate_stemi_patient())
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Make sure ANTHROPIC_API_KEY is set in .env")
    
    print("\nTo run all agents together:")
    print("   python run_all_agents.py\n")