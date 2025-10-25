# EDFlow AI Frontend Implementation Plan

## Project Structure

```
frontend/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── index.html
├── public/
│   ├── favicon.ico
│   └── logo.svg
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Layout.tsx
│   │   │   └── index.ts
│   │   ├── dashboard/
│   │   │   ├── MetricsCards.tsx
│   │   │   ├── LiveCases.tsx
│   │   │   ├── CaseCard.tsx
│   │   │   ├── ActivityLog.tsx
│   │   │   └── index.ts
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   ├── ActivityFeed.tsx
│   │   │   └── index.ts
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── index.ts
│   │   └── common/
│   │       ├── ErrorBoundary.tsx
│   │       ├── StatusIndicator.tsx
│   │       └── index.ts
│   ├── hooks/
│   │   ├── useSocket.ts
│   │   ├── useAgentData.ts
│   │   ├── useRealTimeUpdates.ts
│   │   ├── useChat.ts
│   │   └── index.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── socket.ts
│   │   ├── mockData.ts
│   │   ├── types.ts
│   │   └── index.ts
│   ├── store/
│   │   ├── dashboardStore.ts
│   │   ├── chatStore.ts
│   │   ├── agentStore.ts
│   │   └── index.ts
│   ├── utils/
│   │   ├── formatters.ts
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   └── index.ts
│   └── styles/
│       ├── globals.css
│       └── components.css
└── README.md
```

## File Contents

### package.json

```json
{
  "name": "edflow-ai-dashboard",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "socket.io-client": "^4.7.4",
    "@tanstack/react-query": "^5.8.4",
    "zustand": "^4.4.7",
    "framer-motion": "^10.16.5",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "date-fns": "^2.30.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "typescript": "^5.2.2",
    "vite": "^5.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### vite.config.ts

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/socket.io": {
        target: "http://localhost:8080",
        ws: true,
      },
    },
  },
});
```

### tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          900: "#1e3a8a",
        },
        gray: {
          800: "#1f2937",
          850: "#1a1d29",
          900: "#111827",
          950: "#0f1419",
        },
        success: "#10b981",
        warning: "#f59e0b",
        error: "#ef4444",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
```

### index.html

```html
<!DOCTYPE html>
<html lang="en" class="dark">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/logo.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EDFlow AI - Emergency Department Dashboard</title>
  </head>
  <body class="bg-gray-950 text-white">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### src/main.tsx

```typescript
import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App.tsx";
import "./styles/globals.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
```

### src/App.tsx

```typescript
import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen bg-gray-950 text-white">
          <Layout />
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
```

### src/styles/globals.css

```css
@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";

@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap");

* {
  box-sizing: border-box;
}

body {
  font-family: "Inter", system-ui, -apple-system, sans-serif;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #374151;
}

::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Animation utilities */
@keyframes pulse-slow {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Status indicators */
.status-critical {
  @apply bg-red-500 text-white;
}

.status-urgent {
  @apply bg-orange-500 text-white;
}

.status-stable {
  @apply bg-green-500 text-white;
}

.status-pending {
  @apply bg-yellow-500 text-black;
}

/* Card hover effects */
.card-hover {
  @apply transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/10 hover:border-blue-500/30;
}
```

## Key Implementation Notes

### 1. Component Architecture

- **Layout**: Main layout with header, sidebar, and content area
- **Dashboard**: Metrics cards, live cases, and activity log
- **Chat**: Real-time messaging interface
- **UI Components**: Reusable components with consistent styling

### 2. State Management

- **Zustand**: Lightweight state management for dashboard, chat, and agent data
- **React Query**: Server state management with caching and synchronization
- **Local State**: Component-level state for UI interactions

### 3. Real-time Communication

- **Socket.IO**: WebSocket connection for real-time updates
- **Event Handling**: Patient arrivals, protocol activations, status updates
- **Fallback**: Polling mechanism when WebSocket is unavailable

### 4. Styling Strategy

- **Tailwind CSS**: Utility-first CSS framework
- **Dark Theme**: Primary theme matching the design
- **Responsive**: Mobile-first responsive design
- **Animations**: Subtle animations for better UX

### 5. TypeScript Integration

- **Strict Types**: Full TypeScript coverage
- **API Types**: Shared types between frontend and backend
- **Component Props**: Properly typed component interfaces

### 6. Development Workflow

- **Vite**: Fast development server and build tool
- **ESLint**: Code linting and formatting
- **Hot Reload**: Instant updates during development
- **Proxy**: API proxy for backend communication

## Next Steps

1. **Create Project Structure**: Set up all folders and files
2. **Install Dependencies**: Run npm install with all required packages
3. **Implement Core Components**: Start with layout and basic UI
4. **Add Mock Data**: Create realistic mock data for development
5. **Integrate Real-time Features**: Connect to backend via WebSocket
6. **Style and Polish**: Apply final styling and animations
7. **Testing**: Add unit and integration tests
8. **Deployment**: Configure for production deployment

This plan provides a complete foundation for building the EDFlow AI dashboard that matches the design requirements while maintaining scalability and maintainability.
