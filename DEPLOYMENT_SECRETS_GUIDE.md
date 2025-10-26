# 🔐 Deployment Secrets Guide - All 6 Agents

## 📋 Environment Variables for Each Agent

### ✅ ALL Agents Need These 3 Variables:

```
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=your_claude_api_key_here
```

---

## 🏥 Agent 1: ED Coordinator

**File:** `DEPLOY_ed_coordinator.py`

**Environment Variables:**
```
ED_COORDINATOR_SEED=ed_coordinator_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=your_claude_api_key_here
RESOURCE_MANAGER_ADDRESS=agent1q[get_after_deploying_resource_manager]
SPECIALIST_COORDINATOR_ADDRESS=agent1q[get_after_deploying_specialist]
LAB_SERVICE_ADDRESS=agent1q[get_after_deploying_lab]
PHARMACY_ADDRESS=agent1q[get_after_deploying_pharmacy]
BED_MANAGEMENT_ADDRESS=agent1q[get_after_deploying_bed_mgmt]
```

**⚠️ IMPORTANT:** Deploy other 5 agents FIRST, then add their addresses here!

---

## 🛏️ Agent 2: Bed Management

**File:** `DEPLOY_bed_management.py`

**Environment Variables:**
```
BED_MANAGEMENT_SEED=bed_management_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=your_claude_api_key_here
```

---

## 💊 Agent 3: Pharmacy

**File:** `DEPLOY_pharmacy.py`

**Environment Variables:**
```
PHARMACY_SEED=pharmacy_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=your_claude_api_key_here
```

---

## 🧪 Agent 4: Lab Service

**File:** `DEPLOY_lab_service.py`

**Environment Variables:**
```
LAB_SERVICE_SEED=lab_service_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=your_claude_api_key_here
```

---

## 👨‍⚕️ Agent 5: Specialist Coordinator

**File:** `DEPLOY_specialist_coordinator.py`

**Environment Variables:**
```
SPECIALIST_COORDINATOR_SEED=specialist_coordinator_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=your_claude_api_key_here
```

---

## 📊 Agent 6: Resource Manager

**File:** `DEPLOY_resource_manager.py`

**Environment Variables:**
```
RESOURCE_MANAGER_SEED=resource_manager_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=your_claude_api_key_here
```

---

## 🚀 Deployment Order

### Step 1: Get Claude API Key
1. Go to https://console.anthropic.com/
2. Sign up / Login
3. Go to API Keys
4. Create new key
5. Copy it (starts with `sk-ant-api03-...`)

### Step 2: Deploy Agents 2-6 First
Deploy in this order (doesn't matter much, but logical):
1. ✅ Bed Management
2. ✅ Pharmacy
3. ✅ Lab Service
4. ✅ Specialist Coordinator
5. ✅ Resource Manager

For each:
- Copy the file content
- Paste into AgentVerse `agent.py`
- Add environment variables (3 variables each)
- Deploy
- **COPY THE AGENT ADDRESS** (you'll need it!)

### Step 3: Deploy ED Coordinator Last
1. Copy `DEPLOY_ed_coordinator.py`
2. Paste into AgentVerse
3. Add environment variables (8 variables total!)
4. **Add the 5 agent addresses** you copied in Step 2
5. Deploy

---

## 📝 Quick Copy-Paste Template

### For Agents 2-6 (Bed, Pharmacy, Lab, Specialist, Resource):
```
[AGENT_NAME]_SEED=[agent_name]_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
```

### For ED Coordinator (Agent 1):
```
ED_COORDINATOR_SEED=ed_coordinator_phrase_001
JSONBIN_ID=68fd4c71ae596e708f2c8fb0
JSONBIN_KEY=$2a$10$rwAXxHjp0m8RC1pL5BIW5.bc0orN3f3PivMK6lNPLOw1Gmh333uSa
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
RESOURCE_MANAGER_ADDRESS=agent1q[PASTE_HERE]
SPECIALIST_COORDINATOR_ADDRESS=agent1q[PASTE_HERE]
LAB_SERVICE_ADDRESS=agent1q[PASTE_HERE]
PHARMACY_ADDRESS=agent1q[PASTE_HERE]
BED_MANAGEMENT_ADDRESS=agent1q[PASTE_HERE]
```

---

## ✅ Verification Checklist

After deploying all agents:

- [ ] All 6 agents show "Running" status
- [ ] ED Coordinator has all 5 agent addresses configured
- [ ] All agents have Claude API key
- [ ] All agents have JSONBin credentials
- [ ] Test with simple query to each agent
- [ ] Test ambulance report through ASI:One

---

## 🔍 What Each Agent Will Log

### Startup Logs (All Agents):
```
🏥/💊/🧪/👨‍⚕️/📊/🛏️ [Agent Name] Started
📍 Agent Address: agent1q...
🔧 Tools: JSONBin + Claude AI enabled
📊 JSONBin ID: 68fd4c71ae596e708f2c8fb0...
```

### When Receiving Ambulance Report:
```
📨 Message received from agent1q...
📝 Query: 🚑 AMBULANCE REPORT...
🚑 AMBULANCE REPORT DETECTED - Using Claude AI + Tools
🔧 Tool Call: Fetching [data] from JSONBin...
📊 Tool Result: [results]
🤖 Calling Claude AI for [purpose]...
✅ Claude AI response generated
✅ Response sent
```

### ED Coordinator Additional Logs:
```
📡 Broadcasting to all 5 agents...
✅ Broadcast sent to Resource Manager
✅ Broadcast sent to Lab Service
✅ Broadcast sent to Pharmacy
✅ Broadcast sent to Specialist Coordinator
✅ Broadcast sent to Bed Management
📡 Broadcast complete: 5/5 agents notified
```

---

## 🎯 Success Indicators

You'll know it's working when you see:
1. ✅ All agents start successfully
2. ✅ Logs show "Tools: JSONBin + Claude AI enabled"
3. ✅ Ambulance reports trigger "🚑 AMBULANCE REPORT DETECTED"
4. ✅ Tool calls show "🔧 Tool Call: Fetching..."
5. ✅ Claude AI shows "🤖 Calling Claude AI..."
6. ✅ ED Coordinator broadcasts to all 5 agents
7. ✅ Each agent responds with protocol-specific info

---

## 🚨 Troubleshooting

### "Claude AI not configured"
- Check ANTHROPIC_API_KEY is set correctly
- Verify key starts with `sk-ant-api03-`

### "JSONBin error"
- Check JSONBIN_ID and JSONBIN_KEY are correct
- Test JSONBin URL in browser

### "Agent address not configured"
- Check ED Coordinator has all 5 addresses
- Verify addresses start with `agent1q`

### "Broadcast not reaching agents"
- Ensure all agents are deployed and running
- Check ED Coordinator logs for send errors
- Verify agent addresses are correct

---

**Ready to deploy! Start with agents 2-6, then finish with ED Coordinator!** 🚀