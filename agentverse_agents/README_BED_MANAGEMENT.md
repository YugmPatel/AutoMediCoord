# 🛏️ Bed Management Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Overview

The Bed Management agent handles ICU and regular bed allocation, ensuring appropriate beds are reserved and equipped for incoming critical patients.

## Key Responsibilities

- **Bed Availability**: Monitors real-time ICU and regular bed status
- **Bed Reservation**: Reserves appropriate bed type based on patient acuity
- **Equipment Verification**: Ensures cardiac monitors, ventilators, and defibrillators are functional
- **Location Tracking**: Provides exact bed location for rapid patient placement
- **Database Updates**: Updates bed status from "available" to "reserved" in real-time

## How It Works

1. Receives emergency broadcast from ED Coordinator
2. Queries hospital database for available ICU beds
3. Selects appropriate bed based on protocol (Cardiac ICU for STEMI)
4. Reserves bed and updates database status
5. Verifies all bedside equipment is functional
6. Reports bed location and equipment status

## Technical Details

- **Framework**: Fetch.ai uAgents v1.0.5
- **Database**: JSONBin for bed inventory
- **Response Time**: <2 seconds
- **Bed Types**: ICU, Cardiac ICU, Regular
- **Equipment Tracked**: Monitors, ventilators, defibrillators

## Agent Address

`agent1qdvph9h02dhvs4vfk032hmpuaz3tm65p6n3ksgd9q5d22xyln3vqgkp2str`

## Sample Response

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
• Updated database: Status changed to 'reserved'
• Equipment verified: All functional
• Timestamp: 2025-01-26T12:30:45Z

✅ CURRENT STATUS:
• Bed ICU-3: RESERVED and ready
• Equipment: Tested and functional
• Ready for: Immediate patient occupancy

⏱️ Preparation time: <2 minutes
```

---

**Part of EDFlow AI - Autonomous Emergency Department Coordination System**