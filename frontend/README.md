# EDFlow AI Dashboard - Frontend

A modern React-based dashboard for the EDFlow AI emergency department coordination system, featuring real-time patient monitoring, agent communication, and protocol management.

## 🚀 Features

- **Real-time Dashboard**: Live patient cases, metrics, and activity monitoring
- **Agent Communication**: Chat interface with autonomous agents
- **Protocol Simulation**: STEMI and Stroke protocol triggers
- **Dark Theme UI**: Modern, medical-grade interface design
- **WebSocket Integration**: Real-time updates from uAgents backend
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

### Technology Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Socket.IO** for real-time communication
- **Zustand** for state management
- **React Query** for API state management
- **Framer Motion** for animations

### Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── layout/         # Layout components
│   │   ├── dashboard/      # Dashboard-specific components
│   │   ├── chat/          # Chat interface components
│   │   ├── ui/            # Reusable UI components
│   │   └── common/        # Common components
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API and WebSocket services
│   ├── store/             # Zustand state stores
│   ├── utils/             # Utility functions
│   └── styles/            # CSS styles
├── public/                # Static assets
└── docs/                  # Documentation
```

## 🛠️ Development Setup

### Prerequisites

- Node.js 18+ and npm
- AutoMediCoord backend running on port 8080

### Installation

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start development server**

   ```bash
   npm run dev
   ```

4. **Open browser**
   ```
   http://localhost:3000
   ```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## 🎨 UI Components

### Header

- **Logo**: EDFlow AI branding with medical cross
- **Location Selector**: Hospital/department selection
- **Simulation Buttons**: Trigger STEMI/Stroke scenarios
- **Time Display**: Current time with real-time updates
- **Connection Status**: WebSocket connection indicator

### Dashboard Metrics

- **Active Cases**: Real-time patient count
- **Avg Lab ETA**: Average laboratory turnaround time
- **ICU Beds Held**: Reserved ICU bed count
- **Doctors Paged**: Specialist notifications sent

### Live Cases

- **Patient Cards**: Individual case monitoring
  - Case ID and protocol type
  - Duration timer
  - Vital signs (HR, BP, SpO2)
  - Current status and location
  - Lab ETA and pending actions
- **Color Coding**: Priority-based visual indicators
- **Real-time Updates**: Live status changes

### Chat Interface

- **Message History**: Agent communication log
- **Real-time Messages**: Live agent updates
- **Activity Feed**: Recent system activities
- **Message Input**: Send messages to agents
- **Collapsible Panel**: Space-efficient design

### Activity Log

- **Tabbed Interface**: Lab, Pharmacy, Activity views
- **Real-time Stream**: Live activity updates
- **Status Indicators**: Visual status representation
- **Timestamp Display**: Precise timing information

## 🔌 Backend Integration

### API Endpoints

```
GET  /api/dashboard/metrics     # Dashboard metrics
GET  /api/dashboard/cases       # Active patient cases
GET  /api/dashboard/activity    # Recent activity log
POST /api/simulation/stemi      # Trigger STEMI simulation
POST /api/simulation/stroke     # Trigger stroke simulation
GET  /api/agents/status         # Agent health status
```

### WebSocket Events

```
patient_arrival      # New patient notification
protocol_activation  # Emergency protocol triggered
case_update         # Patient status change
agent_message       # Inter-agent communication
resource_update     # Bed/equipment status change
lab_result          # Laboratory results
medication_ready    # Pharmacy notifications
```

### Real-time Data Flow

```
uAgents Backend → FastAPI Wrapper → Socket.IO → React Frontend
```

## 🎯 Key Features

### Real-time Patient Monitoring

- Live patient case tracking
- Vital signs monitoring
- Protocol status updates
- Resource allocation tracking

### Agent Communication

- Multi-agent message display
- Real-time chat interface
- System notifications
- Activity logging

### Emergency Protocol Simulation

- STEMI (heart attack) scenarios
- Stroke protocol activation
- Multi-patient coordination
- Resource conflict resolution

### Responsive Design

- Mobile-first approach
- Tablet optimization
- Desktop full-screen layout
- Touch-friendly interactions

## 🎨 Design System

### Color Palette

```css
/* Dark Theme */
--bg-primary: #0f1419      /* Main background */
--bg-secondary: #1a1d29    /* Card backgrounds */
--bg-tertiary: #252837     /* Elevated surfaces */
--text-primary: #ffffff    /* Primary text */
--text-secondary: #a0a9c0  /* Secondary text */
--accent-blue: #3b82f6     /* Primary actions */
--accent-green: #10b981    /* Success states */
--accent-red: #ef4444      /* Critical alerts */
--accent-yellow: #f59e0b   /* Warnings */
```

### Typography

- **Primary**: Inter (clean, medical-grade readability)
- **Monospace**: JetBrains Mono (case IDs, timestamps)
- **Scale**: Tailwind CSS typography scale

### Component Styling

- **Rounded Corners**: Consistent border-radius
- **Subtle Shadows**: Depth without distraction
- **Hover States**: Interactive feedback
- **Status Colors**: Intuitive color coding
- **Smooth Transitions**: Professional animations

## 📱 Responsive Breakpoints

```css
/* Mobile First */
sm: 640px   /* Small tablets */
md: 768px   /* Tablets */
lg: 1024px  /* Small desktops */
xl: 1280px  /* Large desktops */
2xl: 1536px /* Extra large screens */
```

## 🔧 Configuration

### Environment Variables

```env
VITE_API_URL=http://localhost:8080
VITE_WS_URL=ws://localhost:8080
VITE_APP_TITLE=EDFlow AI Dashboard
```

### Vite Configuration

- TypeScript support
- Path aliases (@/ for src/)
- API proxy for development
- WebSocket proxy configuration

## 🧪 Testing Strategy

### Unit Tests

- Component rendering
- Hook functionality
- Utility functions
- State management

### Integration Tests

- API communication
- WebSocket connections
- User interactions
- Data flow

### E2E Tests

- Complete user workflows
- Real-time updates
- Cross-browser compatibility
- Performance testing

## 🚀 Deployment

### Development

```bash
npm run dev
```

### Production Build

```bash
npm run build
npm run preview
```

### Docker Deployment

```bash
docker build -t edflow-frontend .
docker run -p 3000:3000 edflow-frontend
```

## 📊 Performance Considerations

### Optimization Strategies

- **Code Splitting**: Route-based lazy loading
- **Bundle Analysis**: Webpack bundle analyzer
- **Image Optimization**: WebP format, lazy loading
- **Caching**: Service worker implementation
- **Minification**: Production build optimization

### Real-time Performance

- **WebSocket Efficiency**: Event batching
- **State Updates**: Optimized re-renders
- **Memory Management**: Cleanup on unmount
- **Connection Handling**: Automatic reconnection

## 🔒 Security

### Frontend Security

- **XSS Prevention**: Content sanitization
- **CSRF Protection**: Token validation
- **Secure Communication**: HTTPS/WSS only
- **Input Validation**: Client-side validation

### API Security

- **CORS Configuration**: Restricted origins
- **Rate Limiting**: API endpoint protection
- **Authentication**: JWT token handling
- **Data Validation**: Request/response validation

## 📈 Monitoring & Analytics

### Performance Monitoring

- **Core Web Vitals**: LCP, FID, CLS tracking
- **Error Tracking**: Runtime error logging
- **User Analytics**: Interaction tracking
- **Performance Metrics**: Load time monitoring

### Real-time Monitoring

- **WebSocket Health**: Connection status
- **API Response Times**: Endpoint performance
- **Agent Communication**: Message delivery
- **System Alerts**: Critical notifications

## 🤝 Contributing

### Development Workflow

1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

### Code Standards

- **TypeScript**: Strict type checking
- **ESLint**: Code quality enforcement
- **Prettier**: Code formatting
- **Conventional Commits**: Commit message format

## 📚 Documentation

- [Architecture](./ARCHITECTURE.md) - System architecture overview
- [Backend Integration](./BACKEND_INTEGRATION.md) - API integration guide
- [Implementation Plan](./IMPLEMENTATION_PLAN.md) - Development roadmap
- [Component Library](./docs/components.md) - UI component documentation

## 🆘 Troubleshooting

### Common Issues

**WebSocket Connection Failed**

- Check backend server is running on port 8080
- Verify CORS configuration
- Check firewall settings

**API Requests Failing**

- Confirm backend API is accessible
- Check network connectivity
- Verify API endpoint URLs

**Real-time Updates Not Working**

- Check WebSocket connection status
- Verify event listeners are registered
- Check browser console for errors

### Debug Mode

```bash
# Enable debug logging
VITE_DEBUG=true npm run dev
```

## 📄 License

This project is part of the EDFlow AI system for the Fetch.ai AI Agent Challenge.

---

**Built with ❤️ for saving lives through intelligent automation**

[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-blue)](https://tailwindcss.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4-green)](https://socket.io/)
