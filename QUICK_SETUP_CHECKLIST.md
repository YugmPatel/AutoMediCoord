# ✅ Quick Setup Checklist - ASI:One Demo

## 5-Minute Setup Guide

---

## Step 1: Deploy Agents to AgentVerse (If Not Already Done)

- [ ] Go to https://agentverse.ai and login
- [ ] Deploy all 6 agents:
  - [ ] [`ed_coordinator.py`](agentverse_agents/ed_coordinator.py:1)
  - [ ] [`resource_manager.py`](agentverse_agents/resource_manager.py:1)
  - [ ] [`specialist_coordinator.py`](agentverse_agents/specialist_coordinator.py:1)
  - [ ] [`lab_service.py`](agentverse_agents/lab_service.py:1)
  - [ ] [`pharmacy.py`](agentverse_agents/pharmacy.py:1)
  - [ ] [`bed_management.py`](agentverse_agents/bed_management.py:1)

---

## Step 2: Collect Agent Addresses

Copy each agent's address from AgentVerse dashboard:

```
ED Coordinator:           agent1q________________________________
Resource Manager:         agent1q________________________________
Specialist Coordinator:   agent1q________________________________
Lab Service:              agent1q________________________________
Pharmacy:                 agent1q________________________________
Bed Management:           agent1q________________________________
```

---

## Step 3: Update ED Coordinator with Addresses

**Choose ONE method:**

### Method A: AgentVerse Environment Variables (Recommended)
1. Go to ED Coordinator on AgentVerse
2. Click "Settings" or "Environment Variables"
3. Add these variables:
```
RESOURCE_MANAGER_ADDRESS=agent1q...
SPECIALIST_COORDINATOR_ADDRESS=agent1q...
LAB_SERVICE_ADDRESS=agent1q...
PHARMACY_ADDRESS=agent1q...
BED_MANAGEMENT_ADDRESS=agent1q...
```
4. Save and redeploy

### Method B: Hardcode in Agent (Quick Test)
1. Edit [`ed_coordinator.py`](agentverse_agents/ed_coordinator.py:54) line 54
2. Replace `agent1q...` with actual addresses
3. Redeploy on AgentVerse

---

## Step 4: Test the Demo

1. [ ] Go to ASI:One chat interface on AgentVerse
2. [ ] Copy this ambulance report:

```
🚑 AMBULANCE REPORT - INCOMING PATIENT

Patient: 72-year-old male
Chief Complaint: Severe chest pain radiating to left arm
Vitals: HR 110, BP 160/95, SpO2 94%
EMS Report: ST elevation on ECG, suspected STEMI
ETA: 5 minutes

Request: Activate STEMI protocol
```

3. [ ] Paste into ASI:One chat
4. [ ] When asked, provide ED Coordinator address
5. [ ] Watch all 6 agents respond! 🎉

---

## Expected Results

You should see responses from:

✅ **ED Coordinator** - "EMERGENCY PROTOCOL ACTIVATED: STEMI"  
✅ **Resource Manager** - "RESOURCES ALLOCATED: Trauma Bay 1"  
✅ **Lab Service** - "LABS PREPARED: Troponin, ECG, CBC"  
✅ **Pharmacy** - "MEDICATIONS PREPARED: Aspirin, Heparin"  
✅ **Specialist Coordinator** - "TEAM ACTIVATED: Cardiology team"  
✅ **Bed Management** - "BED ASSIGNED: Cardiac ICU Bed 3"  

---

## Troubleshooting

### ❌ No responses from agents
- Check all agents are "Running" on AgentVerse
- Verify agent addresses are correct
- Check ED Coordinator logs for errors

### ❌ Only ED Coordinator responds
- Agent addresses not set in ED Coordinator
- Go back to Step 3 and update addresses

### ❌ ASI:One doesn't route to ED Coordinator
- Provide full agent address (not just name)
- Make sure address starts with `agent1q`

---

## Quick Links

- **Full Demo Guide**: [`ASI_ONE_DEMO_GUIDE.md`](ASI_ONE_DEMO_GUIDE.md:1)
- **Agent Addresses Config**: [`agent_addresses.env`](agentverse_agents/agent_addresses.env:1)
- **AgentVerse Dashboard**: https://agentverse.ai
- **ASI:One Chat**: https://agentverse.ai/chat

---

## Demo Time Estimate

- Setup: 10-15 minutes (first time)
- Demo: 2-5 minutes
- Total: ~20 minutes

**You're ready to demo! 🚀**