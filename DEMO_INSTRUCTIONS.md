# 🎬 AutoMediCoord Live Demo - Show Your Friends!

A visual demonstration of all 6 agents communicating in real-time.

## Quick Start

### 1. Make sure your `.env` is configured for local mode:

```bash
DEPLOYMENT_MODE=local
ANTHROPIC_API_KEY=your_key_here
```

### 2. Run the demo:

```bash
python demo.py
```

## What You'll See

The demo simulates a patient arriving with a heart attack (STEMI):

```
🏥 AutoMediCoord Multi-Agent System - LIVE DEMO
======================================================================

📞 PATIENT ARRIVING AT EMERGENCY DEPARTMENT
----------------------------------------------------------------------
Patient ID: DEMO_PATIENT_001
Priority: 1 (CRITICAL)
Chief Complaint: Severe chest pain radiating to left arm and jaw
Heart Rate: 110 bpm
Blood Pressure: 160/95 mmHg

🤖 WATCHING AGENT COMMUNICATION...
----------------------------------------------------------------------

✅ Patient arrival logged by ED Coordinator
✅ Claude AI analyzed patient data (< 2 seconds)
✅ STEMI protocol identified automatically
✅ All 5 agents received protocol activation message:
   - 📊 Resource Manager
   - 👨‍⚕️ Specialist Coordinator  
   - 🧪 Lab Service
   - 💊 Pharmacy
   - 🛏️ Bed Management

✅ DEMO COMPLETE!
```

## The Flow

1. **Patient Arrives** → ED Coordinator receives patient data
2. **AI Analysis** → Claude analyzes vitals and symptoms
3. **Protocol Detection** → System identifies STEMI (heart attack)
4. **Agent Notification** → All 5 agents receive activation message
5. **Coordination** → Agents ready to execute coordinated response

## Press Ctrl+C to Stop

The demo runs continuously. Press `Ctrl+C` when you're done.

## Show Your Friends These Key Points:

✨ **6 Autonomous Agents** working together
✨ **AI-Powered** patient analysis with Claude
✨ **Real-Time** coordination via uAgents framework
✨ **Sub-2-Second** response time for critical patients
✨ **Production-Ready** for Agentverse deployment

---

**Want to deploy to production?** See [`RENDER_DEPLOYMENT.md`](RENDER_DEPLOYMENT.md)