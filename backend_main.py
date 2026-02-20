"""
JARVIS AI Assistant - Main Backend Server
Multi-modal AI personal assistant inspired by Iron Man's JARVIS
"""

from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

from src.ai.orchestrator import AIOrchestrator
from src.modules.face_recognition import FaceRecognitionEngine
from src.ai.speech_engine import SpeechEngine
from src.modules.context_manager import ContextManager

load_dotenv()

app = FastAPI(
    title="JARVIS AI Assistant",
    description="Multi-modal AI personal assistant platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ai_orchestrator = AIOrchestrator()
face_engine = FaceRecognitionEngine()
speech_engine = SpeechEngine()
context_manager = ContextManager()


@app.on_event("startup")
async def startup_event():
    """Initialize all AI engines on startup"""
    logger.info("🤖 JARVIS AI Assistant starting up...")
    await ai_orchestrator.initialize()
    await face_engine.load_models()
    logger.info("✅ All systems online and ready")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "operational",
        "systems": {
            "ai_orchestrator": ai_orchestrator.is_ready,
            "face_recognition": face_engine.is_ready,
            "speech": speech_engine.is_ready,
        }
    }


@app.post("/api/process-text")
async def process_text(request: dict):
    """
    Process text input through JARVIS
    
    Example request:
    {
        "text": "What's the weather like?",
        "context": "general_query"
    }
    """
    try:
        text_input = request.get("text", "")
        context = request.get("context", "general")
        
        # Update conversation context
        await context_manager.add_message("user", text_input)
        
        # Get AI response
        response = await ai_orchestrator.process_text(
            text_input,
            context=context,
            memory=context_manager.get_context()
        )
        
        await context_manager.add_message("assistant", response["text"])
        
        return {
            "status": "success",
            "response": response["text"],
            "action": response.get("action"),
            "confidence": response.get("confidence", 0.95)
        }
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/recognize-face")
async def recognize_face(file: UploadFile = File(...)):
    """
    Upload image for face recognition
    Returns identified user and emotional context
    """
    try:
        contents = await file.read()
        result = await face_engine.recognize(contents)
        
        return {
            "status": "success",
            "identified_user": result.get("user_id"),
            "confidence": result.get("confidence"),
            "emotion": result.get("emotion"),
            "action_recommended": result.get("action")
        }
    except Exception as e:
        logger.error(f"Face recognition error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/process-voice")
async def process_voice(file: UploadFile = File(...)):
    """
    Process voice input (speech-to-text + understanding)
    """
    try:
        contents = await file.read()
        
        # Convert speech to text
        text = await speech_engine.speech_to_text(contents)
        
        # Process through AI orchestrator
        response = await ai_orchestrator.process_text(
            text,
            context="voice_command",
            memory=context_manager.get_context()
        )
        
        # Convert response back to speech
        audio_response = await speech_engine.text_to_speech(response["text"])
        
        await context_manager.add_message("user", text)
        await context_manager.add_message("assistant", response["text"])
        
        return {
            "status": "success",
            "recognized_text": text,
            "response_text": response["text"],
            "response_audio": audio_response,
            "action": response.get("action")
        }
    except Exception as e:
        logger.error(f"Voice processing error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat
    Maintains conversation state and context
    """
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            content = data.get("content")
            
            if message_type == "text":
                response = await ai_orchestrator.process_text(
                    content,
                    context="realtime",
                    memory=context_manager.get_context()
                )
                await context_manager.add_message("user", content)
                await context_manager.add_message("assistant", response["text"])
                
                await websocket.send_json({
                    "type": "response",
                    "text": response["text"],
                    "action": response.get("action"),
                    "thinking_process": response.get("thinking", "")
                })
            
            elif message_type == "command":
                execution = await ai_orchestrator.execute_command(
                    content,
                    context=context_manager.get_context()
                )
                await websocket.send_json({
                    "type": "command_result",
                    "status": execution["status"],
                    "result": execution.get("result")
                })
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()


@app.get("/api/memory")
async def get_memory():
    """Retrieve JARVIS memory and context"""
    return {
        "conversation_history": context_manager.get_context(),
        "learned_patterns": context_manager.get_learned_patterns(),
        "user_preferences": context_manager.get_preferences()
    }


@app.post("/api/learn")
async def learn(request: dict):
    """Allow JARVIS to learn new patterns and preferences"""
    try:
        pattern_type = request.get("type")
        pattern_data = request.get("data")
        
        await context_manager.learn_pattern(pattern_type, pattern_data)
        
        return {
            "status": "success",
            "message": f"Learned new {pattern_type} pattern"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/capabilities")
async def get_capabilities():
    """Return JARVIS capabilities and features"""
    return {
        "capabilities": {
            "voice_interaction": True,
            "face_recognition": True,
            "natural_language": True,
            "task_execution": True,
            "learning": True,
            "emotion_recognition": True,
            "real_time_response": True,
            "multi_language": True,
            "vision": True
        },
        "version": "1.0.0",
        "status": "operational"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV") != "production"
    )
