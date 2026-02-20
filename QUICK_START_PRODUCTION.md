# OchukoAi v6.0 Production Quick Start Guide

**⏱️ Total Time: 90 minutes to production deployment**

---

## Visual Deployment Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    OCHUKO AI DEPLOYMENT FLOW                     │
└─────────────────────────────────────────────────────────────────┘

START
  │
  ├─→ Phase 1: ENVIRONMENT SETUP (5 min)
  │    • Clone repository
  │    • Verify prerequisites
  │    • Create directories
  │
  ├─→ Phase 2: CONFIGURATION (10 min)
  │    • Copy .env.example → .env
  │    • Generate credentials
  │    • Validate configuration
  │
  ├─→ Phase 3: DOCKER BUILD (15 min)
  │    • Build Docker images
  │    • Verify all images
  │    • Start containers
  │
  ├─→ Phase 4: DATABASE INIT (10 min)
  │    • Wait for readiness
  │    • Run migrations
  │    • Verify connections
  │
  ├─→ Phase 5: APPLICATION VERIFY (10 min)
  │    • Test health endpoint
  │    • Run API tests
  │    • Baseline performance
  │
  ├─→ Phase 6: MONITORING SETUP (10 min)
  │    • Enable OpenTelemetry
  │    • Configure logging
  │    • Test alert routing
  │
  ├─→ Phase 7: SSL/TLS CONFIG (5 min optional)
  │    • Install certificates
  │    • Configure Nginx
  │    • Verify HTTPS
  │
  ├─→ Phase 8: HARDENING (15 min)
  │    • Security configuration
  │    • Firewall rules
  │    • Resource limits
  │
  ├─→ Phase 9: SCALING (5 min optional)
  │    • Configure replicas
  │    • Load balancing
  │    • High availability
  │
  ├─→ Phase 10: FINAL VERIFICATION (5 min)
  │    • Run checklist
  │    • System tests
  │    • Sign-off
  │
  └─→ ✅ PRODUCTION READY
```

---

## Phase-by-Phase Instructions

### Phase 1️⃣: Environment Setup (5 minutes)

#### Step 1.1: Clone Repository
```bash
cd /home/c0sm0s/Desktop/2\ -\ 0\ -\ 2\ -\ 6/L-E-G-I-T
git clone https://github.com/MrIridescent/OchukoAi.git
cd OchukoAi
git checkout master
```

**✅ Verify:**
```bash
ls -la | grep -E "docker-compose|backend_main|requirements"
# Should see: docker-compose.yml, backend_main.py, requirements_universal.txt
```

#### Step 1.2: Verify Prerequisites
```bash
echo "=== System Requirements ==="
docker --version          # Need 20.10+
docker compose --version  # Need 2.0+
git --version            # Need 2.30+
python3 --version        # Need 3.11+

echo "=== Available Resources ==="
free -h                  # Should have 8GB+ RAM
df -h /                  # Should have 50GB+ free
```

**✅ Verify:** All versions meet minimums

#### Step 1.3: Create Required Directories
```bash
mkdir -p backups logs data certs config
chmod 755 backups logs data certs config
```

**✅ Verify:**
```bash
ls -d backups logs data certs config
```

---

### Phase 2️⃣: Configuration (10 minutes)

#### Step 2.1: Create Environment File
```bash
cp .env.example .env
chmod 600 .env
```

#### Step 2.2: Generate Secure Credentials
```bash
# Generate strong passwords
DB_PASSWORD=$(openssl rand -base64 32)
MONGO_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -base64 32)

echo "Database password: $DB_PASSWORD"
echo "MongoDB password: $MONGO_PASSWORD"
echo "Redis password: $REDIS_PASSWORD"
echo "Secret key: $SECRET_KEY"
echo "JWT secret: $JWT_SECRET"
```

#### Step 2.3: Edit Environment File
```bash
# Use your favorite editor
nano .env

# Required changes (search and replace):
CHANGEME_DB_PASSWORD          → $DB_PASSWORD
CHANGEME_MONGO_PASSWORD       → $MONGO_PASSWORD
CHANGEME_REDIS_PASSWORD       → $REDIS_PASSWORD
CHANGEME_SECRET_KEY           → $SECRET_KEY
CHANGEME_JWT_SECRET           → $JWT_SECRET
CHANGEME_OPENAI_API_KEY       → [Get from OpenAI]
CHANGEME_ANTHROPIC_API_KEY    → [Get from Anthropic]
CHANGEME_GOOGLE_API_KEY       → [Get from Google]

# Optional but recommended:
APP_ENV                       → production
DEBUG                         → false
LOG_LEVEL                     → info
REPLICAS                      → 3 (for HA)
```

**📝 API Key Sources:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google: https://console.cloud.google.com/

#### Step 2.4: Validate Configuration
```bash
# Check syntax
python3 << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv('.env')
required_keys = [
    'APP_ENV', 'DATABASE_URL', 'MONGODB_URI', 'REDIS_URL',
    'SECRET_KEY', 'JWT_SECRET', 'OPENAI_API_KEY'
]

for key in required_keys:
    value = os.getenv(key, '').strip()
    if not value or 'CHANGEME' in value:
        print(f"❌ Missing/invalid: {key}")
    else:
        print(f"✅ {key}")
EOF
```

**✅ Verify:** All keys show ✅

---

### Phase 3️⃣: Docker Build & Start (15 minutes)

#### Step 3.1: Build Docker Images
```bash
echo "Building Docker images (this takes 10 minutes)..."
docker compose build --no-cache 2>&1 | tail -20
```

**⏳ Monitor Progress:**
```bash
# In another terminal
watch -n 5 "docker images | grep ochuko"
```

**✅ Verify:**
```bash
docker images | grep -E "ochuko-app|postgres|mongo|redis|nginx"
# Should see multiple images listed
```

#### Step 3.2: Start Services
```bash
echo "Starting services..."
docker compose up -d

echo "Waiting for services to initialize..."
sleep 30

echo "Checking service status..."
docker compose ps
```

**✅ Verify Output:**
```
NAME                   STATUS
postgres_db           Up 30s (healthy)
mongo_db              Up 30s (healthy)
redis                 Up 30s (healthy)
ochuko-app            Up 30s (healthy)
nginx                 Up 30s (healthy)
```

#### Step 3.3: Monitor Startup Logs
```bash
echo "Last 50 lines of application startup:"
docker compose logs ochuko-app --tail=50

# Look for:
# "Application startup complete"
# "Database connections verified"
# No "ERROR" messages
```

---

### Phase 4️⃣: Database Initialization (10 minutes)

#### Step 4.1: Wait for PostgreSQL
```bash
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
  if docker compose exec postgres_db pg_isready -U "${DB_USER}" > /dev/null 2>&1; then
    echo "✅ PostgreSQL ready"
    break
  fi
  echo "⏳ Attempt $i/30..."
  sleep 2
done
```

#### Step 4.2: Verify Database Connection
```bash
docker compose exec postgres_db psql \
  -U "${DB_USER}" \
  -d "${DB_NAME}" \
  -c "SELECT 1 as connection_test"
```

**✅ Expected Output:**
```
 connection_test
─────────────────
             1
(1 row)
```

#### Step 4.3: Run Database Migrations
```bash
docker compose exec ochuko-app alembic upgrade head
```

**✅ Verify:**
```bash
docker compose exec postgres_db psql \
  -U "${DB_USER}" \
  -d "${DB_NAME}" \
  -c "\dt"  # List tables
```

#### Step 4.4: Verify MongoDB
```bash
docker compose exec mongo_db mongosh \
  -u "${MONGO_USER}" \
  -p "${MONGO_PASSWORD}" \
  --authenticationDatabase admin \
  --eval "db.adminCommand('ping')"
```

**✅ Expected Output:** `{ ok: 1 }`

#### Step 4.5: Verify Redis
```bash
docker compose exec redis redis-cli \
  -a "${REDIS_PASSWORD}" \
  ping
```

**✅ Expected Output:** `PONG`

---

### Phase 5️⃣: Application Verification (10 minutes)

#### Step 5.1: Health Check
```bash
echo "Testing /health endpoint..."
curl -v http://localhost:8000/health | python3 -m json.tool
```

**✅ Expected Output:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-20T...",
  "services": {
    "database": "connected",
    "cache": "connected",
    "reasoning_engine": "ready"
  }
}
```

#### Step 5.2: Detailed Health Check
```bash
echo "Testing detailed health..."
curl -s http://localhost:8000/health/detailed | python3 -m json.tool | head -30
```

#### Step 5.3: API Test - Reasoning Endpoint
```bash
curl -X POST http://localhost:8000/api/reason \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the implications of artificial intelligence?",
    "modes": ["rational", "creative", "systems"],
    "depth": "comprehensive"
  }' | python3 -m json.tool | head -40
```

**✅ Expected:** Response with reasoning modes executed

#### Step 5.4: Performance Baseline
```bash
echo "Running performance test (10 requests)..."
time for i in {1..10}; do
  curl -s http://localhost:8000/health > /dev/null
done

# Expected: Total time < 2 seconds
```

#### Step 5.5: Documentation Access
```bash
# Verify API docs available
curl -s http://localhost:8000/docs | grep -o "<title>.*</title>"
# Expected: "<title>Swagger UI</title>"

echo "✅ API docs available at: http://localhost:8000/docs"
```

---

### Phase 6️⃣: Monitoring Setup (10 minutes)

#### Step 6.1: Verify Logging
```bash
echo "Checking structured logs..."
docker compose logs ochuko-app --tail=20 | grep -i "INFO\|ERROR"

echo "Recent log entries:"
docker compose logs --timestamps --tail=10
```

#### Step 6.2: OpenTelemetry Verification
```bash
echo "Checking OpenTelemetry traces..."
curl -s http://localhost:4317/v1/traces | wc -c
# Expected: Non-zero bytes indicating traces being collected
```

#### Step 6.3: Prometheus Metrics
```bash
echo "Testing Prometheus endpoint..."
curl -s http://localhost:9090/api/v1/targets | python3 -m json.tool | grep -A 2 "\"job\""
```

#### Step 6.4: Test Alert Routing (Optional)
```bash
# If Slack configured, test notification:
curl -X POST ${SLACK_WEBHOOK_URL} \
  -H 'Content-Type: application/json' \
  -d '{"text": "Test deployment alert - OchukoAi starting"}'
```

---

### Phase 7️⃣: SSL/TLS Configuration (5 minutes - Optional)

#### Step 7.1: Generate Self-Signed Certificates (Testing)
```bash
# For production, use LetsEncrypt instead
mkdir -p certs
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes \
  -subj "/C=US/ST=State/L=City/O=OchukoAi/CN=localhost"

chmod 600 certs/key.pem
chmod 644 certs/cert.pem
```

#### Step 7.2: Configure Nginx for HTTPS
```bash
# Edit docker-compose.yml to include SSL section in nginx
# OR use docker-compose.ssl.yml if available

# Verify SSL configuration
docker compose exec nginx nginx -t
```

#### Step 7.3: Test HTTPS
```bash
curl -k https://localhost:443/health
# -k: ignore self-signed cert warning
```

#### Step 7.4: For Production - Use LetsEncrypt
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure auto-renewal
sudo certbot renew --dry-run
```

---

### Phase 8️⃣: Security Hardening (15 minutes)

#### Step 8.1: File Permissions
```bash
echo "Setting secure file permissions..."
chmod 600 .env                    # Read/write owner only
chmod 700 backups logs data certs # Directory access only for owner
chmod 644 docker-compose.yml      # Config readable
chmod 755 deployment_verification.py
```

#### Step 8.2: Firewall Configuration (Ubuntu/Debian)
```bash
# Install UFW if needed
sudo apt-get install ufw

# Allow only required ports
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh        # Port 22
sudo ufw allow http       # Port 80
sudo ufw allow https      # Port 443
sudo ufw allow from 127.0.0.1  # Localhost only
sudo ufw enable

# Verify
sudo ufw status
```

#### Step 8.3: Docker Security
```bash
# Run security check
docker run --rm --volume /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image ochuko-app:latest
```

#### Step 8.4: Database Security
```bash
# Verify password authentication (no empty passwords)
docker compose exec postgres_db psql \
  -U "${DB_USER}" \
  -c "SELECT usename FROM pg_user WHERE usecanlogin = true;"

# Enable SSL for PostgreSQL (optional)
docker compose exec postgres_db psql \
  -U "${DB_USER}" \
  -c "ALTER SYSTEM SET ssl = on;"
```

#### Step 8.5: Set Resource Limits
```bash
# In docker-compose.yml, verify limits set:
# deploy:
#   resources:
#     limits:
#       cpus: '2'
#       memory: 4G

docker stats --no-stream | grep ochuko-app
```

#### Step 8.6: Disable Debug Mode
```bash
# Verify in .env
grep "DEBUG=" .env
# Should show: DEBUG=false

# If needed, update and restart
docker compose restart ochuko-app
```

---

### Phase 9️⃣: Scaling Configuration (5 minutes - Optional)

#### Step 9.1: Configure Replicas
```bash
# Edit .env to set number of replicas
# REPLICAS=3

# Or scale directly
docker compose up -d --scale ochuko-app=3

# Verify
docker compose ps | grep ochuko-app
# Should show 3 instances
```

#### Step 9.2: Configure Load Balancer
```bash
# Verify Nginx configuration includes upstream
docker compose exec nginx cat /etc/nginx/nginx.conf | grep -A 10 "upstream"
```

#### Step 9.3: Test Load Balancing
```bash
# Make multiple requests and verify distribution
for i in {1..9}; do
  curl -s http://localhost:8000/health | grep -o '"hostname":"[^"]*"'
done
# Should see different hostnames
```

#### Step 9.4: Configure Auto-Scaling (Advanced)
```bash
# Option 1: Manual scaling as needed
docker compose up -d --scale ochuko-app=5

# Option 2: Kubernetes (if available)
kubectl apply -f k8s/deployment.yaml --replicas=5

# Monitor usage
docker stats --no-stream
```

---

### Phase 🔟: Final Verification (5 minutes)

#### Step 10.1: Run Comprehensive Verification Script
```bash
python3 deployment_verification.py
```

**✅ Expected Output:**
```
╔══════════════════════════════════════════════════════════════════╗
║             OchukoAi Production Deployment Verification           ║
╚══════════════════════════════════════════════════════════════════╝

✅ Docker daemon is running and accessible
✅ Docker Compose is installed (v2.X.X+)
✅ All containers are running
✅ PostgreSQL connection successful
✅ MongoDB connection successful
✅ Redis connection successful
✅ API health check passed
✅ Environment configuration is valid
✅ File structure verified
✅ Security configuration verified

═══════════════════════════════════════════════════════════════════
                    ✅ ALL CHECKS PASSED
              🚀 DEPLOYMENT READY FOR PRODUCTION 🚀
═══════════════════════════════════════════════════════════════════

Duration: 2.34 seconds
Timestamp: 2026-02-20 19:25:37

Exit Code: 0 (Success)
```

#### Step 10.2: Performance Check
```bash
# Measure response times
echo "Testing response times..."
for endpoint in "/health" "/api/reason" "/docs"; do
  start=$(date +%s%N)
  curl -s http://localhost:8000$endpoint > /dev/null
  end=$(date +%s%N)
  duration=$(( ($end - $start) / 1000000 ))
  echo "$endpoint: ${duration}ms"
done

# Expected: All < 500ms for /health, < 2000ms for /api/reason
```

#### Step 10.3: Database Backup Test
```bash
# Test backup process
mkdir -p backups
pg_dump -U "${DB_USER}" -d "${DB_NAME}" | gzip > backups/test_backup.sql.gz

# Verify backup
ls -lh backups/test_backup.sql.gz
gzip -t backups/test_backup.sql.gz && echo "✅ Backup valid"
```

#### Step 10.4: Logs Verification
```bash
# Check for errors
docker compose logs --all | grep -i "error\|critical\|failed"

# If none found, logs are clean
echo "✅ No critical errors in logs"
```

#### Step 10.5: Sign-Off Checklist
```
✅ All 5 phases completed
✅ All services healthy
✅ API endpoints working
✅ Database connected
✅ Cache operational
✅ Monitoring active
✅ Backup tested
✅ Security configured
✅ Performance baseline recorded
✅ Team trained

✅ READY FOR PRODUCTION TRAFFIC
```

---

## Quick Reference Commands

### Service Management
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart specific service
docker compose restart ochuko-app

# View logs
docker compose logs -f ochuko-app --tail=50

# Execute command in container
docker compose exec ochuko-app python -c "print('test')"
```

### Database Operations
```bash
# PostgreSQL shell
docker compose exec postgres_db psql -U ${DB_USER} -d ${DB_NAME}

# MongoDB shell
docker compose exec mongo_db mongosh -u ${MONGO_USER} -p ${MONGO_PASSWORD}

# Redis CLI
docker compose exec redis redis-cli -a ${REDIS_PASSWORD}

# Backup database
pg_dump -U ${DB_USER} -d ${DB_NAME} | gzip > backups/backup.sql.gz

# Restore database
gunzip -c backups/backup.sql.gz | psql -U ${DB_USER} -d ${DB_NAME}
```

### Monitoring
```bash
# System resources
docker stats --no-stream

# Container status
docker compose ps

# Detailed health check
curl http://localhost:8000/health/detailed | python3 -m json.tool

# View metrics
curl http://localhost:9090/api/v1/query?query=up
```

### Troubleshooting
```bash
# Full system check
python3 deployment_verification.py

# Check specific service
docker compose exec postgres_db pg_isready

# View resource usage
docker stats ochuko-app

# Test connectivity
docker compose exec ochuko-app ping postgres_db

# Check logs for errors
docker compose logs | grep -i error
```

---

## Emergency Procedures

### Emergency Stop
```bash
docker compose kill
```

### Emergency Restart
```bash
docker compose down && sleep 10 && docker compose up -d
```

### Reset Everything (⚠️ DATA LOSS)
```bash
docker compose down -v
docker compose up -d
```

### Restore from Backup
```bash
gunzip -c backups/latest.sql.gz | docker compose exec -T postgres_db psql -U ${DB_USER} -d ${DB_NAME}
docker compose restart
```

---

## Success Criteria ✅

**Deployment is successful when:**
1. ✅ `docker compose ps` shows all containers running (healthy)
2. ✅ `curl http://localhost:8000/health` returns 200 with "healthy" status
3. ✅ `python3 deployment_verification.py` returns exit code 0
4. ✅ API documentation accessible at `http://localhost:8000/docs`
5. ✅ No error messages in logs: `docker compose logs | grep -i error` returns nothing
6. ✅ Database connections verified with query tests
7. ✅ Backup created successfully in backups directory
8. ✅ Monitoring and alerting configured and tested

---

## Next Steps

After successful deployment:

1. **Monitor**: Watch logs and metrics for 24 hours
2. **Test**: Run full integration tests
3. **Document**: Record any customizations made
4. **Train**: Ensure team knows operations procedures
5. **Schedule**: Set up regular backups and maintenance
6. **Scale**: Monitor load and scale as needed

---

**Created**: February 2026  
**Status**: ✅ PRODUCTION READY  
**Version**: 1.0  
**Support**: See TROUBLESHOOTING_GUIDE.md for issues
