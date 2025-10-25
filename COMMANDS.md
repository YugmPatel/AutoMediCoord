# EDFlow AI - Quick Command Reference

## Testing Commands

### Test Claude API
```bash
python test_claude_api.py
```
Tests if your Claude API key is working.

### Test System Components
```bash
python test_system.py
```
Tests data models, AI engine, and basic functionality.

### Test Single Patient Flow
```bash
python simulate_patient_flow.py
```
Simulates a real STEMI patient with AI analysis.

### Stress Test
```bash
python stress_test.py
```
Tests system with 10 concurrent patients.

---

## Demo Commands

### Multi-Patient Demo
```bash
python scenarios/multi_patient_demo.py
```
Shows 3 critical patients arriving simultaneously.

### Conflict Resolution Demo
```bash
python scenarios/conflict_resolution_demo.py
```
Demonstrates AI-powered resource conflict resolution.

### STEMI Demo
```bash
python scenarios/stemi_demo.py
```
Shows complete STEMI protocol workflow.

---

## Running Agents

### Run All 6 Agents
```bash
python run_all_agents.py
```
Starts all agents in a Bureau (single process).

### Run Individual Agents
```bash
# Terminal 1
python src/agents/ed_coordinator/agent.py

# Terminal 2
python src/agents/resource_manager/agent.py

# Terminal 3
python src/agents/specialist_coordinator/agent.py

# Terminal 4
python src/agents/lab_service/agent.py

# Terminal 5
python src/agents/pharmacy/agent.py

# Terminal 6
python src/agents/bed_management/agent.py
```

---

## Deployment Commands

### Deploy to Agentverse
```bash
python deploy_to_agentverse.py
```
Deploys all agents to Agentverse cloud platform.

### Integration Test
```bash
python integration_test.py
```
Tests full system integration with all agents.

---

## Troubleshooting Commands

### Check Python Version
```bash
python --version
```
Should be 3.9 or higher.

### Check Installed Packages
```bash
pip list | findstr uagents
pip list | findstr anthropic
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt
```

### Clear Python Cache
```bash
python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
python -c "import shutil; shutil.rmtree('src/__pycache__', ignore_errors=True)"
```

### Check Port Usage (Windows)
```powershell
netstat -ano | findstr :8000
```

### Kill Process by Port (Windows)
```powershell
# Find PID first
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

---

## Development Commands

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Virtual Environment
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# CMD
.\venv\Scripts\activate.bat
```

### Install in Development Mode
```bash
pip install -e .
```

---

## Quick Start Sequence

### First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy .env.example to .env
copy .env.example .env

# 3. Edit .env and add your ANTHROPIC_API_KEY

# 4. Test API
python test_claude_api.py

# 5. Run system test
python test_system.py
```

### Run Demos
```bash
# Demo 1: Multi-patient coordination
python scenarios/multi_patient_demo.py

# Demo 2: Conflict resolution
python scenarios/conflict_resolution_demo.py

# Demo 3: Live patient flow
python simulate_patient_flow.py
```

### Run Full System
```bash
# Option 1: All agents in one process
python run_all_agents.py

# Option 2: Agents in separate terminals
# (See "Run Individual Agents" above)
```

---

## Environment Variables

### Required
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Optional (for Agentverse)
```bash
AGENTVERSE_API_KEY=av-...
DEPLOYMENT_MODE=agentverse
```

### Optional (for local development)
```bash
ED_COORDINATOR_PORT=8000
RESOURCE_MANAGER_PORT=8001
SPECIALIST_COORDINATOR_PORT=8002
LAB_SERVICE_PORT=8003
PHARMACY_PORT=8004
BED_MANAGEMENT_PORT=8005
```

---

## Common Workflows

### Testing Workflow
```bash
# 1. Test API
python test_claude_api.py

# 2. Test components
python test_system.py

# 3. Test patient flow
python simulate_patient_flow.py

# 4. Stress test
python stress_test.py
```

### Demo Workflow
```bash
# 1. Multi-patient demo
python scenarios/multi_patient_demo.py

# 2. Conflict resolution
python scenarios/conflict_resolution_demo.py

# 3. Live simulation
python simulate_patient_flow.py
```

### Development Workflow
```bash
# 1. Make changes to code

# 2. Test changes
python test_system.py

# 3. Run specific demo
python simulate_patient_flow.py

# 4. Run full system
python run_all_agents.py
```

### Deployment Workflow
```bash
# 1. Test locally
python test_system.py

# 2. Test integration
python integration_test.py

# 3. Deploy to Agentverse
python deploy_to_agentverse.py

# 4. Verify deployment
# (Check Agentverse dashboard)
```

---

## Useful Shortcuts

### Quick Test
```bash
python test_claude_api.py && python test_system.py
```

### Run All Demos
```bash
python scenarios/multi_patient_demo.py
python scenarios/conflict_resolution_demo.py
python simulate_patient_flow.py
```

### Clean and Test
```bash
python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)" && python test_system.py
```

---

## Getting Help

### View Documentation
```bash
# Main README
type README.md

# Quick start
type QUICKSTART.md

# Troubleshooting
type TROUBLESHOOTING.md

# Architecture
type docs\ARCHITECTURE.md
```

### Check Logs
All logs are printed to console. Look for:
- `ERROR` - Critical issues
- `WARNING` - Potential problems
- `INFO` - Normal operation
- `DEBUG` - Detailed information

### Enable Debug Logging
In .env:
```bash
LOG_LEVEL=DEBUG
```

---

## Competition Submission

### Prepare Submission
```bash
# 1. Review submission document
type COMPETITION_SUBMISSION.md

# 2. Review demo script
type DEMO_VIDEO_SCRIPT.md

# 3. Review project summary
type PROJECT_SUMMARY.md
```

### Record Demo Video
Follow the script in `DEMO_VIDEO_SCRIPT.md` and run:
```bash
python scenarios/multi_patient_demo.py
python scenarios/conflict_resolution_demo.py
python simulate_patient_flow.py
```

---

## Tips

### Windows PowerShell
- Use `type` instead of `cat`
- Use `dir` instead of `ls`
- Use `copy` instead of `cp`
- Use `del` instead of `rm`

### Performance
- First run may be slower (loading models)
- Subsequent runs are faster
- API calls have ~2s latency
- Fallback mode is instant

### Best Practices
- Always test API first
- Run demos before full system
- Check logs for errors
- Use virtual environment
- Keep .env file secure

---

**Last Updated:** October 25, 2025
