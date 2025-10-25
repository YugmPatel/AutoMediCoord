# EDFlow AI - Troubleshooting Guide

## Common Issues and Solutions

### 1. Module Import Errors

#### Error: `ModuleNotFoundError: No module named 'src'`

**Solution:**
```bash
# Make sure you're in the project root directory
cd D:\project\finallevelprojects\ED-FOx

# Run scripts from project root
python scenarios/multi_patient_demo.py
```

**Alternative:** Add project root to PYTHONPATH
```bash
# Windows PowerShell
$env:PYTHONPATH = "D:\project\finallevelprojects\ED-FOx"

# Windows CMD
set PYTHONPATH=D:\project\finallevelprojects\ED-FOx

# Then run
python scenarios/multi_patient_demo.py
```

---

### 2. Claude API Errors

#### Error: `Claude AI error:` (empty error message)

**Cause:** API authentication issue or invalid API key

**Solution:**

1. **Test your API key:**
   ```bash
   python test_claude_api.py
   ```

2. **Check .env file:**
   ```bash
   # Open .env and verify ANTHROPIC_API_KEY is set
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

3. **Get a new API key:**
   - Go to https://console.anthropic.com/
   - Create new API key
   - Update .env file

4. **Verify API key format:**
   - Should start with `sk-ant-api03-`
   - Should be ~100+ characters long
   - No spaces or quotes around it

---

### 3. Agent Communication Issues

#### Error: `'EDCoordinatorAgent' object has no attribute 'get_patient_count'`

**Cause:** Old cached Python files

**Solution:**
```bash
# Clear Python cache
python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
python -c "import shutil; shutil.rmtree('src/__pycache__', ignore_errors=True)"

# Or manually delete all __pycache__ folders
```

---

### 4. Port Already in Use

#### Error: `Address already in use` or `Port 8000 already in use`

**Solution:**

**Windows:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Alternative:** Use different ports in .env
```bash
ED_COORDINATOR_PORT=8010
RESOURCE_MANAGER_PORT=8011
# etc.
```

---

### 5. Demo Scripts Not Working

#### Demos show errors but claim to pass

**Explanation:** Demo scripts are **simulations** - they don't need real agents running.

**Working Demos (No agents needed):**
```bash
python scenarios/conflict_resolution_demo.py  # ✅ Works
python scenarios/multi_patient_demo.py        # ✅ Works (after import fix)
```

**Real System Tests (Need API key):**
```bash
python test_claude_api.py           # Test API first
python simulate_patient_flow.py     # Real AI analysis
python stress_test.py               # Real AI stress test
```

**Full Agent System (Need all agents):**
```bash
python run_all_agents.py            # Runs all 6 agents
```

---

### 6. Agentverse Deployment Issues

#### Error: `AGENTVERSE_API_KEY not set`

**Solution:**
1. Get API key from https://agentverse.ai
2. Add to .env:
   ```bash
   AGENTVERSE_API_KEY=av-...
   ```

#### Agents not connecting to Agentverse

**Solution:**
1. Set deployment mode:
   ```bash
   DEPLOYMENT_MODE=agentverse
   ```

2. Run deployment script:
   ```bash
   python deploy_to_agentverse.py
   ```

---

### 7. Performance Issues

#### AI responses are slow (>2 seconds)

**Possible causes:**
- Network latency
- API rate limits
- Large prompt size

**Solutions:**
1. Check internet connection
2. Reduce timeout in .env:
   ```bash
   AI_RESPONSE_TIMEOUT_SECONDS=5
   ```
3. Use fallback mode (automatic)

---

### 8. Testing Issues

#### Tests pass but show errors

**Explanation:** Tests use fallback mode when API fails.

**To verify real API:**
```bash
# Test API connection first
python test_claude_api.py

# Then run tests
python test_system.py
```

---

## Quick Diagnostic Commands

### Check Environment
```bash
# Verify Python version (need 3.9+)
python --version

# Check installed packages
pip list | findstr uagents
pip list | findstr anthropic

# Verify .env file exists
dir .env
```

### Test Components

```bash
# 1. Test API key
python test_claude_api.py

# 2. Test system components
python test_system.py

# 3. Test single patient flow
python simulate_patient_flow.py

# 4. Test stress load
python stress_test.py
```

### Run Demos (No API needed)
```bash
# Simulation demos
python scenarios/conflict_resolution_demo.py
python scenarios/multi_patient_demo.py
```

---

## Installation Issues

### Missing Dependencies

```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Or install individually
pip install uagents uagents-core anthropic python-dotenv
```

### Virtual Environment Issues

```bash
# Create new virtual environment
python -m venv venv

# Activate it
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
.\venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

---

## Getting Help

### Check Logs

Logs are printed to console. Look for:
- `ERROR` messages (red flags)
- `WARNING` messages (potential issues)
- `INFO` messages (normal operation)

### Enable Debug Mode

In .env:
```bash
LOG_LEVEL=DEBUG
```

### Report Issues

When reporting issues, include:
1. Error message (full traceback)
2. Command you ran
3. Python version
4. Operating system
5. Contents of .env (without API keys!)

---

## Success Checklist

Before running the full system:

- [ ] Python 3.9+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file created with ANTHROPIC_API_KEY
- [ ] API key tested (`python test_claude_api.py`)
- [ ] In project root directory
- [ ] No port conflicts
- [ ] System tests pass (`python test_system.py`)

---

## Quick Fixes

### "It's not working!"

1. **Are you in the right directory?**
   ```bash
   cd D:\project\finallevelprojects\ED-FOx
   ```

2. **Is your API key set?**
   ```bash
   python test_claude_api.py
   ```

3. **Did you install dependencies?**
   ```bash
   pip install -r requirements.txt
   ```

4. **Try the demos first:**
   ```bash
   python scenarios/conflict_resolution_demo.py
   ```

5. **Still stuck? Check the logs carefully!**

---

## Contact & Resources

- **Documentation:** See README.md
- **Architecture:** See docs/ARCHITECTURE.md
- **Deployment:** See DEPLOYMENT_GUIDE.md
- **Quick Start:** See QUICKSTART.md

---

**Last Updated:** October 25, 2025
