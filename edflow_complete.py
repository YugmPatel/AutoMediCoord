"""
EDFlow AI - Complete System Runner
Single entry point for all functionality
"""

import sys
import asyncio


def print_menu():
    """Display main menu"""
    print("\n" + "=" * 70)
    print("EDFlow AI - Emergency Department Flow Optimizer")
    print("=" * 70)
    print("\n🎯 Choose an option:\n")
    print("  DEMOS:")
    print("    1 - STEMI Patient Demo (✅ Tested & Working)")
    print("    2 - Multi-Patient Coordination Demo")
    print("    3 - Resource Conflict Resolution Demo")
    print()
    print("  TESTING:")
    print("    4 - Run System Tests")
    print("    5 - Run Stress Test (10 patients)")
    print("    6 - Run Integration Test")
    print("    7 - Simulate Real Patient Flow with AI")
    print()
    print("  AGENTS:")
    print("    8 - Run All 6 Agents Together (Bureau)")
    print("    9 - Run Single Agent")
    print()
    print("  DEPLOYMENT:")
    print("   10 - Deploy to Agentverse")
    print()
    print("    0 - Exit")
    print("\n" + "=" * 70)


def run_stemi_demo():
    """Run STEMI demo"""
    print("\n🏥 Running STEMI Demo...\n")
    import subprocess
    subprocess.run([sys.executable, "scenarios/stemi_demo.py"])


def run_multi_patient_demo():
    """Run multi-patient demo"""
    print("\n🏥 Running Multi-Patient Demo...\n")
    import subprocess
    subprocess.run([sys.executable, "scenarios/multi_patient_demo.py"])


def run_conflict_demo():
    """Run conflict resolution demo"""
    print("\n🏥 Running Conflict Resolution Demo...\n")
    import subprocess
    subprocess.run([sys.executable, "scenarios/conflict_resolution_demo.py"])


def run_tests():
    """Run system tests"""
    print("\n🧪 Running System Tests...\n")
    import subprocess
    subprocess.run([sys.executable, "test_system.py"])


def run_stress_test():
    """Run stress test"""
    print("\n⚡ Running Stress Test...\n")
    import subprocess
    subprocess.run([sys.executable, "stress_test.py"])


def run_integration_test():
    """Run integration test"""
    print("\n🔗 Running Integration Test...\n")
    import subprocess
    subprocess.run([sys.executable, "integration_test.py"])


def run_patient_simulation():
    """Run patient flow simulation"""
    print("\n🏥 Running Patient Flow Simulation...\n")
    import subprocess
    subprocess.run([sys.executable, "simulate_patient_flow.py"])


def run_all_agents():
    """Run all agents together"""
    print("\n🤖 Starting All 6 Agents...\n")
    import subprocess
    subprocess.run([sys.executable, "run_all_agents.py"])


def run_single_agent():
    """Run a single agent"""
    print("\n🤖 Available Agents:")
    print("   1 - ed_coordinator")
    print("   2 - resource_manager")
    print("   3 - specialist_coordinator")
    print("   4 - lab_service")
    print("   5 - pharmacy")
    print("   6 - bed_management")
    
    choice = input("\nSelect agent (1-6): ").strip()
    
    agents = {
        "1": "ed_coordinator",
        "2": "resource_manager",
        "3": "specialist_coordinator",
        "4": "lab_service",
        "5": "pharmacy",
        "6": "bed_management"
    }
    
    agent_type = agents.get(choice)
    if agent_type:
        print(f"\n🚀 Starting {agent_type}...\n")
        import subprocess
        subprocess.run([sys.executable, "demo.py", agent_type])
    else:
        print("❌ Invalid selection")


def deploy_to_agentverse():
    """Deploy agents to Agentverse"""
    print("\n🌐 Deploying to Agentverse...\n")
    print("⚠️  Make sure AGENTVERSE_API_KEY is set in .env\n")
    import subprocess
    subprocess.run([sys.executable, "deploy_to_agentverse.py"])


def main():
    """Main menu loop"""
    
    print("\n🏥 Welcome to EDFlow AI!")
    print("Emergency Department Flow Optimizer")
    print("Powered by Fetch.ai uAgents & Claude AI")
    
    while True:
        print_menu()
        choice = input("Select option (0-10): ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!")
            break
        elif choice == "1":
            run_stemi_demo()
        elif choice == "2":
            run_multi_patient_demo()
        elif choice == "3":
            run_conflict_demo()
        elif choice == "4":
            run_tests()
        elif choice == "5":
            run_stress_test()
        elif choice == "6":
            run_integration_test()
        elif choice == "7":
            run_patient_simulation()
        elif choice == "8":
            run_all_agents()
        elif choice == "9":
            run_single_agent()
        elif choice == "10":
            deploy_to_agentverse()
        else:
            print("\n❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting EDFlow AI...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")