"""
Voice Emotion Detection System for Ochuko AI v5.0
Analyzes tone, pitch, cadence, rhythm, volume for emotional state
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class VoiceCharacteristic(Enum):
    """Voice characteristics to analyze"""
    PITCH = "pitch"
    VOLUME = "volume"
    SPEED = "speed"
    RHYTHM = "rhythm"
    TIMBRE = "timbre"
    BREATHINESS = "breathiness"
    PAUSE_PATTERNS = "pause_patterns"
    VOCAL_FRY = "vocal_fry"
    HARSHNESS = "harshness"
    SMOOTHNESS = "smoothness"


class VoiceEmotionState(Enum):
    """Emotional states detectable from voice"""
    CONFIDENT = "confident"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    SAD = "sad"
    HAPPY = "happy"
    SURPRISED = "surprised"
    DISGUSTED = "disgusted"
    FEARFUL = "fearful"
    CONTEMPTUOUS = "contemptuous"
    NEUTRAL = "neutral"
    STRESSED = "stressed"
    CALM = "calm"
    EXCITED = "excited"
    BORED = "bored"
    PASSIONATE = "passionate"


@dataclass
class VoiceAcousticProfile:
    """Acoustic measurements"""
    fundamental_frequency: float = 0.0  # Hz
    pitch_variability: float = 0.0
    speaking_rate: float = 0.0  # words per minute
    volume: float = 0.0  # dB
    volume_variability: float = 0.0
    jitter: float = 0.0  # pitch instability
    shimmer: float = 0.0  # amplitude variability
    harmonic_to_noise: float = 0.0
    spectral_centroid: float = 0.0  # brightness
    mean_pause_duration: float = 0.0  # seconds
    speech_to_pause_ratio: float = 0.0


@dataclass
class VoiceEmotionalAnalysis:
    """Complete voice emotion analysis"""
    detected_emotion: VoiceEmotionState = VoiceEmotionState.NEUTRAL
    emotion_confidence: float = 0.0
    secondary_emotions: List[VoiceEmotionState] = field(default_factory=list)
    emotion_trajectory: List[Tuple[float, VoiceEmotionState]] = field(default_factory=list)
    acoustic_profile: VoiceAcousticProfile = field(default_factory=VoiceAcousticProfile)
    voice_characteristics: Dict[str, float] = field(default_factory=dict)
    stress_level: float = 0.0
    authenticity_score: float = 0.0
    arousal_level: float = 0.0  # 0=low to 1=high
    valence_level: float = 0.0  # 0=negative to 1=positive
    dominance_level: float = 0.0  # 0=submissive to 1=dominant
    vulnerability_indicators: List[str] = field(default_factory=list)
    strength_indicators: List[str] = field(default_factory=list)


class VoiceAcousticAnalyzer:
    """Analyzes acoustic properties of voice"""
    
    def __init__(self):
        self.emotion_acoustic_mappings = self._init_emotion_mappings()
        
    def _init_emotion_mappings(self) -> Dict[VoiceEmotionState, Dict[str, tuple]]:
        """Map emotions to acoustic characteristics"""
        return {
            VoiceEmotionState.CONFIDENT: {
                "pitch": (120, 160),  # Hz range
                "volume": (70, 80),   # dB range
                "speed": (150, 180),  # wpm
                "pitch_variability": (0.3, 0.6),
                "pause_pattern": "minimal",
            },
            VoiceEmotionState.ANXIOUS: {
                "pitch": (160, 200),
                "volume": (60, 75),
                "speed": (180, 220),
                "pitch_variability": (0.8, 1.0),
                "pause_pattern": "frequent_short",
            },
            VoiceEmotionState.ANGRY: {
                "pitch": (150, 250),
                "volume": (75, 95),
                "speed": (140, 180),
                "pitch_variability": (0.7, 1.0),
                "pause_pattern": "emphatic",
            },
            VoiceEmotionState.SAD: {
                "pitch": (80, 120),
                "volume": (50, 65),
                "speed": (100, 140),
                "pitch_variability": (0.2, 0.4),
                "pause_pattern": "long_silence",
            },
            VoiceEmotionState.HAPPY: {
                "pitch": (130, 180),
                "volume": (65, 80),
                "speed": (140, 180),
                "pitch_variability": (0.4, 0.7),
                "pause_pattern": "rhythmic",
            },
            VoiceEmotionState.CALM: {
                "pitch": (100, 140),
                "volume": (60, 70),
                "speed": (120, 150),
                "pitch_variability": (0.2, 0.5),
                "pause_pattern": "measured",
            },
            VoiceEmotionState.EXCITED: {
                "pitch": (160, 220),
                "volume": (75, 85),
                "speed": (180, 250),
                "pitch_variability": (0.6, 0.9),
                "pause_pattern": "minimal_fast",
            },
            VoiceEmotionState.STRESSED: {
                "pitch": (150, 200),
                "volume": (65, 80),
                "speed": (170, 220),
                "pitch_variability": (0.7, 1.0),
                "pause_pattern": "irregular",
            },
        }
    
    async def analyze_acoustic_profile(
        self,
        voice_data: Dict[str, float]
    ) -> VoiceAcousticProfile:
        """Analyze acoustic properties"""
        
        profile = VoiceAcousticProfile(
            fundamental_frequency=voice_data.get("pitch", 0.0),
            pitch_variability=voice_data.get("pitch_variability", 0.0),
            speaking_rate=voice_data.get("speed", 0.0),
            volume=voice_data.get("volume", 0.0),
            volume_variability=voice_data.get("volume_variability", 0.0),
            jitter=voice_data.get("jitter", 0.0),
            shimmer=voice_data.get("shimmer", 0.0),
            harmonic_to_noise=voice_data.get("harmonic_to_noise", 0.0),
            spectral_centroid=voice_data.get("spectral_centroid", 0.0),
            mean_pause_duration=voice_data.get("pause_duration", 0.0),
            speech_to_pause_ratio=voice_data.get("speech_pause_ratio", 0.0),
        )
        
        return profile
    
    async def detect_emotion_from_acoustics(
        self,
        profile: VoiceAcousticProfile
    ) -> Tuple[VoiceEmotionState, float, List[VoiceEmotionState]]:
        """Detect emotion based on acoustic profile"""
        
        emotion_scores = {}
        
        for emotion, mappings in self.emotion_acoustic_mappings.items():
            score = 0.0
            num_matches = 0
            
            if "pitch" in mappings and profile.fundamental_frequency > 0:
                pitch_range = mappings["pitch"]
                if pitch_range[0] <= profile.fundamental_frequency <= pitch_range[1]:
                    score += 0.3
                num_matches += 1
            
            if "volume" in mappings and profile.volume > 0:
                vol_range = mappings["volume"]
                if vol_range[0] <= profile.volume <= vol_range[1]:
                    score += 0.3
                num_matches += 1
            
            if "speed" in mappings and profile.speaking_rate > 0:
                speed_range = mappings["speed"]
                if speed_range[0] <= profile.speaking_rate <= speed_range[1]:
                    score += 0.2
                num_matches += 1
            
            if "pitch_variability" in mappings:
                var_range = mappings["pitch_variability"]
                if var_range[0] <= profile.pitch_variability <= var_range[1]:
                    score += 0.2
                num_matches += 1
            
            if num_matches > 0:
                emotion_scores[emotion] = score / num_matches
        
        if not emotion_scores:
            return VoiceEmotionState.NEUTRAL, 0.5, []
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[primary_emotion]
        
        secondary = sorted(
            [(e, s) for e, s in emotion_scores.items() if e != primary_emotion],
            key=lambda x: x[1],
            reverse=True
        )
        secondary_emotions = [e for e, _ in secondary[:3]]
        
        return primary_emotion, confidence, secondary_emotions


class VoiceCharacteristicDetector:
    """Detects specific voice characteristics"""
    
    def __init__(self):
        self.characteristic_indicators = self._init_indicators()
        
    def _init_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Indicators for each characteristic"""
        return {
            "breathiness": {
                "indicators": ["breathy", "airy", "weak"],
                "emotional_association": ["vulnerability", "softness", "intimacy"],
            },
            "harshness": {
                "indicators": ["tense", "strained", "rough"],
                "emotional_association": ["anger", "stress", "determination"],
            },
            "smoothness": {
                "indicators": ["fluid", "warm", "connected"],
                "emotional_association": ["confidence", "calm", "authenticity"],
            },
            "tremor": {
                "indicators": ["shaky", "wavering", "unstable"],
                "emotional_association": ["fear", "sadness", "uncertainty"],
            },
            "resonance": {
                "indicators": ["deep", "grounded", "full"],
                "emotional_association": ["confidence", "power", "presence"],
            },
        }
    
    async def analyze_voice_characteristics(
        self,
        voice_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Detect voice characteristics"""
        
        characteristics = {}
        
        for characteristic, mapping in self.characteristic_indicators.items():
            score = 0.0
            for indicator in mapping["indicators"]:
                if indicator in str(voice_data).lower():
                    score += 0.2
            characteristics[characteristic] = min(1.0, score)
        
        return characteristics


class VoiceEmotionDetectionSystem:
    """Complete voice emotion detection"""
    
    def __init__(self):
        self.acoustic_analyzer = VoiceAcousticAnalyzer()
        self.characteristic_detector = VoiceCharacteristicDetector()
        self.analysis_history = {}
        
    async def detect_voice_emotion(
        self,
        user_id: str,
        voice_data: Dict[str, float]
    ) -> VoiceEmotionalAnalysis:
        """
        Complete voice emotion analysis
        
        voice_data should contain:
        - pitch: fundamental frequency in Hz
        - volume: loudness in dB
        - speed: speaking rate in words per minute
        - pitch_variability: 0-1
        - pauses: pause patterns
        """
        
        acoustic_profile = await self.acoustic_analyzer.analyze_acoustic_profile(voice_data)
        
        primary_emotion, confidence, secondary = (
            await self.acoustic_analyzer.detect_emotion_from_acoustics(acoustic_profile)
        )
        
        voice_chars = await self.characteristic_detector.analyze_voice_characteristics(voice_data)
        
        analysis = VoiceEmotionalAnalysis(
            detected_emotion=primary_emotion,
            emotion_confidence=confidence,
            secondary_emotions=secondary,
            acoustic_profile=acoustic_profile,
            voice_characteristics=voice_chars,
        )
        
        analysis.stress_level = self._calculate_stress_level(acoustic_profile)
        analysis.authenticity_score = self._estimate_authenticity(analysis)
        analysis.arousal_level = self._calculate_arousal(acoustic_profile)
        analysis.valence_level = self._calculate_valence(primary_emotion)
        analysis.dominance_level = self._calculate_dominance(acoustic_profile)
        
        analysis.vulnerability_indicators = self._detect_vulnerability(analysis)
        analysis.strength_indicators = self._detect_strength(analysis)
        
        self._record_analysis(user_id, analysis)
        
        return analysis
    
    def _calculate_stress_level(self, profile: VoiceAcousticProfile) -> float:
        """0 = calm, 1 = highly stressed"""
        stress = 0.0
        
        if profile.pitch_variability > 0.7:
            stress += 0.3
        
        if profile.speaking_rate > 200:
            stress += 0.2
        
        if profile.jitter > 0.02:
            stress += 0.2
        
        if profile.mean_pause_duration < 0.3:
            stress += 0.3
        
        return min(1.0, stress)
    
    def _estimate_authenticity(self, analysis: VoiceEmotionalAnalysis) -> float:
        """How genuine/authentic is the emotional expression?"""
        authenticity = 0.0
        
        if analysis.acoustic_profile.harmonic_to_noise > 0.8:
            authenticity += 0.3
        
        if analysis.voice_characteristics.get("smoothness", 0) > 0.6:
            authenticity += 0.3
        
        if analysis.arousal_level == analysis.valence_level:
            authenticity += 0.2
        
        if analysis.emotion_confidence > 0.7:
            authenticity += 0.2
        
        return min(1.0, authenticity)
    
    def _calculate_arousal(self, profile: VoiceAcousticProfile) -> float:
        """0 = low arousal (sleepy), 1 = high arousal (excited)"""
        arousal = 0.0
        
        if profile.fundamental_frequency > 150:
            arousal += 0.4
        
        if profile.speaking_rate > 180:
            arousal += 0.3
        
        if profile.volume > 70:
            arousal += 0.3
        
        return min(1.0, arousal)
    
    def _calculate_valence(self, emotion: VoiceEmotionState) -> float:
        """0 = negative, 1 = positive"""
        valence_map = {
            VoiceEmotionState.HAPPY: 0.9,
            VoiceEmotionState.EXCITED: 0.85,
            VoiceEmotionState.CALM: 0.7,
            VoiceEmotionState.CONFIDENT: 0.75,
            VoiceEmotionState.NEUTRAL: 0.5,
            VoiceEmotionState.STRESSED: 0.3,
            VoiceEmotionState.SAD: 0.2,
            VoiceEmotionState.ANGRY: 0.15,
            VoiceEmotionState.FEARFUL: 0.25,
            VoiceEmotionState.ANXIOUS: 0.3,
        }
        return valence_map.get(emotion, 0.5)
    
    def _calculate_dominance(self, profile: VoiceAcousticProfile) -> float:
        """0 = submissive, 1 = dominant"""
        dominance = 0.0
        
        if profile.volume > 75:
            dominance += 0.4
        
        if profile.fundamental_frequency > 150:
            dominance += 0.2
        
        if profile.mean_pause_duration < 0.5:
            dominance += 0.2
        
        if profile.pitch_variability < 0.4:
            dominance += 0.2
        
        return min(1.0, dominance)
    
    def _detect_vulnerability(self, analysis: VoiceEmotionalAnalysis) -> List[str]:
        """Indicators of vulnerability in voice"""
        indicators = []
        
        if analysis.stress_level > 0.7:
            indicators.append("High stress response")
        
        if analysis.acoustic_profile.jitter > 0.03:
            indicators.append("Voice tremor")
        
        if analysis.acoustic_profile.volume < 65:
            indicators.append("Soft, quiet voice")
        
        if analysis.detected_emotion in [
            VoiceEmotionState.SAD,
            VoiceEmotionState.FEARFUL,
            VoiceEmotionState.ANXIOUS
        ]:
            indicators.append(f"Emotional state: {analysis.detected_emotion.value}")
        
        if analysis.voice_characteristics.get("breathiness", 0) > 0.6:
            indicators.append("Breathy quality")
        
        return indicators
    
    def _detect_strength(self, analysis: VoiceEmotionalAnalysis) -> List[str]:
        """Indicators of strength/confidence in voice"""
        indicators = []
        
        if analysis.emotion_confidence > 0.8:
            indicators.append("Clear emotional expression")
        
        if analysis.acoustic_profile.volume > 75:
            indicators.append("Strong, projected voice")
        
        if analysis.dominance_level > 0.7:
            indicators.append("Dominant tone")
        
        if analysis.detected_emotion in [
            VoiceEmotionState.CONFIDENT,
            VoiceEmotionState.ANGRY,
            VoiceEmotionState.EXCITED
        ]:
            indicators.append(f"Strong emotion: {analysis.detected_emotion.value}")
        
        if analysis.voice_characteristics.get("resonance", 0) > 0.6:
            indicators.append("Resonant quality")
        
        return indicators
    
    def _record_analysis(self, user_id: str, analysis: VoiceEmotionalAnalysis):
        """Record for learning"""
        if user_id not in self.analysis_history:
            self.analysis_history[user_id] = []
        
        self.analysis_history[user_id].append({
            "timestamp": datetime.now(),
            "analysis": analysis,
        })
    
    def get_voice_emotional_trajectory(self, user_id: str, minutes: int = 30) -> List[Dict]:
        """Get emotional trajectory from voice"""
        if user_id not in self.analysis_history:
            return []
        
        history = self.analysis_history[user_id]
        return history[-10:]  # Return last 10 analyses
