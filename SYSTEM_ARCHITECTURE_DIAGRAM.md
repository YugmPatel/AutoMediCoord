# EDFlow AI System Architecture

## Overall System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        React[React Dashboard]
        Components[UI Components]
        Store[State Management]
        Socket[Socket.IO Client]
    end

    subgraph "API Gateway Layer"
        FastAPI[FastAPI Wrapper]
        SocketServer[Socket.IO Server]
        REST[REST Endpoints]
    end

    subgraph "uAgents Backend"
        EDCoord[ED Coordinator]
        ResourceMgr[Resource Manager]
        Specialist[Specialist Coordinator]
        Lab[Lab Service]
        Pharmacy[Pharmacy Agent]
        BedMgmt[Bed Management]
    end

    subgraph "AI Layer"
        Claude[Claude AI Engine]
    end

    React --> Socket
    React --> REST
    Socket --> SocketServer
    REST --> FastAPI
    FastAPI --> EDCoord
    SocketServer --> EDCoord
    EDCoord --> ResourceMgr
    EDCoord --> Specialist
    EDCoord --> Lab
    EDCoord --> Pharmacy
    EDCoord --> BedMgmt
    EDCoord --> Claude
```

## Real-time Data Flow

```mermaid
sequenceDiagram
    participant UI as React Dashboard
    participant API as FastAPI Gateway
    participant Socket as Socket.IO Server
    participant ED as ED Coordinator
    participant Agents as Other Agents
    participant Claude as Claude AI

    Note over UI,Claude: Patient Arrival Scenario

    UI->>API: POST /api/simulate/stemi
    API->>ED: PatientArrivalNotification
    ED->>Claude: analyze_patient_acuity()
    Claude-->>ED: Analysis Result
    ED->>Agents: Protocol Activation
    ED->>Socket: patient_arrival event
    Socket-->>UI: Real-time update

    Note over UI,Claude: Ongoing Updates

    Agents->>ED: Status Updates
    ED->>Socket: case_update event
    Socket-->>UI: Live case updates

    Agents->>Socket: agent_message event
    Socket-->>UI: Chat messages
```

## Component Hierarchy

```mermaid
graph TD
    App[App.tsx]
    App --> Layout[Layout.tsx]

    Layout --> Header[Header.tsx]
    Layout --> Dashboard[Dashboard.tsx]
    Layout --> Chat[ChatInterface.tsx]

    Header --> Logo[Logo Component]
    Header --> LocationSelect[Location Selector]
    Header --> SimButtons[Simulation Buttons]
    Header --> TimeDisplay[Time Display]

    Dashboard --> Metrics[MetricsCards.tsx]
    Dashboard --> LiveCases[LiveCases.tsx]
    Dashboard --> ActivityLog[ActivityLog.tsx]

    Metrics --> MetricCard1[Active Cases]
    Metrics --> MetricCard2[Avg Lab ETA]
    Metrics --> MetricCard3[ICU Beds Held]
    Metrics --> MetricCard4[Doctors Paged]

    LiveCases --> CaseCard1[CASE-001 STEMI]
    LiveCases --> CaseCard2[CASE-002 STEMI]
    LiveCases --> CaseCard3[CASE-003 Stroke]

    Chat --> MessageList[Message History]
    Chat --> MessageInput[Input Field]
    Chat --> ActivityFeed[Activity Feed]

    ActivityLog --> TabNav[Lab/Pharm/Activity Tabs]
    ActivityLog --> LogEntries[Activity Entries]
```

## State Management Flow

```mermaid
graph LR
    subgraph "Zustand Stores"
        DashStore[Dashboard Store]
        ChatStore[Chat Store]
        AgentStore[Agent Store]
    end

    subgraph "React Components"
        Header[Header]
        Metrics[Metrics Cards]
        Cases[Live Cases]
        Chat[Chat Interface]
        Activity[Activity Log]
    end

    subgraph "Data Sources"
        API[REST API]
        Socket[WebSocket]
        Mock[Mock Data]
    end

    API --> DashStore
    Socket --> DashStore
    Socket --> ChatStore
    Socket --> AgentStore
    Mock --> DashStore

    DashStore --> Header
    DashStore --> Metrics
    DashStore --> Cases
    DashStore --> Activity

    ChatStore --> Chat
    AgentStore --> Cases
    AgentStore --> Activity
```

## WebSocket Event Flow

```mermaid
graph TD
    subgraph "uAgents Events"
        PatientArrival[patient_arrival]
        ProtocolActivation[protocol_activation]
        CaseUpdate[case_update]
        AgentMessage[agent_message]
        ResourceUpdate[resource_update]
        LabResult[lab_result]
        MedicationReady[medication_ready]
    end

    subgraph "Socket.IO Server"
        SocketServer[Socket.IO Server]
    end

    subgraph "React Frontend"
        Dashboard[Dashboard Components]
        Chat[Chat Interface]
        Notifications[Notifications]
    end

    PatientArrival --> SocketServer
    ProtocolActivation --> SocketServer
    CaseUpdate --> SocketServer
    AgentMessage --> SocketServer
    ResourceUpdate --> SocketServer
    LabResult --> SocketServer
    MedicationReady --> SocketServer

    SocketServer --> Dashboard
    SocketServer --> Chat
    SocketServer --> Notifications
```

## Development Workflow

```mermaid
graph LR
    subgraph "Phase 1: Foundation"
        Setup[Project Setup]
        Components[Basic Components]
        Styling[Tailwind Setup]
        MockData[Mock Data Service]
    end

    subgraph "Phase 2: UI Implementation"
        Header[Header Component]
        Dashboard[Dashboard Layout]
        Cases[Live Cases Grid]
        ChatUI[Chat Interface]
    end

    subgraph "Phase 3: Backend Integration"
        FastAPISetup[FastAPI Wrapper]
        SocketSetup[Socket.IO Server]
        APIEndpoints[REST Endpoints]
        RealTimeEvents[WebSocket Events]
    end

    subgraph "Phase 4: Advanced Features"
        ChatFunc[Chat Functionality]
        ActivityLog[Activity Logging]
        Simulations[Simulation Triggers]
        ErrorHandling[Error Handling]
    end

    subgraph "Phase 5: Production"
        Testing[Testing Suite]
        Performance[Optimization]
        Deployment[Production Deploy]
        Monitoring[Health Monitoring]
    end

    Setup --> Header
    Components --> Dashboard
    Styling --> Cases
    MockData --> ChatUI

    Header --> FastAPISetup
    Dashboard --> SocketSetup
    Cases --> APIEndpoints
    ChatUI --> RealTimeEvents

    FastAPISetup --> ChatFunc
    SocketSetup --> ActivityLog
    APIEndpoints --> Simulations
    RealTimeEvents --> ErrorHandling

    ChatFunc --> Testing
    ActivityLog --> Performance
    Simulations --> Deployment
    ErrorHandling --> Monitoring
```

This architecture ensures a scalable, maintainable, and real-time responsive frontend that seamlessly integrates with the existing uAgents backend system.
