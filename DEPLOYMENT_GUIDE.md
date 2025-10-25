# 🚀 EDFlow AI - Production Deployment Guide

Complete guide for deploying EDFlow AI to production environments.

## 📋 Pre-Deployment Checklist

### ✅ **Requirements**

- [ ] Docker and Docker Compose installed
- [ ] Domain name configured (optional)
- [ ] SSL certificates obtained (for HTTPS)
- [ ] Anthropic API key acquired
- [ ] Server with minimum 4GB RAM, 2 CPU cores
- [ ] Ports 80, 443, 8080, 3000 available

### ✅ **Security Setup**

- [ ] Strong JWT secret key generated
- [ ] Production environment variables configured
- [ ] Firewall rules configured
- [ ] SSL/TLS certificates installed
- [ ] Backup strategy implemented

---

## 🔧 Deployment Options

### Option 1: Docker Compose (Recommended)

**Step 1: Clone Repository**

```bash
git clone https://github.com/YugmPatel/EDFlowAI.git
cd AutoMediCoord
```

**Step 2: Configure Environment**

```bash
# Copy production environment template
cp .env.production .env

# Edit with your values
nano .env
```

**Step 3: Deploy with Docker Compose**

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

**Step 4: Verify Deployment**

```bash
# Test API health
curl http://localhost:8080/health

# Test frontend
curl http://localhost:3000

# Run integration tests
python test_system.py
```

### Option 2: Manual Deployment

**Backend Deployment:**

```bash
# Install Python dependencies
pip install -r AutoMediCoord/requirements.txt
pip install -r api_requirements.txt

# Set environment variables
export DEPLOYMENT_MODE=production
export ANTHROPIC_API_KEY=your_key_here

# Start API server
python run_api.py
```

**Frontend Deployment:**

```bash
# Build frontend
cd frontend
npm install
npm run build

# Serve with nginx or static hosting
# Copy dist/ folder to web server
```

### Option 3: Cloud Deployment

**AWS/GCP/Azure:**

- Use container services (ECS, Cloud Run, Container Instances)
- Configure load balancers for high availability
- Set up managed databases for persistence
- Use managed Redis for caching

**Render/Heroku:**

- Deploy API as web service
- Deploy frontend as static site
- Configure environment variables
- Set up custom domains

---

## 🔒 Security Configuration

### **1. JWT Security**

```bash
# Generate secure JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### **2. HTTPS Setup**

```bash
# Using Let's Encrypt (free SSL)
sudo apt install certbot
sudo certbot --nginx -d your-domain.com
```

### **3. Firewall Configuration**

```bash
# Ubuntu/Debian
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# Block direct access to API port in production
sudo ufw deny 8080
```

### **4. Environment Security**

```bash
# Secure environment file
chmod 600 .env
chown root:root .env
```

---

## 📊 Monitoring Setup

### **1. Health Monitoring**

```bash
# API health endpoint
curl http://localhost:8080/health

# Frontend health
curl http://localhost:3000/health

# Agent status
curl http://localhost:8080/api/agents/status
```

### **2. Log Monitoring**

```bash
# API logs
docker-compose logs -f api

# Frontend logs
docker-compose logs -f frontend

# System logs
tail -f /var/log/syslog
```

### **3. Performance Monitoring**

```bash
# Resource usage
docker stats

# Network monitoring
netstat -tulpn | grep :8080
```

---

## 🔄 Backup and Recovery

### **1. Data Backup**

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/app/backups"

# Backup configuration
cp .env "$BACKUP_DIR/env_$DATE.backup"

# Backup logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" logs/

# Backup application state (if using persistent storage)
# docker exec edflow_api python backup_state.py
```

### **2. Recovery Procedures**

```bash
# Stop services
docker-compose down

# Restore from backup
cp backups/env_YYYYMMDD_HHMMSS.backup .env

# Restart services
docker-compose up -d
```

---

## 🚀 Scaling Configuration

### **Horizontal Scaling**

```yaml
# docker-compose.scale.yml
version: "3.8"
services:
  api:
    deploy:
      replicas: 3

  frontend:
    deploy:
      replicas: 2
```

### **Load Balancer Setup**

```nginx
# nginx load balancer
upstream api_backend {
    server api1:8080;
    server api2:8080;
    server api3:8080;
}

upstream frontend_backend {
    server frontend1:3000;
    server frontend2:3000;
}
```

---

## 🔍 Troubleshooting

### **Common Issues**

**1. API Server Won't Start**

```bash
# Check logs
docker-compose logs api

# Common fixes
- Verify ANTHROPIC_API_KEY is set
- Check port 8080 is available
- Ensure all dependencies installed
```

**2. Frontend Build Fails**

```bash
# Check Node.js version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**3. WebSocket Connection Issues**

```bash
# Check CORS configuration
- Verify CORS_ORIGINS includes your domain
- Check firewall allows WebSocket connections
- Ensure proxy configuration is correct
```

**4. Agent Communication Problems**

```bash
# Check agent status
curl http://localhost:8080/api/agents/status

# Restart agents
docker-compose restart api
```

---

## 📈 Performance Optimization

### **1. Frontend Optimization**

```bash
# Enable production build optimizations
npm run build

# Analyze bundle size
npm install -g webpack-bundle-analyzer
npx webpack-bundle-analyzer frontend/dist/static/js/*.js
```

### **2. Backend Optimization**

```python
# Increase worker processes
uvicorn api.main:socket_app --workers 4 --host 0.0.0.0 --port 8080
```

### **3. Database Optimization**

```bash
# Use Redis for caching
docker run -d --name redis redis:alpine

# Configure connection pooling
# Add to .env: REDIS_URL=redis://localhost:6379/0
```

---

## 🛡️ Security Hardening

### **1. Network Security**

```bash
# Use private networks
docker network create --driver bridge edflow-private

# Restrict container communication
# Only expose necessary ports
```

### **2. Container Security**

```dockerfile
# Use non-root user in containers
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

### **3. Data Protection**

```bash
# Encrypt sensitive data at rest
# Use secrets management (Docker secrets, Kubernetes secrets)
# Implement proper access controls
```

---

## 📞 Production Support

### **Monitoring Endpoints**

- **Health Check:** `/health`
- **API Documentation:** `/docs`
- **Agent Status:** `/api/agents/status`
- **System Metrics:** `/api/dashboard/metrics`

### **Log Locations**

- **API Logs:** `/app/logs/edflow-ai.log`
- **Audit Logs:** `/app/logs/audit.log`
- **Container Logs:** `docker-compose logs`

### **Emergency Procedures**

1. **System Down:** Check health endpoints, restart services
2. **High Load:** Scale up containers, check resource usage
3. **Security Incident:** Review audit logs, rotate secrets
4. **Data Loss:** Restore from backups, verify integrity

---

## 🎯 Production Checklist

### **Before Go-Live**

- [ ] All tests passing (`python test_system.py`)
- [ ] Security scan completed
- [ ] Performance testing done
- [ ] Backup procedures tested
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team training completed

### **Post-Deployment**

- [ ] Monitor system health for 24 hours
- [ ] Verify all integrations working
- [ ] Test emergency procedures
- [ ] Update documentation
- [ ] Schedule regular maintenance

---

**🏥 Ready to save lives with intelligent automation!**

For support: Check logs, review documentation, test endpoints.
