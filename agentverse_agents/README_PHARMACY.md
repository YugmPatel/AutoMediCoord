# 💊 Pharmacy Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Overview

The Pharmacy agent manages medication preparation and delivery, ensuring protocol-specific medication kits are ready at bedside for incoming critical patients.

## Key Responsibilities

- **Medication Inventory**: Monitors real-time medication availability
- **Protocol Kits**: Prepares protocol-specific medication kits (STEMI, Stroke, Trauma)
- **Medication Staging**: Delivers medications to trauma bay before patient arrival
- **Drug Verification**: Ensures correct medications, dosages, and expiration dates
- **Pharmacist Consultation**: Makes pharmacist available for drug interaction checks

## How It Works

1. Receives emergency broadcast from ED Coordinator
2. Queries medication inventory database
3. Identifies protocol-specific medications (Aspirin, Heparin for STEMI)
4. Prepares complete medication kit
5. Labels all medications with patient info
6. Stages kit at Trauma Bay 1 medication cart
7. Reports medication readiness and location

## Technical Details

- **Framework**: Fetch.ai uAgents v1.0.5
- **Database**: JSONBin for medication inventory
- **Response Time**: <3 seconds
- **Medication Categories**: Emergency, Cardiac, Neurological, Trauma
- **Delivery Time**: <5 minutes to bedside

## Agent Address

`agent1qd6j2swdef06tgl4ly66r65c4vz6rcggt7rm89udnuvmn8n2y90myq46rfl`

## Sample Response

```
💊 PHARMACY AGENT REPORT

📊 DATA FETCHED FROM MEDICATION DATABASE:
• Aspirin: 500 tablets (Location: Emergency Cart)
• Heparin: 50 vials (Location: Pharmacy)
• Nitroglycerin: 100 tablets (Location: Cardiac Cart)
• Morphine: 30 vials (Location: Controlled Substances)

🔧 ACTIONS TAKEN:
• Identified protocol: STEMI
• Prepared STEMI-specific medication kit
• Medications drawn and labeled
• Staged location: Trauma Bay 1 medication cart
• Timestamp: 2025-01-26T12:30:45Z

✅ CURRENT STATUS:
• All STEMI medications: READY
• Delivery time: <5 minutes to bedside
• Pharmacist: Available for consultation
• Backup medications: Stocked and verified

⏱️ Preparation time: <3 minutes
```

---

**Part of EDFlow AI - Autonomous Emergency Department Coordination System**