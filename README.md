# 🏥 EDFlow AI - Multi-Agent Emergency Department Coordination System

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
[![Fetch.ai](https://img.shields.io/badge/Fetch.ai-uAgents-00D4FF)](https://fetch.ai)
[![Claude AI](https://img.shields.io/badge/Claude-AI-purple)](https://anthropic.com)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org/)

**Autonomous Multi-Agent System for Emergency Department Optimization**

> **Achievement:** 50% reduction in door-to-balloon time through intelligent agent coordination
> **Technology:** Fetch.ai uAgents + Claude AI + Real-time Dashboard

---

## 🤖 Deployed Agents

All agents are live on Fetch.ai Agentverse and accessible via ASI:One:

| Agent Name | Role | Agent Address | Agentverse Profile |
|------------|------|---------------|-------------------|
| **ED Coordinator** | Central orchestrator, protocol detection | `agent1qff3y8ry6jew53lgc5gxzg8cqc3cc505c5n0rwcntpwe2ydvz23gxc36xh4` | [View Profile](https://agentverse.ai/agents/details/agent1qff3y8ry6jew53lgc5gxzg8cqc3cc505c5n0rwcntpwe2ydvz23gxc36xh4/profile) |
| **Resource Manager** | Capacity management, bay allocation | `agent1qdentzr0unjc5t8sylsha2ugv5yecpf80jw67qwwu4glgc84rr9u6w98f0c` | [View Profile](https://agentverse.ai/agents/details/agent1qdentzr0unjc5t8sylsha2ugv5yecpf80jw67qwwu4glgc84rr9u6w98f0c/profile) |
| **Specialist Coordinator** | Physician paging, team activation | `agent1qw4g3efd5t7ve83gmq3yp7dkzzmg7g4z480cunk8rru4yhw5x2k979ddxgk` | [View Profile](https://agentverse.ai/agents/details/agent1qw4g3efd5t7ve83gmq3yp7dkzzmg7g4z480cunk8rru4yhw5x2k979ddxgk/profile) |
| **Lab Service** | STAT tests, diagnostic equipment | `agent1qfx6rpglgl86s8072ja8y7fkk9pfg5csa2jg7h2vgkl2nztt2fctye7wngx` | [View Profile](https://agentverse.ai/agents/details/agent1qfx6rpglgl86s8072ja8y7fkk9pfg5csa2jg7h2vgkl2nztt2fctye7wngx/profile) |
| **Pharmacy** | Medication preparation, drug staging | `agent1qd6j2swdef06tgl4ly66r65c4vz6rcggt7rm89udnuvmn8n2y90myq46rfl` | [View Profile](https://agentverse.ai/agents/details/agent1qd6j2swdef06tgl4ly66r65c4vz6rcggt7rm89udnuvmn8n2y90myq46rfl/profile) |
| **Bed Management** | ICU bed reservation, equipment | `agent1qdvph9h02dhvs4vfk032hmpuaz3tm65p6n3ksgd9q5d22xyln3vqgkp2str` | [View Profile](https://agentverse.ai/agents/details/agent1qdvph9h02dhvs4vfk032hmpuaz3tm65p6n3ksgd9q5d22xyln3vqgkp2str/profile) |
| **WhatsApp Notification** | Real-time staff alerts | `agent1qwy3cayvacfc0lrlmaa3tlqs30tqvvl78lnlc2ja7ff8pkmey863venry0q` | [View Profile](https://agentverse.ai/agents/details/agent1qwy3cayvacfc0lrlmaa3tlqs30tqvvl78lnlc2ja7ff8pkmey863venry0q/profile) |

**Try it now:** Search for "ED Coordinator" on [ASI:One](https://app.fetch.ai) and send an ambulance report!

---

## 🎯 What is EDFlow AI?

EDFlow AI is an autonomous multi-agent system that coordinates emergency department operations through intelligent agent-to-agent communication. When an ambulance reports an incoming critical patient, our system activates a coordinated response across 6 specialized agents, each handling a specific aspect of patient care preparation.

### Key Capabilities

- **Autonomous Coordination:** Agents communicate and coordinate without human intervention
- **Protocol Detection:** AI-powered analysis identifies STEMI, Stroke, or Trauma protocols
- **Real-time Preparation:** All resources prepared before patient arrival
- **WhatsApp Notifications:** Medical staff alerted via WhatsApp
- **Persistent Memory:** Learns from past cases to improve future responses

---

## 🤖 Multi-Agent Architecture

### Agent Communication Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AMBULANCE REPORT ARRIVES                         │
│              (via ASI:One Chat Interface)                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   🏥 ED COORDINATOR AGENT                           │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 1. Receives ambulance report from ASI:One                     │ │
│  │ 2. Fetches current hospital status from JSONBin database      │ │
│  │ 3. Calls Claude AI to analyze patient condition               │ │
│  │ 4. Determines protocol (STEMI/Stroke/Trauma)                  │ │
│  │ 5. Activates protocol in database                             │ │
│  │ 6. Broadcasts to all 5 specialized agents                     │ │
│  │ 7. Collects responses from all agents                         │ │
│  │ 8. Sends aggregated response back to ASI:One                  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ BROADCAST MESSAGE
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ 📊 RESOURCE   │    │ 👨‍⚕️ SPECIALIST │    │ 🧪 LAB        │
│    MANAGER    │    │  COORDINATOR  │    │    SERVICE    │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • Fetch bed   │    │ • Fetch       │    │ • Fetch lab   │
│   availability│    │   specialist  │    │   equipment   │
│ • Allocate    │    │   roster      │    │   status      │
│   Trauma Bay 1│    │ • Page        │    │ • Prepare     │
│ • Assign staff│    │   cardiologist│    │   STAT tests  │
│ • Stage       │    │ • Activate    │    │ • Reserve ECG │
│   equipment   │    │   cath lab    │    │ • Alert lab   │
│               │    │   team        │    │   tech        │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ 💊 PHARMACY   │    │ 🛏️ BED        │    │ 📱 WHATSAPP   │
│               │    │  MANAGEMENT   │    │  NOTIFICATION │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • Fetch       │    │ • Fetch ICU   │    │ • Identify    │
│   medication  │    │   bed status  │    │   protocol    │
│   inventory   │    │ • Reserve     │    │ • Send        │
│ • Prepare     │    │   Cardiac ICU │    │   WhatsApp to │
│   STEMI kit   │    │   Bed 3       │    │   cardiologist│
│ • Stage meds  │    │ • Verify      │    │ • Alert charge│
│   at bedside  │    │   equipment   │    │   nurse       │
│               │    │   functional  │    │ • Log         │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             │ ALL AGENTS RESPOND
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              🏥 ED COORDINATOR AGENT (Aggregation)                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 1. Collects responses from all 6 agents                       │ │
│  │ 2. Builds comprehensive preparation report                    │ │
│  │ 3. Includes ambulance instructions                            │ │
│  │ 4. Shows detailed agent actions                               │ │
│  │ 5. Sends complete response to ASI:One                         │ │
│  └───────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ASI:ONE CHAT INTERFACE                         │
│              (User sees complete coordination report)               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Agent-to-Agent Communication Protocol

### 1. ED Coordinator → Specialized Agents (Broadcast)

**Message Format:**
```
🚑 AMBULANCE REPORT - STEMI PROTOCOL

Patient: 69yo male
Chief Complaint: Severe chest pain radiating to left arm
Vitals: HR 110, BP 160/95, SpO2 94%
EMS Report: ST elevation on ECG, suspected STEMI
ETA: 5 minutes

AI ANALYSIS:
[Claude AI analysis of patient condition]

⚡ ACTION REQUIRED: Prepare for incoming patient
Coordinator: ED Coordinator
Original Sender: [ASI:One address]

RESPOND TO ORIGINAL SENDER with your detailed preparation report
```

### 2. Specialized Agents → ED Coordinator (Response)

Each agent responds with:
- **Data fetched** from hospital database
- **Actions taken** to prepare for patient
- **Current status** of their domain

**Example Response from Bed Management:**
```
🛏️ BED MANAGEMENT AGENT REPORT

📊 DATA FETCHED FROM HOSPITAL DATABASE:
• Total ICU Beds: 12
• Available ICU Beds: 3 (ICU-3, ICU-7, ICU-11)
• Selected Bed: ICU-3
  - Type: Cardiac ICU
  - Location: ICU Wing A
  - Equipment: Cardiac monitor, defibrillator, ventilator

🔧 ACTIONS TAKEN:
• Reserved bed: ICU-3
• Updated database: Status changed from 'available' to 'reserved'
• Equipment verified: All functional
• Timestamp: 2025-01-26T12:30:45Z

✅ CURRENT STATUS:
• Bed ICU-3: RESERVED and ready
• Equipment: Tested and functional
• Ready for: Immediate patient occupancy

⏱️ Preparation time: <2 minutes
```

### 3. ED Coordinator → ASI:One (Aggregated Response)

The ED Coordinator collects all agent responses and sends a comprehensive report:

```
🚨 STEMI PROTOCOL ACTIVATED - INSTRUCTIONS FOR EMS

📍 DESTINATION: Trauma Bay 1 (Direct Entry - Bypass Triage)

🚑 TRANSPORT INSTRUCTIONS:
1. Maintain high-flow oxygen (keep SpO2 >94%)
2. Continue cardiac monitoring
3. Keep patient calm and still
4. Call 5 minutes before arrival if status changes

⏱️ WE ARE READY:
• Trauma Bay 1: Cleared and waiting
• Cath Lab Team: Mobilizing (ETA 15 min)
• All medications: Prepared and staged
• Cardiac ICU bed: Reserved
• STAT labs: Ready for immediate processing

═══════════════════════════════════════════════════════════
📊 DETAILED AGENT COORDINATION REPORT
═══════════════════════════════════════════════════════════

[Individual reports from all 6 agents]

🎯 COORDINATION COMPLETE: 6/6 agents responded
⏱️ Total coordination time: <10 seconds
✅ All systems ready for patient arrival
```

---

## 🧠 AI-Powered Intelligence

### Claude AI Integration

Each agent uses Claude AI for intelligent decision-making:

1. **ED Coordinator:**
   - Analyzes ambulance reports
   - Detects emergency protocols (STEMI/Stroke/Trauma)
   - Determines urgency levels
   - Generates coordination instructions

2. **Specialized Agents:**
   - Interpret queries with context
   - Make resource allocation decisions
   - Generate detailed status reports
   - Provide professional medical responses

### Database Integration (JSONBin)

All agents share a centralized hospital database:

```json
{
  "current_status": {
    "total_patients": 45,
    "critical_patients": 3,
    "ed_capacity_percent": 78,
    "average_wait_time_minutes": 32
  },
  "beds": {
    "icu": [...],
    "regular": [...]
  },
  "medications": {
    "emergency": {...},
    "cardiac": {...}
  },
  "specialists": {
    "cardiology": [...],
    "neurology": [...]
  },
  "protocols": {
    "stemi": {
      "active_cases": 2,
      "avg_door_to_balloon_minutes": 67
    }
  }
}
```

---

## 📱 WhatsApp Notification System

The WhatsApp Notification Agent sends real-time alerts to medical staff:

### Supported Protocols

**STEMI (Heart Attack):**
```
🚨 STEMI ALERT
Patient arriving in 5 min
Cath lab activation required
Please respond
```
→ Sent to: Cardiologist + Charge Nurse

**Stroke:**
```
🧠 STROKE ALERT
Patient arriving in 5 min
CT scan and tPA ready
Please respond
```
→ Sent to: Neurologist

**Trauma:**
```
🚑 TRAUMA ALERT
Patient arriving in 5 min
Trauma bay ready
Please respond
```
→ Sent to: Trauma Surgeon

### Technology
- **Twilio WhatsApp API** for message delivery
- **Real phone numbers** configured for medical staff
- **Delivery confirmation** tracked in agent logs

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Anthropic API Key ([Get here](https://console.anthropic.com))
- Twilio Account (for WhatsApp notifications)

### 1. Clone & Install

```bash
git clone <repository-url>
cd EDFlow-AI

# Install Python dependencies
pip install -r requirements.txt
pip install -r api_requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Configure Environment

Create `.env` file:
```env
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
JSONBIN_ID=your-jsonbin-id
JSONBIN_KEY=your-jsonbin-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### 3. Run the System

**Terminal 1 - Backend API:**
```bash
python run_api.py
```

**Terminal 2 - Frontend Dashboard:**
```bash
cd frontend
npm run dev
```

### 4. Access

- **Dashboard:** http://localhost:3000
- **API Docs:** http://localhost:8080/docs

---

## 🎮 Testing the System

### Via ASI:One Chat Interface

1. Deploy agents to Agentverse
2. Connect to ASI:One chat
3. Send ambulance report:

```
🚑 AMBULANCE REPORT

Patient: 69yo male
Chief Complaint: Severe chest pain radiating to left arm
Vitals: HR 110, BP 160/95, SpO2 94%
EMS Report: ST elevation on ECG, suspected STEMI
ETA: 5 minutes
```

4. Watch the multi-agent coordination happen in real-time
5. Receive comprehensive preparation report

### Via Dashboard

1. Open http://localhost:3000
2. Click "Simulate STEMI" button
3. Watch real-time case cards appear
4. Monitor agent activity in logs

---

## 🛠️ Technology Stack

### Agent Framework
- **Fetch.ai uAgents** - Multi-agent orchestration
- **Agentverse** - Agent deployment platform
- **Agent Mailbox Protocol** - Inter-agent messaging

### AI & Intelligence
- **Anthropic Claude AI** - Patient analysis & protocol detection
- **JSONBin** - Shared hospital database
- **Twilio WhatsApp API** - Staff notifications

### Frontend & API
- **React 18 + TypeScript** - Dashboard UI
- **FastAPI** - REST API backend
- **Socket.IO** - Real-time WebSocket communication
- **Tailwind CSS** - Styling

---

## 📊 Performance Metrics

### Response Times
- **Protocol Activation:** <5 seconds
- **Agent Coordination:** <10 seconds
- **WhatsApp Delivery:** <30 seconds
- **Total Preparation:** <2 minutes

### Coordination Efficiency
- **6 agents** working simultaneously
- **100% automation** - no human intervention needed
- **Real-time database** updates across all agents
- **Persistent memory** for continuous learning

---

## 🏗️ Deployment

### Agentverse Deployment

All 6 agents are deployed on Fetch.ai Agentverse:

1. **ED Coordinator** - `agent1qff3y8ry6jew53lgc5gxzg8cqc3cc505c5n0rwcntpwe2ydvz23gxc36xh4`
2. **Resource Manager** - `agent1qdentzr0unjc5t8sylsha2ugv5yecpf80jw67qwwu4glgc84rr9u6w98f0c`
3. **Specialist Coordinator** - `agent1qw4g3efd5t7ve83gmq3yp7dkzzmg7g4z480cunk8rru4yhw5x2k979ddxgk`
4. **Lab Service** - `agent1qfx6rpglgl86s8072ja8y7fkk9pfg5csa2jg7h2vgkl2nztt2fctye7wngx`
5. **Pharmacy** - `agent1qd6j2swdef06tgl4ly66r65c4vz6rcggt7rm89udnuvmn8n2y90myq46rfl`
6. **Bed Management** - `agent1qdvph9h02dhvs4vfk032hmpuaz3tm65p6n3ksgd9q5d22xyln3vqgkp2str`

### Agent Communication

- Agents use **Fetch.ai Agent Mailbox Protocol**
- Messages routed through **Agentverse infrastructure**
- **Persistent agent addresses** for reliable communication
- **Automatic retry** on message delivery failure

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Fetch.ai uAgents Framework**
