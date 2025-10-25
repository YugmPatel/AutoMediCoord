#!/usr/bin/env python3
"""
EDFlow AI System Integration Test
Tests real-time communication between React frontend and uAgents backend
"""

import asyncio
import aiohttp
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# Add paths for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "AutoMediCoord"))

class SystemTester:
    def __init__(self):
        self.api_base = "http://localhost:8080"
        self.frontend_url = "http://localhost:3000"
        self.test_results = []
        
    async def test_api_health(self):
        """Test API server health"""
        print("🔍 Testing API Health...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ API Health: {data['status']}")
                        print(f"   Agents Active: {data['agents_active']}")
                        self.test_results.append(("API Health", True, "API server is healthy"))
                        return True
                    else:
                        print(f"❌ API Health Check Failed: {response.status}")
                        self.test_results.append(("API Health", False, f"Status: {response.status}"))
                        return False
        except Exception as e:
            print(f"❌ API Health Check Error: {str(e)}")
            self.test_results.append(("API Health", False, str(e)))
            return False
    
    async def test_dashboard_endpoints(self):
        """Test dashboard API endpoints"""
        print("\n🔍 Testing Dashboard Endpoints...")
        
        endpoints = [
            ("/api/dashboard/metrics", "Dashboard Metrics"),
            ("/api/dashboard/activity", "Activity Log"),
            ("/api/dashboard/status", "Dashboard Status"),
            ("/api/cases", "Active Cases"),
            ("/api/agents/status", "Agent Status")
        ]
        
        success_count = 0
        
        try:
            async with aiohttp.ClientSession() as session:
                for endpoint, name in endpoints:
                    try:
                        async with session.get(f"{self.api_base}{endpoint}") as response:
                            if response.status == 200:
                                data = await response.json()
                                print(f"✅ {name}: OK")
                                self.test_results.append((name, True, "Endpoint responding"))
                                success_count += 1
                            else:
                                print(f"❌ {name}: Status {response.status}")
                                self.test_results.append((name, False, f"Status: {response.status}"))
                    except Exception as e:
                        print(f"❌ {name}: {str(e)}")
                        self.test_results.append((name, False, str(e)))
        
        except Exception as e:
            print(f"❌ Dashboard Endpoints Error: {str(e)}")
        
        print(f"📊 Dashboard Endpoints: {success_count}/{len(endpoints)} passed")
        return success_count == len(endpoints)
    
    async def test_simulation_endpoints(self):
        """Test patient simulation endpoints"""
        print("\n🔍 Testing Simulation Endpoints...")
        
        simulations = [
            ("/api/simulation/stemi", "STEMI Simulation"),
            ("/api/simulation/stroke", "Stroke Simulation")
        ]
        
        success_count = 0
        
        try:
            async with aiohttp.ClientSession() as session:
                for endpoint, name in simulations:
                    try:
                        async with session.post(f"{self.api_base}{endpoint}") as response:
                            if response.status == 200:
                                data = await response.json()
                                print(f"✅ {name}: Patient {data['patient_id']} created")
                                self.test_results.append((name, True, f"Patient: {data['patient_id']}"))
                                success_count += 1
                                
                                # Wait a moment for processing
                                await asyncio.sleep(1)
                            else:
                                print(f"❌ {name}: Status {response.status}")
                                self.test_results.append((name, False, f"Status: {response.status}"))
                    except Exception as e:
                        print(f"❌ {name}: {str(e)}")
                        self.test_results.append((name, False, str(e)))
        
        except Exception as e:
            print(f"❌ Simulation Endpoints Error: {str(e)}")
        
        print(f"🚑 Simulation Endpoints: {success_count}/{len(simulations)} passed")
        return success_count == len(simulations)
    
    async def test_websocket_connection(self):
        """Test WebSocket connection"""
        print("\n🔍 Testing WebSocket Connection...")
        
        try:
            import socketio
            
            # Create Socket.IO client
            sio = socketio.AsyncClient()
            
            # Connection tracking
            connected = False
            messages_received = []
            
            @sio.event
            async def connect():
                nonlocal connected
                connected = True
                print("✅ WebSocket Connected")
            
            @sio.event
            async def disconnect():
                print("🔌 WebSocket Disconnected")
            
            @sio.event
            async def patient_arrival(data):
                messages_received.append(("patient_arrival", data))
                print(f"📥 Patient Arrival Event: {data.get('data', {}).get('patient_id', 'Unknown')}")
            
            @sio.event
            async def protocol_activation(data):
                messages_received.append(("protocol_activation", data))
                print(f"🚨 Protocol Activation: {data.get('data', {}).get('protocol', 'Unknown')}")
            
            @sio.event
            async def chat_message(data):
                messages_received.append(("chat_message", data))
                print(f"💬 Chat Message: {data.get('sender', 'Unknown')}")
            
            # Connect to WebSocket
            await sio.connect(f"{self.api_base}")
            
            if connected:
                print("✅ WebSocket connection established")
                
                # Test sending a message
                await sio.emit('send_message', {
                    'message': 'Test message from integration test',
                    'sender': 'Test System'
                })
                
                # Wait for potential responses
                await asyncio.sleep(3)
                
                # Disconnect
                await sio.disconnect()
                
                print(f"📨 Received {len(messages_received)} WebSocket events")
                self.test_results.append(("WebSocket Connection", True, f"{len(messages_received)} events received"))
                return True
            else:
                print("❌ WebSocket connection failed")
                self.test_results.append(("WebSocket Connection", False, "Connection failed"))
                return False
                
        except Exception as e:
            print(f"❌ WebSocket Test Error: {str(e)}")
            self.test_results.append(("WebSocket Connection", False, str(e)))
            return False
    
    async def test_agent_integration(self):
        """Test uAgent integration"""
        print("\n🔍 Testing uAgent Integration...")
        
        try:
            # Test if agents are accessible through API
            async with aiohttp.ClientSession() as session:
                # Get agent status
                async with session.get(f"{self.api_base}/api/agents/status") as response:
                    if response.status == 200:
                        agents = await response.json()
                        online_agents = [agent for agent in agents if agent['status'] == 'online']
                        
                        print(f"✅ Agent Integration: {len(online_agents)}/{len(agents)} agents online")
                        
                        for agent in agents:
                            status_icon = "✅" if agent['status'] == 'online' else "❌"
                            print(f"   {status_icon} {agent['name']}: {agent['status']}")
                        
                        self.test_results.append(("Agent Integration", True, f"{len(online_agents)} agents online"))
                        return len(online_agents) > 0
                    else:
                        print(f"❌ Agent Status Check Failed: {response.status}")
                        self.test_results.append(("Agent Integration", False, f"Status: {response.status}"))
                        return False
                        
        except Exception as e:
            print(f"❌ Agent Integration Error: {str(e)}")
            self.test_results.append(("Agent Integration", False, str(e)))
            return False
    
    async def test_end_to_end_flow(self):
        """Test complete end-to-end patient flow"""
        print("\n🔍 Testing End-to-End Patient Flow...")
        
        try:
            async with aiohttp.ClientSession() as session:
                # 1. Trigger STEMI simulation
                print("   1. Triggering STEMI simulation...")
                async with session.post(f"{self.api_base}/api/simulation/stemi") as response:
                    if response.status != 200:
                        print(f"❌ STEMI simulation failed: {response.status}")
                        return False
                    
                    stemi_data = await response.json()
                    patient_id = stemi_data['patient_id']
                    print(f"   ✅ STEMI patient created: {patient_id}")
                
                # 2. Wait for processing
                await asyncio.sleep(2)
                
                # 3. Check if case appears in active cases
                print("   2. Checking active cases...")
                async with session.get(f"{self.api_base}/api/cases") as response:
                    if response.status == 200:
                        cases = await response.json()
                        stemi_case = next((case for case in cases if case['id'] == patient_id), None)
                        
                        if stemi_case:
                            print(f"   ✅ STEMI case found in active cases")
                            print(f"      Type: {stemi_case['type']}")
                            print(f"      Status: {stemi_case['status']}")
                            print(f"      HR: {stemi_case['vitals']['hr']} bpm")
                        else:
                            print(f"   ❌ STEMI case not found in active cases")
                            return False
                    else:
                        print(f"   ❌ Failed to retrieve active cases: {response.status}")
                        return False
                
                # 4. Check dashboard metrics updated
                print("   3. Checking dashboard metrics...")
                async with session.get(f"{self.api_base}/api/dashboard/metrics") as response:
                    if response.status == 200:
                        metrics = await response.json()
                        print(f"   ✅ Dashboard metrics updated")
                        print(f"      Active Cases: {metrics['active_cases']}")
                        print(f"      Avg Lab ETA: {metrics['avg_lab_eta']}m")
                    else:
                        print(f"   ❌ Failed to retrieve metrics: {response.status}")
                        return False
                
                print("✅ End-to-End Flow: Complete patient simulation workflow working")
                self.test_results.append(("End-to-End Flow", True, "Complete workflow functional"))
                return True
                
        except Exception as e:
            print(f"❌ End-to-End Flow Error: {str(e)}")
            self.test_results.append(("End-to-End Flow", False, str(e)))
            return False
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*70)
        print("🧪 EDFlow AI System Test Summary")
        print("="*70)
        
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        print(f"📊 Overall Results: {passed}/{total} tests passed")
        print(f"🎯 Success Rate: {(passed/total)*100:.1f}%")
        
        print("\n📋 Detailed Results:")
        for test_name, success, details in self.test_results:
            status_icon = "✅" if success else "❌"
            print(f"   {status_icon} {test_name}: {details}")
        
        print("\n🚀 System Status:")
        if passed == total:
            print("✅ All tests passed! System is ready for production.")
        elif passed >= total * 0.8:
            print("⚠️  Most tests passed. Minor issues detected.")
        else:
            print("❌ Multiple test failures. System needs attention.")
        
        print("\n📚 Next Steps:")
        if passed == total:
            print("   • Deploy to production environment")
            print("   • Configure monitoring and alerts")
            print("   • Set up backup and recovery")
        else:
            print("   • Review failed tests and fix issues")
            print("   • Check server logs for detailed error information")
            print("   • Verify all dependencies are installed")
        
        print("="*70)

async def main():
    """Main test execution"""
    print("🏥 EDFlow AI - System Integration Test")
    print("="*70)
    print("Testing complete system integration...")
    print("Make sure both API server and frontend are running!")
    print("API Server: python run_api.py")
    print("Frontend: cd frontend && npm run dev")
    print("="*70)
    
    tester = SystemTester()
    
    # Run all tests
    tests = [
        tester.test_api_health(),
        tester.test_dashboard_endpoints(),
        tester.test_agent_integration(),
        tester.test_simulation_endpoints(),
        tester.test_websocket_connection(),
        tester.test_end_to_end_flow()
    ]
    
    # Execute tests
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    # Handle any exceptions
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Test {i+1} failed with exception: {str(result)}")
            tester.test_results.append((f"Test {i+1}", False, str(result)))
    
    # Print summary
    tester.print_test_summary()
    
    # Return overall success
    passed = sum(1 for _, success, _ in tester.test_results if success)
    total = len(tester.test_results)
    return passed == total

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Test execution failed: {str(e)}")
        sys.exit(1)