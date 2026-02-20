"""
Emotional Intelligence & Personalization System for Ochuko AI v5.0
Deep emotional understanding, personality adaptation, genuine human connection
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class EmotionalState(Enum):
    """Detailed emotional states"""
    JOY = "joy"
    CONTENTMENT = "contentment"
    PRIDE = "pride"
    EXCITEMENT = "excitement"
    SADNESS = "sadness"
    GRIEF = "grief"
    DESPAIR = "despair"
    ANGER = "anger"
    RAGE = "rage"
    FRUSTRATION = "frustration"
    ANXIETY = "anxiety"
    FEAR = "fear"
    PANIC = "panic"
    CONFUSION = "confusion"
    CURIOSITY = "curiosity"
    BOREDOM = "boredom"
    SHAME = "shame"
    GUILT = "guilt"
    LONELINESS = "loneliness"
    LOVE = "love"
    GRATITUDE = "gratitude"


class PersonalityDimension(Enum):
    """Big Five personality traits"""
    OPENNESS = "openness"
    CONSCIENTIOUSNESS = "conscientiousness"
    EXTRAVERSION = "extraversion"
    AGREEABLENESS = "agreeableness"
    NEUROTICISM = "neuroticism"


class InteractionStyle(Enum):
    """How user prefers to interact"""
    DIRECT = "direct"
    COLLABORATIVE = "collaborative"
    REFLECTIVE = "reflective"
    ACTION_ORIENTED = "action_oriented"
    ANALYTICAL = "analytical"
    INTUITIVE = "intuitive"


@dataclass
class EmotionalProfile:
    """User's emotional patterns and tendencies"""
    user_id: str
    baseline_emotional_state: EmotionalState = EmotionalState.CONTENTMENT
    emotional_volatility: float = 0.5
    stress_triggers: List[str] = field(default_factory=list)
    joy_triggers: List[str] = field(default_factory=list)
    emotional_expression_preference: str = "moderate"
    trauma_awareness: Dict[str, str] = field(default_factory=dict)
    resilience_level: float = 0.5
    support_needs: List[str] = field(default_factory=list)
    emotional_history: List[Tuple[datetime, EmotionalState]] = field(default_factory=list)


@dataclass
class PersonalityProfile:
    """User's personality characteristics"""
    user_id: str
    big_five_traits: Dict[PersonalityDimension, float] = field(default_factory=dict)
    interaction_style: InteractionStyle = InteractionStyle.COLLABORATIVE
    learning_style: str = "mixed"
    decision_making_style: str = "balanced"
    values: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    growth_areas: List[str] = field(default_factory=list)
    humor_style: str = "gentle"
    risk_tolerance: float = 0.5


@dataclass
class PreferencesProfile:
    """User's interaction preferences"""
    user_id: str
    communication_frequency: str = "moderate"
    response_length: str = "moderate"
    formality_preference: str = "neutral"
    emoji_usage: bool = False
    use_real_names: bool = True
    privacy_preferences: Dict[str, bool] = field(default_factory=dict)
    notification_preferences: Dict[str, bool] = field(default_factory=dict)
    pacing_preference: str = "user_controlled"
    challenge_preference: str = "moderate"


class EmotionalIntelligenceEngine:
    """
    Detects emotional states, respects emotional boundaries,
    provides emotionally intelligent responses
    """
    
    def __init__(self):
        self.emotional_keywords = self._init_emotional_keywords()
        self.emotional_intensifiers = self._init_emotional_intensifiers()
        self.trauma_informed_responses = self._init_trauma_responses()
        self.emotion_trajectories = {}
    
    def _init_emotional_keywords(self) -> Dict[EmotionalState, List[str]]:
        """Initialize keywords for each emotional state"""
        return {
            EmotionalState.JOY: ["happy", "joyful", "delighted", "wonderful", "great"],
            EmotionalState.CONTENTMENT: ["good", "okay", "fine", "alright", "satisfied"],
            EmotionalState.PRIDE: ["proud", "accomplished", "achieved", "success", "earned"],
            EmotionalState.EXCITEMENT: ["excited", "thrilled", "can't wait", "awesome", "stoked"],
            EmotionalState.SADNESS: ["sad", "down", "unhappy", "melancholy", "blue"],
            EmotionalState.GRIEF: ["grieving", "loss", "bereaved", "mourning", "heartbroken"],
            EmotionalState.DESPAIR: ["hopeless", "desperate", "suicidal", "worthless", "lost"],
            EmotionalState.ANGER: ["angry", "mad", "irritated", "annoyed", "cross"],
            EmotionalState.RAGE: ["furious", "outraged", "enraged", "infuriated", "livid"],
            EmotionalState.FRUSTRATION: ["frustrated", "stuck", "blocked", "fed up", "exasperated"],
            EmotionalState.ANXIETY: ["anxious", "worried", "nervous", "apprehensive", "uneasy"],
            EmotionalState.FEAR: ["afraid", "scared", "frightened", "terrified", "petrified"],
            EmotionalState.PANIC: ["panicking", "panic", "panic attack", "hyperventilating", "dying"],
            EmotionalState.CONFUSION: ["confused", "unclear", "lost", "bewildered", "disoriented"],
            EmotionalState.CURIOSITY: ["curious", "wondering", "interested", "intrigued", "fascinated"],
            EmotionalState.BOREDOM: ["bored", "uninterested", "dull", "tedious", "mundane"],
            EmotionalState.SHAME: ["ashamed", "embarrassed", "humiliated", "shameful", "mortified"],
            EmotionalState.GUILT: ["guilty", "remorseful", "regretful", "apologetic", "culpable"],
            EmotionalState.LONELINESS: ["lonely", "isolated", "alone", "disconnected", "unseen"],
            EmotionalState.LOVE: ["love", "adore", "cherish", "devoted", "affection"],
            EmotionalState.GRATITUDE: ["grateful", "thankful", "appreciative", "blessed", "indebted"],
        }
    
    def _init_emotional_intensifiers(self) -> Dict[str, float]:
        """Initialize intensity multipliers for words"""
        return {
            "very": 1.5,
            "extremely": 2.0,
            "so": 1.4,
            "really": 1.3,
            "absolutely": 1.8,
            "completely": 1.7,
            "utterly": 1.9,
            "incredibly": 1.8,
            "deeply": 1.6,
        }
    
    def _init_trauma_responses(self) -> Dict[str, str]:
        """Initialize trauma-informed response patterns"""
        return {
            "safety_first": "Your safety and wellbeing matter most.",
            "validation": "Your feelings are completely valid and understandable.",
            "pacing": "We can take this at whatever pace feels right for you.",
            "control": "You're in control here. We can talk about what you want, when you want.",
            "no_pressure": "No pressure. Share what you're comfortable sharing.",
            "connection": "You're not alone in this. Many people experience similar things.",
            "hope": "Healing is possible, even when it doesn't feel that way right now.",
            "professional": "If this is urgent, please reach out to a professional. Here are resources...",
        }
    
    async def detect_emotional_state(self, text: str) -> Tuple[EmotionalState, float, List[str]]:
        """
        Detect user's emotional state
        Returns: (primary_emotion, intensity, secondary_emotions)
        """
        text_lower = text.lower()
        
        emotion_scores = {}
        
        for emotion, keywords in self.emotional_keywords.items():
            score = 0.0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1.0
                    
                    for intensifier, multiplier in self.emotional_intensifiers.items():
                        pattern = f"{intensifier} {keyword}"
                        if pattern in text_lower:
                            score += multiplier - 1.0
            
            if score > 0:
                emotion_scores[emotion] = score
        
        if not emotion_scores:
            return EmotionalState.NEUTRAL if hasattr(EmotionalState, 'NEUTRAL') else EmotionalState.CONTENTMENT, 0.5, []
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[primary_emotion]
        
        intensity = min(1.0, max_score / max(1, len(text_lower.split()) / 2))
        
        secondary_emotions = [
            emotion.value for emotion, score in sorted(
                emotion_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[1:4]
        ]
        
        return primary_emotion, intensity, secondary_emotions
    
    async def generate_emotionally_intelligent_response(
        self,
        detected_emotion: EmotionalState,
        emotional_intensity: float,
        user_profile: Optional[EmotionalProfile] = None
    ) -> str:
        """Generate response that respects emotional state"""
        
        if detected_emotion == EmotionalState.DESPAIR or detected_emotion == EmotionalState.PANIC:
            return self.trauma_informed_responses["professional"] + "\n\n" + self._generate_crisis_response()
        
        if emotional_intensity > 0.8:
            return self._generate_intense_emotion_response(detected_emotion)
        
        if detected_emotion in [EmotionalState.GRIEF, EmotionalState.LONELINESS, EmotionalState.GUILT]:
            return self._generate_supportive_response(detected_emotion, user_profile)
        
        if detected_emotion in [EmotionalState.JOY, EmotionalState.EXCITEMENT, EmotionalState.PRIDE]:
            return self._generate_celebratory_response(detected_emotion)
        
        if detected_emotion in [EmotionalState.ANXIETY, EmotionalState.FEAR]:
            return self._generate_reassuring_response(detected_emotion)
        
        return self._generate_balanced_response(detected_emotion)
    
    def _generate_crisis_response(self) -> str:
        """Generate crisis intervention response"""
        return (
            "I'm genuinely concerned about what you've shared. "
            "Your life has value, and there are people who want to help:\n\n"
            "🆘 **National Suicide Prevention Lifeline**: 988 (US)\n"
            "🆘 **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/\n"
            "🆘 **Crisis Text Line**: Text HOME to 741741\n\n"
            "Please reach out to someone you trust, or contact one of these services immediately. "
            "You don't have to face this alone."
        )
    
    def _generate_intense_emotion_response(self, emotion: EmotionalState) -> str:
        """Response for intense emotions"""
        responses = {
            EmotionalState.RAGE: "That sounds like a lot to carry right now. Let's talk about what you're experiencing.",
            EmotionalState.PANIC: "You're in a panic response. Let's ground you: what do you see, hear, feel right now?",
            EmotionalState.DESPAIR: "I hear the hopelessness. But you reached out, which takes strength.",
        }
        return responses.get(emotion, "That's intense. I'm here to listen.")
    
    def _generate_supportive_response(
        self, 
        emotion: EmotionalState, 
        profile: Optional[EmotionalProfile]
    ) -> str:
        """Response for vulnerable emotions"""
        responses = {
            EmotionalState.GRIEF: "Grief is love with nowhere to go. What you're feeling makes sense.",
            EmotionalState.LONELINESS: "Loneliness is real, and it matters. You're not invisible to me.",
            EmotionalState.GUILT: "Guilt often tells us our values. Let's explore what this means for you.",
        }
        base_response = responses.get(emotion, "What you're feeling is valid.")
        
        if profile and profile.support_needs:
            base_response += f"\n\nI know you appreciate support that's {', '.join(profile.support_needs[:2])}."
        
        return base_response
    
    def _generate_celebratory_response(self, emotion: EmotionalState) -> str:
        """Response for positive emotions"""
        responses = {
            EmotionalState.JOY: "That joy is wonderful! Tell me more about what's bringing this.",
            EmotionalState.EXCITEMENT: "Your excitement is contagious! What are you looking forward to?",
            EmotionalState.PRIDE: "You should be proud. That's a real accomplishment.",
        }
        return responses.get(emotion, "I'm genuinely happy for you!")
    
    def _generate_reassuring_response(self, emotion: EmotionalState) -> str:
        """Response for fear and anxiety"""
        responses = {
            EmotionalState.ANXIETY: "That anxiety is real, and it's also treatable. Let's break this down.",
            EmotionalState.FEAR: "Fear is trying to protect you. Let's understand what it's protecting you from.",
        }
        return responses.get(emotion, "I understand you're worried. Let's work through this together.")
    
    def _generate_balanced_response(self, emotion: EmotionalState) -> str:
        """Default balanced response"""
        return f"I hear that you're feeling {emotion.value}. That's completely understandable."
    
    def track_emotional_trajectory(
        self,
        user_id: str,
        emotion: EmotionalState,
        intensity: float
    ):
        """Track emotional patterns over time"""
        if user_id not in self.emotion_trajectories:
            self.emotion_trajectories[user_id] = []
        
        self.emotion_trajectories[user_id].append({
            "timestamp": datetime.now(),
            "emotion": emotion,
            "intensity": intensity
        })
        
        if len(self.emotion_trajectories[user_id]) > 1000:
            self.emotion_trajectories[user_id] = self.emotion_trajectories[user_id][-1000:]
    
    def get_emotional_trend(self, user_id: str, days: int = 7) -> Dict[str, any]:
        """Analyze emotional trends"""
        if user_id not in self.emotion_trajectories:
            return {}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_emotions = [
            e for e in self.emotion_trajectories[user_id]
            if e["timestamp"] > cutoff_date
        ]
        
        if not recent_emotions:
            return {}
        
        emotion_frequencies = {}
        total_intensity = 0
        
        for e in recent_emotions:
            emotion_frequencies[e["emotion"].value] = emotion_frequencies.get(e["emotion"].value, 0) + 1
            total_intensity += e["intensity"]
        
        return {
            "most_common": max(emotion_frequencies, key=emotion_frequencies.get),
            "frequency_distribution": emotion_frequencies,
            "average_intensity": total_intensity / len(recent_emotions),
            "trend_direction": "improving" if recent_emotions[-1]["intensity"] < recent_emotions[0]["intensity"] else "stable"
        }


class PersonalizationEngine:
    """
    Learns user preferences and personalizes all interactions
    Adapts communication to individual user styles
    """
    
    def __init__(self):
        self.user_profiles = {}
        self.interaction_history = {}
        self.preference_learning_threshold = 5
    
    def create_user_profile(
        self,
        user_id: str,
        emotional_profile: Optional[EmotionalProfile] = None,
        personality_profile: Optional[PersonalityProfile] = None,
        preferences_profile: Optional[PreferencesProfile] = None
    ):
        """Create comprehensive user profile"""
        
        profile = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "emotional": emotional_profile or EmotionalProfile(user_id=user_id),
            "personality": personality_profile or PersonalityProfile(user_id=user_id),
            "preferences": preferences_profile or PreferencesProfile(user_id=user_id),
            "interaction_count": 0,
            "last_interaction": None,
        }
        
        self.user_profiles[user_id] = profile
        self.interaction_history[user_id] = []
        
        return profile
    
    def learn_from_interaction(
        self,
        user_id: str,
        interaction_data: Dict[str, any]
    ):
        """Learn from user interactions"""
        
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
        
        if user_id not in self.interaction_history:
            self.interaction_history[user_id] = []
        
        self.interaction_history[user_id].append({
            "timestamp": datetime.now(),
            "data": interaction_data
        })
        
        profile = self.user_profiles[user_id]
        profile["interaction_count"] += 1
        profile["last_interaction"] = datetime.now()
        
        if profile["interaction_count"] >= self.preference_learning_threshold:
            self._update_preferences_from_history(user_id)
    
    def _update_preferences_from_history(self, user_id: str):
        """Update preferences based on interaction history"""
        if user_id not in self.interaction_history:
            return
        
        history = self.interaction_history[user_id][-50:]
        
        if not history:
            return
        
        response_lengths = [
            len(interaction["data"].get("response", "").split())
            for interaction in history
            if "response" in interaction["data"]
        ]
        
        if response_lengths:
            avg_length = sum(response_lengths) / len(response_lengths)
            if avg_length < 20:
                self.user_profiles[user_id]["preferences"].response_length = "brief"
            elif avg_length > 100:
                self.user_profiles[user_id]["preferences"].response_length = "detailed"
            else:
                self.user_profiles[user_id]["preferences"].response_length = "moderate"
    
    async def personalize_response(
        self,
        user_id: str,
        response: str,
        context: Dict[str, any]
    ) -> str:
        """Personalize response based on user profile"""
        
        if user_id not in self.user_profiles:
            return response
        
        profile = self.user_profiles[user_id]
        prefs = profile["preferences"]
        
        if prefs.response_length == "brief":
            response = self._shorten_response(response)
        elif prefs.response_length == "detailed":
            response = self._expand_response(response)
        
        if prefs.emoji_usage:
            response = self._add_emojis(response)
        else:
            response = self._remove_emojis(response)
        
        if prefs.formality_preference == "formal":
            response = self._formalize_response(response)
        elif prefs.formality_preference == "casual":
            response = self._casualize_response(response)
        
        self.learn_from_interaction(user_id, {
            "original_response": response,
            "context": context
        })
        
        return response
    
    def _shorten_response(self, response: str) -> str:
        """Shorten response"""
        sentences = response.split(". ")
        if len(sentences) > 3:
            return ". ".join(sentences[:3]) + "."
        return response
    
    def _expand_response(self, response: str) -> str:
        """Expand response (add examples, details)"""
        return response + "\n\nWould you like me to elaborate on any part of this?"
    
    def _add_emojis(self, response: str) -> str:
        """Add relevant emojis"""
        emoji_map = {
            "happy": "😊",
            "sad": "😔",
            "great": "🌟",
            "help": "🤝",
            "idea": "💡",
        }
        
        for word, emoji in emoji_map.items():
            if word in response.lower():
                response = response.replace(word, f"{word} {emoji}")
        
        return response
    
    def _remove_emojis(self, response: str) -> str:
        """Remove emojis"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub("", response)
    
    def _formalize_response(self, response: str) -> str:
        """Make response more formal"""
        return (
            response
            .replace("hey", "Good day")
            .replace("wanna", "would like to")
            .replace("gonna", "will")
            .replace("can't", "cannot")
            .replace("don't", "do not")
        )
    
    def _casualize_response(self, response: str) -> str:
        """Make response more casual"""
        return (
            response
            .replace("Good day", "Hey")
            .replace("would like to", "wanna")
            .replace("will", "gonna")
            .replace("cannot", "can't")
            .replace("do not", "don't")
        )
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user's profile"""
        return self.user_profiles.get(user_id)


import re
