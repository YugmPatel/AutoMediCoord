# 👨‍⚕️ Specialist Coordinator Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Overview

The Specialist Coordinator agent manages specialist team activation, paging on-call physicians and coordinating procedure room preparation for incoming critical patients.

## Key Responsibilities

- **Specialist Roster**: Maintains real-time on-call specialist schedules
- **Team Paging**: Pages appropriate specialists (Cardiologist, Neurologist, Trauma Surgeon)
- **Procedure Room**: Activates cath lab, OR, or intervention suite
- **Response Tracking**: Monitors specialist response times and availability
- **Backup Coordination**: Identifies backup specialists if primary unavailable

## How It Works

1. Receives emergency broadcast from ED Coordinator
2. Queries specialist roster database
3. Identifies protocol-specific specialist (Cardiologist for STEMI)
4. Pages on-call specialist via hospital system
5. Activates procedure room (cath lab for STEMI)
6. Alerts support team (nurses, techs)
7. Reports specialist ETA and room status

## Technical Details

- **Framework**: Fetch.ai uAgents v1.0.5
- **Database**: JSONBin for specialist schedules
- **Response Time**: <1 second
- **Specialties**: Cardiology, Neurology, Trauma Surgery, Pediatrics
- **Procedure Rooms**: Cath Lab, OR, Intervention Suite

## Agent Address

`agent1qfx6rpglgl86s8072ja8y7fkk9pfg5csa2jg7h2vgkl2nztt2fctye7wngx`

## Sample Response

```
👨‍⚕️ SPECIALIST COORDINATOR AGENT REPORT

📊 DATA FETCHED FROM SPECIALIST DATABASE:
• Dr. Smith (Cardiology): Available, 15min response time
• Dr. Johnson (Neurology): Available, 20min response time
• Dr. Williams (Trauma Surgery): On-call, 10min response time

🔧 ACTIONS TAKEN:
• Identified protocol: STEMI
• Selected specialist team for STEMI
• Paged Dr. Smith (Cardiology) via hospital system
• Activated cath lab team
• Timestamp: 2025-01-26T12:30:45Z

✅ CURRENT STATUS:
• Specialist team: Paged and responding
• ETA: 15 minutes to hospital
• Backup team: On standby
• Cath lab: Reserved and preparing

⏱️ Team activation time: <1 minute
```

---

**Part of EDFlow AI - Autonomous Emergency Department Coordination System**