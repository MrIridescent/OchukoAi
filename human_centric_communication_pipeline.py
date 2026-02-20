"""
Human-Centric Communication Pipeline for Ochuko AI v5.0
Unified system that brings together:
- Human Communication Engine (natural dialogue)
- Multilingual System (translation + cultural context)
- Emotional Intelligence (emotion detection + empathy)
- Personalization (individual adaptation)
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from human_communication_engine import (
    HumanCommunicationEngine,
    HumanDialogueOrchestrator,
    CommunicationContext,
    DialogueResponse,
    CommunicationStyle,
    ToneDetection
)
from multilingual_system import (
    MultilingualTranslationSystem,
    CulturalAdaptationEngine,
    Language,
    CulturalContext,
    TranslationRequest
)
from emotional_intelligence_system import (
    EmotionalIntelligenceEngine,
    PersonalizationEngine,
    EmotionalState
)

logger = logging.getLogger(__name__)


@dataclass
class UserCommunicationSession:
    """Session tracking for continuous adaptation"""
    user_id: str
    session_id: str
    created_at: datetime = field(default_factory=datetime.now)
    detected_language: Language = Language.ENGLISH
    detected_emotional_state: EmotionalState = EmotionalState.CONTENTMENT
    communication_style: CommunicationStyle = CommunicationStyle.EMPATHETIC
    cultural_context: Optional[CulturalContext] = None
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    interaction_count: int = 0


@dataclass
class HumanCentricResponse:
    """Complete response with all human-centered dimensions"""
    content: str
    detected_language: Language
    translated_content: Optional[str] = None
    detected_emotion: EmotionalState = EmotionalState.CONTENTMENT
    emotional_intensity: float = 0.0
    communication_style: CommunicationStyle = CommunicationStyle.EMPATHETIC
    emotional_resonance: float = 0.0
    cultural_adaptations: Dict[str, str] = field(default_factory=dict)
    personalization_applied: Dict[str, Any] = field(default_factory=dict)
    follow_up_question: Optional[str] = None
    confidence_score: float = 0.9
    metadata: Dict[str, Any] = field(default_factory=dict)


class HumanCentricCommunicationPipeline:
    """
    Main pipeline that coordinates all human-centered communication systems
    Produces genuinely human-like interactions across languages and cultures
    """
    
    def __init__(self):
        self.communication_engine = HumanDialogueOrchestrator()
        self.emotional_intelligence = EmotionalIntelligenceEngine()
        self.personalization = PersonalizationEngine()
        self.translation_system = MultilingualTranslationSystem()
        self.cultural_adaptation = CulturalAdaptationEngine()
        
        self.active_sessions = {}
        self.user_sessions_history = {}
        
    async def process_user_input(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None,
        target_language: Optional[Language] = None
    ) -> HumanCentricResponse:
        """
        Process user input through complete human-centric pipeline
        
        Flow:
        1. Language Detection & Translation to internal language
        2. Emotional State Detection
        3. Intent Recognition
        4. Communication Style Adaptation
        5. Personalization
        6. Response Generation
        7. Emotional Resonance Optimization
        8. Cultural Adaptation
        9. Back-translation if needed
        10. Response Delivery
        """
        
        session = await self._get_or_create_session(user_id, session_id)
        
        detected_language, language_confidence = self._detect_language(message)
        session.detected_language = detected_language
        
        internal_message = message
        if detected_language != Language.ENGLISH:
            translation = await self._translate_to_internal(message, detected_language)
            internal_message = translation.translated_text
        
        emotional_state, emotional_intensity, secondary_emotions = (
            await self.emotional_intelligence.detect_emotional_state(internal_message)
        )
        session.detected_emotional_state = emotional_state
        
        dialogue_response = await self.communication_engine.process_user_message(
            user_id,
            session.session_id,
            internal_message,
            detected_language.value
        )
        
        emotionally_aware_response = (
            await self.emotional_intelligence.generate_emotionally_intelligent_response(
                emotional_state,
                emotional_intensity
            )
        )
        
        combined_response = await self._combine_responses(
            dialogue_response,
            emotionally_aware_response,
            emotional_state,
            emotional_intensity
        )
        
        personalized_response = await self.personalization.personalize_response(
            user_id,
            combined_response,
            {"emotion": emotional_state.value, "intensity": emotional_intensity}
        )
        
        final_response = personalized_response
        translated_response = None
        
        output_language = target_language or detected_language
        
        if output_language != Language.ENGLISH and output_language != detected_language:
            translation_request = TranslationRequest(
                text=final_response,
                source_language=Language.ENGLISH,
                target_language=output_language,
                preserve_tone=True
            )
            translated = await self.translation_system.translate(translation_request)
            translated_response = translated.translated_text
            
            if session.cultural_context:
                translated_response = await self.cultural_adaptation.adapt_response(
                    translated_response,
                    output_language,
                    session.cultural_context
                )
            
            final_response = translated_response
        
        human_centric_response = HumanCentricResponse(
            content=final_response,
            detected_language=detected_language,
            translated_content=translated_response,
            detected_emotion=emotional_state,
            emotional_intensity=emotional_intensity,
            communication_style=dialogue_response.style,
            emotional_resonance=dialogue_response.emotional_resonance,
            cultural_adaptations=dialogue_response.personalization_notes,
            personalization_applied={"formality": self.personalization.user_profiles.get(
                user_id, {}
            ).get("preferences", {}).get("formality_preference", "neutral")},
            follow_up_question=dialogue_response.follow_up_question,
            confidence_score=min(language_confidence, dialogue_response.emotional_resonance),
        )
        
        await self._track_interaction(session, message, human_centric_response)
        
        return human_centric_response
    
    def _detect_language(self, text: str) -> tuple:
        """Detect language of input"""
        detected, confidence = self.translation_system.detect_language(text)
        return detected, confidence
    
    async def _translate_to_internal(
        self,
        text: str,
        source_language: Language
    ) -> Any:
        """Translate to internal language (English)"""
        request = TranslationRequest(
            text=text,
            source_language=source_language,
            target_language=Language.ENGLISH,
            preserve_tone=True
        )
        return await self.translation_system.translate(request)
    
    async def _combine_responses(
        self,
        dialogue_response: DialogueResponse,
        emotionally_aware: str,
        emotion: EmotionalState,
        intensity: float
    ) -> str:
        """Intelligently combine dialogue and emotional responses"""
        
        if intensity > 0.7:
            combined = f"{emotionally_aware}\n\n{dialogue_response.text}"
        else:
            combined = dialogue_response.text
        
        if dialogue_response.acknowledgment:
            combined = f"{dialogue_response.acknowledgment} {combined}"
        
        return combined
    
    async def _get_or_create_session(
        self,
        user_id: str,
        session_id: Optional[str] = None
    ) -> UserCommunicationSession:
        """Get existing session or create new one"""
        
        if session_id and session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        new_session = UserCommunicationSession(
            user_id=user_id,
            session_id=session_id or f"{user_id}_{datetime.now().timestamp()}"
        )
        
        if user_id in self.user_sessions_history:
            last_session = self.user_sessions_history[user_id][-1]
            new_session.cultural_context = last_session.cultural_context
            new_session.detected_language = last_session.detected_language
        
        self.active_sessions[new_session.session_id] = new_session
        
        if user_id not in self.user_sessions_history:
            self.user_sessions_history[user_id] = []
        
        return new_session
    
    async def _track_interaction(
        self,
        session: UserCommunicationSession,
        user_message: str,
        response: HumanCentricResponse
    ):
        """Track interaction for learning"""
        
        session.conversation_history.append({
            "timestamp": datetime.now(),
            "user_message": user_message,
            "detected_emotion": response.detected_emotion.value,
            "emotional_intensity": response.emotional_intensity,
            "response": response.content,
        })
        
        session.interaction_count += 1
        
        if session.interaction_count >= 5:
            self.personalization.learn_from_interaction(
                session.user_id,
                {
                    "session_id": session.session_id,
                    "interaction_count": session.interaction_count,
                    "emotional_trajectory": [h["detected_emotion"] for h in session.conversation_history[-10:]],
                }
            )
            
            self.communication_engine.learn_user_communication(
                session.user_id,
                session.session_id
            )
    
    def set_user_context(
        self,
        user_id: str,
        language: Language,
        cultural_context: CulturalContext
    ):
        """Set user's language and cultural context"""
        
        for session in self.active_sessions.values():
            if session.user_id == user_id:
                session.detected_language = language
                session.cultural_context = cultural_context
    
    def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get analytics for a session"""
        
        if session_id not in self.active_sessions:
            return {}
        
        session = self.active_sessions[session_id]
        
        if not session.conversation_history:
            return {}
        
        emotional_states = [h["detected_emotion"] for h in session.conversation_history]
        emotional_intensities = [h["emotional_intensity"] for h in session.conversation_history]
        
        return {
            "session_id": session_id,
            "user_id": session.user_id,
            "duration": (datetime.now() - session.created_at).total_seconds(),
            "interaction_count": session.interaction_count,
            "detected_language": session.detected_language.value,
            "cultural_context": session.cultural_context.value if session.cultural_context else None,
            "emotional_trajectory": emotional_states,
            "average_emotional_intensity": sum(emotional_intensities) / len(emotional_intensities) if emotional_intensities else 0,
            "dominant_emotion": max(set(emotional_states), key=emotional_states.count) if emotional_states else None,
        }
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End session and archive"""
        
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            user_id = session.user_id
            
            if user_id not in self.user_sessions_history:
                self.user_sessions_history[user_id] = []
            
            self.user_sessions_history[user_id].append(session)
            
            analytics = self.get_session_analytics(session_id)
            
            del self.active_sessions[session_id]
            
            return analytics
        
        return {}


class HumanCentricCommunicationAPI:
    """
    Public API for human-centric communication
    Provides simple interface to the pipeline
    """
    
    def __init__(self):
        self.pipeline = HumanCentricCommunicationPipeline()
    
    async def send_message(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None,
        target_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send message and get human-like response
        
        Args:
            user_id: Unique user identifier
            message: User's message (any language)
            session_id: Optional session ID for context
            target_language: Optional target language code (e.g., 'es', 'ja')
        
        Returns:
            Complete response with all dimensions
        """
        
        target_lang = None
        if target_language:
            try:
                target_lang = Language[target_language.upper()]
            except KeyError:
                logger.warning(f"Unknown language: {target_language}")
        
        response = await self.pipeline.process_user_input(
            user_id,
            message,
            session_id,
            target_lang
        )
        
        return {
            "message": response.content,
            "detected_emotion": response.detected_emotion.value,
            "emotional_intensity": response.emotional_intensity,
            "communication_style": response.communication_style.value,
            "detected_language": response.detected_language.value,
            "translated_message": response.translated_content,
            "follow_up": response.follow_up_question,
            "confidence": response.confidence_score,
            "metadata": response.metadata,
        }
    
    def configure_user(
        self,
        user_id: str,
        language: str = "en",
        culture: Optional[str] = None,
    ):
        """Configure user's language and cultural preferences"""
        
        try:
            lang = Language[language.upper()]
        except KeyError:
            logger.warning(f"Unknown language: {language}")
            lang = Language.ENGLISH
        
        cultural = None
        if culture:
            try:
                cultural = CulturalContext[culture.upper()]
            except KeyError:
                logger.warning(f"Unknown culture: {culture}")
        
        self.pipeline.set_user_context(user_id, lang, cultural)
        
        self.pipeline.personalization.create_user_profile(user_id)
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user's profile and preferences"""
        profile = self.pipeline.personalization.get_user_profile(user_id)
        return profile or {}
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End a session and get analytics"""
        return self.pipeline.end_session(session_id)
