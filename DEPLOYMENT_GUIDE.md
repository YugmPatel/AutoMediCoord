# 🚀 EDFlow AI - Deployment Guide

## 📋 Overview

This guide covers deploying all 6 EDFlow AI agents to Agentverse for 24/7 operation.

## 🎯 Deployment Options

### Option 1: Local Development (Current)
- Run agents on your machine
- Good for testing and development
- Requires keeping terminals open

### Option 2: Agentverse Cloud (Production)
- Agents hosted 24/7 on Agentverse
- Built-in mailbox service
- No local resources needed
- Best for competition demo

## 🌐 Deploying to Agentverse

### Prerequisites

1. **Agentverse Account**
   - Sign up at https://agentverse.ai
   - Verify your email

2. **API Key**
   - Go to Profile → API Keys
   - Click "+ New API Key"
   - Save the key (can't be regenerated!)

3. **Agent Seeds**
   - Use the seeds in your `.env` file
   - These ensure consistent agent addresses

### Step-by-Step Deployment

#### 1. Configure for Agentverse

Edit `.env`:
```bash
# Change deployment mode
DEPLOYMENT_MODE=agentverse

# Add your Agentverse API key
AGENTVERSE_API_KEY=your_agentverse_api_key_here
```

#### 2. Deploy Each Agent

**For each of the 6 agents:**

```bash
# Terminal 1 - ED Coordinator
python demo.py ed_coordinator

# Wait for this message in the logs:
# "Agent Inspector: https://agentverse.ai/inspect?uri=..."

# Click the Inspector link or copy it to browser
# This connects the agent to Agentverse
```

**Repeat for all 6 agents:**

```bash
# Terminal 2
python demo.py resource_manager

# Terminal 3
python demo.py specialist_coordinator

# Terminal 4
python demo.py lab_service

# Terminal 5
python demo.py pharmacy

# Terminal 6
python demo.py bed_management
```

#### 3. Verify on Agentverse

1. Login to https://agentverse.ai
2. Go to "My Agents"
3. You should see all 6 agents listed
4. Each agent will show:
   - Name
   - Address
   - Status (Active/Inactive)
   - Last activity

#### 4. Test Agent Communication

In Agentverse:
1. Click on any agent
2. Go to "Chat" tab
3. Send a test message
4. Verify agent responds
5. Check logs for activity

### Agent Addresses

After deployment, note down each agent's address from the logs:

```
ED Coordinator: agent1q...
Resource Manager: agent1qw...
Specialist Coordinator: agent1qe...
Lab Service: agent1qr...
Pharmacy: agent1qt...
Bed Management: agent1qy...
```

These addresses are needed for agents to communicate with each other.

## 🔧 Configuration Management

### Environment Variables

**Required for Agentverse:**
```bash
ANTHROPIC_API_KEY=sk-ant-...        # Your Claude AI key
AGENTVERSE_API_KEY=av-...           # Your Agentverse key
DEPLOYMENT_MODE=agentverse          # Enable Agentverse mode
```

**Agent Seeds (keep consistent):**
```bash
ED_COORDINATOR_SEED=ed_coordinator_recovery_phrase_2025
RESOURCE_MANAGER_SEED=resource_manager_recovery_phrase_2025
# ... (use same seeds for consistent addresses)
```

### Mailbox Mode

When `DEPLOYMENT_MODE=agentverse`, agents automatically:
- Use mailbox service
- Stay online 24/7
- Receive messages even when offline
- Don't need local ports

## 📊 Monitoring Deployed Agents

### In Agentverse Dashboard

1. **Activity Tab**
   - View recent messages
   - See protocol activations
   - Monitor performance

2. **Logs Tab**
   - Real-time logs
   - Error messages
   - Debug information

3. **Stats Tab**
   - Message count
   - Response times
   - Uptime

### Performance Metrics

Monitor these metrics:
- **Response Time**: <2s for AI decisions
- **Message Latency**: <500ms between agents
- **Protocol Activation**: <5 min for STEMI
- **Uptime**: Target 99.5%

## 🔒 Security Best Practices

### API Keys
- ✅ Never commit `.env` to git
- ✅ Use environment variables
- ✅ Rotate keys periodically
- ✅ Limit key permissions

### Agent Security
- ✅ Use unique seeds for each agent
- ✅ Keep seeds private
- ✅ Blockchain-based identity
- ✅ Message verification

## 🐛 Troubleshooting

### Agent Not Connecting
**Problem:** Agent doesn't appear in Agentverse

**Solutions:**
1. Check AGENTVERSE_API_KEY is correct
2. Verify DEPLOYMENT_MODE=agentverse
3. Click the Inspector link from logs
4. Check network/firewall settings

### Messages Not Received
**Problem:** Agents not communicating

**Solutions:**
1. Verify all agents are online
2. Check agent addresses are correct
3. Ensure chat protocol is enabled
4. Review Agentverse logs

### High Latency
**Problem:** Slow response times

**Solutions:**
1. Check Claude AI key is valid
2. Monitor Agentverse dashboard
3. Review agent logs for errors
4. Check network connectivity

## 🎬 Demo Mode vs Production

### Demo Mode (Current)
```bash
# Local execution
DEPLOYMENT_MODE=local

# Run for demonstrations
python scenarios/stemi_demo.py
python demo.py ed_coordinator
```

**Use for:**
- Testing
- Development
- Local demos
- Debugging

### Production Mode (Agentverse)
```bash
# Cloud deployment
DEPLOYMENT_MODE=agentverse

# Deploy all 6 agents
# They stay online 24/7
```

**Use for:**
- Competition submission
- 24/7 operation
- Scalability
- Reliability

## 📋 Deployment Checklist

### Before Deployment
- [ ] Agentverse account created
- [ ] API key obtained
- [ ] `.env` configured
- [ ] All agents tested locally
- [ ] Agent addresses documented

### During Deployment
- [ ] Set DEPLOYMENT_MODE=agentverse
- [ ] Deploy all 6 agents
- [ ] Click Inspector links
- [ ] Verify in Agentverse dashboard
- [ ] Test agent communication

### After Deployment
- [ ] All agents showing "Active"
- [ ] Test messages working
- [ ] Monitor logs for errors
- [ ] Document agent addresses
- [ ] Test protocol activation

## 🏆 Competition Deployment

### Recommended Approach

**For Competition Demo:**
1. Keep `DEPLOYMENT_MODE=local`
2. Run STEMI demo: `python scenarios/stemi_demo.py`
3. Show multi-patient: `python scenarios/multi_patient_demo.py`
4. Explain Agentverse capability

**For Production Claims:**
1. Deploy 1-2 agents to Agentverse
2. Screenshot the dashboard
3. Show agent addresses
4. Prove 24/7 capability

### Why This Approach?

- ✅ Demos run smoothly (no network issues)
- ✅ Easy to control and repeat
- ✅ Shows all features
- ✅ Proves Agentverse compatibility

## 📞 Support

### If You Need Help

**Agentverse Issues:**
- Discord: https://discord.gg/fetchai
- Forum: https://community.fetch.ai
- Docs: https://docs.fetch.ai

**EDFlow AI System:**
- Check logs in console
- Review README.md
- See QUICKSTART.md

## 🎓 Next Steps

1. **Test locally first** ✅ (STEMI demo working!)
2. **Run multi-patient demo** (just created)
3. **Deploy to Agentverse** (optional for competition)
4. **Record demo video** (5-7 minutes)
5. **Submit to competition** 🏆

Your system is ready for deployment whenever you need it!