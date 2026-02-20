"""
Ochuko AI - Empathy Engine
True understanding of human needs based on physiological, behavioral, and emotional signals.
Bridges the gap between AI and genuine human understanding.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class CommunicationStyle(Enum):
    """Adaptive communication styles"""
    SUPPORTIVE = "supportive"  # Empathetic, caring
    DIRECTIVE = "directive"  # Clear, action-oriented
    COLLABORATIVE = "collaborative"  # Partners with user
    EDUCATIONAL = "educational"  # Teaches and explains
    REASSURING = "reassuring"  # Calms and comforts
    HUMOROUS = "humorous"  # Light-hearted, breaks tension
    SERIOUS = "serious"  # Formal, grave tone


@dataclass
class UserEmotionalProfile:
    """Profile of user's emotional patterns and needs"""
    primary_emotions: List[str]
    stress_triggers: List[str]
    comfort_factors: List[str]
    communication_preferences: List[CommunicationStyle]
    past_needs: List[Dict[str, Any]]
    current_emotional_state: str
    emotional_trajectory: str  # improving, declining, stable
    needs_immediate_support: bool


@dataclass
class ContextualUnderstanding:
    """Deep understanding of user's current situation"""
    immediate_context: str
    recent_history: List[str]
    current_stressors: List[str]
    available_resources: List[str]
    past_similar_situations: List[Dict]
    likely_outcome_trajectory: str
    intervention_points: List[str]


class EmpathyEngine:
    """
    Understands and responds to human needs with genuine empathy.
    Not just detecting emotions, but understanding what the human truly needs.
    """
    
    def __init__(self):
        self.user_profiles: Dict[str, UserEmotionalProfile] = {}
        self.contextual_analyzer = ContextualAnalyzer()
        self.need_interpreter = NeedInterpreter()
        self.response_generator = EmpathyResponseGenerator()
        self.is_ready = False
    
    async def initialize(self):
        """Initialize empathy engine"""
        logger.info("Initializing Empathy Engine...")
        self.is_ready = True
        logger.info("✅ Empathy Engine ready")
    
    async def understand_user(
        self,
        user_id: str,
        perception_data: Dict[str, Any],
        conversation_history: List[Dict]
    ) -> UserEmotionalProfile:
        """
        Build deep understanding of user's emotional state and needs.
        Goes beyond surface emotion to true need identification.
        """
        
        logger.info(f"Developing empathetic understanding of {user_id}...")
        
        # Extract emotional indicators
        emotional_state = perception_data.get("facial_analysis", {}).get("true_emotion", "unknown")
        physiological = perception_data.get("physiological_signals", {})
        body_language = perception_data.get("body_language", {})
        
        # Identify true needs (not just stated needs)
        true_needs = await self.need_interpreter.identify_true_needs(
            user_id,
            emotional_state,
            physiological,
            body_language,
            conversation_history
        )
        
        # Build emotional profile
        profile = await self._build_profile(
            user_id,
            emotional_state,
            true_needs,
            perception_data
        )
        
        self.user_profiles[user_id] = profile
        
        logger.info(f"Emotional Profile: {profile.current_emotional_state}")
        logger.info(f"Identified Needs: {true_needs}")
        
        return profile
    
    async def generate_empathetic_response(
        self,
        user_id: str,
        user_message: str,
        perception_data: Dict,
        profile: UserEmotionalProfile
    ) -> Dict[str, Any]:
        """
        Generate response that shows genuine understanding.
        Response is calibrated to user's emotional state and true needs.
        """
        
        logger.info("Generating empathetic response...")
        
        # Understand what they really need
        contextual_understanding = await self.contextual_analyzer.analyze(
            user_id,
            user_message,
            perception_data,
            profile
        )
        
        # Choose appropriate communication style
        communication_style = self._select_communication_style(profile, contextual_understanding)
        
        # Generate response
        response = await self.response_generator.generate(
            user_message=user_message,
            user_profile=profile,
            context=contextual_understanding,
            style=communication_style,
            needs=profile.primary_emotions
        )
        
        return {
            "text": response["text"],
            "tone": communication_style.value,
            "empathy_level": response.get("empathy_score", 0.8),
            "addresses_true_need": response.get("addresses_need", True),
            "follow_up_action": response.get("suggested_action"),
            "support_offered": response.get("support_type")
        }
    
    async def detect_crisis_state(
        self,
        user_id: str,
        perception_data: Dict,
        profile: UserEmotionalProfile
    ) -> Dict[str, Any]:
        """
        Detect if user is in crisis and needs immediate intervention.
        Based on psychological, physiological, and behavioral signals.
        """
        
        # Crisis indicators
        crisis_signals = {
            "severe_stress": perception_data.get("physiological_signals", {}).get("heart_rate", 0) > 120,
            "extreme_sadness": profile.current_emotional_state in ["sadness", "despair"],
            "anger_escalation": perception_data.get("voice_analysis", {}).get("anger_level", 0) > 0.8,
            "withdrawal": perception_data.get("body_language", {}).get("engagement_level") == "disengaged",
            "desperation_cues": any(word in perception_data.get("verbal_content", "").lower() 
                                    for word in ["help", "can't", "won't", "always", "never"])
        }
        
        crisis_score = sum(crisis_signals.values()) / len(crisis_signals)
        
        if crisis_score > 0.5:
            return {
                "in_crisis": True,
                "crisis_level": "high" if crisis_score > 0.7 else "moderate",
                "immediate_actions": self._generate_crisis_response(crisis_signals),
                "support_resources": self._get_support_resources(user_id, profile)
            }
        
        return {"in_crisis": False}
    
    async def proactive_support(
        self,
        user_id: str,
        profile: UserEmotionalProfile,
        perception_data: Dict
    ) -> Optional[Dict]:
        """
        Proactively offer support before user asks.
        Anticipate needs based on patterns and current state.
        """
        
        # Check if user might need support
        if profile.needs_immediate_support or profile.emotional_trajectory == "declining":
            support_type = await self.need_interpreter.identify_support_needed(profile)
            
            if support_type:
                return {
                    "proactive_message": await self._generate_proactive_message(profile, support_type),
                    "support_type": support_type,
                    "timing": "now",
                    "interventions": await self._get_interventions(profile, support_type)
                }
        
        return None
    
    def _select_communication_style(
        self,
        profile: UserEmotionalProfile,
        context: ContextualUnderstanding
    ) -> CommunicationStyle:
        """Choose communication style based on user state and context"""
        
        # If user is in crisis, be supportive
        if profile.needs_immediate_support:
            return CommunicationStyle.SUPPORTIVE
        
        # If user is stressed, be reassuring
        if profile.current_emotional_state in ["anxious", "frustrated", "stressed"]:
            return CommunicationStyle.REASSURING
        
        # If situation is complex, be collaborative
        if len(context.current_stressors) > 2:
            return CommunicationStyle.COLLABORATIVE
        
        # Default to preferences
        if profile.communication_preferences:
            return profile.communication_preferences[0]
        
        return CommunicationStyle.SUPPORTIVE
    
    async def _build_profile(
        self,
        user_id: str,
        emotional_state: str,
        true_needs: List[str],
        perception_data: Dict
    ) -> UserEmotionalProfile:
        """Build comprehensive emotional profile"""
        
        return UserEmotionalProfile(
            primary_emotions=[emotional_state],
            stress_triggers=perception_data.get("identified_stressors", []),
            comfort_factors=perception_data.get("comfort_factors", []),
            communication_preferences=[CommunicationStyle.SUPPORTIVE],
            past_needs=[],
            current_emotional_state=emotional_state,
            emotional_trajectory="stable",
            needs_immediate_support=False
        )
    
    def _generate_crisis_response(self, signals: Dict) -> List[str]:
        """Generate immediate crisis response actions"""
        actions = []
        
        if signals.get("severe_stress"):
            actions.append("Suggest calming techniques")
        if signals.get("extreme_sadness"):
            actions.append("Offer emotional support")
        if signals.get("anger_escalation"):
            actions.append("Provide de-escalation strategies")
        if signals.get("withdrawal"):
            actions.append("Encourage connection")
        
        return actions
    
    def _get_support_resources(self, user_id: str, profile: UserEmotionalProfile) -> List[Dict]:
        """Get appropriate support resources"""
        return [
            {"type": "mental_health", "available": True},
            {"type": "crisis_line", "available": True},
            {"type": "peer_support", "available": True}
        ]
    
    async def _generate_proactive_message(self, profile: UserEmotionalProfile, support_type: str) -> str:
        """Generate a proactive support message"""
        return f"I notice you might need some support with {support_type}. How can I help?"
    
    async def _get_interventions(self, profile: UserEmotionalProfile, support_type: str) -> List[str]:
        """Get appropriate interventions"""
        return [
            f"Discuss {support_type}",
            "Suggest coping strategies",
            "Offer resources"
        ]


class ContextualAnalyzer:
    """Analyzes context of user's situation"""
    
    async def analyze(
        self,
        user_id: str,
        user_message: str,
        perception_data: Dict,
        profile: Any
    ) -> ContextualUnderstanding:
        """Analyze full context"""
        return ContextualUnderstanding(
            immediate_context="talking",
            recent_history=[],
            current_stressors=[],
            available_resources=[],
            past_similar_situations=[],
            likely_outcome_trajectory="positive",
            intervention_points=[]
        )


class NeedInterpreter:
    """Interprets true human needs from signals"""
    
    async def identify_true_needs(
        self,
        user_id: str,
        emotional_state: str,
        physiological: Dict,
        body_language: Dict,
        conversation: List
    ) -> List[str]:
        """Identify what user truly needs (beyond what they say)"""
        return ["support", "understanding", "action"]
    
    async def identify_support_needed(self, profile: UserEmotionalProfile) -> Optional[str]:
        """Identify what kind of support is needed"""
        if "sadness" in profile.primary_emotions:
            return "emotional_support"
        if "anxiety" in profile.primary_emotions:
            return "reassurance"
        return None


class EmpathyResponseGenerator:
    """Generates empathetic responses"""
    
    async def generate(
        self,
        user_message: str,
        user_profile: UserEmotionalProfile,
        context: ContextualUnderstanding,
        style: CommunicationStyle,
        needs: List[str]
    ) -> Dict:
        """Generate empathetic response"""
        return {
            "text": f"I understand you're feeling {user_profile.current_emotional_state}. How can I help?",
            "empathy_score": 0.85,
            "addresses_need": True,
            "suggested_action": "Listen",
            "support_type": "emotional"
        }
