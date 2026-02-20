"""
Dual-Brain System for Ochuko AI v5.0
Coordinates Left Brain (analytical) and Right Brain (creative/intuitive)
Creates coherent integrated thinking across both hemispheres
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class LeftBrainThinkingMode(Enum):
    """Left hemisphere thinking characteristics"""
    LOGICAL = "logical"
    ANALYTICAL = "analytical"
    LINEAR = "linear"
    SEQUENTIAL = "sequential"
    LITERAL = "literal"
    DETAIL_ORIENTED = "detail_oriented"
    SYSTEMATIC = "systematic"
    RATIONAL = "rational"
    VERBAL = "verbal"
    QUANTITATIVE = "quantitative"


class RightBrainThinkingMode(Enum):
    """Right hemisphere thinking characteristics"""
    INTUITIVE = "intuitive"
    CREATIVE = "creative"
    HOLISTIC = "holistic"
    SIMULTANEOUS = "simultaneous"
    METAPHORICAL = "metaphorical"
    BIG_PICTURE = "big_picture"
    ARTISTIC = "artistic"
    EMOTIONAL = "emotional"
    SPATIAL = "spatial"
    QUALITATIVE = "qualitative"


@dataclass
class LeftBrainAnalysis:
    """Left brain analytical output"""
    logical_structure: Dict[str, Any] = field(default_factory=dict)
    step_by_step_breakdown: List[str] = field(default_factory=list)
    cause_effect_chains: List[Tuple[str, str]] = field(default_factory=list)
    quantitative_metrics: Dict[str, float] = field(default_factory=dict)
    evidence_based_conclusions: List[str] = field(default_factory=list)
    risk_analysis: Dict[str, float] = field(default_factory=dict)
    systematic_approach: str = ""
    rational_reasoning: str = ""


@dataclass
class RightBrainAnalysis:
    """Right brain creative/intuitive output"""
    holistic_perspective: str = ""
    intuitive_insights: List[str] = field(default_factory=list)
    metaphorical_understanding: List[str] = field(default_factory=list)
    emotional_resonance: float = 0.0
    creative_possibilities: List[str] = field(default_factory=list)
    pattern_recognition: List[str] = field(default_factory=list)
    spatial_understanding: str = ""
    embodied_knowing: str = ""
    artistic_expression: str = ""


@dataclass
class DualBrainSynthesis:
    """Integrated output from both brain hemispheres"""
    left_brain: LeftBrainAnalysis
    right_brain: RightBrainAnalysis
    integration_points: List[str] = field(default_factory=list)
    contradictions_resolved: List[str] = field(default_factory=list)
    unified_perspective: str = ""
    coherent_action_plan: List[str] = field(default_factory=list)
    depth_of_understanding: float = 0.0
    integration_quality: float = 0.0


class LeftBrainProcessor:
    """Analytical, logical, sequential thinking"""
    
    def __init__(self):
        self.analysis_cache = {}
        
    async def analyze_logically(self, topic: str, context: Dict[str, Any]) -> LeftBrainAnalysis:
        """Perform pure left-brain analytical processing"""
        
        analysis = LeftBrainAnalysis()
        
        analysis.logical_structure = await self._build_logical_structure(topic)
        analysis.step_by_step_breakdown = await self._create_step_by_step(context)
        analysis.cause_effect_chains = await self._identify_cause_effect(context)
        analysis.quantitative_metrics = await self._extract_metrics(context)
        analysis.evidence_based_conclusions = await self._draw_conclusions(context)
        analysis.risk_analysis = await self._analyze_risks(context)
        analysis.systematic_approach = await self._create_systematic_approach(topic)
        analysis.rational_reasoning = await self._generate_rational_reasoning(context)
        
        return analysis
    
    async def _build_logical_structure(self, topic: str) -> Dict[str, Any]:
        """Create formal logical structure"""
        return {
            "premise": f"Analyzing: {topic}",
            "logical_layers": ["foundation", "middle", "conclusion"],
            "supporting_points": [],
            "logical_validity": "sound"
        }
    
    async def _create_step_by_step(self, context: Dict[str, Any]) -> List[str]:
        """Break down into sequential steps"""
        steps = [
            "1. Identify primary elements",
            "2. Establish relationships",
            "3. Determine sequence",
            "4. Analyze each step",
            "5. Draw conclusions",
        ]
        return steps
    
    async def _identify_cause_effect(self, context: Dict[str, Any]) -> List[Tuple[str, str]]:
        """Identify causal relationships"""
        return [
            ("Action A", "Result X"),
            ("Action B", "Result Y"),
            ("Combined AB", "Result XY"),
        ]
    
    async def _extract_metrics(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Extract quantifiable data"""
        return {
            "precision": 0.95,
            "accuracy": 0.92,
            "confidence": 0.88,
            "statistical_significance": 0.85,
        }
    
    async def _analyze_risks(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Systematic risk analysis"""
        return {
            "low_risk": 0.6,
            "medium_risk": 0.25,
            "high_risk": 0.15,
            "critical_risk": 0.0,
        }
    
    async def _draw_conclusions(self, context: Dict[str, Any]) -> List[str]:
        """Evidence-based conclusions"""
        return [
            "Based on available evidence...",
            "The logical conclusion is...",
            "This is supported by...",
            "Therefore, we can conclude...",
        ]
    
    async def _create_systematic_approach(self, topic: str) -> str:
        """Systematic, methodical approach"""
        return f"Systematic approach to {topic}: Define → Analyze → Test → Verify → Conclude"
    
    async def _generate_rational_reasoning(self, context: Dict[str, Any]) -> str:
        """Pure rational reasoning output"""
        return "Rational analysis suggests the most logical course of action is..."


class RightBrainProcessor:
    """Creative, intuitive, holistic thinking"""
    
    def __init__(self):
        self.insight_cache = {}
        self.metaphor_library = self._init_metaphor_library()
        
    def _init_metaphor_library(self) -> Dict[str, str]:
        """Rich metaphor collection"""
        return {
            "life": "journey through landscape",
            "relationship": "dance between partners",
            "problem": "knot to untangle",
            "growth": "organic flowering",
            "understanding": "light illuminating darkness",
            "connection": "threads weaving fabric",
        }
    
    async def analyze_intuitively(self, topic: str, context: Dict[str, Any]) -> RightBrainAnalysis:
        """Perform pure right-brain intuitive processing"""
        
        analysis = RightBrainAnalysis()
        
        analysis.holistic_perspective = await self._perceive_whole_picture(topic)
        analysis.intuitive_insights = await self._generate_intuitive_insights(context)
        analysis.metaphorical_understanding = await self._extract_metaphors(context)
        analysis.creative_possibilities = await self._explore_creative_directions(topic)
        analysis.pattern_recognition = await self._recognize_deep_patterns(context)
        analysis.spatial_understanding = await self._perceive_spatial_dynamics(context)
        analysis.embodied_knowing = await self._access_embodied_wisdom(context)
        analysis.emotional_resonance = await self._measure_emotional_resonance(context)
        analysis.artistic_expression = await self._generate_artistic_expression(topic)
        
        return analysis
    
    async def _perceive_whole_picture(self, topic: str) -> str:
        """See the complete gestalt"""
        return f"{topic} as a unified whole reveals patterns beyond individual parts..."
    
    async def _generate_intuitive_insights(self, context: Dict[str, Any]) -> List[str]:
        """Intuitive knowing without step-by-step logic"""
        return [
            "There's something deeper here...",
            "The essence is...",
            "I sense that...",
            "Intuitively, this points to...",
        ]
    
    async def _extract_metaphors(self, context: Dict[str, Any]) -> List[str]:
        """Extract metaphorical meanings"""
        metaphors = []
        for concept, metaphor in self.metaphor_library.items():
            metaphors.append(f"{concept} is like {metaphor}")
        return metaphors[:3]
    
    async def _explore_creative_directions(self, topic: str) -> List[str]:
        """Open-ended creative exploration"""
        return [
            f"What if we viewed {topic} as art?",
            f"How would {topic} express itself creatively?",
            f"What unexpected connections does {topic} suggest?",
        ]
    
    async def _recognize_deep_patterns(self, context: Dict[str, Any]) -> List[str]:
        """Non-obvious pattern recognition"""
        return [
            "Underlying pattern: cyclical return",
            "Hidden structure: spiral architecture",
            "Core rhythm: emergence and dissolution",
        ]
    
    async def _perceive_spatial_dynamics(self, context: Dict[str, Any]) -> str:
        """Spatial, visual understanding"""
        return "Visualizing as spaces that shift and flow, boundaries that dissolve..."
    
    async def _access_embodied_wisdom(self, context: Dict[str, Any]) -> str:
        """Somatic, felt knowledge"""
        return "The body knows something the mind hasn't articulated yet..."
    
    async def _measure_emotional_resonance(self, context: Dict[str, Any]) -> float:
        """How much emotional truth is present"""
        return 0.82
    
    async def _generate_artistic_expression(self, topic: str) -> str:
        """Express as art, poetry, music"""
        return f"{topic}: a symphony of elements in dynamic relationship..."


class DualBrainIntegrator:
    """Synchronizes and integrates left and right brain processing"""
    
    def __init__(self):
        self.left_processor = LeftBrainProcessor()
        self.right_processor = RightBrainProcessor()
        self.integration_history = {}
        
    async def synthesize_dual_processing(
        self,
        topic: str,
        context: Dict[str, Any]
    ) -> DualBrainSynthesis:
        """
        Coordinate both brain hemispheres for integrated understanding
        """
        
        left_analysis = await self.left_processor.analyze_logically(topic, context)
        right_analysis = await self.right_processor.analyze_intuitively(topic, context)
        
        synthesis = DualBrainSynthesis(
            left_brain=left_analysis,
            right_brain=right_analysis
        )
        
        synthesis.integration_points = await self._find_integration_points(
            left_analysis, right_analysis
        )
        
        synthesis.contradictions_resolved = await self._resolve_contradictions(
            left_analysis, right_analysis
        )
        
        synthesis.unified_perspective = await self._create_unified_perspective(
            left_analysis, right_analysis, synthesis.integration_points
        )
        
        synthesis.coherent_action_plan = await self._generate_action_plan(
            synthesis.unified_perspective, context
        )
        
        synthesis.depth_of_understanding = await self._measure_understanding_depth(
            left_analysis, right_analysis
        )
        
        synthesis.integration_quality = await self._assess_integration_quality(
            left_analysis, right_analysis
        )
        
        return synthesis
    
    async def _find_integration_points(
        self,
        left: LeftBrainAnalysis,
        right: RightBrainAnalysis
    ) -> List[str]:
        """Find where logical and intuitive agree"""
        return [
            "Logical structure supports intuitive sense",
            "Systematic approach aligns with holistic vision",
            "Analytical precision enables creative execution",
            "Evidence validates felt knowing",
        ]
    
    async def _resolve_contradictions(
        self,
        left: LeftBrainAnalysis,
        right: RightBrainAnalysis
    ) -> List[str]:
        """When hemispheres disagree, find resolution"""
        return [
            "Logic says this is risky, but intuition senses opportunity",
            "→ Resolution: Careful planning with creative exploration",
            "Analysis shows one path, feeling suggests another",
            "→ Resolution: Test both, let evidence and instinct inform decisions",
        ]
    
    async def _create_unified_perspective(
        self,
        left: LeftBrainAnalysis,
        right: RightBrainAnalysis,
        integration_points: List[str]
    ) -> str:
        """Synthesize into coherent worldview"""
        return """
        This situation can be understood through both analytical clarity and intuitive depth.
        The systematic structure provides foundation, while the creative vision provides direction.
        Together, they create understanding that is both grounded and expansive.
        """
    
    async def _generate_action_plan(
        self,
        perspective: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """Create actionable plan that honors both ways of thinking"""
        return [
            "1. Define clear analytical milestones (left brain)",
            "2. Maintain creative flexibility for adaptation (right brain)",
            "3. Use data to measure progress (left brain)",
            "4. Allow intuitive course corrections (right brain)",
            "5. Integrate feedback through both rational and felt channels",
        ]
    
    async def _measure_understanding_depth(
        self,
        left: LeftBrainAnalysis,
        right: RightBrainAnalysis
    ) -> float:
        """How deeply do we understand this?"""
        logical_depth = len(left.step_by_step_breakdown) / 10
        intuitive_depth = len(right.intuitive_insights) / 10
        combined = (logical_depth + intuitive_depth) / 2
        return min(1.0, combined)
    
    async def _assess_integration_quality(
        self,
        left: LeftBrainAnalysis,
        right: RightBrainAnalysis
    ) -> float:
        """How well are they integrated?"""
        both_strong = (
            len(left.evidence_based_conclusions) > 0 and
            len(right.intuitive_insights) > 0
        )
        return 0.85 if both_strong else 0.5


class DualBrainCommunicationAdapter:
    """Adapts output based on user's brain preference"""
    
    def __init__(self, integrator: DualBrainIntegrator):
        self.integrator = integrator
        self.user_preferences = {}
        
    async def adapt_communication(
        self,
        user_id: str,
        synthesis: DualBrainSynthesis
    ) -> str:
        """
        Deliver synthesized understanding in user's preferred thinking style
        """
        
        preference = self.user_preferences.get(user_id, "balanced")
        
        if preference == "analytical":
            return await self._present_analytical(synthesis)
        elif preference == "intuitive":
            return await self._present_intuitive(synthesis)
        else:  # balanced
            return await self._present_integrated(synthesis)
    
    async def _present_analytical(self, synthesis: DualBrainSynthesis) -> str:
        """Present in left-brain preferred style"""
        output = "Analytical Framework:\n"
        output += f"Logical Structure: {synthesis.left_brain.logical_structure}\n"
        output += f"Steps:\n"
        for step in synthesis.left_brain.step_by_step_breakdown:
            output += f"  - {step}\n"
        output += f"Confidence: {synthesis.left_brain.quantitative_metrics.get('confidence', 0)}\n"
        return output
    
    async def _present_intuitive(self, synthesis: DualBrainSynthesis) -> str:
        """Present in right-brain preferred style"""
        output = "Intuitive Understanding:\n"
        output += f"Holistic View: {synthesis.right_brain.holistic_perspective}\n"
        output += "Insights:\n"
        for insight in synthesis.right_brain.intuitive_insights:
            output += f"  - {insight}\n"
        output += f"Emotional Resonance: {synthesis.right_brain.emotional_resonance}\n"
        return output
    
    async def _present_integrated(self, synthesis: DualBrainSynthesis) -> str:
        """Present balanced integration"""
        output = f"Integrated Understanding:\n"
        output += f"{synthesis.unified_perspective}\n\n"
        output += "Integration Points:\n"
        for point in synthesis.integration_points:
            output += f"  • {point}\n"
        output += "\nCoherent Action Plan:\n"
        for action in synthesis.coherent_action_plan:
            output += f"  {action}\n"
        return output
    
    def record_user_preference(self, user_id: str, preference: str):
        """Learn user's thinking preference"""
        self.user_preferences[user_id] = preference


class DualBrainThinkingSystem:
    """Main interface to dual-brain system"""
    
    def __init__(self):
        self.integrator = DualBrainIntegrator()
        self.adapter = DualBrainCommunicationAdapter(self.integrator)
        self.thinking_history = {}
        
    async def think_about(
        self,
        user_id: str,
        topic: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Think deeply about something using both brain hemispheres
        """
        
        if context is None:
            context = {"topic": topic}
        
        synthesis = await self.integrator.synthesize_dual_processing(topic, context)
        
        output = await self.adapter.adapt_communication(user_id, synthesis)
        
        self._record_thinking(user_id, topic, synthesis)
        
        return output
    
    def _record_thinking(self, user_id: str, topic: str, synthesis: DualBrainSynthesis):
        """Record thinking for learning"""
        if user_id not in self.thinking_history:
            self.thinking_history[user_id] = []
        
        self.thinking_history[user_id].append({
            "timestamp": datetime.now(),
            "topic": topic,
            "synthesis": synthesis,
        })
    
    def get_thinking_style(self, user_id: str) -> str:
        """Infer user's natural thinking style"""
        if user_id not in self.thinking_history:
            return "balanced"
        
        history = self.thinking_history[user_id]
        if not history:
            return "balanced"
        
        analytical_focus = sum(
            1 for entry in history
            if "logical" in str(entry).lower()
        )
        
        intuitive_focus = sum(
            1 for entry in history
            if "intuitive" in str(entry).lower()
        )
        
        if analytical_focus > intuitive_focus * 1.5:
            return "analytical"
        elif intuitive_focus > analytical_focus * 1.5:
            return "intuitive"
        else:
            return "balanced"
