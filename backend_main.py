"""
Ochuko AI - Main Backend Server
Advanced multi-modal AI assistant inspired by JARVIS from Iron Man
UNIFIED INTELLIGENCE SYSTEM - ALL COMPONENTS INTEGRATED
Author: David Akpoviroro Oke (MrIridescent)
"""

from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from pathlib import Path
from dotenv import load_dotenv
import os
import asyncio
import json

from unified_system_orchestrator import UnifiedSystemOrchestrator

load_dotenv()

app = FastAPI(
    title="Ochuko AI",
    description="Production-grade multi-modal AI with unified superintelligence - inspired by JARVIS",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the unified intelligence system
unified_orchestrator = UnifiedSystemOrchestrator()


@app.on_event("startup")
async def startup_event():
    """Initialize unified intelligence system on startup"""
    logger.info("")
    logger.info("🚀" * 40)
    logger.info("")
    logger.info("STARTING Ochuko AI - UNIFIED SUPERINTELLIGENCE")
    logger.info("")
    logger.info("🚀" * 40)
    
    try:
        await unified_orchestrator.initialize()
        logger.info("")
        logger.info("✅ UNIFIED INTELLIGENCE ONLINE - READY FOR OPERATION")
        logger.info("")
    except Exception as e:
        logger.critical(f"❌ STARTUP FAILED: {e}")
        raise


@app.get("/health")
async def health_check():
    """Comprehensive system health check"""
    return await unified_orchestrator.health_check()


@app.post("/api/process-text")
async def process_text(request: dict):
    """
    Process text input through unified superintelligence
    Routes through all analytical subsystems for comprehensive understanding
    
    Example request:
    {
        "user_id": "user123",
        "query": "I'm struggling with my career transition",
        "observations": [],
        "credentials": {"token": "auth_token"}
    }
    """
    try:
        user_id = request.get("user_id", "anonymous")
        query = request.get("query", request.get("text", ""))
        
        # Route through unified orchestrator
        result = await unified_orchestrator.process_user_interaction(
            user_id=user_id,
            input_data={
                "query": query,
                "context": request.get("context", "general"),
                "observations": request.get("observations", []),
                "conversation_history": request.get("conversation_history", []),
                "credentials": request.get("credentials", {}),
                "ip": request.get("ip", "")
            }
        )
        
        return result
    
    except Exception as e:
        logger.error(f"❌ Error processing interaction: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )


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
            "vision": True,
            "precognitive_intelligence": True,
            "empathy_engine": True,
            "universal_task_assistant": True,
            "multi_channel_messaging": True,
            "micro_expression_detection": True,
            "body_language_analysis": True,
            "physiological_monitoring": True
        },
        "version": "2.0.0",
        "status": "operational",
        "advanced_features": "Pre-cognitive, Empathy, Universal Life Tasks, Multi-channel Messaging"
    }


@app.post("/api/analyze-perception")
async def analyze_perception(request: dict):
    """
    Advanced perception analysis: micro-expressions, body language, physiology.
    Get true emotional state beyond what the user says.
    """
    try:
        user_id = request.get("user_id", "anonymous")
        facial_data = request.get("facial_data")
        voice_data = request.get("voice_data")
        body_data = request.get("body_data")
        
        perception = await ai_orchestrator.perception_engine.analyze_user(
            user_id=user_id,
            facial_data=facial_data,
            voice_data=voice_data,
            body_data=body_data
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "perception_analysis": perception,
            "micro_expressions": perception.get("micro_expressions", []),
            "body_language": perception.get("body_language", {}),
            "physiological_state": perception.get("physiological", {}),
            "true_emotional_state": perception.get("true_emotion", "unknown")
        }
    except Exception as e:
        logger.error(f"Perception analysis error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/predict-needs")
async def predict_needs(request: dict):
    """
    Pre-cognitive prediction: anticipate user needs before they ask.
    """
    try:
        user_id = request.get("user_id", "anonymous")
        current_state = request.get("current_state", {})
        
        patterns = ai_orchestrator.precognitive_engine.identified_patterns.get(user_id, [])
        
        predictions = await ai_orchestrator.precognitive_engine.predict_immediate_needs(
            user_id=user_id,
            current_state=current_state,
            patterns=patterns
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "predictions": [
                {
                    "need": p.subject,
                    "probability": f"{p.probability * 100:.0f}%",
                    "timeframe": p.timeframe,
                    "suggested_actions": p.suggested_actions
                }
                for p in predictions
            ],
            "count": len(predictions)
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/empathetic-response")
async def generate_empathetic_response(request: dict):
    """
    Generate genuinely empathetic response based on true user understanding.
    """
    try:
        user_id = request.get("user_id", "anonymous")
        user_message = request.get("message", "")
        perception_data = request.get("perception_data", {})
        
        profile = ai_orchestrator.empathy_engine.user_profiles.get(user_id)
        
        if not profile:
            profile = await ai_orchestrator.empathy_engine.understand_user(
                user_id=user_id,
                perception_data=perception_data,
                conversation_history=context_manager.get_context()
            )
        
        empathetic_response = await ai_orchestrator.empathy_engine.generate_empathetic_response(
            user_id=user_id,
            user_message=user_message,
            perception_data=perception_data,
            profile=profile
        )
        
        return {
            "status": "success",
            "response": empathetic_response["text"],
            "tone": empathetic_response.get("tone"),
            "empathy_level": f"{empathetic_response.get('empathy_level', 0.8) * 100:.0f}%",
            "addresses_true_need": empathetic_response.get("addresses_true_need")
        }
    except Exception as e:
        logger.error(f"Empathetic response error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/help-with-task")
async def help_with_task(request: dict):
    """
    Get comprehensive help with any life task across any domain.
    Returns complete solution: steps, timeline, resources, obstacles, contingencies.
    """
    try:
        user_id = request.get("user_id", "anonymous")
        task_description = request.get("task_description", "")
        context = request.get("context", {})
        
        solution = await ai_orchestrator.task_assistant.help_with_task(
            user_id=user_id,
            task_description=task_description,
            context=context
        )
        
        return {
            "status": "success",
            "task_summary": solution["task_summary"],
            "domain": solution["domain"],
            "priority": solution["priority"],
            "immediate_steps": solution["immediate_next_steps"],
            "full_plan": solution["full_plan"],
            "timeline": solution["timeline"],
            "success_probability": solution["success_probability"],
            "estimated_effort": solution["estimated_effort"],
            "resources": solution["resources_needed"],
            "obstacles": solution["obstacles_to_watch"],
            "contingencies": solution["contingency_plans"]
        }
    except Exception as e:
        logger.error(f"Task assistance error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/unified-messages")
async def get_unified_messages(user_id: str = "anonymous"):
    """
    Get unified view of all messages across all channels.
    Email, Slack, Discord, WhatsApp, etc. in one place.
    """
    try:
        messages = await ai_orchestrator.messaging_engine.get_unified_inbox(user_id)
        
        return {
            "status": "success",
            "user_id": user_id,
            "total_messages": len(messages) if messages else 0,
            "messages": messages if messages else [],
            "channels_connected": [
                "email", "slack", "discord", "whatsapp", 
                "telegram", "teams", "signal", "messenger"
            ]
        }
    except Exception as e:
        logger.error(f"Unified messages error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV") != "production"
    )
