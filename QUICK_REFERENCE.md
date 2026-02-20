# Ochuko AI v5.0 - Quick Reference Card

**Print this page for quick access to commands and URLs**

---

## 🚀 Getting Started (Copy & Paste)

### First Time Setup (Choose ONE)

```bash
# Option A: One-Click (Easiest, recommended)
bash deploy.sh --quick-start

# Option B: Interactive Setup
bash setup.sh

# Option C: Manual (Advanced)
docker-compose up -d
```

---

## 🌐 Access Your System

| What | URL | Use |
|------|-----|-----|
| **Web UI** | http://localhost:3000 | Main interface |
| **API Docs** | http://localhost:8000/docs | Interactive docs |
| **API** | http://localhost:8000 | Programmatic access |
| **Health** | http://localhost:8000/health | Status check |

**On a server?** Replace `localhost` with your IP/domain

---

## ⚡ Essential Commands

### Status & Monitoring
```bash
bash scripts/health-check.sh        # Check everything
bash scripts/logs.sh                # View logs (live)
bash scripts/access-info.sh         # Show URLs
```

### Control Services
```bash
docker-compose up -d                # Start all
docker-compose down                 # Stop all
docker-compose restart              # Restart all
docker-compose logs -f              # Watch logs
```

### Service-Specific
```bash
docker-compose restart backend      # Restart just backend
docker-compose logs backend         # Backend logs only
docker-compose exec backend bash    # Enter container
```

---

## 🔧 Configuration

### Edit Settings
```bash
nano .env                           # Edit configuration
nano docker-compose.yml             # Edit services
```

### Common Changes
```bash
# Change frontend port (default 3000)
# In docker-compose.yml, find frontend section:
ports:
  - "3001:3000"  # Change first number

# Add API key
nano .env
# Add: OPENAI_API_KEY=sk-your-key-here
# Restart: docker-compose restart backend
```

---

## 🔍 Troubleshooting

### Port In Use
```bash
# Port 3000 in use?
lsof -ti:3000 | xargs kill -9

# Port 8000 in use?
lsof -ti:8000 | xargs kill -9
```

### Service Won't Start
```bash
# Check why
docker-compose logs service_name

# Rebuild and restart
docker-compose up -d --build service_name
```

### Out of Disk
```bash
docker system prune -a              # Clean up everything
```

---

## 📊 System Status Commands

```bash
docker-compose ps                   # Running containers
docker stats                        # Resource usage
docker images                       # Downloaded images
docker volume ls                    # Storage volumes
```

---

## 🚨 Emergency Commands

```bash
# Stop everything (safe)
docker-compose down

# Complete reset (deletes data!)
docker-compose down -v
docker system prune -a
bash deploy.sh --quick-start

# Backup before major changes
bash scripts/backup.sh

# Restore from backup
bash scripts/restore.sh backup_name
```

---

## 📝 Configuration Keys (in .env)

```bash
# Environment
ENV=development                     # or production
DEBUG=true                          # or false

# Ports
PORT=8000                           # Backend port
FRONTEND_PORT=3000                  # Frontend port

# Database
DATABASE_URL=postgresql://...       # PostgreSQL
MONGO_URI=mongodb://...             # MongoDB
REDIS_URL=redis://...               # Redis

# API Keys (Optional)
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...

# Security
SECRET_KEY=your-secret-key          # Generated automatically
JWT_EXPIRATION_HOURS=24             # Token lifetime
```

---

## 🐛 Quick Debugging

### "It's not working!"

```bash
# Step 1: Check health
bash scripts/health-check.sh

# Step 2: View logs
docker-compose logs

# Step 3: Check system
bash scripts/system-requirements.sh

# Step 4: Restart everything
docker-compose restart

# Step 5: If still broken, nuclear reset
docker-compose down -v
bash deploy.sh --quick-start
```

---

## 📱 Useful Key Combinations

| Key | What | Use When |
|-----|------|----------|
| **Ctrl+C** | Stop logs | Watching logs |
| **Ctrl+D** | Exit container | Inside container shell |
| **Ctrl+L** | Clear terminal | Terminal too cluttered |
| **↑ Arrow** | Previous command | Running similar commands |

---

## 🌍 Multi-Computer Setup

### Access from Another Machine

```bash
# Find your IP
hostname -I                         # Linux
ifconfig | grep inet                # macOS

# Access from other computer
# http://192.168.1.100:3000        # Replace with your IP

# For internet access (advanced)
# See DEPLOYMENT_READY.md for nginx/domain setup
```

---

## 💾 Backup & Restore

### Backup Your Data
```bash
bash scripts/backup.sh              # Create backup
ls -la backups/                     # See backups
```

### Restore From Backup
```bash
bash scripts/restore.sh backup_name # Restore data
```

---

## 📞 Help Resources

| Resource | Where | What |
|----------|-------|------|
| **This Card** | QUICK_REFERENCE.md | Quick answers |
| **Full Guide** | DEPLOYMENT_READY.md | Complete setup |
| **Troubleshooting** | TROUBLESHOOTING.md | Problem solving |
| **API Docs** | http://localhost:8000/docs | Code reference |
| **Architecture** | V5_INTEGRATION_ARCHITECTURE.md | How it works |
| **GitHub Issues** | Repository/issues | Report bugs |

---

## 🎯 Common Workflows

### "I Want to Start Fresh"
```bash
docker-compose down -v
bash deploy.sh --quick-start
```

### "Add New API Key"
```bash
nano .env
# Add key
docker-compose restart backend
```

### "Debug a Problem"
```bash
bash scripts/health-check.sh
docker-compose logs | grep -i error
```

### "Check System Load"
```bash
docker stats
free -h
df -h
```

### "View What's Running"
```bash
docker-compose ps
docker-compose logs -f --tail 50
```

---

## ✅ Pre-Deployment Checklist

- [ ] Docker installed (`docker --version`)
- [ ] Docker Compose installed (`docker-compose --version`)
- [ ] Enough disk space (`df -h` shows 10GB+)
- [ ] Enough RAM (`free -h` shows 4GB+)
- [ ] Ports available (3000, 8000 not in use)
- [ ] Read DEPLOYMENT_READY.md
- [ ] Run `bash scripts/system-requirements.sh`

---

## 🎓 After Deployment Checklist

- [ ] Web UI accessible at http://localhost:3000
- [ ] API responding at http://localhost:8000/health
- [ ] All containers running (`docker-compose ps`)
- [ ] No errors in logs (`docker-compose logs`)
- [ ] Backups set up (`bash scripts/backup.sh`)
- [ ] API keys configured (optional but recommended)
- [ ] Read V5_INTEGRATION_ARCHITECTURE.md to understand it

---

## 🔗 Useful Links

- **Docker Docs**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **OpenAI API**: https://platform.openai.com/api-keys
- **Anthropic Claude**: https://console.anthropic.com/
- **GitHub**: https://github.com/yourusername/githubautom8

---

## ⚠️ Remember

- **Backups**: Do them regularly!
- **API Keys**: Don't share your .env file
- **Secrets**: Change SECRET_KEY in production
- **Updates**: Check for code updates regularly
- **Logs**: Check them when something's wrong
- **Documentation**: See DEPLOYMENT_READY.md first

---

**Last Updated**: February 2026  
**Print this card and keep it handy!**  
**Questions? See TROUBLESHOOTING.md**
