"""
Real-Time Visualization Engine for Ochuko AI v5.0
Displays emotional states, cognitive processes, and system understanding
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class VisualizationType(Enum):
    """Types of visualizations"""
    EMOTION_SPECTRUM = "emotion_spectrum"
    THINKING_MAP = "thinking_map"
    ENERGY_DYNAMICS = "energy_dynamics"
    COGNITIVE_STATE = "cognitive_state"
    GROUP_DYNAMICS = "group_dynamics"
    UNDERSTANDING_DEPTH = "understanding_depth"
    NEURAL_MAP = "neural_map"
    INFORMATION_FLOW = "information_flow"


@dataclass
class EmotionVisualization:
    """Visual representation of emotional state"""
    primary_emotion: str
    intensity: float  # 0-1
    secondary_emotions: Dict[str, float] = field(default_factory=dict)
    arousal_level: float = 0.5
    valence_level: float = 0.5
    dominance_level: float = 0.5
    emotional_signature: str = ""  # ASCII art representation
    color_representation: str = ""  # Color code
    animation_state: str = "steady"  # steady, growing, fading, oscillating


@dataclass
class ThinkingMapVisualization:
    """Visualization of thinking process"""
    main_concept: str
    connected_concepts: Dict[str, float] = field(default_factory=dict)
    logical_branches: List[List[str]] = field(default_factory=list)
    intuitive_threads: List[str] = field(default_factory=list)
    integration_points: List[str] = field(default_factory=list)
    depth_indicator: float = 0.5
    coherence_score: float = 0.5


@dataclass
class EnergyDynamicsVisualization:
    """Energy and momentum visualization"""
    current_energy_level: float  # 0-1
    energy_direction: str  # rising, steady, falling
    momentum_vectors: Dict[str, float] = field(default_factory=dict)
    resistance_points: List[str] = field(default_factory=list)
    catalytic_elements: List[str] = field(default_factory=list)
    overall_trajectory: str = "stable"


@dataclass
class CognitiveStateVisualization:
    """Visualization of cognitive/processing state"""
    processing_speed: float  # 0-1
    mental_clarity: float  # 0-1
    cognitive_load: float  # 0-1
    focus_quality: float  # 0-1
    insight_frequency: str = "low"  # low, medium, high
    stream_of_thought: List[str] = field(default_factory=list)
    cognitive_patterns: Dict[str, int] = field(default_factory=dict)


class EmotionVisualizer:
    """Creates emotion visualizations"""
    
    def __init__(self):
        self.emotion_colors = self._init_emotion_colors()
        self.emotion_symbols = self._init_emotion_symbols()
        
    def _init_emotion_colors(self) -> Dict[str, str]:
        """Color mapping for emotions"""
        return {
            "joy": "🟡",
            "sadness": "🔵",
            "anger": "🔴",
            "fear": "🟣",
            "surprise": "⚪",
            "disgust": "🟢",
            "trust": "💚",
            "anticipation": "🟠",
            "anxiety": "🟣",
            "calm": "🔵",
            "excitement": "🔴",
            "love": "❤️",
            "neutral": "⚫",
        }
    
    def _init_emotion_symbols(self) -> Dict[str, str]:
        """ASCII symbols for emotions"""
        return {
            "joy": "(^_^)",
            "sadness": "T_T",
            "anger": "(╯°□°)╯︵ ┻━┻",
            "fear": "(>_<)",
            "surprise": "(o_o)",
            "disgust": "(╯︵╰,)",
            "calm": "( ´ ▽ ` )",
            "love": "(´♡ω♡`)",
        }
    
    async def visualize_emotion(
        self,
        emotion: str,
        intensity: float,
        secondary_emotions: Optional[Dict[str, float]] = None
    ) -> EmotionVisualization:
        """Create emotion visualization"""
        
        viz = EmotionVisualization(
            primary_emotion=emotion,
            intensity=intensity,
            secondary_emotions=secondary_emotions or {},
        )
        
        viz.color_representation = self.emotion_colors.get(emotion, "⚪")
        viz.emotional_signature = self.emotion_symbols.get(emotion, "o_o")
        
        viz.arousal_level = await self._calculate_arousal(emotion, intensity)
        viz.valence_level = await self._calculate_valence(emotion)
        viz.dominance_level = await self._calculate_dominance(emotion)
        
        viz.animation_state = await self._determine_animation(intensity)
        
        return viz
    
    async def _calculate_arousal(self, emotion: str, intensity: float) -> float:
        """Calculate arousal level"""
        arousal_map = {
            "joy": 0.8,
            "excitement": 0.9,
            "anger": 0.85,
            "fear": 0.8,
            "calm": 0.2,
            "sadness": 0.3,
        }
        return arousal_map.get(emotion, 0.5) * intensity
    
    async def _calculate_valence(self, emotion: str) -> float:
        """0 = negative, 1 = positive"""
        valence_map = {
            "joy": 0.9,
            "love": 0.95,
            "excitement": 0.85,
            "trust": 0.8,
            "neutral": 0.5,
            "anticipation": 0.6,
            "fear": 0.2,
            "sadness": 0.15,
            "anger": 0.1,
            "disgust": 0.05,
        }
        return valence_map.get(emotion, 0.5)
    
    async def _calculate_dominance(self, emotion: str) -> float:
        """0 = submissive, 1 = dominant"""
        dominance_map = {
            "anger": 0.9,
            "joy": 0.75,
            "confidence": 0.85,
            "fear": 0.1,
            "sadness": 0.15,
            "neutral": 0.5,
        }
        return dominance_map.get(emotion, 0.5)
    
    async def _determine_animation(self, intensity: float) -> str:
        """Determine animation style"""
        if intensity > 0.8:
            return "oscillating"
        elif intensity > 0.6:
            return "growing"
        elif intensity < 0.3:
            return "fading"
        else:
            return "steady"
    
    async def render_emotion_ascii(self, visualization: EmotionVisualization) -> str:
        """Render ASCII emotion display"""
        
        output = "\n"
        output += "╔════ EMOTIONAL STATE ════╗\n"
        output += f"║ {visualization.color_representation} {visualization.primary_emotion.upper():20} ║\n"
        output += f"║ Intensity: {'█' * int(visualization.intensity * 10)}{'░' * (10 - int(visualization.intensity * 10))} ║\n"
        output += f"║ {visualization.emotional_signature:21} ║\n"
        output += "╚════════════════════════╝\n"
        
        if visualization.secondary_emotions:
            output += "\nSecondary Emotions:\n"
            for emotion, intensity in visualization.secondary_emotions.items():
                bar = '█' * int(intensity * 10) + '░' * (10 - int(intensity * 10))
                output += f"  {emotion:15} {bar}\n"
        
        output += f"\nArousal: {'█' * int(visualization.arousal_level * 10)}{'░' * (10 - int(visualization.arousal_level * 10))}\n"
        output += f"Valence: {'█' * int(visualization.valence_level * 10)}{'░' * (10 - int(visualization.valence_level * 10))}\n"
        output += f"Dominance: {'█' * int(visualization.dominance_level * 10)}{'░' * (10 - int(visualization.dominance_level * 10))}\n"
        
        return output


class ThinkingMapVisualizer:
    """Visualizes thinking processes"""
    
    async def visualize_thinking_map(
        self,
        central_topic: str,
        related_concepts: Dict[str, float],
        branches: Optional[List[List[str]]] = None
    ) -> ThinkingMapVisualization:
        """Create thinking map visualization"""
        
        viz = ThinkingMapVisualization(
            main_concept=central_topic,
            connected_concepts=related_concepts,
            logical_branches=branches or []
        )
        
        viz.depth_indicator = min(1.0, len(related_concepts) / 15)
        viz.coherence_score = await self._calculate_coherence(related_concepts)
        
        return viz
    
    async def _calculate_coherence(self, concepts: Dict[str, float]) -> float:
        """How well integrated are the concepts?"""
        if not concepts:
            return 0.0
        
        avg_strength = sum(concepts.values()) / len(concepts)
        return min(1.0, avg_strength)
    
    async def render_thinking_map_ascii(self, visualization: ThinkingMapVisualization) -> str:
        """Render ASCII thinking map"""
        
        output = "\n"
        output += "╔════ THINKING MAP ════╗\n"
        output += f"║ Core: {visualization.main_concept:15} ║\n"
        output += "╚════════════════════╝\n\n"
        
        output += "Connected Concepts:\n"
        for concept, strength in sorted(
            visualization.connected_concepts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:8]:
            connection = "—●" + "—" * int(strength * 8) + "→"
            output += f"  {connection} {concept} ({strength:.1%})\n"
        
        if visualization.logical_branches:
            output += "\nLogical Branches:\n"
            for branch in visualization.logical_branches[:3]:
                output += f"  {' → '.join(branch)}\n"
        
        output += f"\nDepth: {'█' * int(visualization.depth_indicator * 10)}{'░' * (10 - int(visualization.depth_indicator * 10))}\n"
        output += f"Coherence: {'█' * int(visualization.coherence_score * 10)}{'░' * (10 - int(visualization.coherence_score * 10))}\n"
        
        return output


class CognitiveStateVisualizer:
    """Visualizes cognitive state"""
    
    async def visualize_cognitive_state(
        self,
        processing_speed: float,
        clarity: float,
        load: float,
        focus: float,
        stream_of_thought: Optional[List[str]] = None
    ) -> CognitiveStateVisualization:
        """Create cognitive state visualization"""
        
        viz = CognitiveStateVisualization(
            processing_speed=processing_speed,
            mental_clarity=clarity,
            cognitive_load=load,
            focus_quality=focus,
            stream_of_thought=stream_of_thought or []
        )
        
        viz.insight_frequency = await self._determine_insight_frequency(clarity, focus)
        
        return viz
    
    async def _determine_insight_frequency(self, clarity: float, focus: float) -> str:
        """How often are insights occurring?"""
        combined = (clarity + focus) / 2
        if combined > 0.7:
            return "high"
        elif combined > 0.4:
            return "medium"
        else:
            return "low"
    
    async def render_cognitive_state_ascii(self, visualization: CognitiveStateVisualization) -> str:
        """Render ASCII cognitive state"""
        
        output = "\n"
        output += "╔════ COGNITIVE STATE ════╗\n"
        output += f"║ Speed:   {'█' * int(visualization.processing_speed * 8)}{'░' * (8 - int(visualization.processing_speed * 8))} ║\n"
        output += f"║ Clarity: {'█' * int(visualization.mental_clarity * 8)}{'░' * (8 - int(visualization.mental_clarity * 8))} ║\n"
        output += f"║ Load:    {'█' * int(visualization.cognitive_load * 8)}{'░' * (8 - int(visualization.cognitive_load * 8))} ║\n"
        output += f"║ Focus:   {'█' * int(visualization.focus_quality * 8)}{'░' * (8 - int(visualization.focus_quality * 8))} ║\n"
        output += f"║ Insights: {visualization.insight_frequency.upper():10} ║\n"
        output += "╚════════════════════════╝\n"
        
        if visualization.stream_of_thought:
            output += "\nStream of Thought:\n"
            for i, thought in enumerate(visualization.stream_of_thought[:5]):
                output += f"  {i+1}. {thought}\n"
        
        return output


class RealTimeVisualizationEngine:
    """Main visualization engine"""
    
    def __init__(self):
        self.emotion_visualizer = EmotionVisualizer()
        self.thinking_visualizer = ThinkingMapVisualizer()
        self.cognitive_visualizer = CognitiveStateVisualizer()
        self.visualization_cache = {}
        
    async def render_complete_state(
        self,
        emotion: str,
        emotion_intensity: float,
        secondary_emotions: Dict[str, float],
        thinking_topic: str,
        related_concepts: Dict[str, float],
        cognitive_state: Dict[str, float]
    ) -> str:
        """Render complete real-time visualization"""
        
        emotion_viz = await self.emotion_visualizer.visualize_emotion(
            emotion, emotion_intensity, secondary_emotions
        )
        emotion_render = await self.emotion_visualizer.render_emotion_ascii(emotion_viz)
        
        thinking_viz = await self.thinking_visualizer.visualize_thinking_map(
            thinking_topic, related_concepts
        )
        thinking_render = await self.thinking_visualizer.render_thinking_map_ascii(thinking_viz)
        
        cognitive_viz = await self.cognitive_visualizer.visualize_cognitive_state(
            cognitive_state.get("processing_speed", 0.5),
            cognitive_state.get("clarity", 0.5),
            cognitive_state.get("load", 0.5),
            cognitive_state.get("focus", 0.5)
        )
        cognitive_render = await self.cognitive_visualizer.render_cognitive_state_ascii(cognitive_viz)
        
        output = "\n"
        output += "═" * 50 + "\n"
        output += "     REAL-TIME COGNITIVE-EMOTIONAL STATE\n"
        output += "═" * 50 + "\n"
        
        output += emotion_render
        output += thinking_render
        output += cognitive_render
        
        output += "\n" + "═" * 50 + "\n"
        
        return output
    
    async def create_summary_display(
        self,
        user_id: str,
        primary_metrics: Dict[str, float]
    ) -> str:
        """Create summary display for dashboard"""
        
        output = f"\n📊 USER: {user_id}\n"
        output += "─" * 40 + "\n"
        
        for metric, value in primary_metrics.items():
            bar = "█" * int(value * 20) + "░" * (20 - int(value * 20))
            output += f"{metric:20} [{bar}] {value:.1%}\n"
        
        return output
