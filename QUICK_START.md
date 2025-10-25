# 🚀 EDFlow AI - Quick Start Guide

## 🔧 **Fix Backend Import Issues**

The backend needs additional dependencies. Here's how to fix and run:

### **Step 1: Install Additional Dependencies**

```bash
# Make sure you're in the root directory
cd "D:\Job Stuff\Projects\calhacks1"

# Install FastAPI and WebSocket dependencies
pip install fastapi uvicorn python-socketio python-multipart aiohttp
```

### **Step 2: Alternative Startup Method**

Instead of `python run_api.py`, try this:

```bash
# Method 1: Direct uvicorn command
uvicorn api.main:socket_app --host 0.0.0.0 --port 8080 --reload

# Method 2: Python module execution
python -m uvicorn api.main:socket_app --host 0.0.0.0 --port 8080

# Method 3: Set PYTHONPATH and run
set PYTHONPATH=.;.\AutoMediCoord
python run_api.py
```

### **Step 3: Verify API is Running**

```bash
# Test health endpoint
curl http://localhost:8080/health

# Or open in browser
# http://localhost:8080/docs
```

### **Step 4: Start Frontend**

```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

### **Step 5: Access Dashboard**

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8080/docs
- **Health Check:** http://localhost:8080/health

## 🔍 **Troubleshooting**

### **If API Still Won't Start:**

**Option A: Simplified API Server**
Create a simple test API first:

```bash
# Create test_api.py
pip install fastapi uvicorn
```

**Option B: Check Dependencies**

```bash
# Verify all packages installed
pip list | grep fastapi
pip list | grep uvicorn
pip list | grep socketio
```

**Option C: Run from AutoMediCoord Directory**

```bash
cd AutoMediCoord
python app.py  # Run your original uAgents app
```

### **If Frontend Won't Start:**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 🎯 **Expected Results**

When working correctly:

1. **API Server** runs on port 8080 with WebSocket support
2. **Frontend Dashboard** runs on port 3000 with your UI design
3. **Real-time Communication** between frontend and uAgents
4. **Simulation Buttons** create new patient cases
5. **Chat Interface** shows agent communications

## 📞 **Quick Demo**

Once both are running:

1. Open http://localhost:3000
2. Click "Simulate STEMI" button
3. Watch new patient case appear in real-time
4. Send chat message and see agent response
5. Monitor activity log for updates

The system is designed to work with your existing AutoMediCoord uAgents while providing the modern dashboard interface you requested!
