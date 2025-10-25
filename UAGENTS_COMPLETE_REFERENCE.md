# uAgents Framework - Complete Reference Guide

**Version:** 1.0.5  
**Last Updated:** October 24, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Agent Communication](#agent-communication)
4. [Chat Protocol](#chat-protocol)
5. [Payment Protocol](#payment-protocol)
6. [Agentverse Platform](#agentverse-platform)
7. [Deployment Guide](#deployment-guide)
8. [Code Examples](#code-examples)
9. [Best Practices](#best-practices)

---

## Overview

The uAgents Framework enables creation of autonomous agents that can communicate, negotiate, and execute tasks. Agents can run locally or be hosted on Agentverse cloud platform.

### Key Features

- **Autonomous Operation**: Agents run independently with event-driven handlers
- **Secure Communication**: Blockchain-based identity and message verification
- **Protocol Support**: Built-in chat and payment protocols
- **Cloud Hosting**: Deploy on Agentverse for 24/7 uptime
- **REST Integration**: Expose agents via HTTP endpoints
- **Mailbox Service**: Receive messages even when offline

### Installation

```bash
pip install uagents uagents-core
```

---

## Core Concepts

### Agent Initialization

```python
from uagents import Agent, Context

# Local agent
agent = Agent(
    name="my_agent",
    port=8000,
    seed="my_recovery_phrase",  # Optional: for consistent address
    endpoint=["http://localhost:8000/submit"]
)

# Agentverse agent (mailbox-enabled)
agent = Agent(
    name="my_agent",
    mailbox=True
)
```


### Event Handlers

#### Startup Handler
```python
@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"Agent {ctx.agent.name} started")
    ctx.logger.info(f"Address: {ctx.agent.address}")
```

#### Shutdown Handler
```python
@agent.on_event("shutdown")
async def shutdown_handler(ctx: Context):
    ctx.logger.info("Agent shutting down")
```

#### Interval Handler
```python
@agent.on_interval(period=5.0)
async def periodic_task(ctx: Context):
    ctx.logger.info("Running periodic task")
```

### Data Models

```python
from uagents import Model

class MyMessage(Model):
    text: str
    value: int
    optional_field: str | None = None
```

---

## Agent Communication

### Communication Methods

#### 1. One-Way Communication (ctx.send)

Fire-and-forget messaging for notifications and updates.

```python
from uagents import Agent, Context, Model

class Message(Model):
    text: str

alice = Agent(name="alice", seed="alice phrase")
bob = Agent(name="bob", seed="bob phrase")

@alice.on_interval(period=2.0)
async def send_message(ctx: Context):
    await ctx.send(bob.address, Message(text="Hello Bob!"))

@bob.on_message(model=Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received from {sender}: {msg.text}")
```


#### 2. Request-Response Communication (ctx.send_and_receive)

Synchronous communication with response waiting (available from v0.21.1+).

```python
@alice.on_interval(period=5.0)
async def send_and_wait(ctx: Context):
    msg = Message(text="How are you?")
    reply, status = await ctx.send_and_receive(
        bob.address, 
        msg, 
        response_type=Message
    )
    
    if isinstance(reply, Message):
        ctx.logger.info(f"Got response: {reply.text}")
    else:
        ctx.logger.info(f"Failed: {status}")

@bob.on_message(model=Message)
async def respond(ctx: Context, sender: str, msg: Message):
    await ctx.send(sender, Message(text="I'm good!"))
```

### Running Multiple Agents

```python
from uagents import Bureau

bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

if __name__ == "__main__":
    bureau.run()
```

### REST Endpoints

Expose agents via HTTP for external integration.

```python
from typing import Dict, Any
import time

class Request(Model):
    text: str

class Response(Model):
    timestamp: int
    text: str
    agent_address: str

agent = Agent(name="rest_agent")

@agent.on_rest_get("/rest/get", Response)
async def handle_get(ctx: Context) -> Dict[str, Any]:
    return {
        "timestamp": int(time.time()),
        "text": "Hello from GET!",
        "agent_address": ctx.agent.address,
    }

@agent.on_rest_post("/rest/post", Request, Response)
async def handle_post(ctx: Context, req: Request) -> Response:
    return Response(
        text=f"Received: {req.text}",
        agent_address=ctx.agent.address,
        timestamp=int(time.time()),
    )
```

**Usage:**
```bash
# GET request
curl http://localhost:8000/rest/get

# POST request
curl -d '{"text": "test"}' -H "Content-Type: application/json" \
     -X POST http://localhost:8000/rest/post
```

---


## Chat Protocol

Standardized communication framework for structured agent conversations.

### Core Models

#### TextContent
```python
from uagents_core.contrib.protocols.chat import TextContent

class TextContent(Model):
    type: Literal['text']
    text: str
```

#### Resource Models
```python
class Resource(Model):
    uri: str
    metadata: dict[str, str]

class ResourceContent(Model):
    type: Literal['resource']
    resource_id: UUID4
    resource: Resource | list[Resource]
```

#### Session Control
```python
class StartSessionContent(Model):
    type: Literal['start-session']

class EndSessionContent(Model):
    type: Literal['end-session']
```

#### Stream Control
```python
class StartStreamContent(Model):
    type: Literal['start-stream']
    stream_id: UUID4

class EndStreamContent(Model):
    type: Literal['end-stream']
    stream_id: UUID4
```

#### Message Types
```python
class ChatMessage(Model):
    timestamp: datetime
    msg_id: UUID4
    content: list[AgentContent]  # List of content types

class ChatAcknowledgement(Model):
    timestamp: datetime
    acknowledged_msg_id: UUID4
    metadata: dict[str, str] | None = None
```


### Chat Protocol Implementation

#### Basic Chat Flow
1. Agent A sends `ChatMessage` to Agent B
2. Agent B sends `ChatAcknowledgement` back to Agent A
3. Agent B sends `ChatMessage` response to Agent A
4. Agent A sends `ChatAcknowledgement` back to Agent B

#### Example: Agent 1 (Initiator)
```python
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

agent1 = Agent(name="agent1", mailbox=True)
chat_proto = Protocol(spec=chat_protocol_spec)

# Agent2's address (replace with actual)
agent2_address = "agent1qf8n9q8ndlfvphmnwjzj9p077yq0m6kqc22se9g89y5en22sc38ck4p4e8d"

@agent1.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"Agent: {ctx.agent.name}, Address: {ctx.agent.address}")
    
    # Send initial message
    initial_message = ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text="Hello from Agent1!")]
    )
    await ctx.send(agent2_address, initial_message)

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    for item in msg.content:
        if isinstance(item, TextContent):
            ctx.logger.info(f"Received: {item.text}")
            
            # Send acknowledgment
            ack = ChatAcknowledgement(
                timestamp=datetime.utcnow(),
                acknowledged_msg_id=msg.msg_id
            )
            await ctx.send(sender, ack)
            
            # Send response
            response = ChatMessage(
                timestamp=datetime.utcnow(),
                msg_id=uuid4(),
                content=[TextContent(type="text", text="Hello from Agent1!")]
            )
            await ctx.send(sender, response)

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Ack received for: {msg.acknowledged_msg_id}")

agent1.include(chat_proto, publish_manifest=True)

if __name__ == '__main__':
    agent1.run()
```


#### Example: Agent 2 (Responder)
```python
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

agent2 = Agent(name="agent2", mailbox=True)
chat_proto = Protocol(spec=chat_protocol_spec)

@agent2.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"Agent: {ctx.agent.name}, Address: {ctx.agent.address}")

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    for item in msg.content:
        if isinstance(item, TextContent):
            ctx.logger.info(f"Received from {sender}: {item.text}")
            
            # Send acknowledgment
            ack = ChatAcknowledgement(
                timestamp=datetime.utcnow(),
                acknowledged_msg_id=msg.msg_id
            )
            await ctx.send(sender, ack)
            
            # Send response
            response = ChatMessage(
                timestamp=datetime.utcnow(),
                msg_id=uuid4(),
                content=[TextContent(type="text", text="Hello from Agent2!")]
            )
            await ctx.send(sender, response)

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Ack from {sender} for: {msg.acknowledged_msg_id}")

agent2.include(chat_proto, publish_manifest=True)

if __name__ == '__main__':
    agent2.run()
```

---


## Payment Protocol

Standardized framework for negotiating and finalizing payments between agents.

### Core Models

#### Funds
```python
class Funds(Model):
    amount: str              # Amount as string for precision
    currency: str            # USDC, FET, etc.
    payment_method: str = "fet_direct"  # skyfire, fet_direct
```

#### RequestPayment
```python
class RequestPayment(Model):
    accepted_funds: list[Funds]      # Acceptable payment options
    recipient: str                    # Payment recipient address
    deadline_seconds: int             # Validity window
    reference: str | None = None      # Optional reference
    description: str | None = None    # Optional description
    metadata: dict[str, str | dict[str, str]] | None = None
```

#### RejectPayment
```python
class RejectPayment(Model):
    reason: str | None = None
```

#### CommitPayment
```python
class CommitPayment(Model):
    funds: Funds                      # Exact funds to pay
    recipient: str                    # Recipient address
    transaction_id: str               # Unique transaction ID
    reference: str | None = None
    description: str | None = None
    metadata: dict[str, str | dict[str, str]] | None = None
```

#### CancelPayment
```python
class CancelPayment(Model):
    transaction_id: str | None = None
    reason: str | None = None
```

#### CompletePayment
```python
class CompletePayment(Model):
    transaction_id: str | None = None
```


### Protocol Specification

```python
from uagents_core.contrib.protocols.payment import payment_protocol_spec

payment_protocol_spec = ProtocolSpecification(
    name="AgentPaymentProtocol",
    version="0.1.0",
    interactions={
        RequestPayment: {CommitPayment, RejectPayment},
        CommitPayment: {CompletePayment, CancelPayment},
        CompletePayment: set(),
        CancelPayment: set(),
        RejectPayment: set(),
    },
    roles={
        "seller": {RequestPayment, CancelPayment, CompletePayment},
        "buyer": {CommitPayment, RejectPayment},
    },
)
```

### Payment Flow
1. Seller sends `RequestPayment` to Buyer
2. Buyer responds with `CommitPayment` or `RejectPayment`
3. If committed, Seller sends `CompletePayment` or `CancelPayment`

### Example: Seller Agent
```python
import os
from uuid import uuid4
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.payment import (
    Funds,
    RequestPayment,
    CommitPayment,
    RejectPayment,
    CompletePayment,
    payment_protocol_spec,
)

SELLER_PORT = 8091
BUYER_ADDRESS = "agent1q...replace_with_buyer_address..."

seller = Agent(
    name="seller", 
    port=SELLER_PORT, 
    endpoint=[f"http://localhost:{SELLER_PORT}/submit"]
)
payment_proto = Protocol(spec=payment_protocol_spec, role="seller")

@seller.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Seller address: {ctx.agent.address}")
    
    req = RequestPayment(
        accepted_funds=[
            Funds(currency="USDC", amount="0.001", payment_method="skyfire")
        ],
        recipient=ctx.agent.address,
        deadline_seconds=300,
        reference=str(uuid4()),
        description="demo payment",
        metadata={},
    )
    await ctx.send(BUYER_ADDRESS, req)

@payment_proto.on_message(CommitPayment)
async def on_commit(ctx: Context, sender: str, msg: CommitPayment):
    ctx.logger.info(f"Received CommitPayment: {msg}")
    await ctx.send(sender, CompletePayment(transaction_id=msg.transaction_id))

@payment_proto.on_message(RejectPayment)
async def on_reject(ctx: Context, sender: str, msg: RejectPayment):
    ctx.logger.info(f"Payment rejected: {msg.reason}")

seller.include(payment_proto, publish_manifest=True)

if __name__ == "__main__":
    seller.run()
```


### Example: Buyer Agent
```python
import os
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.payment import (
    Funds,
    RequestPayment,
    CommitPayment,
    RejectPayment,
    CompletePayment,
    payment_protocol_spec,
)

BUYER_PORT = 8092
BUYER_MODE = "commit"  # or "reject"

buyer = Agent(
    name="buyer", 
    port=BUYER_PORT, 
    endpoint=[f"http://localhost:{BUYER_PORT}/submit"]
)
payment_proto = Protocol(spec=payment_protocol_spec, role="buyer")

@payment_proto.on_message(RequestPayment)
async def on_request(ctx: Context, sender: str, msg: RequestPayment):
    ctx.logger.info(f"Received RequestPayment: {msg}")
    
    if not msg.accepted_funds:
        await ctx.send(sender, RejectPayment(reason="no accepted funds"))
        return
    
    selected = msg.accepted_funds[0]
    
    if BUYER_MODE == "reject":
        await ctx.send(sender, RejectPayment(reason="demo reject"))
        return
    
    commit = CommitPayment(
        funds=Funds(
            currency=selected.currency,
            amount=selected.amount,
            payment_method=selected.payment_method
        ),
        recipient=msg.recipient,
        transaction_id="demo-txn-001",
        reference=msg.reference,
        description=msg.description,
        metadata=msg.metadata or {},
    )
    await ctx.send(sender, commit)

@payment_proto.on_message(CompletePayment)
async def on_complete(ctx: Context, sender: str, msg: CompletePayment):
    ctx.logger.info(f"Payment completed: {msg}")

buyer.include(payment_proto, publish_manifest=True)

if __name__ == "__main__":
    buyer.run()
```

---


## Agentverse Platform

Cloud-based platform for hosting agents with continuous uptime.

### Key Features

- **Continuous Uptime**: Agents remain online 24/7
- **Integrated IDE**: Browser-based code editor
- **Blockchain Integration**: Built-in wallets for transactions
- **Marketplace**: Agent discovery via Almanac
- **Mailroom Service**: Offline message queuing
- **Scalability**: Auto-scaling based on load

### Getting API Key

1. Login to [Agentverse](https://agentverse.ai)
2. Go to Profile → API Keys
3. Click "+ New API Key"
4. Set name and permissions (30-day validity)
5. Complete authentication
6. Save the generated key (cannot be regenerated)

### Agent Discovery & Search

#### Search API
```python
import requests

body = {
    "filters": {
        "state": [],              # active, inactive
        "category": [],           # fetch-ai, community
        "agent_type": [],         # hosted, local, mailbox, proxy
        "protocol_digest": []
    },
    "sort": "relevancy",
    "direction": "asc",
    "search_text": "financial analysis",
    "offset": 0,
    "limit": 10,
}

response = requests.post(
    "https://agentverse.ai/v1/search",
    headers={"Authorization": "Bearer <your_token>"},
    json=body
)

agents = response.json()
```

#### Response Format
```json
[
  {
    "address": "agent1q...",
    "name": "Agent Name",
    "readme": "Description",
    "status": "active",
    "total_interactions": 10848,
    "recent_interactions": 10838,
    "rating": null,
    "type": "hosted",
    "category": "fetch-ai",
    "featured": true,
    "last_updated": "2025-01-06T12:46:03Z"
  }
]
```


### Agent Handles

Use handles for quick agent discovery and interaction.

```python
# Agent can be found using handle like @financial_agent
# Use in ASI:One chat: "@financial_agent analyze Apple stock"
```

### README Best Practices

A well-structured README improves discoverability and ranking.

#### Essential Elements

1. **Descriptive Title**: Use specific, keyword-rich titles
   - ✅ "AI Tutor for Middle School Algebra"
   - ❌ "TutorBot"

2. **Overview Section**: 2-4 sentence summary
   ```markdown
   This agent retrieves real-time stock prices for publicly traded companies.
   Simply input a ticker symbol (e.g., AAPL, TSLA) to get current prices.
   ```

3. **Use Cases**: 2-3 practical examples
   ```markdown
   - Get detailed revenue analysis from SEC filings
   - Analyze risk factors from latest 10-K
   - Track financial metrics and trends
   ```

4. **Data Models**: Document inputs/outputs
   ```markdown
   **Input Data Model**
   class StockPriceRequest(Model):
       ticker: str

   **Output Data Model**
   class StockPriceResponse(Model):
       price: float
   ```

5. **Tags**: Use badges for categorization
   ```markdown
   ![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
   ![tag:hackathon](https://img.shields.io/badge/hackathon-2E5CK3)
   ![tag:finance](https://img.shields.io/badge/finance-FF6B6B)
   ```

#### README Template
```markdown
![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:domain](https://img.shields.io/badge/finance-FF6B6B)

**Description**: This AI Agent retrieves real-time stock prices for any 
publicly traded company based on its ticker symbol. Simply input a stock 
ticker (e.g., AAPL, TSLA) to get the latest stock price.

**Use Cases**:
- Get current stock prices
- Monitor portfolio values
- Compare multiple stock prices

**Input Data Model**
class StockPriceRequest(Model):
    ticker: str

**Output Data Model**
class StockPriceResponse(Model):
    price: float
    timestamp: datetime
```


### Agent Registration with Agentverse

```python
from uagents import Identity
from uagents.registration import register_with_agentverse
import os

# Initialize identity
identity = Identity.from_seed(os.getenv("AGENT_SEED"), 0)

# Register agent
register_with_agentverse(
    identity=identity,
    url="http://localhost:8000/webhook",
    agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
    agent_title="My Financial Agent",
    readme="""
        <description>
        A comprehensive financial analysis agent that combines SEC filing 
        analysis with real-time market data.
        </description>
        <use_cases>
            <use_case>Get detailed revenue analysis from SEC filings</use_case>
            <use_case>Analyze risk factors from latest 10-K</use_case>
            <use_case>Track financial metrics and trends</use_case>
        </use_cases>
        <payload_requirements>
            <payload>
                <requirement>
                    <parameter>query</parameter>
                    <description>Financial analysis question</description>
                </requirement>
            </payload>
        </payload_requirements>
    """
)
```

---


## Deployment Guide

### Local Development

#### Single Agent
```python
from uagents import Agent

agent = Agent(
    name="my_agent",
    port=8000,
    endpoint=["http://localhost:8000/submit"]
)

if __name__ == "__main__":
    agent.run()
```

Run: `python agent.py`

#### Multiple Agents (Bureau)
```python
from uagents import Agent, Bureau

agent1 = Agent(name="agent1", port=8000, 
               endpoint=["http://localhost:8000/submit"])
agent2 = Agent(name="agent2", port=8001, 
               endpoint=["http://localhost:8001/submit"])

bureau = Bureau()
bureau.add(agent1)
bureau.add(agent2)

if __name__ == "__main__":
    bureau.run()
```

### Agentverse Deployment

#### Mailbox-Enabled Agent
```python
from uagents import Agent

agent = Agent(
    name="my_agent",
    mailbox=True  # Enable mailbox for Agentverse
)

if __name__ == "__main__":
    agent.run()
```

Steps:
1. Run agent locally: `python agent.py`
2. Open Agent Inspector link from logs
3. Connect to Agentverse via mailbox
4. Agent appears under "Local Agents" in Agentverse


### Render Deployment

Deploy agents on Render for 24/7 uptime.

#### Project Structure
```
asi-agent/
├── app.py
├── requirements.txt
├── .env
└── README.md
```

#### requirements.txt
```
uagents
uagents-core
openai>=1.0.0
python-dotenv
```

#### .env
```
ASI_API_KEY=sk-...
AGENT_SEED=my_recovery_phrase
AGENTVERSE_API_KEY=av-...
```

#### app.py (Example with ASI Integration)
```python
from datetime import datetime
from uuid import uuid4
import os
from dotenv import load_dotenv
from openai import OpenAI
from uagents import Context, Protocol, Agent
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

load_dotenv()

client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key=os.getenv("ASI_API_KEY"),
)

agent = Agent(
    name="ASI-agent",
    seed=os.getenv("AGENT_SEED"),
    mailbox=True,
)

protocol = Protocol(spec=chat_protocol_spec)

@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Send acknowledgment
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(), 
            acknowledged_msg_id=msg.msg_id
        ),
    )
    
    # Extract text
    text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text
    
    # Query ASI model
    response = "Sorry, I wasn't able to process that."
    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": text},
            ],
            max_tokens=2048,
        )
        response = str(r.choices[0].message.content)
    except Exception as e:
        ctx.logger.exception("Error querying model")
    
    # Send response
    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[
            TextContent(type="text", text=response),
            EndSessionContent(type="end-session"),
        ]
    ))

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
```


#### Render Deployment Steps

1. **Sign up** at [render.com](https://render.com)

2. **Push code** to GitHub/GitLab/Bitbucket

3. **Create Background Worker**:
   - Click "+ New" → "Background Worker"
   - Connect repository
   - Select repository

4. **Configure**:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Add environment variables:
     - `ASI_API_KEY`
     - `AGENT_SEED`
     - `AGENTVERSE_API_KEY`

5. **Deploy**: Click "Create Background Worker"

6. **Monitor**: Check logs for Agent Inspector link

7. **Connect**: Use Inspector link to connect to Agentverse

---


## Code Examples

### Complete Chat Agent Example

```python
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

# Initialize agent
agent = Agent(name="chat_agent", mailbox=True)
chat_proto = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Agent started: {ctx.agent.address}")

@chat_proto.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    # Send acknowledgment
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )
    
    # Process message
    for item in msg.content:
        if isinstance(item, TextContent):
            ctx.logger.info(f"Received: {item.text}")
            
            # Send response
            response = ChatMessage(
                timestamp=datetime.utcnow(),
                msg_id=uuid4(),
                content=[
                    TextContent(type="text", text=f"Echo: {item.text}")
                ]
            )
            await ctx.send(sender, response)

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Message acknowledged: {msg.acknowledged_msg_id}")

agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
```


### Complete Payment Agent Example

```python
from uuid import uuid4
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.payment import (
    Funds,
    RequestPayment,
    CommitPayment,
    RejectPayment,
    CompletePayment,
    payment_protocol_spec,
)

# Seller Agent
seller = Agent(name="seller", port=8091, 
               endpoint=["http://localhost:8091/submit"])
seller_proto = Protocol(spec=payment_protocol_spec, role="seller")

BUYER_ADDRESS = "agent1q..."  # Replace with actual

@seller.on_event("startup")
async def seller_startup(ctx: Context):
    ctx.logger.info(f"Seller: {ctx.agent.address}")
    
    # Request payment
    req = RequestPayment(
        accepted_funds=[
            Funds(currency="USDC", amount="10.00", payment_method="skyfire")
        ],
        recipient=ctx.agent.address,
        deadline_seconds=300,
        reference=str(uuid4()),
        description="Service payment"
    )
    await ctx.send(BUYER_ADDRESS, req)

@seller_proto.on_message(CommitPayment)
async def on_commit(ctx: Context, sender: str, msg: CommitPayment):
    ctx.logger.info(f"Payment committed: {msg.transaction_id}")
    # Process payment...
    await ctx.send(sender, CompletePayment(transaction_id=msg.transaction_id))

@seller_proto.on_message(RejectPayment)
async def on_reject(ctx: Context, sender: str, msg: RejectPayment):
    ctx.logger.info(f"Payment rejected: {msg.reason}")

seller.include(seller_proto, publish_manifest=True)

# Buyer Agent
buyer = Agent(name="buyer", port=8092, 
              endpoint=["http://localhost:8092/submit"])
buyer_proto = Protocol(spec=payment_protocol_spec, role="buyer")

@buyer_proto.on_message(RequestPayment)
async def on_request(ctx: Context, sender: str, msg: RequestPayment):
    ctx.logger.info(f"Payment requested: {msg.description}")
    
    if not msg.accepted_funds:
        await ctx.send(sender, RejectPayment(reason="No payment options"))
        return
    
    # Commit to payment
    selected = msg.accepted_funds[0]
    commit = CommitPayment(
        funds=selected,
        recipient=msg.recipient,
        transaction_id=f"txn-{uuid4()}",
        reference=msg.reference,
        description=msg.description
    )
    await ctx.send(sender, commit)

@buyer_proto.on_message(CompletePayment)
async def on_complete(ctx: Context, sender: str, msg: CompletePayment):
    ctx.logger.info(f"Payment completed: {msg.transaction_id}")

buyer.include(buyer_proto, publish_manifest=True)

# Run both agents
if __name__ == "__main__":
    from uagents import Bureau
    bureau = Bureau()
    bureau.add(seller)
    bureau.add(buyer)
    bureau.run()
```


### Multi-Agent System with Discovery

```python
import os
import requests
from uagents import Agent, Context, Model
from uagents.registration import register_with_agentverse
from uagents import Identity

class Query(Model):
    question: str

class Response(Model):
    answer: str

# Service Agent (to be discovered)
service_agent = Agent(name="service_agent", port=8000,
                      endpoint=["http://localhost:8000/submit"])

@service_agent.on_event("startup")
async def register_service(ctx: Context):
    # Register with Agentverse
    identity = Identity.from_seed(os.getenv("SERVICE_SEED"), 0)
    register_with_agentverse(
        identity=identity,
        url="http://localhost:8000/webhook",
        agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
        agent_title="Question Answering Service",
        readme="Answers general knowledge questions"
    )
    ctx.logger.info(f"Service registered: {ctx.agent.address}")

@service_agent.on_message(model=Query)
async def handle_query(ctx: Context, sender: str, msg: Query):
    ctx.logger.info(f"Query: {msg.question}")
    answer = f"Answer to: {msg.question}"
    await ctx.send(sender, Response(answer=answer))

# Client Agent (discovers and uses service)
client_agent = Agent(name="client_agent", port=8001,
                     endpoint=["http://localhost:8001/submit"])

def discover_service(search_term: str):
    """Search for agents on Agentverse"""
    response = requests.post(
        "https://agentverse.ai/v1/search",
        headers={"Authorization": f"Bearer {os.getenv('AGENTVERSE_API_KEY')}"},
        json={
            "search_text": search_term,
            "limit": 1
        }
    )
    agents = response.json()
    return agents[0]['address'] if agents else None

@client_agent.on_event("startup")
async def query_service(ctx: Context):
    # Discover service agent
    service_address = discover_service("Question Answering Service")
    
    if service_address:
        ctx.logger.info(f"Found service: {service_address}")
        await ctx.send(
            service_address,
            Query(question="What is the capital of France?")
        )
    else:
        ctx.logger.error("Service not found")

@client_agent.on_message(model=Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received answer: {msg.answer}")

# Run both agents
if __name__ == "__main__":
    from uagents import Bureau
    bureau = Bureau()
    bureau.add(service_agent)
    bureau.add(client_agent)
    bureau.run()
```


---

## Best Practices

### 1. Agent Design

#### Use Descriptive Names
```python
# Good
agent = Agent(name="financial_analysis_agent")

# Avoid
agent = Agent(name="agent1")
```

#### Use Seeds for Consistent Addresses
```python
# Consistent address across restarts
agent = Agent(name="my_agent", seed="my_recovery_phrase")
```

#### Enable Mailbox for Cloud Deployment
```python
# For Agentverse/Render deployment
agent = Agent(name="my_agent", mailbox=True)
```

### 2. Message Handling

#### Always Acknowledge Messages
```python
@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Send acknowledgment first
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(),
        acknowledged_msg_id=msg.msg_id
    ))
    # Then process message
    # ...
```

#### Use Type Checking
```python
for item in msg.content:
    if isinstance(item, TextContent):
        # Process text
        pass
    elif isinstance(item, ResourceContent):
        # Process resource
        pass
```

#### Handle Errors Gracefully
```python
@agent.on_message(model=Query)
async def handle_query(ctx: Context, sender: str, msg: Query):
    try:
        result = process_query(msg.question)
        await ctx.send(sender, Response(answer=result))
    except Exception as e:
        ctx.logger.error(f"Error processing query: {e}")
        await ctx.send(sender, Response(answer="Error processing request"))
```


### 3. Protocol Usage

#### Specify Roles for Protocol Specs
```python
# For payment protocol
payment_proto = Protocol(spec=payment_protocol_spec, role="seller")
# or
payment_proto = Protocol(spec=payment_protocol_spec, role="buyer")
```

#### Include Protocols with Manifest
```python
# Makes agent discoverable
agent.include(protocol, publish_manifest=True)
```

### 4. Environment Variables

#### Use .env Files
```python
from dotenv import load_dotenv
import os

load_dotenv()

agent = Agent(
    name="my_agent",
    seed=os.getenv("AGENT_SEED")
)

api_key = os.getenv("API_KEY")
```

#### Never Commit Secrets
```bash
# .gitignore
.env
*.key
secrets/
```

### 5. Logging

#### Use Context Logger
```python
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Agent started")
    ctx.logger.debug("Debug information")
    ctx.logger.error("Error occurred")
```

#### Log Important Events
```python
@agent.on_message(model=Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}")
    ctx.logger.debug(f"Message content: {msg}")
```


### 6. Testing

#### Test Locally First
```python
# Run single agent
if __name__ == "__main__":
    agent.run()

# Run multiple agents
if __name__ == "__main__":
    bureau = Bureau()
    bureau.add(agent1)
    bureau.add(agent2)
    bureau.run()
```

#### Use Different Ports
```python
agent1 = Agent(name="agent1", port=8000)
agent2 = Agent(name="agent2", port=8001)
```

#### Test Message Flow
```python
# Agent 1: Send test message on startup
@agent1.on_event("startup")
async def test_send(ctx: Context):
    await ctx.send(agent2.address, TestMessage(data="test"))

# Agent 2: Log received message
@agent2.on_message(model=TestMessage)
async def test_receive(ctx: Context, sender: str, msg: TestMessage):
    ctx.logger.info(f"Test passed: {msg.data}")
```

### 7. Documentation

#### Write Clear READMEs
- Use descriptive titles
- Include use cases
- Document data models
- Add relevant tags
- Provide examples

#### Document Code
```python
class FinancialQuery(Model):
    """
    Model for financial analysis queries.
    
    Attributes:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        query_type: Type of analysis ('price', 'fundamentals', 'news')
        timeframe: Analysis timeframe ('1d', '1w', '1m', '1y')
    """
    ticker: str
    query_type: str
    timeframe: str = "1d"
```


### 8. Performance

#### Use Intervals Wisely
```python
# Good: Reasonable interval
@agent.on_interval(period=60.0)  # Every minute
async def periodic_task(ctx: Context):
    pass

# Avoid: Too frequent
@agent.on_interval(period=0.1)  # Every 100ms - too frequent
async def bad_task(ctx: Context):
    pass
```

#### Batch Operations
```python
@agent.on_interval(period=300.0)  # Every 5 minutes
async def batch_process(ctx: Context):
    # Process multiple items at once
    items = get_pending_items()
    for item in items:
        await process_item(item)
```

#### Use Async Properly
```python
# Good: Await async operations
@agent.on_message(model=Query)
async def handle_query(ctx: Context, sender: str, msg: Query):
    result = await async_api_call(msg.question)
    await ctx.send(sender, Response(answer=result))

# Avoid: Blocking operations
@agent.on_message(model=Query)
async def bad_handler(ctx: Context, sender: str, msg: Query):
    result = blocking_api_call(msg.question)  # Blocks event loop
    await ctx.send(sender, Response(answer=result))
```

### 9. Security

#### Validate Input
```python
@agent.on_message(model=Query)
async def handle_query(ctx: Context, sender: str, msg: Query):
    # Validate input
    if not msg.question or len(msg.question) > 1000:
        ctx.logger.warning(f"Invalid query from {sender}")
        return
    
    # Process valid input
    result = process_query(msg.question)
    await ctx.send(sender, Response(answer=result))
```

#### Use Environment Variables for Secrets
```python
# Good
api_key = os.getenv("API_KEY")

# Never do this
api_key = "sk-1234567890abcdef"  # Hardcoded secret
```

#### Verify Sender
```python
TRUSTED_AGENTS = ["agent1q...", "agent1qw..."]

@agent.on_message(model=SensitiveRequest)
async def handle_sensitive(ctx: Context, sender: str, msg: SensitiveRequest):
    if sender not in TRUSTED_AGENTS:
        ctx.logger.warning(f"Unauthorized request from {sender}")
        return
    
    # Process trusted request
    # ...
```


### 10. Deployment

#### Use Process Managers
```bash
# For production, use process managers like systemd, supervisor, or PM2
pm2 start app.py --name my-agent --interpreter python3
```

#### Monitor Logs
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
```

#### Health Checks
```python
@agent.on_rest_get("/health", Response)
async def health_check(ctx: Context) -> Dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "agent_address": ctx.agent.address
    }
```

#### Graceful Shutdown
```python
@agent.on_event("shutdown")
async def cleanup(ctx: Context):
    ctx.logger.info("Cleaning up resources...")
    # Close connections, save state, etc.
    await cleanup_resources()
    ctx.logger.info("Shutdown complete")
```

---

## Quick Reference

### Common Imports
```python
# Core
from uagents import Agent, Context, Model, Protocol, Bureau
from uagents import Identity
from uagents.registration import register_with_agentverse

# Chat Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    ResourceContent,
    StartSessionContent,
    EndSessionContent,
    chat_protocol_spec,
)

# Payment Protocol
from uagents_core.contrib.protocols.payment import (
    Funds,
    RequestPayment,
    CommitPayment,
    RejectPayment,
    CompletePayment,
    CancelPayment,
    payment_protocol_spec,
)

# Utilities
from datetime import datetime
from uuid import uuid4
import os
from dotenv import load_dotenv
```


### Agent Initialization Patterns

```python
# Local agent with endpoint
agent = Agent(
    name="my_agent",
    port=8000,
    seed="recovery_phrase",
    endpoint=["http://localhost:8000/submit"]
)

# Mailbox-enabled agent (for Agentverse)
agent = Agent(
    name="my_agent",
    mailbox=True
)

# Agent with custom configuration
agent = Agent(
    name="my_agent",
    port=8000,
    seed="recovery_phrase",
    endpoint=["http://localhost:8000/submit"],
    log_level="DEBUG"
)
```

### Message Handler Patterns

```python
# Simple message handler
@agent.on_message(model=Message)
async def handle(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"From {sender}: {msg.text}")

# Protocol message handler
@protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    # Process message
    pass

# Multiple handlers for same model
@agent.on_message(model=Query)
async def handler1(ctx: Context, sender: str, msg: Query):
    if msg.type == "type1":
        # Handle type1
        pass

@agent.on_message(model=Query)
async def handler2(ctx: Context, sender: str, msg: Query):
    if msg.type == "type2":
        # Handle type2
        pass
```

### Event Handler Patterns

```python
# Startup
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Agent started")

# Shutdown
@agent.on_event("shutdown")
async def shutdown(ctx: Context):
    ctx.logger.info("Agent stopping")

# Interval
@agent.on_interval(period=60.0)
async def periodic(ctx: Context):
    ctx.logger.info("Periodic task")
```


### Communication Patterns

```python
# One-way send
await ctx.send(recipient_address, Message(text="Hello"))

# Request-response
reply, status = await ctx.send_and_receive(
    recipient_address,
    Query(question="What time is it?"),
    response_type=Response
)

if isinstance(reply, Response):
    ctx.logger.info(f"Got reply: {reply.answer}")
else:
    ctx.logger.error(f"Failed: {status}")

# Broadcast to multiple agents
recipients = ["agent1q...", "agent1qw...", "agent1qe..."]
for recipient in recipients:
    await ctx.send(recipient, Notification(message="Update available"))
```

### Protocol Patterns

```python
# Create protocol
protocol = Protocol(name="my_protocol")

# Create protocol with spec
protocol = Protocol(spec=chat_protocol_spec)

# Create protocol with role
protocol = Protocol(spec=payment_protocol_spec, role="seller")

# Include protocol in agent
agent.include(protocol, publish_manifest=True)

# Multiple protocols
chat_proto = Protocol(spec=chat_protocol_spec)
payment_proto = Protocol(spec=payment_protocol_spec, role="buyer")

agent.include(chat_proto, publish_manifest=True)
agent.include(payment_proto, publish_manifest=True)
```

---

## Troubleshooting

### Common Issues

#### Agent Address Changes
**Problem**: Agent address changes on restart  
**Solution**: Use a seed for consistent address
```python
agent = Agent(name="my_agent", seed="my_recovery_phrase")
```

#### Messages Not Received
**Problem**: Agent not receiving messages  
**Solution**: 
- Check agent is running
- Verify recipient address is correct
- Ensure both agents use same data model
- Check network connectivity

#### Protocol Errors
**Problem**: "Locked spec" or role errors  
**Solution**: Specify role when using protocol specs
```python
protocol = Protocol(spec=payment_protocol_spec, role="seller")
```


#### Mailbox Connection Issues
**Problem**: Agent not connecting to Agentverse mailbox  
**Solution**:
- Ensure `mailbox=True` in Agent initialization
- Check network/firewall allows outbound traffic
- Use Agent Inspector link from logs
- Verify Agentverse account is active

#### Import Errors
**Problem**: Cannot import protocol modules  
**Solution**: Install required packages
```bash
pip install uagents uagents-core
```

#### Port Already in Use
**Problem**: "Address already in use" error  
**Solution**: Use different port or kill existing process
```python
agent = Agent(name="my_agent", port=8001)  # Use different port
```

### Debugging Tips

#### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = Agent(name="my_agent", log_level="DEBUG")
```

#### Print Agent Address
```python
@agent.on_event("startup")
async def startup(ctx: Context):
    print(f"Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"Agent Address: {ctx.agent.address}")
```

#### Test Message Models
```python
# Test model serialization
msg = Message(text="test")
print(msg.json())
print(msg.dict())
```

#### Monitor Network Traffic
```python
@agent.on_message(model=Message)
async def log_all(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received from {sender}: {msg}")
```

---

## Resources

### Official Documentation
- [uAgents Documentation](https://docs.fetch.ai/uAgents)
- [Agentverse Platform](https://agentverse.ai)
- [Fetch.ai Developer Portal](https://fetch.ai/developers)

### Community
- [Discord](https://discord.gg/fetchai)
- [GitHub](https://github.com/fetchai/uAgents)
- [Forum](https://community.fetch.ai)

### Tools
- [Agent Inspector](https://agentverse.ai/inspect)
- [Almanac Explorer](https://explore.fetch.ai)
- [ASI:One Chat](https://asi1.ai)

---

## Appendix

### Environment Variables Reference

```bash
# Agent Configuration
AGENT_SEED=my_recovery_phrase
AGENT_PORT=8000

# Agentverse
AGENTVERSE_API_KEY=av-...

# External APIs
ASI_API_KEY=sk-...
OPENAI_API_KEY=sk-...

# Network
AGENT_ENDPOINT=http://localhost:8000/submit
```


### Data Model Examples

```python
# Simple model
class Message(Model):
    text: str

# Model with optional fields
class Query(Model):
    question: str
    context: str | None = None
    max_length: int = 100

# Model with nested types
class AnalysisRequest(Model):
    ticker: str
    metrics: list[str]
    timeframe: str
    metadata: dict[str, str] | None = None

# Model with validation
from pydantic import validator

class Payment(Model):
    amount: float
    currency: str
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('amount must be positive')
        return v
    
    @validator('currency')
    def currency_must_be_valid(cls, v):
        valid = ['USD', 'EUR', 'GBP', 'FET', 'USDC']
        if v not in valid:
            raise ValueError(f'currency must be one of {valid}')
        return v
```

### Complete Minimal Agent Template

```python
#!/usr/bin/env python3
"""
Minimal uAgent Template
"""
from uagents import Agent, Context, Model
from dotenv import load_dotenv
import os

load_dotenv()

# Define message model
class Message(Model):
    text: str

# Initialize agent
agent = Agent(
    name="my_agent",
    seed=os.getenv("AGENT_SEED", "default_seed"),
    port=int(os.getenv("AGENT_PORT", "8000")),
    endpoint=[os.getenv("AGENT_ENDPOINT", "http://localhost:8000/submit")]
)

# Startup handler
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Agent started: {ctx.agent.name}")
    ctx.logger.info(f"Address: {ctx.agent.address}")

# Message handler
@agent.on_message(model=Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received from {sender}: {msg.text}")
    await ctx.send(sender, Message(text=f"Echo: {msg.text}"))

# Shutdown handler
@agent.on_event("shutdown")
async def shutdown(ctx: Context):
    ctx.logger.info("Agent shutting down")

# Run agent
if __name__ == "__main__":
    agent.run()
```


### Complete Chat Agent Template

```python
#!/usr/bin/env python3
"""
Chat Protocol Agent Template
"""
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    EndSessionContent,
    chat_protocol_spec,
)
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize agent
agent = Agent(
    name=os.getenv("AGENT_NAME", "chat_agent"),
    seed=os.getenv("AGENT_SEED"),
    mailbox=True  # Enable for Agentverse
)

# Initialize chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Chat agent started: {ctx.agent.address}")

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Send acknowledgment
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )
    
    # Process message content
    response_text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            ctx.logger.info(f"Received: {item.text}")
            # Process and generate response
            response_text = f"You said: {item.text}"
    
    # Send response
    if response_text:
        await ctx.send(
            sender,
            ChatMessage(
                timestamp=datetime.utcnow(),
                msg_id=uuid4(),
                content=[
                    TextContent(type="text", text=response_text),
                    EndSessionContent(type="end-session")
                ]
            )
        )

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Message acknowledged: {msg.acknowledged_msg_id}")

# Include protocol
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
```

---

## Version History

- **1.0.5** (October 2025): Current version with full protocol support
- **0.21.1**: Added `ctx.send_and_receive` for synchronous communication
- **0.20.0**: Introduced mailbox service for Agentverse
- **0.19.0**: Added REST endpoint support
- **0.18.0**: Initial protocol specifications

---

## License

This documentation is provided for reference purposes. The uAgents framework is developed by Fetch.ai.

---

**End of Reference Guide**

For the latest updates and detailed API documentation, visit [docs.fetch.ai](https://docs.fetch.ai)
