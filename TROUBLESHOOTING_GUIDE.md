# OchukoAi Production Troubleshooting Guide

## Quick Diagnostics

### Check Overall System Health
```bash
python deployment_verification.py
docker compose ps
docker compose logs -f --tail=50
```

### View Recent Errors
```bash
docker compose logs ochuko-app --tail=100 | grep -i error
docker compose exec postgres_db psql -U ${DB_USER} -d ${DB_NAME} -c "SELECT * FROM pg_stat_activity;"
docker compose exec mongo_db mongosh --eval "db.currentOp()"
```

---

## Common Issues & Solutions

### 1. Application Won't Start

#### Problem: Container exits immediately
```bash
# Check logs
docker compose logs ochuko-app

# Expected: Should see startup sequence
```

**Solutions:**
- [ ] Check `.env` file exists and is readable: `ls -la .env`
- [ ] Validate `.env` syntax: `python -c "import dotenv; dotenv.load_dotenv()"`
- [ ] Check all required keys present in `.env`
- [ ] Ensure no CHANGEME values remain: `grep CHANGEME .env`
- [ ] Check permissions: `chmod 644 .env`
- [ ] Verify Python syntax: `python -m py_compile backend_main.py`
- [ ] Check memory: `free -h` (need at least 2GB free)

#### Problem: Port already in use
```bash
# Find process using port
lsof -i :8000
lsof -i :5432
lsof -i :27017
lsof -i :6379

# Kill if necessary
kill -9 <PID>
```

**Solutions:**
- [ ] Change ports in `.env` and `docker-compose.yml`
- [ ] Stop conflicting services: `systemctl stop service_name`
- [ ] Wait for TCP TIME_WAIT: `netstat -an | grep TIME_WAIT | wc -l`

#### Problem: Insufficient memory
```bash
docker system df
docker stats --no-stream
```

**Solutions:**
- [ ] Increase Docker daemon memory limit
- [ ] Reduce replica count in `.env` (REPLICAS=1)
- [ ] Close other applications
- [ ] Check disk space: `df -h /`

---

### 2. Database Connection Failures

#### Problem: PostgreSQL connection refused
```bash
docker compose logs postgres_db | tail -20
docker compose exec postgres_db psql -U ${DB_USER} -c "SELECT 1"
```

**Solutions:**
- [ ] Ensure PostgreSQL container is running: `docker compose ps postgres_db`
- [ ] Check credentials in `.env`: `grep POSTGRES_ .env`
- [ ] Verify password doesn't contain special chars that break connection string
- [ ] Wait 30 seconds for initialization: `sleep 30`
- [ ] Check PostgreSQL logs for startup errors
- [ ] Reset PostgreSQL: `docker compose down -v && docker compose up -d postgres_db`
- [ ] Verify network connectivity: `docker compose exec ochuko-app ping postgres_db`

#### Problem: MongoDB authentication failed
```bash
docker compose logs mongo_db | tail -20
docker compose exec mongo_db mongosh --username ${MONGO_USER} --password ${MONGO_PASSWORD} --authenticationDatabase admin
```

**Solutions:**
- [ ] Verify MongoDB credentials in `.env`
- [ ] Check password encoding (no special chars or escape them)
- [ ] MongoDB may require URI encoding for special characters
- [ ] Reset MongoDB: `docker compose down -v && docker compose up -d mongo_db`
- [ ] Enable MongoDB auth: Set `MONGO_AUTH_ENABLED=true`

#### Problem: Redis connection timeout
```bash
docker compose logs redis --tail=20
docker compose exec redis redis-cli ping
```

**Solutions:**
- [ ] Check Redis container running: `docker compose ps redis`
- [ ] Verify Redis password: `docker compose exec redis redis-cli --no-auth-warning -a ${REDIS_PASSWORD} ping`
- [ ] Increase timeout in code: `REDIS_TIMEOUT=10`
- [ ] Check Redis memory: `docker compose exec redis redis-cli info memory`
- [ ] Restart Redis: `docker compose restart redis`

---

### 3. API Endpoints Not Responding

#### Problem: GET /health returns 500
```bash
curl -v http://localhost:8000/health
docker compose logs ochuko-app | grep -A5 "health"
```

**Solutions:**
- [ ] Check if app container is running: `docker compose ps ochuko-app`
- [ ] Verify database connections initialized
- [ ] Check dependencies loaded: Look for import errors in logs
- [ ] Restart application: `docker compose restart ochuko-app`
- [ ] Check port mapping: `docker compose port ochuko-app 8000`

#### Problem: Requests timeout (>30 seconds)
```bash
curl -v --max-time 5 http://localhost:8000/api/reason
# Check processing logs
docker compose logs ochuko-app --since 1m | grep -i "timeout\|slow"
```

**Solutions:**
- [ ] Increase timeout: Set `REQUEST_TIMEOUT=60` in `.env`
- [ ] Check database performance: Slow queries in PostgreSQL logs
- [ ] Profile API endpoint: Add timing logs
- [ ] Check reasoning mode complexity: Reduce simultaneously running modes
- [ ] Check system resources: `docker stats`
- [ ] Optimize database queries: Add indexes
- [ ] Scale up: Increase `REPLICAS` and use load balancer

#### Problem: 405 Method Not Allowed
```bash
# Check if endpoint exists
curl -X GET http://localhost:8000/api/reason
curl -X POST http://localhost:8000/api/reason
```

**Solutions:**
- [ ] Verify HTTP method (GET vs POST vs PUT vs DELETE)
- [ ] Check API endpoint defined correctly in `backend_main.py`
- [ ] Verify CORS configuration for method
- [ ] Restart app after code changes: `docker compose restart ochuko-app`

#### Problem: 401 Unauthorized
```bash
curl -H "Authorization: Bearer ${TOKEN}" http://localhost:8000/api/protected-endpoint
```

**Solutions:**
- [ ] Include Bearer token in header
- [ ] Verify JWT secret matches in `.env`
- [ ] Check token expiration: `jwt.decode(token, options={"verify_signature": False})`
- [ ] Generate new token if expired
- [ ] Verify authentication middleware configured

---

### 4. Performance Issues

#### Problem: High CPU usage
```bash
docker stats --no-stream | grep ochuko-app
top -p $(docker inspect -f '{{.State.Pid}}' $(docker ps -q -f 'label=com.docker.compose.service=ochuko-app'))
```

**Solutions:**
- [ ] Check reasoning mode complexity: Disable complex modes
- [ ] Profile hot paths: Add Python profiling
- [ ] Reduce concurrent tasks: Lower `REASONING_CONCURRENT_MODES`
- [ ] Cache results: Enable `INTELLIGENT_CACHING=true`
- [ ] Scale horizontally: Increase `REPLICAS` with load balancer
- [ ] Check for memory leaks: Monitor growth over time
- [ ] Profile with: `python -m cProfile -o prof.stats app.py`

#### Problem: High memory usage
```bash
docker stats --no-stream | grep ochuko-app
docker compose exec ochuko-app python -c "import tracemalloc; tracemalloc.start()"
```

**Solutions:**
- [ ] Reduce in-memory caching: Lower `CACHE_MEMORY_LIMIT`
- [ ] Enable database offloading: Set `CACHE_BACKEND=redis`
- [ ] Reduce batch size: Lower `BATCH_SIZE`
- [ ] Enable garbage collection: `gc.collect()` more frequently
- [ ] Check for memory leaks in reasoning engines
- [ ] Reduce `REPLICAS` if memory constrained
- [ ] Use memory profiler: `pip install memory-profiler`

#### Problem: Slow database queries
```bash
docker compose exec postgres_db psql -U ${DB_USER} -d ${DB_NAME} -c "\dt"
# Check query times
docker compose logs postgres_db | grep "duration:"
```

**Solutions:**
- [ ] Add indexes: `CREATE INDEX idx_name ON table(column);`
- [ ] Analyze query: `EXPLAIN ANALYZE SELECT ...`
- [ ] Reduce result set: Use LIMIT
- [ ] Enable query caching: Set `QUERY_CACHE_ENABLED=true`
- [ ] Denormalize if needed
- [ ] Archive old data
- [ ] Check connection pooling: `PG_POOL_SIZE=20`

#### Problem: Cache misses / low hit rate
```bash
# Check Redis stats
docker compose exec redis redis-cli info stats | grep hits
```

**Solutions:**
- [ ] Increase cache size: `CACHE_MAX_SIZE=10000`
- [ ] Extend TTL: `CACHE_TTL=3600`
- [ ] Enable persistent cache: `CACHE_PERSISTENT=true`
- [ ] Warm cache on startup: Pre-load frequent queries
- [ ] Check cache key consistency
- [ ] Monitor hit rate: `docker compose exec redis redis-cli info stats`

---

### 5. Logging & Monitoring Issues

#### Problem: Logs not appearing
```bash
docker compose logs ochuko-app | head -20
docker compose logs --timestamps --tail=100
```

**Solutions:**
- [ ] Verify logging enabled: `LOGGING_ENABLED=true`
- [ ] Check log level: `LOG_LEVEL=info` (should be info or debug)
- [ ] Check container stdout: Logs must go to stdout/stderr
- [ ] Verify log file permissions if writing to disk
- [ ] Restart logging service: `docker compose restart ochuko-app`
- [ ] Check Docker daemon logs: `journalctl -u docker`

#### Problem: Metrics not being collected
```bash
curl http://localhost:9090/metrics
docker compose logs prometheus | tail -20
```

**Solutions:**
- [ ] Verify Prometheus enabled: `PROMETHEUS_ENABLED=true`
- [ ] Check metrics endpoint: `GET /metrics`
- [ ] Verify Prometheus scrape config
- [ ] Check Prometheus container running: `docker compose ps prometheus`
- [ ] Verify port mapping correct
- [ ] Check metric naming conventions

#### Problem: Health check failing
```bash
curl -v http://localhost:8000/health
docker compose ps # Check "healthy" status
```

**Solutions:**
- [ ] Check health endpoint implementation
- [ ] Verify dependencies checked (DB, cache, etc)
- [ ] Increase health check timeout: `HEALTH_CHECK_TIMEOUT=10`
- [ ] Check startup time: May need longer delay before first check
- [ ] Review health check logs: `docker compose logs ochuko-app | grep health`

---

### 6. Backup & Recovery Issues

#### Problem: Backup failed
```bash
docker compose logs postgres_db | grep -i backup
ls -la backups/
```

**Solutions:**
- [ ] Check backup directory exists: `mkdir -p backups`
- [ ] Verify permissions: `chmod 755 backups`
- [ ] Check disk space: `df -h backups/`
- [ ] Test PostgreSQL dump: `pg_dump -U ${DB_USER} -d ${DB_NAME} > test.sql`
- [ ] Verify backup schedule: `crontab -l`
- [ ] Check backup script: `cat backup.sh`

#### Problem: Cannot restore backup
```bash
# List backups
ls -lh backups/*.sql.gz

# Test restore (to test database)
gunzip -c backup.sql.gz | psql -U ${DB_USER} -d ${DB_NAME}_test
```

**Solutions:**
- [ ] Ensure target database exists
- [ ] Verify backup file not corrupted: `gzip -t backup.sql.gz`
- [ ] Check PostgreSQL version compatibility
- [ ] Drop and recreate database first
- [ ] Use proper restore command: `pg_restore -U ${DB_USER} -d ${DB_NAME} backup.dump`
- [ ] Check permissions on backup file

#### Problem: Backups consuming too much space
```bash
du -sh backups/
du -sh backups/* | sort -hr
```

**Solutions:**
- [ ] Reduce backup retention: `BACKUP_RETENTION_DAYS=14`
- [ ] Enable compression: Already in standard setup
- [ ] Archive old backups: Move to separate storage
- [ ] Implement incremental backups
- [ ] Clean up old files: `find backups -mtime +30 -delete`

---

### 7. Security Issues

#### Problem: SSL certificate expired
```bash
openssl x509 -in cert.pem -noout -dates
```

**Solutions:**
- [ ] Renew certificate: `certbot renew`
- [ ] For LetsEncrypt: Should auto-renew
- [ ] Manual renewal: `certbot certonly --standalone`
- [ ] Update `.env`: Set correct cert paths
- [ ] Restart Nginx: `docker compose restart nginx`

#### Problem: Cannot authenticate / JWT failing
```bash
curl -H "Authorization: Bearer invalid_token" http://localhost:8000/api/protected
```

**Solutions:**
- [ ] Generate new token from auth endpoint
- [ ] Check JWT secret in `.env`: `grep JWT_SECRET .env`
- [ ] Verify token format: Should be "Bearer <token>"
- [ ] Check token expiration: Set `JWT_EXPIRY_HOURS=24`
- [ ] Verify request headers: `curl -v -H "Authorization: Bearer ..."`

#### Problem: Rate limiting too aggressive
```bash
# Check current rate limiting
curl -H "X-Forwarded-For: 127.0.0.1" http://localhost:8000/api/endpoint
# Response: 429 Too Many Requests
```

**Solutions:**
- [ ] Increase limits: `RATE_LIMIT_REQUESTS=1000`
- [ ] Increase window: `RATE_LIMIT_WINDOW_SECONDS=60`
- [ ] Whitelist IPs: Add to `RATE_LIMIT_WHITELIST`
- [ ] Disable for testing: `RATE_LIMIT_ENABLED=false`
- [ ] Check headers: Look for rate-limit info in response

---

### 8. Deployment Issues

#### Problem: Docker Compose build fails
```bash
docker compose build --no-cache
```

**Solutions:**
- [ ] Clean build cache: `docker builder prune`
- [ ] Check Dockerfile syntax
- [ ] Verify base image available
- [ ] Check network (downloading dependencies)
- [ ] Check disk space: `df -h`
- [ ] Review build logs completely
- [ ] Try manual build: `docker build -f Dockerfile -t ochuko-app .`

#### Problem: Containers can't communicate
```bash
docker compose exec ochuko-app ping postgres_db
docker network ls
docker network inspect $(docker network ls -q | head -1)
```

**Solutions:**
- [ ] Verify network created: `docker network ls`
- [ ] Check service names in `docker-compose.yml`
- [ ] Restart Docker daemon: `systemctl restart docker`
- [ ] Recreate network: `docker compose down && docker compose up -d`
- [ ] Check DNS: `docker compose exec ochuko-app cat /etc/resolv.conf`
- [ ] Verify container links configured

#### Problem: Port forwarding not working
```bash
docker compose port ochuko-app 8000
netstat -tlnp | grep 8000
```

**Solutions:**
- [ ] Check ports in `docker-compose.yml` format
- [ ] Verify host can reach container: `curl -v http://localhost:8000`
- [ ] Check Docker daemon network: `docker network inspect bridge`
- [ ] Verify port not in use: `lsof -i :8000`
- [ ] Check iptables: `iptables -L -n | grep 8000`

---

### 9. Scalability Issues

#### Problem: Load not balancing across replicas
```bash
docker compose ps | grep ochuko-app
curl http://localhost:8000/health | grep hostname
```

**Solutions:**
- [ ] Increase replicas: Set `REPLICAS=3` in `.env` and redeploy
- [ ] Verify load balancer: `docker compose ps nginx`
- [ ] Check load balancer config: `docker compose exec nginx cat /etc/nginx/nginx.conf | grep upstream`
- [ ] Test round-robin: Make multiple requests, check response hostnames
- [ ] Monitor connections: `netstat -an | grep ESTABLISHED`

#### Problem: Not enough resources for scaling
```bash
docker stats --no-stream
docker system df
```

**Solutions:**
- [ ] Check available memory: `free -h`
- [ ] Check disk space: `df -h`
- [ ] Reduce replica count
- [ ] Optimize container memory limits
- [ ] Enable memory swapping (last resort)
- [ ] Consider horizontal scaling: Different machines

---

### 10. Integration Issues

#### Problem: External API calls failing
```bash
# Test API connectivity
curl https://api.openai.com/v1/models -H "Authorization: Bearer ${OPENAI_API_KEY}"
```

**Solutions:**
- [ ] Verify API keys in `.env`
- [ ] Check API rate limits not exceeded
- [ ] Verify firewall allows outbound HTTPS
- [ ] Test proxy settings if behind corporate proxy
- [ ] Check API endpoint URLs are correct
- [ ] Add retry logic with exponential backoff
- [ ] Monitor API status pages
- [ ] Implement circuit breaker pattern

#### Problem: Webhook delivery failing
```bash
# Check webhook logs
docker compose logs ochuko-app | grep -i webhook
# Test webhook endpoint
curl -X POST http://localhost:8000/webhooks/test -d '{"test": true}'
```

**Solutions:**
- [ ] Verify webhook URL accessible externally
- [ ] Check firewall allows inbound on webhook port
- [ ] Verify authentication tokens
- [ ] Check webhook signature validation
- [ ] Add retry logic for failed deliveries
- [ ] Monitor webhook delivery logs
- [ ] Test with webhook.site for debugging

---

## Advanced Diagnostics

### Database Performance Profiling
```bash
# PostgreSQL
docker compose exec postgres_db psql -U ${DB_USER} -d ${DB_NAME}
> SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

# MongoDB
docker compose exec mongo_db mongosh
> db.system.profile.find().sort({millis: -1}).limit(5)
```

### Memory Leak Detection
```bash
# Python memory profiler
docker compose exec ochuko-app pip install memory-profiler
docker compose exec ochuko-app python -m memory_profiler app.py

# Check for growing memory
watch 'docker stats --no-stream | grep ochuko-app'
```

### Network Debugging
```bash
# Check network traffic
docker compose exec ochuko-app tcpdump -i eth0 -A -s 0 'tcp port 5432'

# Test connectivity
docker compose exec ochuko-app nslookup postgres_db
docker compose exec ochuko-app netstat -an | grep ESTABLISHED
```

### Log Analysis
```bash
# Search for errors
docker compose logs --all --follow | grep -i error

# Performance patterns
docker compose logs ochuko-app | grep -E "duration|latency"

# Recent activity
docker compose logs --timestamps --tail=200 | head -50
```

---

## Recovery Procedures

### Emergency Restart
```bash
# Full system restart
docker compose down
docker compose up -d
sleep 30
python deployment_verification.py
```

### Database Recovery
```bash
# Reset databases (WARNING: DATA LOSS)
docker compose down -v
docker compose up -d postgres_db mongo_db
sleep 30
# Re-run migrations
docker compose exec postgres_db psql -U ${DB_USER} -f migrations.sql
```

### Clear Cache
```bash
docker compose exec redis redis-cli FLUSHALL
```

### Reset to Known Good State
```bash
# From backup
gunzip -c backups/latest.sql.gz | docker compose exec -T postgres_db psql -U ${DB_USER} -d ${DB_NAME}

# Restart services
docker compose restart
```

---

## When All Else Fails

### Collect Debug Information
```bash
#!/bin/bash
echo "=== System Info ===" > debug.txt
uname -a >> debug.txt
docker --version >> debug.txt
docker compose --version >> debug.txt

echo "=== Docker Status ===" >> debug.txt
docker compose ps >> debug.txt

echo "=== Logs ===" >> debug.txt
docker compose logs --tail=200 >> debug.txt

echo "=== Environment ===" >> debug.txt
docker compose exec ochuko-app env | grep -i db >> debug.txt

echo "=== Network ===" >> debug.txt
docker network inspect $(docker compose ps -q | head -1 | xargs docker inspect -f '{{.HostConfig.NetworkMode}}') >> debug.txt

echo "Debug info saved to debug.txt"
```

### Contact Support
**Include:**
- [ ] Output from: `python deployment_verification.py`
- [ ] Last 100 lines of logs: `docker compose logs --tail=100`
- [ ] `.env` file (sanitized - remove secrets)
- [ ] `docker compose config` output
- [ ] System info: `uname -a`, `free -h`, `df -h`
- [ ] What you were doing when issue occurred
- [ ] Steps already taken to troubleshoot
- [ ] Time issue started
- [ ] Any error messages

---

**Last Updated**: February 2026  
**Version**: 1.0  
**Status**: Production-Ready
