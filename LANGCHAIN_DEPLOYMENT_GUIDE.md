# LangChain + Claude AI Enhanced Orchestrator - Deployment Guide

## 🎯 Overview

This guide covers deploying the **AI-enhanced orchestrator** that uses:
- **Claude AI** for intelligent reasoning
- **LangChain** for AI orchestration and routing
- **uAgents** for agent communication
- **Chat Protocol** for ASI:One compatibility

## 🆚 Version Comparison

### Simple Version (ed_coordinator_orchestrator.py)
- ✅ Keyword-based routing
- ✅ Fast (<1ms routing)
- ✅ No AI dependencies
- ✅ No API costs
- ❌ Limited to exact keywords

### AI-Enhanced Version (ed_coordinator_langchain_claude.py) ⭐
- ✅ Natural language understanding
- ✅ Intelligent intent classification  
- ✅ Context-aware agent selection
- ✅ Adaptive reasoning
- ⚠️ Requires Claude API key
- ⚠️ ~100-500ms AI processing
- ⚠️ API costs per query

## 📦 What You Get

### File Structure
```
agentverse_agents/
├── ed_coordinator_langchain_claude.py  ← Main agent file (726 lines)
├── requirements_langchain.txt          ← Dependencies
└── .env                                ← Environment config (create this)
```

### Key Features

#### 1. **AI-Powered Intent Classification** 🤖
```python
User: "We have a heart attack patient coming in"
AI: 
  - Understands context (heart attack = STEMI)
  - Classifies as "protocol" type
  - Identifies "stemi" protocol
  - Provides confidence score
  - Executes multi-agent coordination
```

#### 2. **Intelligent Agent Selection** 🎯
```python
User: "Can we accommodate a critical patient who needs monitoring?"
AI:
  - Analyzes requirements
  - Selects: bed_manager (for ICU), resource_manager (for monitoring equipment)
  - Routes query appropriately
  - Provides reasoning
```

#### 3. **Natural Language Processing** 💬
```python
User: "What's the situation with beds and equipment?"
AI:
  - Understands composite query
  - Routes to multiple agents
  - Returns coordinated response
```

## 🚀 Deployment Steps

### Step 1: Prerequisites

**Required:**
- Agentverse account
- Anthropic API key ([Get here](https://console.anthropic.com))
- Your 6 agents deployed (addresses in code)

**Check:**
```bash
# Verify you have Anthropic API key
echo $ANTHROPIC_API_KEY

# Or on Windows
echo %ANTHROPIC_API_KEY%
```

### Step 2: Configure Environment

#### Option A: In Agentverse UI

1. Go to Agentverse → Your ED Coordinator
2. Go to "Secrets" or "Environment" tab
3. Add secret:
   - Key: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-api03-...` (your key)

#### Option B: Local .env File (for testing)

Create `agentverse_agents/.env`:
```env
# Anthropic Claude AI
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Agent Configuration
ED_COORDINATOR_SEED=ed_coordinator_phrase_001
```

### Step 3: Upload to Agentverse

#### Via UI (Recommended)

1. **Navigate** to Agentverse → ED Coordinator → Build

2. **Upload Main File**:
   - Click "Upload" or "New File"
   - Name: `agent.py`
   - Paste contents of [`ed_coordinator_langchain_claude.py`](agentverse_agents/ed_coordinator_langchain_claude.py:1)

3. **Upload Requirements**:
   - Click "Add File"
   - Name: `requirements.txt`
   - Paste contents of [`requirements_langchain.txt`](agentverse_agents/requirements_langchain.txt:1)

4. **Configure Secrets**:
   - Go to "Secrets" tab
   - Add `ANTHROPIC_API_KEY`

5. **Deploy**:
   - Click "Deploy" button
   - Wait for build to complete (~2-3 minutes for dependencies)

### Step 4: Verify Deployment

Check logs for:
```
🏥 ED Coordinator with Claude AI + LangChain started
📍 Agent address: agent1qgucygwnndlwvemlrg6r676unu50eaya2fqdcdr4ljwjxwnw2fun55t27su
✅ Chat Protocol enabled - Ready for ASI:One
🤖 Claude AI enabled for intelligent routing
🔗 LangChain integration active
🔄 Can coordinate 5 agents
🚨 Emergency protocols: stemi, stroke, trauma
```

**Success indicators:**
- ✅ No import errors
- ✅ Claude AI enabled message
- ✅ LangChain integration message
- ✅ Agent address shown

## 🧪 Testing

### Test 1: Natural Language Protocol Activation

**Send:**
```
"We have a patient with chest pain and suspected heart attack"
```

**Expected AI Behavior:**
1. Claude analyzes: "chest pain + heart attack = STEMI"
2. Classifies as protocol type
3. Identifies STEMI protocol
4. Coordinates 5 agents
5. Returns comprehensive status

**Look for in logs:**
```
🤖 Using Claude AI for intent classification...
   AI Classification: protocol (confidence: 0.95)
   Reasoning: Patient symptoms indicate cardiac emergency
🚨 Executing STEMI Protocol with AI coordination
```

### Test 2: Intelligent Agent Routing

**Send:**
```
"Do we have capacity for a critical care patient?"
```

**Expected AI Behavior:**
1. Claude understands: "critical care" needs ICU + resources
2. Selects: bed_manager, resource_manager
3. Routes to both
4. Provides reasoning

**Look for in logs:**
```
🤖 Using Claude AI for agent selection...
   Selected agents: bed_manager, resource_manager
   Reasoning: Critical care requires ICU beds and monitoring resources
```

### Test 3: Ambiguous Query Handling

**Send:**
```
"Patient needs urgent attention, what's available?"
```

**Expected AI Behavior:**
1. Claude recognizes urgency
2. Interprets "what's available" as resource query
3. Routes to resource_manager
4. Provides context-aware response

### Test 4: Fallback Mechanism

**With API key removed (testing robustness):**

**Send:**
```
"activate stemi protocol"
```

**Expected Behavior:**
1. AI parsing attempts first
2. Fails (no API key)
3. Falls back to keyword matching
4. Still executes protocol successfully

**Look for in logs:**
```
❌ AI intent parsing failed: ...
   Falling back to keyword-based parsing...
   Keyword Classification: stemi (confidence: 0.9)
```

## 📊 AI Enhancement Features

### 1. Intent Classification

**How it works:**
```python
# User query → Claude AI → Structured intent

User: "We need to prepare for a stroke patient"
      ↓
Claude analyzes:
  - "stroke" = medical emergency
  - "prepare" = protocol activation
  - Context: emergency department
      ↓
Result: {
  "type": "protocol",
  "protocol": "stroke",
  "reasoning": "Stroke keyword with preparation context",
  "confidence": 0.92
}
```

**Benefits:**
- Understands variations ("heart attack" = "STEMI")
- Handles typos and natural language
- Provides confidence scores
- Explains reasoning

### 2. Agent Selection

**How it works:**
```python
# Query → Claude → Best agent(s)

User: "Need to check on medication prep and lab readiness"
      ↓
Claude selects:
  - pharmacy (medication prep)
  - lab_service (lab readiness)
      ↓
Routes to both agents simultaneously
```

**Benefits:**
- Multi-agent queries handled intelligently
- Context-aware selection
- Explains why agents were chosen
- Adapts to query complexity

### 3. Natural Language Understanding

**Examples:**

| User Says | AI Understands | Action |
|-----------|----------------|--------|
| "Heart attack patient incoming" | STEMI protocol | Activate protocol |
| "Check if we can admit" | Resource/bed query | Route to bed_manager |
| "Med prep status?" | Pharmacy query | Route to pharmacy |
| "Everything ready for trauma?" | Trauma protocol check | Route to multiple agents |

## 🎛️ Configuration Options

### Adjust AI Behavior

Edit `ed_coordinator_langchain_claude.py`:

#### 1. Change AI Model
```python
# Line ~94
def get_claude_llm():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",  # Current: Most capable
        # model="claude-3-haiku-20240307",   # Faster, cheaper
        # model="claude-3-opus-20240229",    # Most powerful
        temperature=0.1,  # Low = consistent, High = creative
        max_tokens=500
    )
```

#### 2. Adjust Confidence Thresholds
```python
# Add after line ~219 in parse_intent_with_ai
if result.get('confidence', 0) < 0.7:
    # Fall back to keyword matching for low confidence
    return fallback_intent_parse(query)
```

#### 3. Enable Response Enhancement (Optional)
```python
# Uncomment and use after line ~607
# enhancement_chain = create_response_enhancement_chain()
# enhanced = enhancement_chain.invoke({
#     "query": text,
#     "responses": json.dumps(responses)
# })
```

## 💰 Cost Considerations

### API Usage

**Per Query:**
- Intent classification: ~$0.001-0.003
- Agent selection: ~$0.001-0.002
- Total per query: ~$0.002-0.005

**Daily Estimates:**
- 100 queries/day: $0.20-0.50
- 500 queries/day: $1.00-2.50
- 1000 queries/day: $2.00-5.00

**Optimization Tips:**
1. Use cache for common queries
2. Increase fallback threshold
3. Use Haiku model for non-critical queries
4. Batch similar queries

## 🔄 Fallback Strategy

### Three-Tier Approach

```
User Query
    ↓
Tier 1: Claude AI (Primary)
    ├─ Success → AI-powered routing ✅
    ├─ API Error → Tier 2
    └─ Timeout → Tier 2
        ↓
Tier 2: Keyword Matching (Fallback)
    ├─ Match found → Route ✅
    ├─ No match → Tier 3
    └─ Ambiguous → Tier 3
        ↓
Tier 3: Default Handling
    └─ Local processing or help message
```

**Reliability:**
- System remains operational even if Claude API fails
- Graceful degradation
- User always gets response

## 🚨 Troubleshooting

### Issue: "ANTHROPIC_API_KEY not set"

**Symptoms:**
```
⚠️ ANTHROPIC_API_KEY not set - AI routing unavailable
   Will fall back to keyword-based routing
```

**Solutions:**
1. Add API key to Agentverse Secrets
2. Create `.env` file with key
3. Set environment variable before running

### Issue: "Import Error: langchain"

**Symptoms:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Solutions:**
1. Ensure `requirements.txt` uploaded to Agentverse
2. Wait for build to complete (can take 2-3 min)
3. Check Build logs for installation errors
4. Manually trigger rebuild

### Issue: "AI routing slow"

**Symptoms:**
- Queries take >2 seconds
- Logs show multiple retries

**Solutions:**
1. Switch to Haiku model (faster)
2. Reduce max_tokens
3. Check network connectivity
4. Add local caching

### Issue: "Incorrect agent selection"

**Symptoms:**
- AI routes to wrong agent
- Multiple queries needed

**Solutions:**
1. Improve prompt specificity
2. Add examples to system prompt
3. Adjust temperature (lower = more deterministic)
4. Review agent selection logs

## 📈 Monitoring

### Key Metrics to Track

**From Logs:**
```
💓 Health Check:
   📊 Active Cases: X
   🛏️ Available Beds: Y
   📞 Total Queries: Z
   🤖 AI Routings: N
```

**Calculate:**
- AI success rate: AI Routings / Total Queries
- Fallback rate: (Total - AI) / Total
- Average confidence: Check logs for confidence scores

### Performance Benchmarks

**Target Metrics:**
- AI intent classification: <500ms
- Agent selection: <300ms
- Total query processing: <1000ms
- Fallback rate: <10%
- AI confidence: >0.8 average

## 🎯 Best Practices

### 1. Environment Management
- ✅ Use Agentverse Secrets for API keys
- ✅ Never commit keys to code
- ✅ Rotate keys regularly

### 2. Error Handling
- ✅ Always have fallback logic
- ✅ Log AI failures for debugging
- ✅ Return helpful error messages

### 3. Cost Optimization
- ✅ Cache common queries
- ✅ Use appropriate model for task
- ✅ Set reasonable token limits

### 4. Monitoring
- ✅ Track AI usage metrics
- ✅ Monitor confidence scores
- ✅ Alert on high fallback rates

## 📚 Additional Resources

- **LangChain Docs**: https://python.langchain.com/docs/get_started/introduction
- **Claude API**: https://docs.anthropic.com/claude/reference/getting-started-with-the-api
- **uAgents Docs**: https://docs.fetch.ai
- **Agentverse**: https://agentverse.ai

## 🎉 Success Checklist

After deployment, verify:

- [ ] Agent starts without errors
- [ ] Claude AI enabled message in logs
- [ ] LangChain integration active
- [ ] "Heart attack patient" activates STEMI protocol
- [ ] Natural language queries work
- [ ] Fallback works when API unavailable
- [ ] No import errors
- [ ] AI routing counter increments
- [ ] Confidence scores logged
- [ ] Response times acceptable (<1s)

---

**Status**: ✅ Production-ready AI-enhanced orchestrator  
**AI Model**: Claude 3.5 Sonnet  
**Framework**: LangChain  
**Routing**: AI-powered with keyword fallback  
**Reliability**: High (three-tier fallback)  

**Deploy with confidence!** 🚀 Your orchestrator now has human-level understanding with AI-powered reasoning.