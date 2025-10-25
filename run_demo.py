#!/usr/bin/env python3
"""
EDFlow AI - Interactive Demo Launcher
Run all demos with a simple menu
"""

import os
import sys
import subprocess
import time

# Fix Windows Unicode encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print demo menu header"""
    print("=" * 70)
    print("🏥 EDFlow AI - Interactive Demo Launcher")
    print("=" * 70)
    print()


def print_menu():
    """Print demo menu options"""
    print("Choose a demo to run:")
    print()
    print("  1. 🧪 Test API Connection (30 seconds)")
    print("  2. 🏥 Multi-Patient Coordination Demo (2 minutes)")
    print("  3. ⚡ Conflict Resolution Demo (2 minutes)")
    print("  4. 🤖 Live AI Patient Analysis (2 minutes)")
    print("  5. 📊 System Stress Test (1 minute)")
    print("  6. 🎬 Run ALL Demos (8 minutes)")
    print()
    print("  7. 📚 View Documentation")
    print("  8. ❓ Help & Troubleshooting")
    print()
    print("  0. Exit")
    print()


def run_command(command, description):
    """Run a command and handle errors"""
    print("\n" + "=" * 70)
    print(f"▶️  {description}")
    print("=" * 70)
    print()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True
        )
        
        print("\n" + "=" * 70)
        print("✅ Demo completed successfully!")
        print("=" * 70)
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 70)
        print(f"❌ Demo failed with error code {e.returncode}")
        print("=" * 70)
        print("\n💡 Tip: Check TROUBLESHOOTING.md for help")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        return False


def wait_for_continue():
    """Wait for user to press Enter"""
    print()
    input("Press Enter to continue...")


def demo_1_api_test():
    """Test API connection"""
    clear_screen()
    return run_command(
        "python test_claude_api.py",
        "Testing Claude API Connection"
    )


def demo_2_multi_patient():
    """Multi-patient coordination demo"""
    clear_screen()
    return run_command(
        "python scenarios/multi_patient_demo.py",
        "Multi-Patient Coordination Demo"
    )


def demo_3_conflict_resolution():
    """Conflict resolution demo"""
    clear_screen()
    return run_command(
        "python scenarios/conflict_resolution_demo.py",
        "Resource Conflict Resolution Demo"
    )


def demo_4_live_analysis():
    """Live AI analysis demo"""
    clear_screen()
    return run_command(
        "python simulate_patient_flow.py",
        "Live AI Patient Analysis"
    )


def demo_5_stress_test():
    """System stress test"""
    clear_screen()
    return run_command(
        "python stress_test.py",
        "System Stress Test (10 Concurrent Patients)"
    )


def demo_6_run_all():
    """Run all demos in sequence"""
    clear_screen()
    print("=" * 70)
    print("🎬 Running ALL Demos")
    print("=" * 70)
    print("\nThis will run all demos in sequence (~8 minutes)")
    print()
    
    response = input("Continue? (y/n): ").lower()
    if response != 'y':
        print("Cancelled.")
        return False
    
    demos = [
        ("python test_claude_api.py", "API Test"),
        ("python scenarios/multi_patient_demo.py", "Multi-Patient Demo"),
        ("python scenarios/conflict_resolution_demo.py", "Conflict Resolution"),
        ("python simulate_patient_flow.py", "Live Analysis"),
        ("python stress_test.py", "Stress Test"),
    ]
    
    results = []
    for i, (cmd, name) in enumerate(demos, 1):
        print(f"\n\n{'=' * 70}")
        print(f"Demo {i}/{len(demos)}: {name}")
        print('=' * 70)
        time.sleep(1)
        
        success = run_command(cmd, name)
        results.append((name, success))
        
        if i < len(demos):
            print("\n⏳ Next demo in 3 seconds...")
            time.sleep(3)
    
    # Summary
    clear_screen()
    print("=" * 70)
    print("🎬 All Demos Complete!")
    print("=" * 70)
    print("\n📊 Results:")
    print()
    
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {status}  {name}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    print()
    print(f"Total: {passed}/{total} demos passed")
    
    return True


def show_documentation():
    """Show documentation menu"""
    clear_screen()
    print("=" * 70)
    print("📚 Documentation")
    print("=" * 70)
    print()
    print("Available documentation:")
    print()
    print("  1. README.md - Project overview")
    print("  2. QUICKSTART.md - Quick start guide")
    print("  3. DEMO_GUIDE.md - How to run demos")
    print("  4. TROUBLESHOOTING.md - Problem solving")
    print("  5. COMMANDS.md - Command reference")
    print("  6. STATUS.md - Current status")
    print("  7. docs/ARCHITECTURE.md - System architecture")
    print()
    print("  0. Back to main menu")
    print()
    
    choice = input("Choose document to view (0-7): ").strip()
    
    docs = {
        '1': 'README.md',
        '2': 'QUICKSTART.md',
        '3': 'DEMO_GUIDE.md',
        '4': 'TROUBLESHOOTING.md',
        '5': 'COMMANDS.md',
        '6': 'STATUS.md',
        '7': 'docs/ARCHITECTURE.md',
    }
    
    if choice in docs:
        clear_screen()
        if os.name == 'nt':
            os.system(f'type {docs[choice]} | more')
        else:
            os.system(f'cat {docs[choice]} | less')
        wait_for_continue()


def show_help():
    """Show help and troubleshooting"""
    clear_screen()
    print("=" * 70)
    print("❓ Help & Troubleshooting")
    print("=" * 70)
    print()
    print("Common Issues:")
    print()
    print("1. API Errors:")
    print("   - Make sure ANTHROPIC_API_KEY is set in .env")
    print("   - Run: python test_claude_api.py")
    print()
    print("2. Import Errors:")
    print("   - Make sure you're in project root directory")
    print("   - Run: pip install -r requirements.txt")
    print()
    print("3. Port Conflicts:")
    print("   - Check if ports 8000-8005 are available")
    print("   - Edit .env to use different ports")
    print()
    print("4. Unicode Errors (Windows):")
    print("   - This launcher handles it automatically")
    print("   - Or run: chcp 65001 (in CMD)")
    print()
    print("📚 For more help, see TROUBLESHOOTING.md")
    print()
    wait_for_continue()


def main():
    """Main demo launcher"""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("Enter your choice (0-8): ").strip()
        
        if choice == '0':
            clear_screen()
            print("\n👋 Thank you for using EDFlow AI!")
            print("🏆 Good luck with your demo!\n")
            break
        
        elif choice == '1':
            demo_1_api_test()
            wait_for_continue()
        
        elif choice == '2':
            demo_2_multi_patient()
            wait_for_continue()
        
        elif choice == '3':
            demo_3_conflict_resolution()
            wait_for_continue()
        
        elif choice == '4':
            demo_4_live_analysis()
            wait_for_continue()
        
        elif choice == '5':
            demo_5_stress_test()
            wait_for_continue()
        
        elif choice == '6':
            demo_6_run_all()
            wait_for_continue()
        
        elif choice == '7':
            show_documentation()
        
        elif choice == '8':
            show_help()
        
        else:
            print("\n❌ Invalid choice. Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("See TROUBLESHOOTING.md for help")
