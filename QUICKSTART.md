# 🚀 Quick Start Guide - Ochuko AI

Get Ochuko AI (inspired by JARVIS) up and running in **5 minutes** with Docker.

## One-Command Setup

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/Ochuko AI.git
cd Ochuko AI

# 2. Copy environment file and add your API keys
cp .env.example .env
# Edit .env file: add your OpenAI API key
nano .env

# 3. Start everything
docker-compose up -d

# 4. Done! Open your browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

---

## What's Running?

| Service | URL | Purpose |
|---------|-----|---------|
| **Ochuko AI Frontend** | http://localhost:3000 | Chat interface & UI |
| **API Server** | http://localhost:8000 | FastAPI backend |
| **API Docs** | http://localhost:8000/docs | Interactive documentation |
| **Database** | postgres:5432 | PostgreSQL data store |
| **Cache** | redis:6379 | Redis cache/sessions |
| **MongoDB** | 27017 | Document database |

---

## First Time Using Ochuko AI?

### Try These Commands

```bash
# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Restart everything
docker-compose restart

# View container status
docker-compose ps
```

### Access the API

```bash
# Health check
curl http://localhost:8000/health

# Chat with Ochuko AI (via REST)
curl -X POST http://localhost:8000/api/process-text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello Ochuko AI!", "context": "greeting"}'

# View API documentation
open http://localhost:8000/docs
```

---

## Troubleshooting

### Services won't start?
```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

### Port already in use?
Edit `docker-compose.yml` and change port mappings:
```yaml
ports:
  - "8001:8000"  # Change 8001 to your preferred port
```

### Need to configure API keys?
1. Edit `.env` file
2. Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
3. Restart: `docker-compose restart backend`

---

## Next Steps

- 📖 Read the [full README](README.md)
- 🔧 [Configure settings](./config.py)
- 📚 Explore [API documentation](http://localhost:8000/docs)
- 💻 [Run locally without Docker](README.md#local-development-setup)
- 🧪 [Run tests](README.md#testing)

---

## Local Development (Without Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## Key Features to Try

### 1. Text Chat
- Click message input at bottom
- Type any question or command
- JARVIS responds instantly

### 2. Voice Input
- Click 🎤 Voice button
- Speak your request
- JARVIS responds with voice

### 3. Face Recognition
- Enable camera (if browser asks)
- JARVIS recognizes and greets you
- Detects your emotional state

### 4. Real-time Thinking
- See JARVIS's reasoning process
- Expandable "💭 Show thinking" sections
- Understand decision-making

### 5. Task Execution
- Request actions: "Set a reminder"
- View action results
- See execution status

---

## Project Structure

```
jarvis-ai-assistant/
├── backend/          # FastAPI Python server
├── frontend/         # React TypeScript UI
├── docker-compose.yml
├── README.md
└── .env.example
```

---

## Support

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/jarvis-ai-assistant/issues)
- 💬 [Discussions](https://github.com/yourusername/jarvis-ai-assistant/discussions)
- ⭐ Star on GitHub if you like it!

---

**Ready to explore JARVIS? Let's go!** 🚀
