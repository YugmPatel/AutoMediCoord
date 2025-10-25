# EDFlow AI Agent Deployment Guide - Render & Agentverse

This guide walks you through deploying all 6 EDFlow AI agents to Agentverse via Render cloud platform.

## 📋 Prerequisites

- GitHub account (to host your code)
- Render account (sign up at [render.com](https://render.com))
- Anthropic API key (get from [console.anthropic.com](https://console.anthropic.com/))
- Agentverse account (optional - for viewing agents)

## 🗂️ Project Structure

Your EDFlow AI project is already structured correctly:

```
EDFlow AI/
├── app.py                    # Main entry point for Render
├── render.yaml               # Render auto-deploy configuration
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── .env                     # Your secrets (DO NOT COMMIT)
├── src/
│   ├── agents.py           # All 6 agent implementations
│   ├── ai.py               # Claude AI integration
│   ├── models.py           # Data models
│   └── utils.py            # Configuration & logging
└── README.md
```

**Note:** The [`render.yaml`](render.yaml:1) file enables automatic deployment and PR previews on Render.

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Environment

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and set:**
   ```bash
   DEPLOYMENT_MODE=agentverse
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key
   ```

3. **Test locally first:**
   ```bash
   python app.py
   ```
   
   You should see Agent Inspector links in the logs. This confirms everything works.

### Step 2: Push to GitHub

1. **Ensure `.env` is in `.gitignore`** (it already is)

2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 3: Deploy to Render (Automatic with render.yaml)

**Option A: Automatic Deployment (Recommended)**

The [`render.yaml`](render.yaml:1) file is already configured for automatic deployment:

1. **Sign up/Login to Render:**
   - Go to [render.com](https://render.com)
   - Create an account or sign in

2. **Connect Repository:**
   - Click **"New" → "Blueprint"**
   - Connect your GitHub account
   - Select your **EDFlow AI** repository
   - Render will automatically detect `render.yaml`

3. **Add ANTHROPIC_API_KEY:**
   - During setup, you'll be prompted to add the API key
   - This is the **only** environment variable you need to set manually
   - All other variables are auto-configured in `render.yaml`

4. **Deploy:**
   - Click **"Apply"**
   - Render will automatically build and deploy your agents

**Option B: Manual Configuration**

If you prefer manual setup:

1. Click **"+ New"** → **"Background Worker"**
2. Configure:
   ```
   Name: ed-fox-agents
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

3. Add Environment Variables:
   
   | Key | Value | Notes |
   |-----|-------|-------|
   | `DEPLOYMENT_MODE` | `agentverse` | **Required** |
   | `ANTHROPIC_API_KEY` | `your_key` | **Required** |
   | `LOG_LEVEL` | `INFO` | Optional |

4. Click **"Create Background Worker"**

### Step 4: Monitor Deployment

1. **Watch the logs:**
   - Render shows a real-time log explorer
   - Look for these success indicators:
   ```
   ✅ Running in AGENTVERSE mode
   ✅ All 6 agents created successfully!
   Agent Addresses (Register these in Agentverse):
     1. ED Coordinator:          agent1q...
     2. Resource Manager:        agent1q...
     ...
   🚀 Starting Bureau - All Agents Running
   ```

2. **Copy Agent Inspector Links:**
   - Each agent will show a link like:
   ```
   Agent Inspector: https://agentverse.ai/inspect?uri=...
   ```
   - Open each link to register agents with Agentverse

### Step 5: Register Agents in Agentverse

1. **For each Agent Inspector link:**
   - Open in browser
   - Sign in to Agentverse
   - The agent will appear under **"My Agents" → "Local Agents"**

2. **Update Agent Profiles:**
   - Set friendly names (ED Coordinator, Resource Manager, etc.)
   - Add descriptions
   - Add tags: `healthcare`, `emergency-department`, `ed-fox`

3. **Test Communication:**
   - Use the Agentverse chat interface
   - Send test messages to ED Coordinator
   - Verify other agents receive protocol activations

## 🎯 All 6 Agents

Your deployment includes:

1. **ED Coordinator** - Central orchestrator, receives patients
2. **Resource Manager** - Manages beds, equipment, staff
3. **Specialist Coordinator** - Activates specialist teams (STEMI, Stroke, Trauma)
4. **Lab Service** - Processes lab orders and results
5. **Pharmacy** - Handles medication orders
6. **Bed Management** - Assigns and tracks patient beds

## 🧪 Testing Your Deployment

### Test 1: Send Patient Arrival

Send this to **ED Coordinator** via Agentverse chat:

```
PATIENT ARRIVAL:
- Vitals: HR=95, BP=145/90, SpO2=96%
- Complaint: Chest pain radiating to left arm
- Priority: 1 (Critical)
```

**Expected Results:**
- ED Coordinator analyzes patient
- STEMI protocol activated
- All 5 other agents receive protocol notification

### Test 2: Check Logs

In Render logs, you should see:

```
INFO - Patient arrival processed
INFO - AI analysis completed
INFO - Activating STEMI protocol
INFO - resource_manager received: PROTOCOL: STEMI
INFO - specialist_coordinator received: PROTOCOL: STEMI
INFO - lab_service received: PROTOCOL: STEMI
INFO - pharmacy received: PROTOCOL: STEMI
INFO - bed_management received: PROTOCOL: STEMI
```

## 🔧 Troubleshooting

### Issue: "DEPLOYMENT_MODE must be set to 'agentverse'"
- **Solution:** Add `DEPLOYMENT_MODE=agentverse` to Render environment variables
- Redeploy the service

### Issue: "Claude AI error"
- **Solution:** Verify `ANTHROPIC_API_KEY` is correct in Render environment
- Check you have API credits at console.anthropic.com
- Ensure no extra spaces in the API key

### Issue: Agents not appearing in Agentverse
- **Solution:** 
  - Check Render logs for Agent Inspector links
  - Open each link in browser while logged into Agentverse
  - Ensure mailbox connection is successful

### Issue: Build fails on Render
- **Solution:**
  - Check `requirements.txt` is present
  - Verify Python version compatibility
  - Look for dependency conflicts in logs

### Issue: Agents start but don't communicate
- **Solution:**
  - Verify all 6 agents are registered in Agentverse
  - Check ED Coordinator has other agents' addresses
  - Test with simple chat message first

## 📊 Monitoring & Logs

### View Live Logs
```
Render Dashboard → Your Service → Logs
```

### Key Log Messages to Monitor
- `✅ Running in AGENTVERSE mode` - Correct mode
- `✅ All 6 agents created successfully!` - All agents started
- `🚀 Starting Bureau` - System running
- `INFO - Patient ... arriving` - Patient processing
- `INFO - Activating ... protocol` - Protocol activation
- `INFO - [agent] received: PROTOCOL` - Inter-agent communication

## 🎉 Success Checklist

- [ ] All 6 agents deployed on Render
- [ ] No errors in Render logs
- [ ] All agents registered in Agentverse
- [ ] Agent Inspector links working
- [ ] Test patient triggers STEMI protocol
- [ ] All 5 agents receive protocol message
- [ ] Logs show successful communication

## 💡 Next Steps

1. **Add More Protocols:**
   - Implement Stroke protocol
   - Add Trauma protocol
   - Create Pediatric protocol

2. **Enhance AI Analysis:**
   - Improve acuity scoring
   - Add resource prediction
   - Implement outcome tracking

3. **Build Dashboard:**
   - Real-time patient tracking
   - Resource utilization metrics
   - Protocol activation statistics

4. **Scale Up:**
   - Add more agent instances
   - Implement load balancing
   - Add redundancy

## 📚 Useful Links

- **Render Docs:** [render.com/docs](https://render.com/docs)
- **Agentverse Docs:** [fetch.ai/docs](https://fetch.ai/docs)
- **uAgents Guide:** [github.com/fetchai/uAgents](https://github.com/fetchai/uAgents)
- **Claude API:** [docs.anthropic.com](https://docs.anthropic.com)

## 🆘 Support

If you encounter issues:
1. Check Render logs first
2. Verify environment variables
3. Test locally with `python app.py`
4. Review Agentverse agent status
5. Check this troubleshooting guide

---

## 🏷️ Tags for Agentverse

When setting up agents in Agentverse, use these tags:

![tag:healthcare](https://img.shields.io/badge/healthcare-3D8BD3)
![tag:emergency-department](https://img.shields.io/badge/emergency--department-3D8BD3)
![tag:ed-fox](https://img.shields.io/badge/ed--fox-3D8BD3)
![tag:multi-agent](https://img.shields.io/badge/multi--agent-3D8BD3)
![tag:ai-powered](https://img.shields.io/badge/ai--powered-3D8BD3)

---

**🎯 Your EDFlow AI Multi-Agent System is ready for deployment!**