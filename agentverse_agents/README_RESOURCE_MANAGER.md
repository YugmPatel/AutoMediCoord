# 📊 Resource Manager Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Overview

The Resource Manager agent handles overall emergency department capacity management, allocating trauma bays, assigning staff, and staging emergency equipment for incoming critical patients.

## Key Responsibilities

- **Capacity Assessment**: Monitors ED capacity, bed availability, and system load
- **Bay Allocation**: Assigns appropriate trauma bay based on protocol type
- **Staff Assignment**: Allocates nurses and physicians to incoming patient
- **Equipment Staging**: Ensures crash carts, defibrillators, and monitors are ready
- **Resource Optimization**: Balances current ED load with incoming emergency needs

## How It Works

1. Receives emergency broadcast from ED Coordinator
2. Fetches overall ED capacity from hospital database
3. Analyzes current patient load and staff availability
4. Allocates Trauma Bay 1 for critical cases
5. Assigns 2 RNs and 1 physician to bay
6. Stages crash cart and defibrillator
7. Verifies all equipment is functional
8. Reports resource allocation status

## Technical Details

- **Framework**: Fetch.ai uAgents v1.0.5
- **Database**: JSONBin for real-time capacity data
- **Response Time**: <2 seconds
- **Data Tracked**: Beds, staff, equipment, ED capacity percentage

## Agent Address

`agent1qdentzr0unjc5t8sylsha2ugv5yecpf80jw67qwwu4glgc84rr9u6w98f0c`

## Sample Response

```
📊 RESOURCE MANAGER AGENT REPORT

📊 DATA FETCHED FROM RESOURCE DATABASE:
• Total Beds: 45
• Available Beds: 12
• Nurses on Duty: 15 (8 available)
• Physicians on Duty: 6 (3 available)
• ED Capacity: 78%

🔧 ACTIONS TAKEN:
• Allocated Trauma Bay 1 for patient
• Assigned 2 RNs and 1 physician to bay
• Staged crash cart and defibrillator
• Verified all equipment functional

✅ CURRENT STATUS:
• Trauma Bay 1: Cleared and ready
• Staff: Assigned and briefed
• Equipment: Positioned and tested

⏱️ Resource allocation time: <2 minutes
```

---

**Part of EDFlow AI - Autonomous Emergency Department Coordination System**