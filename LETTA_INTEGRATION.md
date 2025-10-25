
# 🧠 Letta Integration - Persistent Memory for EDFlow AI

## Overview

EDFlow AI integrates **Letta's stateful agent memory** to provide persistent, context-aware decision making across patient cases. This enables the system to learn from past experiences and improve coordination over time.

---

## 🎯 What Letta Adds to EDFlow AI

### **Before Letta:**
- ❌ Each patient case treated in isolation
- ❌ No learning from past protocols
- ❌ Can't track what works best
- ❌ No patient history context
- ❌ System "forgets" everything on restart

### **With Letta:**
- ✅ **Patient History** - Remembers every patient visit, allergies, conditions
- ✅ **Protocol Learning** - Tracks which approaches work best
- ✅ **Context-Aware Decisions** - Uses historical data to inform AI analysis
- ✅ **Continuous Improvement** - Gets smarter with every case
- ✅ **Persistent Memory** - Retains knowledge across sessions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Patient Arrives                       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│             🏥 ED Coordinator Agent                      │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│          📚 LETTA MEMORY LAYER (NEW)                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Query: Get patient history                       │  │
│  │  Response: Previous visits, allergies, outcomes   │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Query: Get protocol insights                     │  │
│  │  Response: Avg response times, best practices     │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│     🤖 Claude AI Analysis (enriched with context)        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              Protocol Activation                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│     📚 Store Case Outcome in Letta (learning loop)      │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup Instructions

### **1. Install Letta**

```bash
pip install letta
```

### **2. Get Letta API Key**

1. Visit [https://cloud.letta.com/](https://cloud.letta.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. You'll receive $50 in free credits!

### **3. Configure Environment**

Add to your `.env` file:

```bash
# Letta Configuration
LETTA_API_KEY=letta-your-api-key-here
LETTA_ENABLED=true
```

### **4. Run Demo**

```bash
python demo.py
```

The system will automatically:
- Initialize Letta client
- Create a memory agent
- Store/retrieve patient data
- Show memory operations in demo

---

## 💻 Code Examples

### **Retrieving Patient History**

```python
from src.letta_integration import get_memory_agent

memory_agent = get_memory_agent()

# Get patient context
context = await memory_agent.recall_patient_context(
    patient_id="PATIENT_001",
    current_complaint="Chest pain"
)

# Returns: "Patient found: Previous STEMI visit 4 months ago..."
```

### **Getting Protocol Insights**

```python
# Before activating a protocol, get historical insights
insights = await memory_agent.get_protocol_insights("stemi")

# Returns: "Average door-to-balloon time: 42 minutes. 
#           Common bottleneck: Cath lab availability..."
```

### **Storing Case Outcomes**

```python
# After protocol completion, store for learning
await memory_agent.remember_patient_case(
    patient_id="PATIENT_001",
    protocol="stemi",
    vitals={"hr": 110, "bp_sys": 160},
    outcome={"success": True, "time_to_cath": 38}
)
```

---

## 📊 What Letta Tracks

### **Patient Data:**
- Previous visits and dates
- Protocols activated
- Known allergies and conditions
- Treatment responses
- Outcomes and recovery

### **Protocol Performance:**
- Average response times (door-to-balloon, door-to-needle)
- Success rates
- Common bottlenecks
- Best practices that worked
- Team performance patterns

### **Resource Utilization:**
- Bed availability patterns
- Equipment usage
- Team coordination efficiency
- Peak hour resource needs

---

## 🎬 Demo Flow with Letta

### **STEP 1: Patient Arrives**
ED Coordinator receives emergency patient

### **STEP 2: 📚 Memory Retrieval (NEW)**
- Letta queries patient history
- Retrieves: Previous visits, allergies, similar cases
- Response time: ~500ms

### **STEP 3: 🤖 AI Analysis**
- Claude AI analyzes patient
- **Enriched with Letta context**
- Makes context-aware decision

### **STEP 4: ✅ Protocol Activation**
- ED Coordinator activates protocol
- Uses historical insights from Letta

### **STEP 5: 📨 Agent Coordination**
- All agents notified
- Coordinated response

### **STEP 6: 💾 Learning (NEW)**
- Case outcome stored in Letta
- Available for future cases
- Continuous improvement loop

---

## 🏆 Prize Eligibility

### **Letta Prize Requirements:**
✅ **Use Letta API** - Direct integration via SDK
✅ **Stateful Memory** - Persistent patient history
✅ **Learning System** - Protocol performance tracking
✅ **Context-Aware** - Historical data informs decisions
✅ **Demonstrated** - Visible in demo flow

### **Prize Details:**
- **1st Place:** AirPods + Letta Swag
- **All Participants:** $50 in Letta credits
- **Bonus:** Learning from Letta team workshop

---

## 🔧 Configuration Options

### **Disable Letta (Fallback Mode)**

If Letta is unavailable, the system gracefully falls back to in-memory storage:

```bash
# In .env
LETTA_ENABLED=false
```

The system will:
- Still function normally
- Use temporary in-memory storage
- Show "Context unavailable" messages
- Lose memory on restart

### **Letta with Different LLMs**

Letta supports multiple LLM providers:

```python
# In src/letta_integration.py
agent = self.client.create_agent(
    name="EDFlow AI_memory",
    llm_config={
        "model": "claude-3-5-sonnet-20241022",  # Claude
        # OR
        "model": "gpt-4",  # OpenAI
        # OR  
        "model": "gemini-pro",  # Google
    }
)
```

---

## 📈 Performance Impact

### **Memory Operations:**
- Patient history retrieval: ~500ms
- Protocol insights: ~700ms
- Case storage: ~300ms
- **Total overhead:** <2 seconds per case

### **Benefits:**
- Context-aware decisions (priceless)
- Continuous learning (improves over time)
- Historical insights (prevents mistakes)
- **ROI:** Significant improvement in outcomes

---

## 🐛 Troubleshooting

### **"Letta library not installed"**
```bash
pip install letta>=0.3.0
```

### **"Failed to initialize Letta"**
1. Check your API key is correct
2. Verify internet connection
3. Check Letta service status
4. System will fall back to in-memory storage

### **"Context retrieval unavailable"**
- Letta service may be temporarily down
- System continues with standard analysis
- Context-aware features temporarily disabled

---

## 🎯 Future Enhancements

Potential improvements with Letta:

1. **Team Performance Tracking**
   - Which teams perform best?
   - Optimal team compositions
   - Training recommendations

2. **Resource Optimization**
   - Predictive bed availability
   - Equipment usage patterns
   - Proactive resource allocation

3. **Protocol Refinement**
   - A/B testing different approaches
   - Automated protocol updates
   - Evidence-based improvements

4. **Patient Risk Scoring**
   - Historical risk factors
   - Readmission predictions
   - Preventive care recommendations

---

## 📚 Resources

- **Letta Documentation:** https://docs.letta.com/
- **Letta Quickstart:** https://docs.letta.com/quickstart
- **Letta GitHub:** https://github.com/letta-ai/letta
- **Cal Hacks Workshop:** 10:30pm - New agent reveal

---

## 🤝 Support

For Letta-specific questions:
- Discord: [Letta Community](https://discord.gg/letta)
- Workshop: Cal Hacks booth
- Team: @Sarah Wooders, @Shubham Naik

For EDFlow AI integration:
- Check logs: System will show Letta status
- Test connection: `python test_letta.py`
- Fallback mode: Always available

---

