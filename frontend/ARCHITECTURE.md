# EDFlow AI Frontend Architecture

## Overview

React-based dashboard that replicates the EDFlow AI emergency department interface with real-time communication to the existing uAgents backend.

## Technology Stack

### Frontend

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling and dark theme
- **Socket.IO Client** for real-time WebSocket communication
- **React Query** for API state management
- **Zustand** for global state management
- **React Router** for navigation
- **Framer Motion** for animations
- **Lucide React** for icons

### Backend Integration

- **FastAPI** wrapper around existing uAgents
- **Socket.IO** server for real-time events
- **CORS** configuration for cross-origin requests
- **Pydantic** models for API serialization

## Component Architecture

```
src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx
│   ├── dashboard/
│   │   ├── MetricsCards.tsx
│   │   ├── LiveCases.tsx
│   │   ├── CaseCard.tsx
│   │   └── ActivityLog.tsx
│   ├── chat/
│   │   ├── ChatInterface.tsx
│   │   ├── MessageList.tsx
│   │   ├── MessageInput.tsx
│   │   └── ActivityFeed.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   └── Input.tsx
│   └── common/
│       ├── LoadingSpinner.tsx
│       ├── ErrorBoundary.tsx
│       └── StatusIndicator.tsx
├── hooks/
│   ├── useSocket.ts
│   ├── useAgentData.ts
│   ├── useRealTimeUpdates.ts
│   └── useChat.ts
├── services/
│   ├── api.ts
│   ├── socket.ts
│   ├── mockData.ts
│   └── types.ts
├── store/
│   ├── dashboardStore.ts
│   ├── chatStore.ts
│   └── agentStore.ts
├── utils/
│   ├── formatters.ts
│   ├── constants.ts
│   └── helpers.ts
└── styles/
    ├── globals.css
    └── components.css
```

## Data Flow Architecture

### Real-time Communication

```
uAgents Backend → FastAPI Wrapper → Socket.IO → React Frontend
```

### API Endpoints

```
GET  /api/dashboard/metrics     - Current ED metrics
GET  /api/cases/active          - Active patient cases
GET  /api/activity/recent       - Recent activity log
POST /api/simulate/stemi        - Trigger STEMI simulation
POST /api/simulate/stroke       - Trigger stroke simulation
GET  /api/agents/status         - Agent health status
```

### WebSocket Events

```
patient_arrival     - New patient notification
protocol_activation - Emergency protocol triggered
case_update        - Patient status change
agent_message      - Inter-agent communication
resource_update    - Bed/equipment status change
lab_result         - Laboratory results
medication_ready   - Pharmacy notifications
```

## UI Component Specifications

### Header Component

- Logo with medical cross icon
- Location selector dropdown
- Emergency department title
- Simulation buttons (STEMI/Stroke)
- Current time display
- Connection status indicator

### Dashboard Metrics

- **Active Cases**: Real-time count from agents
- **Avg Lab ETA**: Calculated from pending lab orders
- **ICU Beds Held**: Resource manager data
- **Doctors Paged**: Specialist coordinator data

### Live Cases Section

- Grid layout of patient case cards
- Each card shows:
  - Case ID and type (STEMI/Stroke/Trauma)
  - Duration timer
  - Vital signs (HR, BP, SpO2)
  - Current status and location
  - Lab ETA and pending actions
- Color-coded by urgency level
- Real-time updates via WebSocket

### Chat Interface

- Collapsible chat panel
- Message history with timestamps
- Real-time agent communications
- Message input with send functionality
- Activity feed showing recent actions
- Auto-scroll to latest messages

### Activity Log

- Tabbed interface (Lab, Pharm, Activity)
- Real-time activity stream
- Timestamped entries
- Status indicators (Ready, Pending, Complete)
- Filterable by agent type

## Styling & Theme

### Color Scheme (Dark Theme)

```css
--bg-primary: #1a1d29
--bg-secondary: #252837
--bg-card: #2d3142
--text-primary: #ffffff
--text-secondary: #a0a9c0
--accent-blue: #3b82f6
--accent-green: #10b981
--accent-red: #ef4444
--accent-yellow: #f59e0b
--border: #374151
```

### Typography

- **Primary Font**: Inter
- **Monospace**: JetBrains Mono (for case IDs, times)
- **Sizes**: text-xs to text-2xl following Tailwind scale

### Component Styling

- Rounded corners (rounded-lg)
- Subtle shadows and borders
- Hover states and transitions
- Status-based color coding
- Responsive breakpoints

## State Management

### Dashboard Store (Zustand)

```typescript
interface DashboardState {
  metrics: EDMetrics
  activeCases: PatientCase[]
  activityLog: ActivityEntry[]
  isConnected: boolean
  lastUpdate: Date
  updateMetrics: (metrics: EDMetrics) => void
  addCase: (case: PatientCase) => void
  updateCase: (caseId: string, updates: Partial<PatientCase>) => void
  addActivity: (activity: ActivityEntry) => void
}
```

### Chat Store

```typescript
interface ChatState {
  messages: ChatMessage[];
  isOpen: boolean;
  unreadCount: number;
  addMessage: (message: ChatMessage) => void;
  markAsRead: () => void;
  toggleChat: () => void;
}
```

## Real-time Integration

### Socket Connection

```typescript
const socket = io("ws://localhost:8080", {
  transports: ["websocket"],
  autoConnect: true,
});

socket.on("patient_arrival", (data) => {
  dashboardStore.addCase(data.case);
  chatStore.addMessage({
    type: "system",
    content: `New ${data.case.type} patient arrived`,
    timestamp: new Date(),
  });
});
```

### API Integration

```typescript
const useAgentData = () => {
  return useQuery({
    queryKey: ["dashboard-metrics"],
    queryFn: () => api.getDashboardMetrics(),
    refetchInterval: 5000, // Fallback polling
    enabled: !socket.connected,
  });
};
```

## Development Phases

### Phase 1: Core Setup

- React project initialization
- Component structure setup
- Basic styling with Tailwind
- Mock data service

### Phase 2: UI Implementation

- Header and navigation
- Dashboard metrics cards
- Live cases grid
- Basic chat interface

### Phase 3: Backend Integration

- FastAPI wrapper for uAgents
- Socket.IO server setup
- API endpoint implementation
- Real-time event handling

### Phase 4: Advanced Features

- Chat functionality
- Activity log
- Simulation triggers
- Error handling

### Phase 5: Polish & Deploy

- Responsive design
- Performance optimization
- Testing
- Production deployment

## Mock Data Structure

### Patient Cases

```typescript
interface PatientCase {
  id: string;
  type: "STEMI" | "Stroke" | "Trauma" | "General";
  duration: number; // minutes
  vitals: {
    hr: number;
    bp_sys: number;
    bp_dia: number;
    spo2: number;
  };
  status: "Arriving" | "Triaged" | "In Treatment" | "Pending";
  location: string;
  labETA?: number;
  assignedBed?: string;
  priority: 1 | 2 | 3 | 4 | 5;
}
```

### Activity Entries

```typescript
interface ActivityEntry {
  id: string;
  timestamp: Date;
  type: "Lab" | "Pharm" | "Bed" | "Doctor" | "System";
  message: string;
  status: "Ready" | "Pending" | "Complete" | "Failed";
  caseId?: string;
}
```

This architecture provides a solid foundation for building the EDFlow AI dashboard with real-time capabilities and seamless integration with the existing uAgents backend.
