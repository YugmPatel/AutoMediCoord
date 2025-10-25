# 🧠 Letta Integration Testing Guide

This guide will walk you through testing the Letta memory integration in EDFlow AI.

## Prerequisites

- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed
- ✅ Anthropic API key configured
- ✅ Letta API key obtained from [cloud.letta.com](https://cloud.letta.com)

---

## Step 1: Setup Letta Account

### 1.1 Create Account
1. Visit [https://cloud.letta.com](https://cloud.letta.com)
2. Sign up with your email
3. Verify your email address

### 1.2 Get API Key
1. Log in to Letta dashboard
2. Click on your profile (top right)
3. Go to **Settings** → **API Keys**
4. Click **"Create New API Key"**
5. Copy the key (format: `sk-let-...`)

### 1.3 Note Your Project ID
- Your Project ID is visible in the Letta dashboard
- Format: `c4280b2d-0da1-438c-a105-abd8677bad16`
- You'll use this to track your agents

---

## Step 2: Configure Environment

### 2.1 Update `.env` File

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```env
# Enable Letta
LETTA_ENABLED=true
LETTA_API_KEY=sk-let-OGRlNDQxNTktN2Q1ZS00OTc1LThjODQtNDMxMzM3M2ZlNDQ1OmVmOWEzMTQ3LTgzMTktNGFjMi1iODdhLTBlYzI4MWM4ZGY2MA==

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# Deployment
DEPLOYMENT_MODE=local
```

### 2.2 Install Dependencies

```bash
# Install Python packages including Letta
pip install -r requirements.txt
pip install letta

# Install frontend dependencies
cd frontend
npm install
cd ..
```

---

## Step 3: Start the System

### Terminal 1 - Backend API

```bash
python run_api.py
```

**Expected Output:**
```
INFO: Letta client created successfully
INFO: Letta agent initialized: agent_xxxxx
INFO: Starting FastAPI server on http://localhost:8080
INFO: Application startup complete.
```

### Terminal 2 - Frontend Dashboard

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:3000/
```

---

## Step 4: Test Letta Workflow

### 4.1 Simulate First Patient Visit

1. Open browser: http://localhost:3000
2. Click **"Simulate STEMI"** button
3. Watch the case appear in real-time

**What Happens Behind the Scenes:**

```
1. Patient arrives → ED Coordinator receives case
2. Letta is queried: "Recall patient history"
   └─ Returns: "No previous history found (new patient)"
3. Claude AI analyzes patient WITH Letta context
4. Protocol activates (STEMI)
5. Case completes
6. Letta stores the outcome for future reference
```

### 4.2 Check Terminal Logs

Look for these messages in **Terminal 1**:

```
INFO: Retrieved patient context for PATIENT_001
INFO: Stored patient case in Letta memory: PATIENT_001
INFO: Stored protocol performance: stemi
```

### 4.3 Verify on Letta Dashboard

1. Go to [https://cloud.letta.com](https://cloud.letta.com)
2. Click **"Agents"** in sidebar
3. Find agent named: **"EDFlowAI_memory"**
4. Click on it to view details

**You Should See:**
- Agent Status: Active
- Messages: Patient case data stored
- Memory: Core memory blocks with patient info

### 4.4 Test Memory Recall (Second Visit)

1. Click **"Simulate STEMI"** again (same patient)
2. Check Terminal 1 for:

```
INFO: Retrieved patient context for PATIENT_001
Context: "Previous visit found: STEMI protocol on 2024-10-25..."
```

3. Letta now provides historical context!
4. Claude AI makes better decisions with this context

---

## Step 5: Explore Letta Features

### 5.1 View Agent Conversations

In Letta Dashboard:
- Click on **"EDFlowAI_memory"** agent
- View **Message History** tab
- See all patient interactions stored

### 5.2 Check Memory Blocks

- **Core Memory**: Key facts always available
- **Archival Memory**: Long-term storage
- **Recall Memory**: Retrieved relevant context

### 5.3 Query Letta Directly (Optional)

In Letta Dashboard:
- Go to agent page
- Use the chat interface
- Ask: "What patients have you seen today?"
- Letta will summarize stored cases

---

## Step 6: Advanced Testing

### 6.1 Test Different Protocols

Run multiple simulations:
```bash
# Via API
curl -X POST http://localhost:8080/api/simulation/stemi
curl -X POST http://localhost:8080/api/simulation/stroke
curl -X POST http://localhost:8080/api/simulation/trauma
```

### 6.2 Verify Protocol Learning

After 3-5 cases, Letta should:
- Track average response times
- Identify common patterns
- Suggest improvements

Check logs for protocol insights:
```
INFO: Retrieved protocol insights for stemi
Insights: "Historical average door-to-balloon: 4.2 minutes..."
```

### 6.3 Test Resource Recommendations

Letta learns optimal resource allocation:
- Which beds work best for STEMI
- Which teams respond fastest
- Resource availability patterns

---

## Step 7: Debugging

### Common Issues

**Issue: "Letta initialization failed"**
```
Solution:
1. Verify API key in .env
2. Check internet connection
3. Ensure LETTA_ENABLED=true
```

**Issue: "Agent not found in dashboard"**
```
Solution:
1. Refresh Letta dashboard page
2. Check correct Project ID
3. Agent is created on first patient case
```

**Issue: "Context retrieval unavailable"**
```
Solution:
1. System falls back to in-memory storage
2. Check logs for specific error
3. Verify Letta API key is valid
```

### Enable Debug Logging

In `.env`:
```env
LOG_LEVEL=DEBUG
```

This shows detailed Letta operations.

---

## Step 8: Verify Data Flow

### Complete Workflow Test

1. **Patient Arrives**
   ```
   Dashboard → Simulate STEMI
   ```

2. **Letta Recalls History**
   ```
   Logs: "Retrieved patient context for PATIENT_001"
   ```

3. **Claude AI Analyzes (with context)**
   ```
   Logs: "Analyzing patient with historical context"
   ```

4. **Protocol Activates**
   ```
   Dashboard: Case appears with status
   ```

5. **Letta Stores Outcome**
   ```
   Logs: "Stored patient case in Letta memory"
   ```

6. **Verify in Letta Dashboard**
   ```
   cloud.letta.com → Agents → EDFlowAI_memory
   ```

---

## What Success Looks Like

✅ **Backend Terminal Shows:**
- Letta client created successfully
- Agent initialized with ID
- Context retrieved for patients
- Cases stored in memory

✅ **Frontend Dashboard Shows:**
- Real-time case updates
- Protocol activations
- Agent communications

✅ **Letta Dashboard Shows:**
- Agent "EDFlowAI_memory" active
- Message history with patient data
- Memory blocks populated

---

## Next Steps

### Explore Advanced Features

1. **Custom Queries**
   - Ask Letta about patient patterns
   - Get protocol performance summaries

2. **Memory Management**
   - View and edit memory blocks
   - Archive old patient data

3. **Integration Testing**
   - Test with multiple concurrent patients
   - Verify context across sessions

4. **Production Deployment**
   - Deploy with persistent Letta storage
   - Monitor memory usage and performance

---

## Support

**Letta Issues:**
- Documentation: [https://docs.letta.com](https://docs.letta.com)
- Discord: [Letta Community](https://discord.gg/letta)

**Project Issues:**
- Check logs in both terminals
- Verify API keys are correct
- Ensure all dependencies installed

---

## Summary

You've successfully:
- ✅ Set up Letta account and API key
- ✅ Configured EDFlow AI with Letta integration
- ✅ Tested patient memory recall workflow
- ✅ Verified data storage in Letta dashboard
- ✅ Confirmed context-aware AI analysis

Letta is now providing **persistent memory and learning** capabilities to your emergency department coordination system! 🎉