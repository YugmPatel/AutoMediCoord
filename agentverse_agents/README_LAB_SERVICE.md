# 🧪 Lab Service Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Overview

The Lab Service agent coordinates all laboratory and diagnostic testing, ensuring STAT tests are ordered and equipment is ready for incoming critical patients.

## Key Responsibilities

- **Test Ordering**: Orders protocol-specific STAT laboratory tests
- **Equipment Preparation**: Positions ECG machines and diagnostic equipment at bedside
- **Lab Technician Alert**: Notifies lab staff for priority processing
- **Turnaround Time**: Tracks expected test completion times
- **Priority Queue**: Sets CRITICAL priority for emergency cases

## How It Works

1. Receives emergency broadcast from ED Coordinator
2. Queries database for available diagnostic equipment
3. Identifies protocol-specific tests (Troponin for STEMI, CT for Stroke)
4. Orders STAT tests with CRITICAL priority
5. Reserves ECG machine for immediate use
6. Alerts lab technician for sample collection
7. Reports expected turnaround times

## Technical Details

- **Framework**: Fetch.ai uAgents v1.0.5
- **Database**: JSONBin for equipment and test inventory
- **Response Time**: <2 seconds
- **Equipment**: ECG, CT Scanner, Lab Analyzers
- **Tests**: Troponin, CBC, BMP, Coagulation panels

## Agent Address

`agent1qw4g3efd5t7ve83gmq3yp7dkzzmg7g4z480cunk8rru4yhw5x2k979ddxgk`

## Sample Response

```
🧪 LAB SERVICE AGENT REPORT

📊 DATA FETCHED FROM LAB DATABASE:
Equipment Status:
• ECG Machine: 3/4 available
• CT Scanner: 1/2 available
• Lab Analyzer: 2/2 available

Test Availability:
• Troponin: 15min turnaround, 50 tests available
• CBC/BMP: 20-25min turnaround, 100 tests available

🔧 ACTIONS TAKEN:
• Identified protocol: STEMI
• Prepared STAT test orders for STEMI
• Reserved ECG machine for immediate use
• Alerted lab technician for STAT processing
• Set priority: CRITICAL

✅ CURRENT STATUS:
• ECG: Ready at bedside
• Lab tech: Standing by for sample collection
• Test processing: STAT priority queue
• Expected results: Troponin 15min, CBC/BMP 20-25min

⏱️ Preparation time: <2 minutes
```

---

**Part of EDFlow AI - Autonomous Emergency Department Coordination System**