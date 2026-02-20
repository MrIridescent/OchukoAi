# Ochuko AI v5.0 - Troubleshooting Guide

**Complete troubleshooting and problem-solving reference**

**Author**: David Akpoviroro Oke (MrIridescent)  
**Version**: 5.0.0  
**Last Updated**: February 2026

---

## Quick Diagnostics

Before diving into specific issues, run these commands:

```bash
# Check system health
bash scripts/system-requirements.sh

# Check running services
bash scripts/health-check.sh

# View detailed logs
docker-compose logs
```

---

## Common Issues & Solutions

### 1. Docker Not Found / Not Installed

**Error message:**
```
Command 'docker' not found
```

**Solution:**

#### On Ubuntu/Debian:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

#### On macOS:
```bash
# Install Docker Desktop from:
https://www.docker.com/products/docker-desktop

# Then restart your terminal
```

#### On Windows:
1. Install WSL2: https://docs.microsoft.com/en-us/windows/wsl/install
2. Install Docker Desktop for Windows
3. Ensure WSL2 backend is enabled in Docker settings

---

### 2. Docker Daemon Not Running

**Error message:**
```
Cannot connect to Docker daemon
```

**Solution:**

```bash
# Start Docker daemon
sudo systemctl start docker

# For macOS, start Docker Desktop application
# For Windows, start Docker Desktop from Start menu

# Verify it's running
docker ps
```

---

### 3. Docker Compose Not Found

**Error message:**
```
Command 'docker-compose' not found
```

**Solution:**

Try the new format:
```bash
docker compose --version
```

If that works, you can use `docker compose` instead of `docker-compose` in commands.

If neither works:
```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

---

### 4. Port Already in Use

**Error message:**
```
Error response from daemon: driver failed programming external connectivity
Bind for 0.0.0.0:3000 failed: port is already allocated
```

**Solution:**

#### Find and kill process using port:
```bash
# Find process on port 3000
lsof -i :3000

# Kill process (replace PID with actual number)
kill -9 PID

# Or kill all on port
lsof -ti:3000 | xargs kill -9
```

#### Or use different ports:
```bash
# Edit docker-compose.yml
nano docker-compose.yml

# Change the port mapping, for example:
# From: "3000:3000"
# To:   "3001:3000"
```

---

### 5. Out of Disk Space

**Error message:**
```
No space left on device
```

**Solution:**

```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a

# Remove old logs
rm logs/*.log

# Remove old data (WARNING: deletes everything!)
docker-compose down -v
docker volume prune
```

---

### 6. Out of Memory

**Error message:**
```
OOMkilled
Cannot allocate memory
```

**Solution:**

```bash
# Check memory usage
free -h

# Reduce running services
# Edit docker-compose.yml and comment out unused services

# Or increase memory limits
# In docker-compose.yml, add under each service:
mem_limit: 2g  # 2GB per service
```

---

### 7. Backend API Not Responding

**Error message:**
```
curl: (7) Failed to connect to localhost port 8000
```

**Solution:**

```bash
# Check if backend is running
docker-compose ps backend

# View backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Rebuild if needed
docker-compose up -d --build backend
```

**Common causes:**
- Port 8000 is in use
- Database not ready (PostgreSQL, MongoDB)
- Missing API keys (add optional ones to .env)
- Insufficient memory

---

### 8. Frontend Not Loading

**Error message:**
```
Cannot get http://localhost:3000
```

**Solution:**

```bash
# Check if frontend is running
docker-compose ps frontend

# View frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend

# Rebuild
docker-compose up -d --build frontend

# Try accessing http://localhost:3000 again
```

---

### 9. Database Connection Error

**Error message:**
```
could not translate host name "postgres" to address
```

**Solution:**

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Wait 30 seconds for database to start
sleep 30

# Restart backend
docker-compose restart backend
```

---

### 10. MongoDB Connection Failed

**Error message:**
```
MongoNetworkError: connect ECONNREFUSED
```

**Solution:**

```bash
# Check MongoDB status
docker-compose ps mongodb

# View logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb

# Wait for it to start
sleep 10

# Restart backend
docker-compose restart backend
```

---

### 11. Redis Connection Error

**Error message:**
```
Error: connect ECONNREFUSED
```

**Solution:**

```bash
# Check Redis
docker-compose ps redis

# Restart Redis
docker-compose restart redis

# Verify it works
redis-cli ping
```

---

### 12. Build Errors

**Error message:**
```
Error building image
```

**Solution:**

```bash
# Check what failed
docker-compose build --no-cache

# View specific service error
docker-compose build backend 2>&1 | tail -50

# Clean up and rebuild
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

---

### 13. Permission Denied

**Error message:**
```
permission denied
```

**Solution:**

```bash
# Run with sudo
sudo docker-compose up -d

# OR add current user to docker group
sudo usermod -aG docker $USER
newgrp docker
# Then log out and back in

# Fix file permissions
chmod +x deploy.sh setup.sh
chmod -R 755 scripts/
```

---

### 14. Network Issues

**Error message:**
```
Failed to get D-Bus connection
```

**Solution:**

```bash
# This is usually in containers, not a real issue
# If network seems down:

# Check Docker network
docker network ls

# Restart Docker
sudo systemctl restart docker

# Rebuild containers with network
docker-compose down
docker-compose up -d
```

---

### 15. Services Keep Crashing

**Error message:**
```
status: exited
```

**Solution:**

```bash
# View why it crashed
docker-compose logs service_name

# Common reasons:
# 1. Port in use (see #4 above)
# 2. Out of memory (see #6 above)
# 3. Missing environment variables

# Check .env file
cat .env | head -20

# Ensure OPENAI_API_KEY and CLAUDE_API_KEY are set
# (or at least have placeholder values)
```

---

### 16. Changes Not Taking Effect

**Error message:**
```
Code changes not reflected
```

**Solution:**

```bash
# Rebuild the image
docker-compose up -d --build

# Or rebuild specific service
docker-compose up -d --build backend

# For frontend changes, may need to clear cache
docker-compose down frontend
docker-compose up -d frontend
```

---

### 17. Can't Access from Other Computer

**Error message:**
```
Cannot connect to http://your-ip:3000
```

**Solution:**

```bash
# Find your local IP
hostname -I  # Linux
ifconfig     # macOS

# Access using your IP instead of localhost
# http://192.168.1.100:3000  (example)

# For external internet access, need to:
# 1. Configure firewall
# 2. Use domain with SSL
# 3. Set up reverse proxy (nginx)

# See DEPLOYMENT_READY.md for cloud deployment
```

---

### 18. API Keys Not Working

**Error message:**
```
401 Unauthorized
Invalid API key
```

**Solution:**

```bash
# Check .env file
cat .env | grep API_KEY

# Verify format:
# OPENAI_API_KEY=sk-...  (starts with sk-)
# CLAUDE_API_KEY=sk-ant-...  (starts with sk-ant-)

# If wrong, edit .env
nano .env

# Restart backend to pick up changes
docker-compose restart backend
```

---

### 19. Health Check Failing

**Error message:**
```
Unhealthy
```

**Solution:**

```bash
# Run detailed health check
bash scripts/health-check.sh

# View service logs
docker-compose logs

# Common issues:
# - Backend not ready (takes 1-2 minutes)
# - Database not accessible
# - Port conflicts

# Wait a bit and try again
sleep 30
bash scripts/health-check.sh
```

---

### 20. SSL/HTTPS Certificate Issues

**Error message:**
```
Certificate verification failed
```

**Solution:**

```bash
# For local development, this is normal (use http://)
# For production, get real certificate:

# Using Let's Encrypt:
sudo apt-get install certbot
sudo certbot certonly --standalone -d your-domain.com

# Point nginx to certificate
# See DEPLOYMENT_READY.md for nginx setup
```

---

## Advanced Troubleshooting

### View Real-Time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail 100

# With timestamps
docker-compose logs -t
```

### Check Container Health

```bash
# Detailed status
docker-compose ps -a

# Inspect specific container
docker inspect container_name

# View resource usage
docker stats

# Monitor in real-time
watch -n 1 'docker stats'
```

### Access Container Shell

```bash
# Enter backend container
docker-compose exec backend bash

# Enter database
docker-compose exec postgres psql -U postgres -d ochuko_ai

# MongoDB shell
docker-compose exec mongodb mongosh
```

### Backup Before Major Changes

```bash
# Backup data
bash scripts/backup.sh

# Verify backup exists
ls -lah backups/

# If needed, restore
bash scripts/restore.sh backup_name
```

### Reset Everything (DANGEROUS)

```bash
# Full reset - deletes all data!
docker-compose down -v

# Clean up images
docker system prune -a

# Start fresh
docker-compose up -d

# WARNING: This deletes all your data!
```

---

## Getting More Help

### Check Logs by Component

```bash
# Backend API
docker-compose logs backend | tail -50

# Frontend
docker-compose logs frontend | tail -50

# PostgreSQL
docker-compose logs postgres | tail -50

# MongoDB
docker-compose logs mongodb | tail -50

# Redis
docker-compose logs redis | tail -50
```

### Enable Debug Logging

```bash
# Edit .env
nano .env

# Change to:
DEBUG=true
LOG_LEVEL=DEBUG

# Restart services
docker-compose restart
```

### Check System Resources

```bash
# Memory
free -h

# Disk
df -h

# CPU
top
htop  # if installed

# Docker stats
docker stats
```

---

## When to Rebuild vs Restart

**Use `restart` when:**
- Changing .env configuration
- Updating environment variables
- Testing same code with different settings

```bash
docker-compose restart
```

**Use `down` and `up` when:**
- Adding/removing services
- Major configuration changes
- Want complete fresh start

```bash
docker-compose down
docker-compose up -d
```

**Use `rebuild` when:**
- Code has changed
- Dependencies updated
- Dockerfile modified

```bash
docker-compose up -d --build
```

---

## Performance Troubleshooting

### Slow Performance

```bash
# Check resource usage
docker stats

# Increase workers (in .env)
WORKERS=8  # default is 4

# Increase memory (in docker-compose.yml)
mem_limit: 2g

# Restart
docker-compose restart
```

### High CPU Usage

```bash
# Find process using CPU
docker stats

# Check logs for errors
docker-compose logs
```

### High Memory Usage

```bash
# See which container uses most memory
docker stats

# Reduce number of workers
WORKERS=2

# Increase available RAM
# Or reduce number of running services
```

---

## If All Else Fails

**Step 1: Clean everything**
```bash
docker-compose down -v
docker system prune -a
```

**Step 2: Rebuild from scratch**
```bash
git pull  # Get latest code
bash deploy.sh --quick-start
```

**Step 3: Check system requirements**
```bash
bash scripts/system-requirements.sh
```

**Step 4: Create detailed error report**
```bash
# Collect system info
bash scripts/system-requirements.sh > report.txt
docker-compose logs >> report.txt

# Share on GitHub Issues:
# https://github.com/yourusername/githubautom8/issues
```

---

## Common Error Messages Translation

| Error | Means | Solution |
|-------|-------|----------|
| `port is already allocated` | Another app using port | Kill that process or use different port |
| `no such file or directory` | File/path doesn't exist | Check file path, run from correct directory |
| `OOMkilled` | Out of memory | Increase RAM or reduce services |
| `connection refused` | Service not running | Check logs, restart service |
| `timeout` | Service taking too long | Wait longer, restart, check logs |
| `permission denied` | Not enough access | Use sudo or fix permissions |
| `insufficient funds` | API quota exceeded | Check billing, add credits |
| `401 Unauthorized` | Bad credentials | Check API keys in .env |
| `404 Not Found` | Wrong URL or endpoint | Check URL, see API docs |
| `500 Internal Server Error` | Backend error | Check backend logs |

---

## Preventive Measures

### Regular Maintenance

```bash
# Weekly: Check logs
docker-compose logs | grep -i error

# Weekly: Check disk space
df -h

# Monthly: Clean up
docker system prune

# Monthly: Backup data
bash scripts/backup.sh
```

### Monitoring

```bash
# Set up monitoring script
watch -n 5 'bash scripts/health-check.sh'

# Or use external monitoring
# See DEPLOYMENT_READY.md
```

### Documentation

- Keep .env secure (don't share!)
- Document any custom changes
- Keep deployment scripts updated
- Store backups safely

---

## Still Having Issues?

1. **Read this whole guide** - 90% of issues are covered
2. **Check system requirements** - `bash scripts/system-requirements.sh`
3. **View detailed logs** - `docker-compose logs`
4. **Search GitHub issues** - May be a known issue
5. **Create new issue** with:
   - Error message (exact text)
   - System info (OS, Docker version)
   - Steps to reproduce
   - Logs from `bash scripts/health-check.sh`

---

**Status**: ✅ **Most Common Issues Covered**  
**Last Updated**: February 2026  
**Questions?** See DEPLOYMENT_READY.md or GitHub Issues
