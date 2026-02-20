# Ochuko AI v5.0 - Deployment Ready Guide

**For Complete Newbies to Prod Experts**

**Author**: David Akpoviroro Oke (MrIridescent)  
**Version**: 5.0.0 - Deployment Ready  
**Date**: February 2026  
**Status**: ✅ **ONE-CLICK DEPLOYMENT READY**

---

## 🚀 The 5-Minute Deployment (Complete Newbie)

### Step 1: One-Click Deploy
```bash
# Copy this entire command and paste it into your terminal
git clone https://github.com/yourusername/githubautom8.git && cd githubautom8 && bash deploy.sh --quick-start
```

**What happens:**
- ✅ Checks your system (Docker, git, etc.)
- ✅ Creates environment file (.env)
- ✅ Starts all services (backend, frontend, databases)
- ✅ Verifies everything works
- ✅ Gives you the URL to access it

**When it's done** (you'll see):
```
✅ DEPLOYMENT COMPLETE
🌐 Frontend: http://localhost:3000
📡 Backend API: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
```

**Access it:**
- Open browser → http://localhost:3000
- Done! Start using it.

---

## 📋 What You Need (System Requirements)

### Minimum (Works)
- **CPU**: 2 cores (Intel/AMD or ARM)
- **RAM**: 4GB
- **Storage**: 10GB
- **Internet**: Yes (for API keys)
- **OS**: Linux, macOS, Windows (with WSL2), or cloud VM

### Recommended (Better)
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 20GB+ SSD
- **Internet**: Stable connection
- **OS**: Ubuntu 20.04+ / Debian / macOS 11+ / Windows 11 with WSL2

### What Software To Have
- **Docker** (automatic checker will tell you if missing)
- **Docker Compose** (comes with Docker Desktop)
- **Git** (optional, can download ZIP instead)

---

## 🔧 Installation Methods

### Method 1: One-Click (Easiest)
**For**: Complete newbies, quick testing, local development

```bash
bash deploy.sh --quick-start
```

- Creates everything automatically
- Starts all services
- No manual configuration
- Perfect for: Testing the system

---

### Method 2: Step-by-Step (Transparent)
**For**: People who want to understand what's happening

```bash
# 1. Clone the code
git clone https://github.com/yourusername/githubautom8.git
cd githubautom8

# 2. Run setup wizard
bash setup.sh

# 3. Configure your API keys (it will guide you)
nano .env
# OR
vim .env

# 4. Start services
docker-compose up -d

# 5. Check status
bash scripts/health-check.sh

# 6. View access info
bash scripts/access-info.sh
```

---

### Method 3: Production (Cloud Deployment)
**For**: Real servers, AWS/GCP/Azure, long-term usage

#### On Ubuntu/Debian Server:

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Clone and deploy
git clone https://github.com/yourusername/githubautom8.git
cd githubautom8

# 4. Use production deployment
bash deploy.sh --production

# 5. Configure domain (optional)
# Edit docker-compose.yml to change 0.0.0.0 to your domain
```

**Result:**
- ✅ Running on your server
- ✅ Accessible from internet (if configured)
- ✅ Persistent storage
- ✅ Automatic backups (optional)

---

## 🗝️ API Keys Setup

**What you need:**
These are optional but recommended for full features.

### 1. OpenAI (For GPT-4)
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy it
4. Paste in `.env` file: `OPENAI_API_KEY=sk-...`

### 2. Anthropic Claude (For Claude 3)
1. Go to https://console.anthropic.com/
2. Create new API key
3. Copy it
4. Paste in `.env` file: `CLAUDE_API_KEY=sk-ant-...`

### 3. Other APIs (Optional)
- Google Cloud (for speech/vision)
- AWS (for storage)
- Slack (for integration)
- etc.

**Don't have keys?**
→ System works without them, just with reduced features
→ You can add keys later anytime

---

## 📁 What Gets Created

After deployment:

```
githubautom8/
├── .env                          # Your configuration (auto-created)
├── .env.example                  # Template (don't edit)
├── docker-compose.yml            # Services definition
├── deploy.sh                      # Deployment script
├── setup.sh                       # Setup wizard
├── scripts/
│   ├── health-check.sh          # Check if everything works
│   ├── access-info.sh           # Show URLs and access info
│   ├── restart-services.sh      # Restart everything
│   ├── logs.sh                  # View logs
│   └── stop.sh                  # Stop everything safely
├── data/
│   ├── postgres/                # Database files (auto-created)
│   ├── mongodb/                 # Document store (auto-created)
│   ├── redis/                   # Cache (auto-created)
│   └── uploads/                 # User uploads (auto-created)
└── logs/
    └── app.log                  # Application logs
```

---

## ✅ Verify It's Working

After deployment completes:

### Check Status
```bash
bash scripts/health-check.sh
```

**You'll see:**
```
✅ Backend API: Running
✅ Frontend: Running
✅ PostgreSQL: Running
✅ Redis: Running
✅ MongoDB: Running
All systems operational (5/5)
```

### View Logs
```bash
bash scripts/logs.sh

# OR just the last 50 lines:
docker-compose logs -f --tail 50
```

### Try It Out
```bash
# Visit the web interface
open http://localhost:3000

# Test the API
curl http://localhost:8000/health
# Should respond with: {"status": "healthy"}
```

---

## 🌐 Accessing Your System

After deployment:

| Component | URL | What It Does |
|-----------|-----|--------------|
| **Web Interface** | http://localhost:3000 | The UI - use this for everything |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **API** | http://localhost:8000 | Backend API endpoint |
| **Health Check** | http://localhost:8000/health | Quick status check |
| **Metrics** | http://localhost:8000/metrics | Performance metrics |

**On a server?**
- Replace `localhost` with your server IP or domain
- Example: http://123.45.67.89:3000

---

## 🔧 Managing Your System

### Start Everything
```bash
docker-compose up -d
```

### Stop Everything (Safely)
```bash
docker-compose down
```

### View Logs (Real-Time)
```bash
docker-compose logs -f
```

### Restart Specific Service
```bash
docker-compose restart backend
# or
docker-compose restart frontend
# or
docker-compose restart postgres
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

### Check Usage (CPU, Memory, Disk)
```bash
bash scripts/resource-monitor.sh
```

---

## ⚡ Quick Commands Reference

```bash
# View all helper scripts
ls scripts/

# Check system status
bash scripts/health-check.sh

# View access information
bash scripts/access-info.sh

# View logs
bash scripts/logs.sh

# Restart all services
bash scripts/restart-services.sh

# Stop all services
bash scripts/stop.sh

# Reset everything (CAREFUL!)
bash scripts/reset-all.sh

# Monitor resources
bash scripts/resource-monitor.sh

# Backup data
bash scripts/backup.sh

# Restore backup
bash scripts/restore.sh
```

---

## 🐛 Troubleshooting

### "Docker not found"
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
# Then try deployment again
```

### "Port 3000 already in use"
```bash
# Kill process using port 3000
lsof -ti :3000 | xargs kill -9
# Or use different port in .env
echo "PORT=3001" >> .env
```

### "Port 8000 already in use"
```bash
# Kill process using port 8000
lsof -ti :8000 | xargs kill -9
# Or change in docker-compose.yml
```

### "Out of disk space"
```bash
# Clean up Docker
docker system prune -a

# Check disk usage
df -h

# Or delete old logs
rm logs/*.log
```

### "Database won't start"
```bash
# Check logs
docker-compose logs postgres

# Reset database
docker-compose down -v  # WARNING: deletes data!
docker-compose up -d
```

### "API keys not working"
```bash
# Check your .env file
cat .env | grep API_KEY

# Verify key format:
# OPENAI_API_KEY=sk-...  (should start with sk-)
# CLAUDE_API_KEY=sk-ant-...  (should start with sk-ant-)

# Restart services to pick up new keys
docker-compose restart backend
```

### "Frontend won't load"
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose up -d --build frontend
```

### "Can't access from another computer"
```bash
# Find your IP
hostname -I  # on Linux
ifconfig    # on macOS

# Then use in browser:
# http://YOUR_IP:3000

# Note: Won't work over internet unless configured for that
```

---

## 📊 Performance Tuning

### For Better Speed
```bash
# Increase backend workers
# Edit docker-compose.yml:
WORKERS=8  # default is 4

# Increase database connections
# In .env:
DATABASE_POOL_SIZE=20
```

### For Better Stability
```bash
# Increase memory limit
# Edit docker-compose.yml services section:
mem_limit: 2g  # for 2GB per service

# Enable auto-restart
# Services already have restart: unless-stopped
```

### Monitor Performance
```bash
# Real-time monitoring
bash scripts/resource-monitor.sh

# View metrics
curl http://localhost:8000/metrics
```

---

## 🔒 Security Best Practices

### Before Going Live

```bash
# 1. Change secret key
# Edit .env:
SECRET_KEY=YOUR_VERY_LONG_RANDOM_STRING_HERE

# 2. Change database passwords
# Edit .env:
POSTGRES_PASSWORD=strong_password_here
MONGO_PASSWORD=strong_password_here

# 3. Set environment to production
# Edit .env:
ENV=production
DEBUG=false

# 4. Configure CORS properly
# Edit .env:
CORS_ORIGINS=["https://yourdomain.com"]

# 5. Use HTTPS (get SSL cert)
# See nginx configuration below
```

### Backing Up Your Data

```bash
# Daily backup (add to crontab)
0 2 * * * cd /path/to/githubautom8 && bash scripts/backup.sh

# Restore from backup if needed
bash scripts/restore.sh backup_name
```

---

## 🌍 Deploying to Cloud

### AWS EC2
```bash
# 1. Create EC2 instance (Ubuntu 20.04, t3.medium minimum)
# 2. SSH in
# 3. Follow "Method 3: Production" above
```

### Google Cloud
```bash
# 1. Create Compute Engine instance
# 2. SSH in
# 3. Follow "Method 3: Production" above
```

### DigitalOcean
```bash
# 1. Create Droplet (Ubuntu 20.04, $5-10/month)
# 2. SSH in
# 3. Follow "Method 3: Production" above
```

### Heroku (Easiest Cloud)
```bash
# 1. Install Heroku CLI
# 2. heroku create yourappname
# 3. heroku config:set OPENAI_API_KEY=...
# 4. git push heroku main
# (Requires Procfile configuration)
```

---

## 📞 Support & Help

### If Something Goes Wrong

**Step 1**: Check health
```bash
bash scripts/health-check.sh
```

**Step 2**: View logs
```bash
bash scripts/logs.sh
```

**Step 3**: Check troubleshooting section above

**Step 4**: Search GitHub issues
```
https://github.com/yourusername/githubautom8/issues
```

**Step 5**: Create a new issue with:
- What you were trying to do
- What error you got
- Output of: `bash scripts/health-check.sh`

---

## ✨ Next Steps After Deployment

### 1. Explore Features
- Open http://localhost:3000
- Try the chat interface
- Test voice (if enabled)
- Try face recognition (if available)

### 2. Configure APIs
- Add your OpenAI key for GPT-4
- Add Anthropic key for Claude
- Configure other services as needed

### 3. Customize Settings
- Edit `.env` to change behavior
- Configure language, timezone, etc.
- Set up integrations you want

### 4. Create Users
- Set up user accounts
- Configure permissions
- Enable 2FA if desired

### 5. Monitor Performance
- Use `bash scripts/resource-monitor.sh`
- Check logs regularly
- Monitor disk space

### 6. Backup Important Data
- Set up automated backups
- Test restore process
- Keep backups off-site

---

## 🎓 Learning Resources

### Understanding the System
- **README.md** - What this system is
- **V5_INTEGRATION_ARCHITECTURE.md** - How everything works
- **SYSTEM_CAPABILITIES_v5.md** - What it can do
- **API docs** - http://localhost:8000/docs

### Development
- **MCP_CREWAI_ARCHITECTURE.md** - How to extend with agents/tools
- **SESSION_COMPLETION_SUMMARY_v5.md** - What was built
- Check individual files for detailed comments

### Operations
- **This file** - Deployment & operations
- **TECHNICAL_SPECIFICATIONS.md** - System requirements
- **IMPLEMENTATION_ROADMAP_v5.md** - Future plans

---

## 🎯 Common Use Cases

### Use Case 1: Personal AI Assistant
```bash
# 1. Deploy locally
bash deploy.sh --quick-start

# 2. Access at http://localhost:3000
# 3. Start chatting
# 4. Add API keys for better responses
```

### Use Case 2: Team Collaboration
```bash
# 1. Deploy on server
bash deploy.sh --production

# 2. Create multiple user accounts
# 3. Share URL with team
# 4. Collaborate in real-time
```

### Use Case 3: Business Integration
```bash
# 1. Deploy with custom domain
# 2. Configure Slack/Teams integration
# 3. Set up API access for other systems
# 4. Enable advanced analytics
```

### Use Case 4: Research Project
```bash
# 1. Deploy on GPU server (optional)
# 2. Configure local LLM if needed
# 3. Run experiments
# 4. Analyze results
```

---

## 📈 Scaling (When You Grow)

### If You Get More Users

```bash
# Increase backend workers
WORKERS=16  # in .env

# Use external database
DATABASE_URL=postgresql://prod-db.com/...

# Add load balancer (nginx)
# See deployment-nginx.conf

# Use CDN for frontend
# Configure CloudFlare or similar
```

### If You Run Out of Storage

```bash
# Use external storage
STORAGE_TYPE=s3  # in .env
AWS_S3_BUCKET=...

# Archive old data
bash scripts/archive.sh

# Clean up logs
bash scripts/cleanup-logs.sh
```

---

## 🏁 Final Checklist

- ✅ System deployed and running
- ✅ Health check passes
- ✅ Can access web interface
- ✅ API responding at /health
- ✅ Databases connected
- ✅ API keys configured (optional)
- ✅ Backups set up
- ✅ Monitoring enabled
- ✅ Security configured
- ✅ Team members can access

**YOU'RE READY! 🎉**

---

## 📞 Get Help

- **Issues**: GitHub Issues on repository
- **Docs**: This guide + files in repository
- **Community**: Discussions on GitHub
- **Commercial**: Contact support@ochuko-ai.com

---

**Status**: ✅ **PRODUCTION READY**  
**Last Updated**: February 2026  
**Maintained By**: David Akpoviroro Oke (MrIridescent)
