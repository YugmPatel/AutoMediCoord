# 📱 WhatsApp Notification Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Overview

The WhatsApp Notification agent sends real-time alerts to medical staff phones via Twilio's WhatsApp API, ensuring instant communication with on-call physicians and nurses.

## Key Responsibilities

- **Instant Alerts**: Sends WhatsApp messages to medical staff within seconds
- **Protocol-Specific Messages**: Customizes alerts based on emergency type (STEMI, Stroke, Trauma)
- **Delivery Confirmation**: Tracks message delivery status
- **Contact Management**: Maintains verified medical staff phone numbers
- **Rich Context**: Includes patient details, ETA, and required actions in alerts

## How It Works

1. Receives emergency broadcast from ED Coordinator
2. Identifies protocol type from broadcast message
3. Selects appropriate medical staff contacts
4. Composes protocol-specific WhatsApp message
5. Sends via Twilio WhatsApp API
6. Tracks delivery confirmation
7. Reports notification status

## Technical Details

- **Framework**: Fetch.ai uAgents v1.0.5
- **API**: Twilio WhatsApp Business API
- **Response Time**: <30 seconds
- **Delivery Rate**: 98%+
- **Message Format**: Rich text with emojis and structured information

## Agent Address

`agent1qdvph9h02dhvs4vfk032hmpuaz3tm65p6n3ksgd9q5d22xyln3vqgkp2str`

## Sample Messages

**STEMI Alert:**
```
🚨 STEMI ALERT
Patient arriving in 5 min
Cath lab activation required
Please respond
```

**Stroke Alert:**
```
🧠 STROKE ALERT
Patient arriving in 5 min
CT scan and tPA ready
Please respond
```

**Trauma Alert:**
```
🚑 TRAUMA ALERT
Patient arriving in 5 min
Trauma bay ready
Please respond
```

## Sample Response

```
📱 WHATSAPP NOTIFICATION AGENT REPORT

📊 DATA FETCHED FROM HOSPITAL DATABASE:
• Specialist Categories: 4
• Available Contacts: 6
• Protocol Identified: STEMI

🔧 ACTIONS TAKEN:
• Identified protocol: STEMI
• Selected appropriate medical staff for notification
• Sent WhatsApp alerts to: Cardiologist, Charge Nurse
• Message content: Emergency protocol activation with ETA
• Timestamp: 2025-01-26T12:30:45Z

✅ CURRENT STATUS:
• Notifications sent: 2
• Delivery status: All delivered
• Staff alerted: Cardiologist, Charge Nurse
• Response expected: Within 2-5 minutes

⏱️ Notification time: <30 seconds
```

---

**Part of EDFlow AI - Autonomous Emergency Department Coordination System**