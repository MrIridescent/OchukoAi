"""
Facial Emotion Recognition System for Ochuko AI v5.0
Detects emotions from facial expressions, micro-expressions, and dynamics
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class FacialAction(Enum):
    """Facial Action Coding System (FACS) actions"""
    INNER_BROW_RAISE = "AU1"
    OUTER_BROW_RAISE = "AU2"
    BROW_LOWER = "AU4"
    UPPER_LID_RAISE = "AU5"
    CHEEK_RAISE = "AU6"
    LID_TIGHTEN = "AU7"
    LIP_CORNER_PULLER = "AU12"
    LIP_CORNER_DEPRESSOR = "AU15"
    CHIN_RAISE = "AU17"
    LIP_PUCKER = "AU18"
    MOUTH_STRETCH = "AU27"


class FacialEmotion(Enum):
    """Basic emotions detectable from face"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SURPRISED = "surprised"
    DISGUSTED = "disgusted"
    NEUTRAL = "neutral"
    CONTEMPTUOUS = "contemptuous"


@dataclass
class FacialFeatures:
    """Facial feature measurements"""
    eye_openness: float = 0.5  # 0-1
    brow_position: float = 0.5  # 0-1 (lower to higher)
    mouth_openness: float = 0.5  # 0-1
    mouth_corners: float = 0.5  # 0-1 (down to up)
    cheek_height: float = 0.5  # 0-1
    nose_wrinkle: float = 0.5  # 0-1
    eye_gaze_direction: str = "forward"  # forward, left, right, up, down
    head_pose: Dict[str, float] = field(default_factory=lambda: {"pitch": 0, "yaw": 0, "roll": 0})
    skin_color: str = "normal"  # normal, flushed, pale
    micro_expressions: List[str] = field(default_factory=list)


@dataclass
class FacialEmotionAnalysis:
    """Complete facial emotion analysis"""
    primary_emotion: FacialEmotion = FacialEmotion.NEUTRAL
    emotion_confidence: float = 0.0
    secondary_emotions: List[Tuple[FacialEmotion, float]] = field(default_factory=list)
    facial_actions: Dict[str, float] = field(default_factory=dict)
    facial_features: FacialFeatures = field(default_factory=FacialFeatures)
    micro_expressions: List[Tuple[str, float]] = field(default_factory=list)
    emotional_authenticity: float = 0.0
    emotional_intensity: float = 0.0
    temporal_dynamics: Dict[str, float] = field(default_factory=dict)
    eye_contact_quality: float = 0.0
    expression_symmetry: float = 0.0
    dynamic_expression_changes: List[Tuple[float, FacialEmotion]] = field(default_factory=list)


class FacialActionDetector:
    """Detects facial action units"""
    
    def __init__(self):
        self.emotion_action_mappings = self._init_action_mappings()
        
    def _init_action_mappings(self) -> Dict[FacialEmotion, Dict[str, float]]:
        """Map emotions to facial actions"""
        return {
            FacialEmotion.HAPPY: {
                "AU12": 0.9,  # Lip corner puller
                "AU6": 0.8,   # Cheek raise
                "AU1": 0.7,   # Inner brow raise
                "AU5": 0.6,   # Upper lid raise
            },
            FacialEmotion.SAD: {
                "AU1": 0.8,   # Inner brow raise
                "AU4": 0.7,   # Brow lower
                "AU15": 0.8,  # Lip corner depressor
                "AU17": 0.7,  # Chin raise
            },
            FacialEmotion.ANGRY: {
                "AU4": 0.9,   # Brow lower
                "AU5": 0.8,   # Upper lid raise
                "AU7": 0.8,   # Lid tighten
                "AU23": 0.7,  # Lip tighten
            },
            FacialEmotion.FEARFUL: {
                "AU1": 0.8,   # Inner brow raise
                "AU2": 0.9,   # Outer brow raise
                "AU5": 0.9,   # Upper lid raise
                "AU20": 0.8,  # Lip stretch
            },
            FacialEmotion.SURPRISED: {
                "AU1": 0.8,   # Inner brow raise
                "AU2": 0.9,   # Outer brow raise
                "AU5": 0.9,   # Upper lid raise
                "AU26": 0.8,  # Jaw drop
            },
            FacialEmotion.DISGUSTED: {
                "AU9": 0.8,   # Nose wrinkle
                "AU15": 0.8,  # Lip corner depressor
                "AU16": 0.7,  # Lower lip depressor
            },
            FacialEmotion.CONTEMPTUOUS: {
                "AU12": 0.7,  # Asymmetric lip corner puller
                "AU14": 0.7,  # Dimpler
                "AU17": 0.6,  # Chin raise
            },
            FacialEmotion.NEUTRAL: {
                "AU1": 0.0,
                "AU4": 0.0,
                "AU6": 0.0,
                "AU12": 0.0,
            },
        }
    
    async def detect_facial_actions(
        self,
        facial_features: FacialFeatures
    ) -> Dict[str, float]:
        """Detect which facial actions are present"""
        
        actions = {}
        
        if facial_features.brow_position > 0.6:
            actions["AU1"] = facial_features.brow_position
        
        if facial_features.mouth_corners > 0.6:
            actions["AU12"] = facial_features.mouth_corners
        
        if facial_features.cheek_height > 0.6:
            actions["AU6"] = facial_features.cheek_height
        
        if facial_features.nose_wrinkle > 0.6:
            actions["AU9"] = facial_features.nose_wrinkle
        
        if facial_features.mouth_openness > 0.7:
            actions["AU27"] = facial_features.mouth_openness
        
        return actions
    
    async def match_emotion_from_actions(
        self,
        detected_actions: Dict[str, float]
    ) -> Tuple[FacialEmotion, float, List[Tuple[FacialEmotion, float]]]:
        """Match detected actions to emotions"""
        
        emotion_scores = {}
        
        for emotion, action_mapping in self.emotion_action_mappings.items():
            score = 0.0
            matches = 0
            
            for action, importance in action_mapping.items():
                if action in detected_actions:
                    action_value = detected_actions[action]
                    if action_value > 0.3:
                        score += action_value * importance
                        matches += 1
            
            if matches > 0:
                emotion_scores[emotion] = score / matches
        
        if not emotion_scores:
            return FacialEmotion.NEUTRAL, 0.5, []
        
        primary = max(emotion_scores, key=emotion_scores.get)
        confidence = min(1.0, emotion_scores[primary])
        
        secondary = sorted(
            [(e, s) for e, s in emotion_scores.items() if e != primary],
            key=lambda x: x[1],
            reverse=True
        )
        
        return primary, confidence, secondary[:3]


class MicroExpressionDetector:
    """Detects micro-expressions (fleeting, involuntary emotions)"""
    
    def __init__(self):
        self.micro_expression_indicators = self._init_indicators()
        
    def _init_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Indicators for micro-expressions"""
        return {
            "concealed_happiness": {
                "duration": (1, 2),  # frames
                "intensity_change": (0.2, 0.4),
                "indicates": "Genuine pleasure despite neutral mask",
            },
            "concealed_anger": {
                "duration": (1, 2),
                "intensity_change": (0.3, 0.5),
                "indicates": "Hidden anger or frustration",
            },
            "concealed_fear": {
                "duration": (1, 2),
                "intensity_change": (0.2, 0.4),
                "indicates": "Concealed worry or concern",
            },
            "concealed_sadness": {
                "duration": (1, 2),
                "intensity_change": (0.2, 0.3),
                "indicates": "Hidden grief or hurt",
            },
            "contempt": {
                "duration": (1, 5),
                "intensity_change": (0.2, 0.3),
                "indicates": "Dismissal, superiority feeling",
            },
            "surprise": {
                "duration": (1, 10),
                "intensity_change": (0.4, 0.8),
                "indicates": "Genuine surprise",
            },
        }
    
    async def detect_micro_expressions(
        self,
        expression_sequence: List[FacialFeatures]
    ) -> List[Tuple[str, float]]:
        """Detect fleeting expressions"""
        
        detected = []
        
        if len(expression_sequence) < 2:
            return detected
        
        for i in range(len(expression_sequence) - 1):
            current = expression_sequence[i]
            next_expr = expression_sequence[i + 1]
            
            intensity_change = abs(
                (next_expr.mouth_corners - current.mouth_corners) * 0.5 +
                (next_expr.brow_position - current.brow_position) * 0.5
            )
            
            if 0.2 < intensity_change < 0.5:
                detected.append(("micro_expression_detected", intensity_change))
        
        return detected


class FacialEmotionRecognitionSystem:
    """Complete facial emotion recognition"""
    
    def __init__(self):
        self.action_detector = FacialActionDetector()
        self.micro_detector = MicroExpressionDetector()
        self.analysis_history = {}
        
    async def recognize_face_emotion(
        self,
        user_id: str,
        facial_features: FacialFeatures,
        temporal_context: Optional[List[FacialFeatures]] = None
    ) -> FacialEmotionAnalysis:
        """
        Recognize emotion from facial features
        """
        
        facial_actions = await self.action_detector.detect_facial_actions(facial_features)
        
        primary_emotion, confidence, secondary = (
            await self.action_detector.match_emotion_from_actions(facial_actions)
        )
        
        analysis = FacialEmotionAnalysis(
            primary_emotion=primary_emotion,
            emotion_confidence=confidence,
            secondary_emotions=secondary,
            facial_actions=facial_actions,
            facial_features=facial_features,
        )
        
        if temporal_context and len(temporal_context) > 1:
            analysis.micro_expressions = await self.micro_detector.detect_micro_expressions(
                temporal_context
            )
        
        analysis.emotional_authenticity = self._assess_authenticity(analysis)
        analysis.emotional_intensity = self._calculate_intensity(facial_features)
        analysis.eye_contact_quality = self._assess_eye_contact(facial_features)
        analysis.expression_symmetry = self._assess_symmetry(facial_features)
        
        self._record_analysis(user_id, analysis)
        
        return analysis
    
    def _assess_authenticity(self, analysis: FacialEmotionAnalysis) -> float:
        """Is the emotion genuine (Duchenne) or fake?"""
        authenticity = 0.0
        
        if "AU6" in analysis.facial_actions and "AU12" in analysis.facial_actions:
            authenticity += 0.4
        
        if analysis.micro_expressions:
            authenticity += 0.3
        
        if analysis.expression_symmetry > 0.8:
            authenticity -= 0.2
        
        if len(analysis.micro_expressions) == 0:
            authenticity += 0.3
        
        return min(1.0, max(0.0, authenticity))
    
    def _calculate_intensity(self, features: FacialFeatures) -> float:
        """How intense is the emotional expression?"""
        intensity = 0.0
        
        intensity += features.eye_openness * 0.2
        intensity += features.mouth_openness * 0.2
        intensity += abs(features.mouth_corners - 0.5) * 0.3
        intensity += abs(features.brow_position - 0.5) * 0.3
        
        return min(1.0, intensity)
    
    def _assess_eye_contact(self, features: FacialFeatures) -> float:
        """Quality of eye contact"""
        if features.eye_gaze_direction == "forward":
            return 0.9
        elif features.eye_gaze_direction in ["left", "right"]:
            return 0.6
        else:
            return 0.3
    
    def _assess_symmetry(self, features: FacialFeatures) -> float:
        """Is expression symmetrical (neutral) or asymmetrical (genuine)?"""
        asymmetry = abs(features.mouth_corners - 0.5)
        return 1.0 - min(asymmetry, 0.5) / 0.5
    
    def _record_analysis(self, user_id: str, analysis: FacialEmotionAnalysis):
        """Record for learning"""
        if user_id not in self.analysis_history:
            self.analysis_history[user_id] = []
        
        self.analysis_history[user_id].append({
            "timestamp": datetime.now(),
            "analysis": analysis,
        })
    
    def get_face_emotional_trajectory(self, user_id: str) -> List[Dict]:
        """Get emotional trajectory from facial expressions"""
        if user_id not in self.analysis_history:
            return []
        
        return self.analysis_history[user_id][-20:]


class FullBodyExpressionAnalyzer:
    """Analyzes full body emotional expression (posture, gestures)"""
    
    def __init__(self):
        self.posture_indicators = self._init_posture_indicators()
        
    def _init_posture_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Posture meaning"""
        return {
            "open": {
                "arms": "extended or relaxed",
                "chest": "exposed",
                "emotions": ["confidence", "happiness", "openness"],
            },
            "closed": {
                "arms": "crossed or held",
                "chest": "protected",
                "emotions": ["defensiveness", "sadness", "insecurity"],
            },
            "tense": {
                "muscles": "contracted",
                "posture": "rigid",
                "emotions": ["stress", "anger", "fear"],
            },
            "relaxed": {
                "muscles": "loose",
                "posture": "natural",
                "emotions": ["calm", "confidence", "ease"],
            },
            "forward": {
                "lean": "toward other",
                "indicates": ["interest", "engagement", "openness"],
            },
            "backward": {
                "lean": "away from other",
                "indicates": ["withdrawal", "disinterest", "fear"],
            },
        }
    
    async def analyze_body_expression(self, body_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze whole body expression"""
        
        expression_scores = {}
        
        for posture_type, indicators in self.posture_indicators.items():
            score = 0.0
            
            if posture_type in str(body_data).lower():
                score += 0.5
            
            for key, value in indicators.items():
                if value in str(body_data).lower():
                    score += 0.25
            
            expression_scores[posture_type] = min(1.0, score)
        
        return expression_scores
