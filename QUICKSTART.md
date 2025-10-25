# 🚀 EDFlow AI - Quick Start Guide

## ✅ Your API Key is Configured!

Your Anthropic API key has been added to `.env` and the system is ready to test.

## 📦 Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## 🎬 Step 2: Run the STEMI Demo

```bash
python scenarios/stemi_demo.py
```

This will show a simulated STEMI patient scenario with protocol activation.

## 🤖 Step 3: Test Individual Agents

Open separate terminals and run:

```bash
# Terminal 1 - ED Coordinator
python demo.py ed_coordinator

# Terminal 2 - Resource Manager  
python demo.py resource_manager

# Terminal 3 - Specialist Coordinator
python demo.py specialist_coordinator

# Terminal 4 - Lab Service
python demo.py lab_service

# Terminal 5 - Pharmacy
python demo.py pharmacy

# Terminal 6 - Bed Management
python demo.py bed_management
```

Each agent will start and display its address. The agents can now communicate!

## 🧪 Step 4: Test AI Integration

The ED Coordinator agent uses your Claude AI key for patient acuity analysis. When it receives a patient notification, it will:

1. Analyze vitals and symptoms with Claude
2. Determine acuity level (1-5)
3. Recommend protocol (STEMI, Stroke, Trauma, etc.)
4. Activate appropriate protocol
5. Coordinate with other agents

## 🌐 Step 5: Deploy to Agentverse (Optional)

To deploy on Agentverse for 24/7 operation:

1. Get API key from https://agentverse.ai
2. Add to `.env`: `AGENTVERSE_API_KEY=your_key_here`
3. Set: `DEPLOYMENT_MODE=agentverse`
4. Run agents - they'll use mailbox mode
5. Use Inspector link from logs to connect

## 📊 What You Can Do Now

### Run Demos
```bash
# STEMI scenario
python scenarios/stemi_demo.py
```

### Test Agents Locally
```bash
# Run any individual agent
python demo.py ed_coordinator
```

### Monitor Logs
Agents will log:
- Startup and address
- Incoming messages
- AI analysis results
- Protocol activations
- Resource allocations

### Send Test Messages
Agents communicate via chat protocol. You can:
1. Start multiple agents
2. They'll exchange messages
3. Monitor coordination in logs

## 🎯 Next Steps

### For Competition
1. ✅ All 6 agents implemented
2. ✅ Claude AI integrated
3. ✅ Demo scenario ready
4. ⏳ Record 5-7 min demo video showing:
   - Problem statement
   - Live STEMI demo
   - Agent coordination
   - Results and impact

### For Testing
1. Run STEMI demo
2. Start all agents
3. Test communication
4. Verify AI responses
5. Check logs for coordination

## 🐛 Troubleshooting

### If you see import errors:
```bash
pip install -r requirements.txt
```

### If agents don't start:
- Check .env file exists
- Verify API key is set
- Try different ports if blocked

### If AI doesn't work:
- Check ANTHROPIC_API_KEY in .env
- Verify key is valid
- System will fall back to rules if needed

## 📝 Available Commands

```bash
# Run STEMI demo
python scenarios/stemi_demo.py

# Run specific agent
python demo.py <agent_name>

# Available agents:
# - ed_coordinator
# - resource_manager
# - specialist_coordinator
# - lab_service
# - pharmacy
# - bed_management
```

## 🎓 Understanding the System

### Agent Roles
1. **ED Coordinator** - Central hub, AI analysis, protocol activation
2. **Resource Manager** - Beds, equipment, allocation
3. **Specialist Coordinator** - Team activation, specialists
4. **Lab Service** - Laboratory orders and results
5. **Pharmacy** - Medication management
6. **Bed Management** - Bed assignments

### How It Works
1. Patient arrives (via PatientArrivalNotification)
2. ED Coordinator uses Claude AI to analyze
3. System identifies protocol (STEMI, Stroke, etc.)
4. Coordinator broadcasts to all agents
5. Each agent performs their role
6. Full coordination in <5 minutes

## 🏆 You're Ready!

Everything is set up and ready to go. Start with the STEMI demo to see the system in action!

```bash
python scenarios/stemi_demo.py
```

Good luck with your competition submission! 🎉