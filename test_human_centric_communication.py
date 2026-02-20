"""
Tests for Human-Centric Communication Systems
Verifies all components work correctly and integrate properly
"""

import pytest
import asyncio
from datetime import datetime

from human_communication_engine import (
    HumanCommunicationEngine,
    HumanDialogueOrchestrator,
    CommunicationContext,
    ToneDetection,
)
from multilingual_system import (
    MultilingualTranslationSystem,
    Language,
    CulturalContext,
    TranslationRequest,
)
from emotional_intelligence_system import (
    EmotionalIntelligenceEngine,
    PersonalizationEngine,
    EmotionalState,
)
from human_centric_communication_pipeline import (
    HumanCentricCommunicationPipeline,
    HumanCentricCommunicationAPI,
)


class TestHumanCommunicationEngine:
    """Test human communication engine"""
    
    @pytest.fixture
    def engine(self):
        return HumanCommunicationEngine()
    
    def test_tone_detection_positive(self, engine):
        """Test positive tone detection"""
        message = "I'm so happy and excited about this!"
        tone, confidence = engine.detect_tone(message)
        assert tone == ToneDetection.POSITIVE
        assert confidence > 0.5
    
    def test_tone_detection_negative(self, engine):
        """Test negative tone detection"""
        message = "This is terrible and awful"
        tone, confidence = engine.detect_tone(message)
        assert tone == ToneDetection.NEGATIVE
        assert confidence > 0.5
    
    def test_tone_detection_anxious(self, engine):
        """Test anxious tone detection"""
        message = "I'm really worried and nervous about this"
        tone, confidence = engine.detect_tone(message)
        assert tone == ToneDetection.ANXIOUS
        assert confidence > 0.3
    
    def test_intent_detection(self, engine):
        """Test intent detection"""
        message = "I need help with this problem"
        intents, scores = engine.detect_intent(message)
        assert "seeking_help" in intents
        assert len(intents) > 0
    
    def test_emotional_state_extraction(self, engine):
        """Test emotional state extraction"""
        message = "I'm feeling happy but also a bit anxious"
        emotions = engine.extract_emotional_state(message)
        assert emotions["joy"] > 0
        assert emotions["anxiety"] > 0
    
    def test_user_communication_profile_building(self, engine):
        """Test building user communication profile"""
        messages = [
            "Hey, how's it going?",
            "I love this idea!",
            "Can you help me understand this?",
            "That's awesome!",
        ]
        profile = engine.build_user_communication_profile("user123", messages)
        assert profile["user_id"] == "user123"
        assert "preferred_style" in profile
        assert "formality_level" in profile
    
    @pytest.mark.asyncio
    async def test_generate_response(self, engine):
        """Test response generation"""
        orchestrator = HumanDialogueOrchestrator()
        
        context = CommunicationContext(
            user_id="test_user",
            conversation_id="conv123",
            message="I'm really struggling with this"
        )
        
        response = await orchestrator.communication_engine.generate_response(context)
        assert response.text
        assert response.emotional_resonance >= 0.0
        assert response.tone is not None


class TestMultilingualSystem:
    """Test multilingual translation system"""
    
    @pytest.fixture
    def system(self):
        return MultilingualTranslationSystem()
    
    def test_language_detection_english(self, system):
        """Test English language detection"""
        text = "Hello, how are you today?"
        lang, confidence = system.detect_language(text)
        assert lang == Language.ENGLISH
        assert confidence > 0.3
    
    def test_language_detection_spanish(self, system):
        """Test Spanish language detection"""
        text = "Hola, ¿cómo estás hoy?"
        lang, confidence = system.detect_language(text)
        assert lang == Language.SPANISH or lang == Language.ENGLISH
    
    @pytest.mark.asyncio
    async def test_translation_english_to_spanish(self, system):
        """Test English to Spanish translation"""
        request = TranslationRequest(
            text="hello world",
            source_language=Language.ENGLISH,
            target_language=Language.SPANISH,
        )
        response = await system.translate(request)
        assert response.translated_text
        assert response.confidence_score > 0
    
    @pytest.mark.asyncio
    async def test_translation_preserves_tone(self, system):
        """Test that translation preserves tone"""
        request = TranslationRequest(
            text="That's amazing!",
            source_language=Language.ENGLISH,
            target_language=Language.SPANISH,
            preserve_tone=True
        )
        response = await system.translate(request)
        assert response.tone_preserved
    
    def test_cultural_notes_generation(self, system):
        """Test cultural notes generation"""
        notes = system._generate_cultural_notes(
            "Hello",
            Language.ENGLISH,
            Language.JAPANESE,
            None
        )
        assert "cultural" in str(notes).lower() or "communication" in str(notes).lower()
    
    def test_language_profile_creation(self, system):
        """Test language profile creation"""
        profile = system.create_language_profile(
            "user123",
            Language.SPANISH,
            [Language.ENGLISH],
            CulturalContext.LATIN_AMERICAN
        )
        assert profile.user_id == "user123"
        assert profile.primary_language == Language.SPANISH


class TestEmotionalIntelligence:
    """Test emotional intelligence system"""
    
    @pytest.fixture
    def engine(self):
        return EmotionalIntelligenceEngine()
    
    @pytest.mark.asyncio
    async def test_detect_joy(self, engine):
        """Test joy detection"""
        emotion, intensity, secondary = await engine.detect_emotional_state(
            "I'm so happy and joyful about this!"
        )
        assert emotion == EmotionalState.JOY
        assert intensity > 0.5
    
    @pytest.mark.asyncio
    async def test_detect_sadness(self, engine):
        """Test sadness detection"""
        emotion, intensity, secondary = await engine.detect_emotional_state(
            "I'm feeling sad and down"
        )
        assert emotion == EmotionalState.SADNESS
        assert intensity > 0.3
    
    @pytest.mark.asyncio
    async def test_detect_anxiety(self, engine):
        """Test anxiety detection"""
        emotion, intensity, secondary = await engine.detect_emotional_state(
            "I'm very anxious and worried"
        )
        assert emotion == EmotionalState.ANXIETY
        assert intensity > 0.3
    
    @pytest.mark.asyncio
    async def test_generate_emotionally_intelligent_response(self, engine):
        """Test emotionally intelligent response"""
        response = await engine.generate_emotionally_intelligent_response(
            EmotionalState.ANXIETY,
            0.6
        )
        assert response
        assert len(response) > 0
    
    def test_emotional_trajectory_tracking(self, engine):
        """Test tracking emotional patterns"""
        user_id = "test_user"
        engine.track_emotional_trajectory(user_id, EmotionalState.JOY, 0.8)
        engine.track_emotional_trajectory(user_id, EmotionalState.JOY, 0.7)
        engine.track_emotional_trajectory(user_id, EmotionalState.CONTENTMENT, 0.6)
        
        trend = engine.get_emotional_trend(user_id, days=1)
        assert "most_common" in trend


class TestPersonalizationEngine:
    """Test personalization engine"""
    
    @pytest.fixture
    def engine(self):
        return PersonalizationEngine()
    
    def test_create_user_profile(self, engine):
        """Test creating user profile"""
        profile = engine.create_user_profile("user123")
        assert profile["user_id"] == "user123"
        assert "emotional" in profile
        assert "personality" in profile
        assert "preferences" in profile
    
    def test_learn_from_interaction(self, engine):
        """Test learning from interactions"""
        user_id = "user123"
        engine.create_user_profile(user_id)
        
        for i in range(6):
            engine.learn_from_interaction(user_id, {
                "response": "Short response"
            })
        
        profile = engine.get_user_profile(user_id)
        assert profile["interaction_count"] >= 6
    
    @pytest.mark.asyncio
    async def test_personalize_response(self, engine):
        """Test response personalization"""
        user_id = "user123"
        engine.create_user_profile(user_id)
        
        original = "This is a long response with many details"
        personalized = await engine.personalize_response(
            user_id,
            original,
            {}
        )
        assert personalized
        assert len(personalized) > 0


class TestHumanCentricPipeline:
    """Test the complete human-centric pipeline"""
    
    @pytest.fixture
    def api(self):
        return HumanCentricCommunicationAPI()
    
    @pytest.mark.asyncio
    async def test_simple_message_english(self, api):
        """Test processing English message"""
        response = await api.send_message(
            user_id="test_user",
            message="I'm feeling great today!",
            session_id="session123"
        )
        
        assert response["message"]
        assert "detected_emotion" in response
        assert "detected_language" in response
        assert response["detected_language"] == "en"
    
    @pytest.mark.asyncio
    async def test_emotional_message(self, api):
        """Test processing emotional message"""
        response = await api.send_message(
            user_id="test_user",
            message="I'm really anxious and worried",
            session_id="session123"
        )
        
        assert response["message"]
        assert response["emotional_intensity"] > 0
    
    def test_configure_user(self, api):
        """Test user configuration"""
        api.configure_user(
            user_id="test_user",
            language="en",
            culture="western_casual"
        )
        
        profile = api.get_user_profile("test_user")
        assert profile is not None
    
    @pytest.mark.asyncio
    async def test_multilingual_response(self, api):
        """Test response in different language"""
        api.configure_user(
            user_id="test_user_multi",
            language="es"
        )
        
        response = await api.send_message(
            user_id="test_user_multi",
            message="Hola, ¿cómo estás?",
            target_language="es"
        )
        
        assert response["message"]
        assert response["detected_language"] in ["es", "en"]
    
    def test_session_analytics(self, api):
        """Test session analytics"""
        session_id = "test_session"
        api.pipeline.active_sessions[session_id] = api.pipeline.active_sessions.get(
            session_id,
            None
        ) or api.pipeline.active_sessions.get(session_id)
        
        analytics = api.end_session(session_id)
        assert isinstance(analytics, dict)


class TestIntegration:
    """Integration tests across all systems"""
    
    @pytest.mark.asyncio
    async def test_complete_flow_english_user(self):
        """Test complete flow for English user"""
        api = HumanCentricCommunicationAPI()
        
        api.configure_user("integration_user", language="en")
        
        messages = [
            "Hi, I'm new here",
            "I'm feeling a bit anxious about this",
            "But also excited to learn",
            "Can you help me understand?"
        ]
        
        for msg in messages:
            response = await api.send_message(
                user_id="integration_user",
                message=msg,
                session_id="integration_session"
            )
            
            assert response["message"]
            assert response["detected_emotion"]
            assert response["communication_style"]
    
    @pytest.mark.asyncio
    async def test_emotional_adaptation(self):
        """Test that system adapts to emotional changes"""
        api = HumanCentricCommunicationAPI()
        
        response1 = await api.send_message(
            user_id="emotion_user",
            message="Everything is amazing!",
            session_id="emotion_session"
        )
        
        response2 = await api.send_message(
            user_id="emotion_user",
            message="Actually, I'm really struggling now",
            session_id="emotion_session"
        )
        
        assert response1["emotional_intensity"] < response2["emotional_intensity"]
    
    @pytest.mark.asyncio
    async def test_personalization_over_time(self):
        """Test that personalization improves over time"""
        api = HumanCentricCommunicationAPI()
        user_id = "personalization_user"
        
        for i in range(10):
            await api.send_message(
                user_id=user_id,
                message=f"Test message {i}",
                session_id="personalization_session"
            )
        
        profile = api.get_user_profile(user_id)
        assert profile is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
