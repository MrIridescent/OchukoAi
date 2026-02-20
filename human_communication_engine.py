"""
Human Communication Engine for Ochuko AI v5.0
Enables natural, empathetic dialogue that feels genuinely human
Detects emotion, intent, context, and responds with authentic understanding
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class CommunicationStyle(Enum):
    """Communication personality styles"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    EMPATHETIC = "empathetic"
    TECHNICAL = "technical"
    SOCRATIC = "socratic"
    NARRATIVE = "narrative"


class ToneDetection(Enum):
    """User's emotional tone"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"
    THOUGHTFUL = "thoughtful"
    CELEBRATORY = "celebratory"


@dataclass
class CommunicationContext:
    """Context for conversation flow"""
    user_id: str
    conversation_id: str
    message: str
    previous_messages: List[str] = field(default_factory=list)
    detected_tone: ToneDetection = ToneDetection.NEUTRAL
    communication_style: CommunicationStyle = CommunicationStyle.EMPATHETIC
    emotional_state: Dict[str, float] = field(default_factory=dict)
    intent: Optional[str] = None
    cultural_context: Optional[str] = None
    user_language: str = "en"
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class DialogueResponse:
    """Response with human characteristics"""
    text: str
    tone: ToneDetection
    style: CommunicationStyle
    emotional_resonance: float
    follow_up_question: Optional[str] = None
    acknowledgment: str = ""
    personalization_notes: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class HumanCommunicationEngine:
    """
    Core engine for natural human-like communication
    Handles tone detection, emotional understanding, and adaptive responses
    """
    
    def __init__(self):
        self.emotional_markers = self._init_emotional_markers()
        self.intent_patterns = self._init_intent_patterns()
        self.dialogue_templates = self._init_dialogue_templates()
        self.communication_profiles = {}
        self.conversation_history = {}
        
    def _init_emotional_markers(self) -> Dict[ToneDetection, List[str]]:
        """Initialize emotional tone markers"""
        return {
            ToneDetection.POSITIVE: [
                "great", "amazing", "wonderful", "awesome", "excellent", "happy",
                "love", "incredible", "fantastic", "brilliant", "perfect", "thrilled",
                "delighted", "grateful", "excited", "ecstatic"
            ],
            ToneDetection.NEGATIVE: [
                "hate", "terrible", "awful", "horrible", "disgusting", "angry",
                "frustrated", "devastated", "furious", "disgusted", "angry", "mad"
            ],
            ToneDetection.ANXIOUS: [
                "worried", "anxious", "concerned", "nervous", "stressed", "afraid",
                "scared", "panic", "dread", "uneasy", "overwhelmed", "desperate"
            ],
            ToneDetection.CURIOUS: [
                "wondering", "why", "how", "what if", "curious", "intriguing",
                "interesting", "question", "explore", "discover", "understand"
            ],
            ToneDetection.FRUSTRATED: [
                "stuck", "can't", "won't work", "problem", "issue", "broken",
                "failing", "not working", "confusion", "unclear", "complicated"
            ],
            ToneDetection.THOUGHTFUL: [
                "think", "consider", "reflect", "pondering", "realize", "understand",
                "recognize", "acknowledge", "appreciate", "perspective"
            ],
            ToneDetection.CELEBRATORY: [
                "finally", "success", "achieved", "done", "completed", "finished",
                "victory", "won", "passed", "made it", "breakthrough"
            ]
        }
    
    def _init_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize intent detection patterns"""
        return {
            "seeking_help": [
                "help", "how do i", "how can i", "need help", "stuck",
                "don't know", "unable", "can't", "guidance", "support"
            ],
            "seeking_understanding": [
                "why", "explain", "what does", "understand", "clarify",
                "elaborate", "details", "more about", "teach me"
            ],
            "decision_making": [
                "should i", "which is better", "pros and cons", "advise",
                "recommendation", "option", "choose", "decision", "better"
            ],
            "emotional_support": [
                "feel", "sad", "stressed", "worried", "alone", "struggling",
                "help me", "support", "understand", "listen", "care"
            ],
            "creative_exploration": [
                "idea", "create", "design", "imagine", "what if", "innovative",
                "unique", "novel", "different", "experiment"
            ],
            "problem_solving": [
                "problem", "issue", "broken", "error", "fix", "solve",
                "solution", "bug", "wrong", "incorrect"
            ]
        }
    
    def _init_dialogue_templates(self) -> Dict[str, List[str]]:
        """Initialize natural dialogue response templates"""
        return {
            "acknowledgment": [
                "I hear you.",
                "That makes sense.",
                "I understand where you're coming from.",
                "I can see why that matters to you.",
                "That's a meaningful point.",
                "I appreciate you sharing that.",
            ],
            "empathetic_response": [
                "It sounds like {emotion} is really affecting you right now.",
                "That must be {feeling} for you.",
                "I can imagine how {adjective} that would be.",
                "It makes complete sense that you feel {emotion}.",
                "Your {emotion} is completely valid.",
            ],
            "clarifying_questions": [
                "Can you tell me more about {topic}?",
                "What's the most important aspect of this for you?",
                "How has this been impacting you?",
                "What would ideal look like to you?",
                "What have you tried so far?",
                "What matters most in this situation?",
            ],
            "supportive_affirmation": [
                "You're thinking about this in a really smart way.",
                "That shows real insight.",
                "You're asking the right questions.",
                "This kind of reflection is valuable.",
                "You're clearly taking this seriously.",
            ],
            "authentic_uncertainty": [
                "I'm not entirely sure, but let me think through this with you.",
                "That's a complex question. Let me explore it.",
                "I want to be honest—I have some uncertainty here too.",
                "This deserves careful consideration.",
                "Let me break down what I do know with confidence.",
            ]
        }
    
    def detect_tone(self, message: str) -> Tuple[ToneDetection, float]:
        """
        Detect emotional tone from message
        Returns: (detected_tone, confidence_score)
        """
        message_lower = message.lower()
        scores = {}
        
        for tone, markers in self.emotional_markers.items():
            match_count = sum(1 for marker in markers if marker in message_lower)
            scores[tone] = match_count
        
        if not any(scores.values()):
            return ToneDetection.NEUTRAL, 0.0
        
        detected = max(scores, key=scores.get)
        max_score = scores[detected]
        total_markers = len(message_lower.split())
        confidence = min(1.0, (max_score / total_markers) * 2)
        
        return detected, confidence
    
    def detect_intent(self, message: str) -> Tuple[List[str], Dict[str, float]]:
        """
        Detect user's underlying intent
        Returns: (intents, confidence_scores)
        """
        message_lower = message.lower()
        detected_intents = {}
        
        for intent, patterns in self.intent_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in message_lower)
            if matches > 0:
                confidence = min(1.0, matches / len(message_lower.split()))
                detected_intents[intent] = confidence
        
        sorted_intents = sorted(detected_intents.items(), key=lambda x: x[1], reverse=True)
        return [intent for intent, _ in sorted_intents], {k: v for k, v in sorted_intents}
    
    def extract_emotional_state(self, message: str) -> Dict[str, float]:
        """
        Extract specific emotional state markers
        Returns emotional intensity for different emotions
        """
        emotions = {
            "joy": 0.0,
            "sadness": 0.0,
            "frustration": 0.0,
            "confusion": 0.0,
            "anxiety": 0.0,
            "confidence": 0.0,
            "curiosity": 0.0,
            "gratitude": 0.0,
        }
        
        emotion_keywords = {
            "joy": ["happy", "glad", "joy", "love", "excited", "thrilled"],
            "sadness": ["sad", "unhappy", "down", "depressed", "lonely"],
            "frustration": ["frustrated", "annoyed", "irritated", "fed up"],
            "confusion": ["confused", "uncertain", "unclear", "lost", "puzzled"],
            "anxiety": ["anxious", "worried", "nervous", "scared", "afraid"],
            "confidence": ["confident", "sure", "certain", "strong", "capable"],
            "curiosity": ["curious", "interested", "wondering", "intrigued"],
            "gratitude": ["grateful", "thankful", "appreciate", "blessed"],
        }
        
        message_lower = message.lower()
        for emotion, keywords in emotion_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            emotions[emotion] = min(1.0, matches * 0.3)
        
        return emotions
    
    async def generate_response(self, context: CommunicationContext) -> DialogueResponse:
        """
        Generate human-like response based on context
        """
        tone, tone_confidence = self.detect_tone(context.message)
        intents, intent_scores = self.detect_intent(context.message)
        emotional_state = self.extract_emotional_state(context.message)
        
        context.detected_tone = tone
        context.emotional_state = emotional_state
        context.intent = intents[0] if intents else None
        
        acknowledgment = self._select_response(self.dialogue_templates["acknowledgment"])
        
        response_text = await self._craft_response(context, intents, emotional_state)
        follow_up = await self._generate_followup(context, intents)
        
        emotional_resonance = self._calculate_emotional_resonance(context, response_text)
        
        return DialogueResponse(
            text=response_text,
            tone=tone,
            style=context.communication_style,
            emotional_resonance=emotional_resonance,
            follow_up_question=follow_up,
            acknowledgment=acknowledgment,
            personalization_notes={
                "tone_confidence": tone_confidence,
                "detected_intent": intents,
                "emotional_state": emotional_state,
            }
        )
    
    def _select_response(self, templates: List[str]) -> str:
        """Select from response templates"""
        import random
        return random.choice(templates)
    
    async def _craft_response(
        self, 
        context: CommunicationContext, 
        intents: List[str], 
        emotional_state: Dict[str, float]
    ) -> str:
        """Craft personalized response"""
        primary_intent = intents[0] if intents else None
        
        if context.detected_tone == ToneDetection.ANXIOUS or emotional_state.get("anxiety", 0) > 0.5:
            intro = "I can sense this is weighing on you. "
        elif context.detected_tone == ToneDetection.POSITIVE:
            intro = "That's wonderful! "
        elif context.detected_tone == ToneDetection.FRUSTRATED:
            intro = "I can understand your frustration. "
        else:
            intro = ""
        
        if primary_intent == "emotional_support":
            response = f"{intro}Your feelings are completely valid. Let's work through this together."
        elif primary_intent == "seeking_understanding":
            response = f"{intro}That's a great question. Let me break this down for you."
        elif primary_intent == "decision_making":
            response = f"{intro}Let's think through your options carefully."
        elif primary_intent == "problem_solving":
            response = f"{intro}Let's identify what's causing this and find a real solution."
        else:
            response = f"{intro}I'm here to help you with whatever you need."
        
        return response
    
    async def _generate_followup(
        self, 
        context: CommunicationContext, 
        intents: List[str]
    ) -> Optional[str]:
        """Generate natural follow-up question"""
        if not intents:
            return None
        
        primary_intent = intents[0]
        templates = self.dialogue_templates.get("clarifying_questions", [])
        
        if templates:
            question_template = self._select_response(templates)
            return question_template.format(topic="this", adjective="challenging", emotion="concerned")
        
        return None
    
    def _calculate_emotional_resonance(self, context: CommunicationContext, response: str) -> float:
        """
        Calculate how well response resonates emotionally
        1.0 = perfect emotional match
        """
        emotional_alignment = sum(context.emotional_state.values()) / len(context.emotional_state)
        
        has_acknowledgment = any(word in response.lower() for word in 
                                ["understand", "sense", "hear", "appreciate"])
        
        has_validation = any(word in response.lower() for word in 
                            ["valid", "makes sense", "reasonable", "right"])
        
        has_empathy = any(word in response.lower() for word in 
                         ["feel", "care", "here for you", "together"])
        
        resonance = (emotional_alignment * 0.4 + 
                    (0.2 if has_acknowledgment else 0) +
                    (0.2 if has_validation else 0) +
                    (0.2 if has_empathy else 0))
        
        return min(1.0, resonance)
    
    def build_user_communication_profile(self, user_id: str, messages: List[str]) -> Dict[str, Any]:
        """
        Learn user's communication style and preferences
        """
        if not messages:
            return {}
        
        preferred_style = self._infer_communication_style(messages)
        common_tones = self._analyze_tone_patterns(messages)
        preferred_response_length = self._analyze_message_patterns(messages)
        
        profile = {
            "user_id": user_id,
            "preferred_style": preferred_style,
            "common_tones": common_tones,
            "response_length_preference": preferred_response_length,
            "formality_level": self._detect_formality(messages),
            "use_emojis": self._detect_emoji_usage(messages),
            "preferred_depth": self._detect_depth_preference(messages),
        }
        
        self.communication_profiles[user_id] = profile
        return profile
    
    def _infer_communication_style(self, messages: List[str]) -> CommunicationStyle:
        """Infer preferred communication style"""
        text = " ".join(messages).lower()
        
        if any(word in text for word in ["why", "how", "explain", "understand"]):
            return CommunicationStyle.SOCRATIC
        elif any(word in text for word in ["imagine", "create", "idea", "design"]):
            return CommunicationStyle.NARRATIVE
        elif any(word in text for word in ["please", "thank", "care"]):
            return CommunicationStyle.EMPATHETIC
        elif any(word in text for word in ["api", "code", "function", "parameter"]):
            return CommunicationStyle.TECHNICAL
        elif any(word in text for word in ["hi", "hey", "lol", "cool"]):
            return CommunicationStyle.CASUAL
        else:
            return CommunicationStyle.PROFESSIONAL
    
    def _analyze_tone_patterns(self, messages: List[str]) -> Dict[str, float]:
        """Analyze common emotional tones"""
        tone_counts = {}
        for msg in messages:
            tone, _ = self.detect_tone(msg)
            tone_counts[tone.value] = tone_counts.get(tone.value, 0) + 1
        
        total = len(messages)
        return {tone: count / total for tone, count in tone_counts.items()} if total > 0 else {}
    
    def _analyze_message_patterns(self, messages: List[str]) -> str:
        """Analyze preferred message length"""
        avg_length = sum(len(msg.split()) for msg in messages) / len(messages) if messages else 0
        
        if avg_length < 10:
            return "brief"
        elif avg_length < 50:
            return "moderate"
        else:
            return "detailed"
    
    def _detect_formality(self, messages: List[str]) -> str:
        """Detect formality level"""
        text = " ".join(messages).lower()
        formal_words = len([w for w in text.split() if len(w) > 8])
        informal_words = len([w for w in text.split() if w in ["lol", "haha", "cool", "awesome"]])
        
        if informal_words > formal_words:
            return "casual"
        elif formal_words > informal_words:
            return "formal"
        else:
            return "neutral"
    
    def _detect_emoji_usage(self, messages: List[str]) -> bool:
        """Detect if user uses emojis"""
        text = " ".join(messages)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "]+",
            flags=re.UNICODE
        )
        return bool(emoji_pattern.search(text))
    
    def _detect_depth_preference(self, messages: List[str]) -> str:
        """Detect preference for depth of explanation"""
        questions = sum(1 for msg in messages if "?" in msg)
        explanations = sum(1 for msg in messages if any(
            word in msg.lower() for word in ["explain", "understand", "why", "how"]
        ))
        
        if (questions + explanations) / len(messages) > 0.5 if messages else False:
            return "deep"
        else:
            return "surface"


class HumanDialogueOrchestrator:
    """
    Coordinates human-like dialogue across communication engine
    Manages conversation flow and context persistence
    """
    
    def __init__(self):
        self.communication_engine = HumanCommunicationEngine()
        self.active_conversations = {}
        self.user_profiles = {}
    
    async def process_user_message(
        self,
        user_id: str,
        conversation_id: str,
        message: str,
        language: str = "en"
    ) -> DialogueResponse:
        """Process user message and generate human-like response"""
        
        if conversation_id not in self.active_conversations:
            self.active_conversations[conversation_id] = []
        
        context = CommunicationContext(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            previous_messages=self.active_conversations[conversation_id],
            user_language=language
        )
        
        if user_id in self.user_profiles:
            context.communication_style = self.user_profiles[user_id].get(
                "preferred_style", 
                CommunicationStyle.EMPATHETIC
            )
        
        response = await self.communication_engine.generate_response(context)
        
        self.active_conversations[conversation_id].append(message)
        if len(self.active_conversations[conversation_id]) > 50:
            self.active_conversations[conversation_id] = self.active_conversations[conversation_id][-50:]
        
        return response
    
    def learn_user_communication(self, user_id: str, conversation_id: str):
        """Learn user's communication style from conversation"""
        if conversation_id in self.active_conversations:
            messages = self.active_conversations[conversation_id]
            profile = self.communication_engine.build_user_communication_profile(user_id, messages)
            self.user_profiles[user_id] = profile
            return profile
        return None
