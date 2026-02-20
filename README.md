# 🤖 JARVIS - Multi-Modal AI Personal Assistant

An advanced, multi-modal AI assistant platform inspired by Iron Man's JARVIS. A full-stack project that demonstrates modern AI integration with voice, vision, natural language processing, and real-time communication.

**Status**: ⚡ MVP Phase - Core infrastructure and proof of concept

---

## 🌟 Features

### AI Capabilities
- **🗣️ Voice Interaction** - Natural speech-to-text and text-to-speech
- **👁️ Vision & Face Recognition** - Identify users and detect emotions
- **🧠 Advanced Reasoning** - Chain-of-thought thinking process (explainable AI)
- **💬 Natural Language Processing** - Context-aware conversations
- **🎯 Task Execution** - Execute commands and automate workflows
- **📚 Memory & Learning** - Remembers preferences, patterns, and context
- **😊 Emotional Intelligence** - Recognizes and responds to emotional cues
- **⚡ Real-time Communication** - WebSocket-based live interaction

### Technical Features
- **Multi-LLM Support** - Integration with OpenAI GPT-4, Claude, and local models
- **Modular Architecture** - Pluggable AI engines and task executors
- **Async-First Design** - High-performance async/await throughout
- **Docker Containerization** - Full Docker Compose setup for easy deployment
- **REST + WebSocket APIs** - Multiple communication protocols
- **Database Persistence** - PostgreSQL + MongoDB + Redis
- **Production Ready** - Error handling, logging, health checks

---

## 🏗️ Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)             │
│              ChatInterface | VoiceInput | Dashboard          │
└──────────────────────────┬──────────────────────────────────┘
                           │ WebSocket / REST
┌──────────────────────────▼──────────────────────────────────┐
│                 FastAPI Backend (Python)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          AI Orchestrator (Central Brain)               │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │ LLM Engine   │  │Vision Engine │  │Speech Engine│ │ │
│  │  │(GPT/Claude) │  │(Face Recog)  │  │(STT/TTS)   │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │ │
│  │  ┌────────────────────────────────────────────────────┐ │
│  │  │  Task Executor | Context Manager | Memory Layer   │ │
│  │  └────────────────────────────────────────────────────┘ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ PostgreSQL   │  │  MongoDB     │  │     Redis       │  │
│  │ (Relational) │  │ (Documents)  │  │ (Cache/Queue)   │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
jarvis-ai-assistant/
├── backend/                          # Python FastAPI backend
│   ├── src/
│   │   ├── main.py                  # FastAPI application entry
│   │   ├── config.py                # Configuration management
│   │   ├── api/
│   │   │   ├── routes.py            # REST API endpoints
│   │   │   └── websocket.py         # WebSocket handlers
│   │   ├── ai/
│   │   │   ├── orchestrator.py      # Central AI brain
│   │   │   ├── llm_engine.py        # LLM (GPT/Claude) integration
│   │   │   ├── vision_engine.py     # Computer vision models
│   │   │   ├── speech_engine.py     # Speech processing
│   │   │   └── memory.py            # Persistent memory layer
│   │   ├── modules/
│   │   │   ├── face_recognition.py  # Face detection & emotion
│   │   │   ├── emotional_intelligence.py
│   │   │   ├── task_executor.py     # Execute commands
│   │   │   └── context_manager.py   # Conversation context
│   │   └── utils/
│   │       ├── logger.py
│   │       └── helpers.py
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile
│   └── .env.example
├── frontend/                         # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx     # Main chat UI
│   │   │   ├── VoiceInput.tsx
│   │   │   ├── FaceRecognition.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   └── TaskManager.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Settings.tsx
│   │   │   └── Analytics.tsx
│   │   ├── services/
│   │   │   ├── api.ts               # HTTP client
│   │   │   ├── websocket.ts         # WebSocket client
│   │   │   └── audio.ts             # Audio processing
│   │   ├── store/                   # State management
│   │   └── App.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml               # Multi-container orchestration
├── README.md                        # This file
└── .env.example
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.11+ (if running locally)
- Node.js 18+ (for frontend development)
- API Keys: OpenAI and/or Claude (for LLM functionality)

### Using Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant

# 2. Copy environment file and configure
cp .env.example .env
# Edit .env and add your API keys

# 3. Start all services with Docker Compose
docker-compose up -d

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs

# 5. View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Local Development Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install
# or
pnpm install

# Run development server
npm run dev
# Frontend will be available at http://localhost:5173
```

---

## 📡 API Documentation

### REST Endpoints

#### Health Check
```bash
GET /health
```

#### Text Processing
```bash
POST /api/process-text
Content-Type: application/json

{
  "text": "What's the weather like?",
  "context": "general_query"
}

Response:
{
  "status": "success",
  "response": "I'll check the weather for you...",
  "action": "get_weather",
  "confidence": 0.95
}
```

#### Face Recognition
```bash
POST /api/recognize-face
Content-Type: multipart/form-data

Body: binary image file

Response:
{
  "identified_user": "user123",
  "confidence": 0.98,
  "emotion": "happy",
  "action_recommended": "increase_engagement"
}
```

#### Voice Processing
```bash
POST /api/process-voice
Content-Type: multipart/form-data

Body: audio file (WAV/MP3)

Response:
{
  "recognized_text": "What time is it?",
  "response_text": "It's 3:45 PM",
  "response_audio": "base64_encoded_audio"
}
```

#### Memory & Learning
```bash
GET /api/memory
Response: { conversation_history, learned_patterns, user_preferences }

POST /api/learn
{
  "type": "user_preference",
  "data": { "preference_name": "value" }
}
```

### WebSocket Events

Real-time communication via `/ws/chat`:

```typescript
// Send text message
{ "type": "text", "content": "Hello JARVIS" }

// Execute command
{ "type": "command", "content": "play_music jazz" }

// Receive response
{
  "type": "response",
  "text": "Playing jazz music...",
  "action": "play_music",
  "thinking_process": "The user wants music..."
}
```

---

## 🧠 AI Components

### 1. LLM Engine
Integrates with multiple language models for natural conversation:
- **OpenAI GPT-4** - Latest and most capable
- **Claude** - Alternative LLM provider
- **Local Models** - Llama2, Mistral (for privacy)

```python
# Example usage
response = await llm_engine.generate_response(
    prompt="What is the capital of France?",
    context="general_knowledge",
    thinking=True  # Enable chain-of-thought
)
```

### 2. Vision Engine
Computer vision for image understanding and face recognition:
- Face detection and identification
- Emotion recognition
- Object detection
- OCR (text recognition)

```python
# Face recognition example
result = await face_engine.recognize(image_bytes)
# Returns: { identified_user, confidence, emotion }
```

### 3. Speech Engine
Voice interaction for hands-free operation:
- Speech-to-text (STT)
- Text-to-speech (TTS)
- Voice activity detection
- Audio quality enhancement

```python
# Voice processing
text = await speech_engine.speech_to_text(audio_bytes)
audio = await speech_engine.text_to_speech(text)
```

### 4. Task Executor
Executes commands and integrates with external systems:
- System commands
- API calls
- Scheduled tasks
- Custom plugin execution

```python
# Execute task
result = await task_executor.execute(
    action="send_email",
    params={"to": "user@example.com", "subject": "Hello"}
)
```

### 5. Context Manager
Maintains conversation context and learning:
- Conversation history
- User preferences
- Learned patterns
- Long-term memory

```python
# Add to memory
await context_manager.add_message("user", "I like coffee")
await context_manager.learn_pattern("preference", {"drink": "coffee"})
```

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=src  # With coverage
```

### Run Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Integration Tests
```bash
# Test full stack
docker-compose -f docker-compose.test.yml up
npm run test:integration
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
# Backend
ENV=development
HOST=0.0.0.0
PORT=8000

# LLM APIs
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=...

# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/jarvis
MONGO_URI=mongodb+srv://user:pass@mongodb.com/jarvis
REDIS_URL=redis://redis:6379

# Features
ENABLE_VOICE=true
ENABLE_FACE_RECOGNITION=true
ENABLE_LEARNING=true

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## 📊 Performance & Scaling

### Optimization Tips
- **Cache LLM responses** for common queries
- **Use Redis** for session management
- **Batch process** vision tasks
- **Stream audio** for real-time voice processing
- **Implement rate limiting** to prevent abuse

### Scaling Considerations
- **Horizontal scaling**: Use load balancer in front of backend
- **Database sharding**: Partition user data by region
- **Async queues**: Use Celery for long-running tasks
- **Edge deployment**: Deploy vision models closer to users

---

## 🔒 Security

### Security Measures
- ✅ API authentication (JWT tokens)
- ✅ HTTPS/WSS encryption
- ✅ Input validation & sanitization
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Environment variable secrets

### Privacy
- User data stored securely
- Optional local-only mode (no cloud)
- GDPR compliant data handling

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Additional LLM providers
- [ ] More task executors
- [ ] Enhanced emotion recognition
- [ ] Mobile app (React Native)
- [ ] Additional languages
- [ ] More creative examples

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📚 Resources

- **OpenAI API**: https://platform.openai.com/docs
- **Anthropic Claude**: https://docs.anthropic.com
- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **MediaPipe**: https://mediapipe.dev

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 🌟 Show Your Support

If this project helps you, please give it a ⭐ on GitHub!

---

## 📧 Contact & Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@example.com

---

**Built with 🚀 and ❤️ by developers who love AI**

