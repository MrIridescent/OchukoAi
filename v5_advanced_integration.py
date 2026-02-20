"""
v5.0 Advanced Integration Layer
Integrates all new advanced systems into the unified pipeline
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from advanced_cognitive_intelligence import UnifiedAdvancedCognition
from dual_brain_system import DualBrainThinkingSystem
from whole_picture_intelligence import WholePictureIntelligence
from voice_emotion_detection import VoiceEmotionDetectionSystem
from facial_emotion_recognition import FacialEmotionRecognitionSystem
from multiparty_conversation_system import MultiPartyConversationSystem
from realtime_visualization import RealTimeVisualizationEngine
from custom_cultural_profiles import CulturalProfileManager
from human_centric_communication_pipeline import HumanCentricCommunicationAPI

logger = logging.getLogger(__name__)


@dataclass
class AdvancedUserSession:
    """Complete user session with all advanced systems"""
    user_id: str
    session_id: str
    created_at: datetime = field(default_factory=datetime.now)
    
    emotional_state: Dict[str, Any] = field(default_factory=dict)
    cognitive_state: Dict[str, Any] = field(default_factory=dict)
    voice_state: Dict[str, Any] = field(default_factory=dict)
    facial_state: Dict[str, Any] = field(default_factory=dict)
    thinking_map: Dict[str, Any] = field(default_factory=dict)
    cultural_profile: Optional[str] = None
    group_context: Optional[str] = None
    
    interaction_count: int = 0
    last_update: datetime = field(default_factory=datetime.now)
    detected_needs: List[str] = field(default_factory=list)
    insights_generated: List[str] = field(default_factory=list)


class UniversalAIv5AdvancedCore:
    """
    Core integration bringing together:
    - Advanced Cognitive Intelligence (20x)
    - Dual Brain System (left/right coordination)
    - Whole Picture Intelligence (macro/micro)
    - Voice Emotion Detection
    - Facial Emotion Recognition
    - Multi-party Conversation System
    - Real-time Visualization
    - Custom Cultural Profiles
    - Human-Centric Communication
    """
    
    def __init__(self):
        self.advanced_cognition = UnifiedAdvancedCognition()
        self.dual_brain = DualBrainThinkingSystem()
        self.whole_picture = WholePictureIntelligence()
        self.voice_detection = VoiceEmotionDetectionSystem()
        self.facial_recognition = FacialEmotionRecognitionSystem()
        self.multiparty_system = MultiPartyConversationSystem()
        self.visualization = RealTimeVisualizationEngine()
        self.cultural_profiles = CulturalProfileManager()
        self.human_centric_api = HumanCentricCommunicationAPI()
        
        self.active_sessions = {}
        self.user_profiles = {}
        
    async def initialize_user_session(
        self,
        user_id: str,
        session_id: str,
        cultural_profile_name: Optional[str] = None
    ) -> AdvancedUserSession:
        """Initialize comprehensive user session"""
        
        session = AdvancedUserSession(
            user_id=user_id,
            session_id=session_id,
            cultural_profile=cultural_profile_name
        )
        
        await self.advanced_cognition.create_integrated_cognitive_profile(user_id)
        self.human_centric_api.configure_user(user_id)
        
        self.active_sessions[session_id] = session
        
        logger.info(f"✅ Session initialized: {user_id} ({session_id})")
        
        return session
    
    async def process_complete_input(
        self,
        session_id: str,
        text_input: str,
        voice_data: Optional[Dict[str, float]] = None,
        facial_data: Optional[Dict[str, Any]] = None,
        conversation_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process input through ALL advanced systems
        Integrates text, voice, facial, and context data
        """
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        voice_analysis = None
        if voice_data:
            voice_analysis = await self.voice_detection.detect_voice_emotion(
                session.user_id,
                voice_data
            )
            session.voice_state = {
                "emotion": voice_analysis.detected_emotion.value,
                "confidence": voice_analysis.emotion_confidence,
                "stress": voice_analysis.stress_level,
            }
        
        facial_analysis = None
        if facial_data:
            from facial_emotion_recognition import FacialFeatures
            features = FacialFeatures(**facial_data)
            facial_analysis = await self.facial_recognition.recognize_face_emotion(
                session.user_id,
                features
            )
            session.facial_state = {
                "emotion": facial_analysis.primary_emotion.value,
                "confidence": facial_analysis.emotion_confidence,
                "authenticity": facial_analysis.emotional_authenticity,
            }
        
        text_response = await self.human_centric_api.send_message(
            user_id=session.user_id,
            message=text_input,
            session_id=session_id
        )
        session.emotional_state = {
            "detected": text_response.get("detected_emotion"),
            "intensity": text_response.get("emotional_intensity"),
            "style": text_response.get("communication_style"),
        }
        
        dual_brain_thinking = await self.dual_brain.think_about(
            session.user_id,
            text_input
        )
        
        whole_picture = await self.whole_picture.understand_deeply(text_input)
        
        cognitive_insights = await self.advanced_cognition.generate_cognitive_insights(
            session.user_id,
            [{"text": text_input}]
        )
        
        visualization = await self.visualization.render_complete_state(
            emotion=text_response.get("detected_emotion", "neutral"),
            emotion_intensity=text_response.get("emotional_intensity", 0.5),
            secondary_emotions={},
            thinking_topic=text_input,
            related_concepts={},
            cognitive_state={
                "processing_speed": 0.7,
                "clarity": 0.8,
                "load": 0.5,
                "focus": 0.8
            }
        )
        
        if conversation_context and "group_id" in conversation_context:
            group_response = await self.multiparty_system.process_group_message(
                conversation_id=conversation_context["group_id"],
                participant_id=session.user_id,
                message=text_input,
                emotion=text_response.get("detected_emotion"),
                intent="contribute"
            )
        else:
            group_response = None
        
        session.interaction_count += 1
        session.last_update = datetime.now()
        
        complete_response = {
            "session_id": session_id,
            "user_id": session.user_id,
            "timestamp": datetime.now().isoformat(),
            
            "primary_response": text_response.get("message"),
            "emotional_analysis": session.emotional_state,
            
            "voice_analysis": {
                "emotion": voice_analysis.detected_emotion.value if voice_analysis else None,
                "stress_level": voice_analysis.stress_level if voice_analysis else None,
                "authenticity": voice_analysis.authenticity_score if voice_analysis else None,
            },
            
            "facial_analysis": {
                "emotion": facial_analysis.primary_emotion.value if facial_analysis else None,
                "authenticity": facial_analysis.emotional_authenticity if facial_analysis else None,
                "micro_expressions": facial_analysis.micro_expressions if facial_analysis else [],
            },
            
            "dual_brain_analysis": dual_brain_thinking,
            
            "whole_picture_understanding": whole_picture,
            
            "cognitive_insights": cognitive_insights,
            
            "visualization": visualization,
            
            "group_dynamics": group_response,
            
            "multimodal_integration": await self._integrate_modalities(
                text_response, voice_analysis, facial_analysis
            ),
        }
        
        return complete_response
    
    async def _integrate_modalities(self, text, voice, facial) -> Dict[str, Any]:
        """Integrate text, voice, and facial data"""
        
        integration = {
            "congruence_score": 0.0,
            "insights": [],
            "contradictions": [],
        }
        
        if text and voice:
            text_emotion = text.get("detected_emotion", "neutral")
            voice_emotion = voice.detected_emotion.value if voice else None
            
            if text_emotion == voice_emotion:
                integration["congruence_score"] += 0.33
                integration["insights"].append(f"Consistent emotion across text and voice: {text_emotion}")
            else:
                integration["contradictions"].append(
                    f"Text suggests {text_emotion} but voice suggests {voice_emotion}"
                )
        
        if text and facial:
            text_emotion = text.get("detected_emotion", "neutral")
            facial_emotion = facial.primary_emotion.value if facial else None
            
            if text_emotion == facial_emotion:
                integration["congruence_score"] += 0.33
            else:
                integration["contradictions"].append(
                    f"Text suggests {text_emotion} but face shows {facial_emotion}"
                )
        
        if voice and facial:
            voice_emotion = voice.detected_emotion.value if voice else None
            facial_emotion = facial.primary_emotion.value if facial else None
            
            if voice_emotion == facial_emotion:
                integration["congruence_score"] += 0.34
            else:
                integration["contradictions"].append(
                    f"Voice suggests {voice_emotion} but face shows {facial_emotion}"
                )
        
        return integration
    
    async def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get complete session summary"""
        
        if session_id not in self.active_sessions:
            return {}
        
        session = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "user_id": session.user_id,
            "duration": (datetime.now() - session.created_at).total_seconds(),
            "interactions": session.interaction_count,
            "emotional_state": session.emotional_state,
            "cognitive_state": session.cognitive_state,
            "voice_state": session.voice_state,
            "facial_state": session.facial_state,
            "cultural_profile": session.cultural_profile,
            "detected_needs": session.detected_needs,
            "insights": session.insights_generated,
        }
    
    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """End session and return summary"""
        
        summary = await self.get_session_summary(session_id)
        
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        return summary


class AdvancedCapabilityAPI:
    """Public API for advanced capabilities"""
    
    def __init__(self):
        self.core = UniversalAIv5AdvancedCore()
    
    async def start_session(
        self,
        user_id: str,
        session_id: str,
        cultural_profile: Optional[str] = None
    ) -> Dict[str, Any]:
        """Start new advanced session"""
        
        session = await self.core.initialize_user_session(user_id, session_id, cultural_profile)
        
        return {
            "status": "ready",
            "session_id": session_id,
            "user_id": user_id,
            "systems_active": [
                "Advanced Cognition",
                "Dual Brain",
                "Whole Picture Intelligence",
                "Voice Detection",
                "Facial Recognition",
                "Multiparty Conversation",
                "Real-time Visualization",
                "Cultural Profiles",
            ]
        }
    
    async def process_interaction(
        self,
        session_id: str,
        message: str,
        voice_data: Optional[Dict] = None,
        facial_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process complete multimodal interaction"""
        
        return await self.core.process_complete_input(
            session_id=session_id,
            text_input=message,
            voice_data=voice_data,
            facial_data=facial_data
        )
    
    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """End session and get summary"""
        
        return await self.core.end_session(session_id)
