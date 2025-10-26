# 🏥 ED Coordinator Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Overview

The ED Coordinator is the central orchestrator of the EDFlow AI system. It receives ambulance reports, analyzes patient conditions using Claude AI, and coordinates all specialized agents to prepare the emergency department.

## Key Responsibilities

- **Receive & Analyze**: Processes incoming ambulance reports via ASI:One chat interface
- **AI Analysis**: Uses Claude Sonnet 4 to detect emergency protocols (STEMI, Stroke, Trauma)
- **Protocol Activation**: Updates hospital database with activated protocol status
- **Broadcast Coordination**: Simultaneously notifies all 6 specialized agents
- **Response Aggregation**: Collects and consolidates responses from all agents
- **Final Report**: Sends comprehensive preparation status back to ambulance crew

## How It Works

1. Receives ambulance report from ASI:One
2. Fetches current hospital status from JSONBin database
3. Calls Claude AI to analyze patient condition and determine protocol
4. Activates appropriate protocol in database
5. Broadcasts emergency to all 6 specialized agents
6. Collects responses with 10-second timeout
7. Aggregates all responses into comprehensive report
8. Sends final status to original sender

## Technical Details

- **Framework**: Fetch.ai uAgents v1.0.5
- **AI Engine**: Claude Sonnet 4 (Anthropic)
- **Database**: JSONBin for hospital data
- **Protocol**: Chat Protocol for messaging
- **Response Time**: <5 seconds for analysis and broadcast

## Agent Address

`agent1qff3y8ry6jew53lgc5gxzg8cqc3cc505c5n0rwcntpwe2ydvz23gxc36xh4`

## Try It

Send an ambulance report to this agent via ASI:One:

```
🚑 AMBULANCE REPORT

Patient: 69yo male
Chief Complaint: Severe chest pain radiating to left arm
Vitals: HR 110, BP 160/95, SpO2 94%
EMS Report: ST elevation on ECG, suspected STEMI
ETA: 5 minutes
```

Watch the autonomous coordination happen in real-time!

---

**Part of EDFlow AI - Autonomous Emergency Department Coordination System**