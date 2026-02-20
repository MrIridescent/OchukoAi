"""
Real-Time Deduction Engine for Ochuko AI v5.0
Instantaneous logical inference, pattern recognition, hidden meaning detection
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class DeductionType(Enum):
    """Types of logical deduction"""
    MODUS_PONENS = "modus_ponens"  # If A then B, A is true, therefore B is true
    MODUS_TOLLENS = "modus_tollens"  # If A then B, B is false, therefore A is false
    SYLLOGISM = "syllogism"  # All A are B, C is A, therefore C is B
    CONTRAPOSITIVE = "contrapositive"  # If A then B, therefore if not B then not A
    ABDUCTIVE = "abductive"  # Best explanation inference
    ANALOGICAL = "analogical"  # Pattern matching across domains


class DiscernmentLevel(Enum):
    """Depth of pattern recognition"""
    SURFACE = "surface"  # Obvious patterns
    SUBTLE = "subtle"  # Non-obvious connections
    HIDDEN = "hidden"  # Deeply concealed patterns
    UNCONSCIOUS = "unconscious"  # Patterns person isn't aware of
    SYSTEMIC = "systemic"  # Structural/system-level patterns


@dataclass
class Observation:
    """Single observable fact"""
    statement: str
    evidence_strength: float  # 0-1
    source_reliability: float  # 0-1
    timestamp: datetime = field(default_factory=datetime.now)
    context: Optional[str] = None
    assumptions: List[str] = field(default_factory=list)


@dataclass
class DeductiveConclusion:
    """Result of logical deduction"""
    conclusion: str
    deduction_type: DeductionType
    confidence: float  # 0-1
    supporting_observations: List[str] = field(default_factory=list)
    logical_chain: List[str] = field(default_factory=list)
    potential_fallacies: List[str] = field(default_factory=list)
    alternative_conclusions: List[Tuple[str, float]] = field(default_factory=list)
    requires_additional_evidence: bool = False


@dataclass
class DiscernedPattern:
    """Pattern recognized through discernment"""
    pattern_name: str
    discernment_level: DiscernmentLevel
    confidence: float
    description: str
    examples: List[str] = field(default_factory=list)
    implications: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    hidden_meaning: Optional[str] = None
    underlying_structure: Optional[str] = None


class RealTimeDeductionEngine:
    """Performs instantaneous logical deduction"""
    
    def __init__(self):
        self.logical_rules = self._init_logical_rules()
        self.inference_cache = {}
        
    def _init_logical_rules(self) -> Dict[DeductionType, Dict[str, Any]]:
        """Initialize logical deduction rules"""
        return {
            DeductionType.MODUS_PONENS: {
                "name": "If P then Q; P; therefore Q",
                "validity": 1.0,
                "requires": ["if_then_statement", "antecedent_true"],
            },
            DeductionType.MODUS_TOLLENS: {
                "name": "If P then Q; Q is false; therefore P is false",
                "validity": 1.0,
                "requires": ["if_then_statement", "consequent_false"],
            },
            DeductionType.SYLLOGISM: {
                "name": "All A are B; C is A; therefore C is B",
                "validity": 1.0,
                "requires": ["major_premise", "minor_premise"],
            },
            DeductionType.ANALOGICAL: {
                "name": "A and B share properties; A has property C; therefore B likely has C",
                "validity": 0.7,  # Lower validity, more probabilistic
                "requires": ["similarity_score", "property_match"],
            },
            DeductionType.ABDUCTIVE: {
                "name": "Best explanation from available evidence",
                "validity": 0.8,
                "requires": ["competing_explanations", "evidence_fit"],
            },
        }
    
    async def deduce_from_observations(
        self,
        observations: List[Observation]
    ) -> List[DeductiveConclusion]:
        """Perform logical deduction from observations"""
        
        conclusions = []
        
        for i, obs in enumerate(observations):
            for deduction_type in DeductionType:
                conclusion = await self._apply_deduction(
                    deduction_type, 
                    observations,
                    i
                )
                if conclusion:
                    conclusions.append(conclusion)
        
        return sorted(conclusions, key=lambda x: x.confidence, reverse=True)
    
    async def _apply_deduction(
        self,
        deduction_type: DeductionType,
        observations: List[Observation],
        primary_obs_index: int
    ) -> Optional[DeductiveConclusion]:
        """Apply specific deduction rule"""
        
        if deduction_type == DeductionType.MODUS_PONENS:
            return await self._modus_ponens(observations, primary_obs_index)
        elif deduction_type == DeductionType.MODUS_TOLLENS:
            return await self._modus_tollens(observations, primary_obs_index)
        elif deduction_type == DeductionType.SYLLOGISM:
            return await self._syllogism(observations, primary_obs_index)
        elif deduction_type == DeductionType.ANALOGICAL:
            return await self._analogical(observations, primary_obs_index)
        elif deduction_type == DeductionType.ABDUCTIVE:
            return await self._abductive(observations, primary_obs_index)
        
        return None
    
    async def _modus_ponens(
        self,
        observations: List[Observation],
        index: int
    ) -> Optional[DeductiveConclusion]:
        """If A then B; A is true; therefore B is true"""
        
        obs = observations[index]
        
        if "if" in obs.statement.lower() and "then" in obs.statement.lower():
            conclusion = DeductiveConclusion(
                conclusion="Consequent of the conditional is true",
                deduction_type=DeductionType.MODUS_PONENS,
                confidence=min(1.0, obs.evidence_strength * obs.source_reliability),
                supporting_observations=[obs.statement],
                logical_chain=["If P then Q", "P is true", "Therefore Q is true"],
            )
            return conclusion
        
        return None
    
    async def _modus_tollens(
        self,
        observations: List[Observation],
        index: int
    ) -> Optional[DeductiveConclusion]:
        """If A then B; B is false; therefore A is false"""
        
        obs = observations[index]
        
        if "not" in obs.statement.lower() or "false" in obs.statement.lower():
            conclusion = DeductiveConclusion(
                conclusion="Antecedent of the conditional must be false",
                deduction_type=DeductionType.MODUS_TOLLENS,
                confidence=min(1.0, obs.evidence_strength * obs.source_reliability),
                supporting_observations=[obs.statement],
                logical_chain=["If P then Q", "Q is false", "Therefore P is false"],
            )
            return conclusion
        
        return None
    
    async def _syllogism(
        self,
        observations: List[Observation],
        index: int
    ) -> Optional[DeductiveConclusion]:
        """All A are B; C is A; therefore C is B"""
        
        if len(observations) < 2:
            return None
        
        obs1 = observations[index]
        obs2 = observations[(index + 1) % len(observations)]
        
        conclusion = DeductiveConclusion(
            conclusion=f"Conclusion from {obs1.statement} and {obs2.statement}",
            deduction_type=DeductionType.SYLLOGISM,
            confidence=0.85,
            supporting_observations=[obs1.statement, obs2.statement],
            logical_chain=["Major premise", "Minor premise", "Conclusion"],
        )
        return conclusion
    
    async def _analogical(
        self,
        observations: List[Observation],
        index: int
    ) -> Optional[DeductiveConclusion]:
        """Analogical reasoning across similar cases"""
        
        obs = observations[index]
        
        similar_count = sum(
            1 for other in observations
            if self._calculate_similarity(obs.statement, other.statement) > 0.6
        )
        
        if similar_count > 1:
            conclusion = DeductiveConclusion(
                conclusion=f"Pattern likely holds for similar cases",
                deduction_type=DeductionType.ANALOGICAL,
                confidence=0.65 + (similar_count * 0.05),
                supporting_observations=[o.statement for o in observations[:similar_count]],
            )
            return conclusion
        
        return None
    
    async def _abductive(
        self,
        observations: List[Observation],
        index: int
    ) -> Optional[DeductiveConclusion]:
        """Best explanation from available evidence"""
        
        obs = observations[index]
        
        best_explanation = f"The most likely explanation for '{obs.statement}' is..."
        
        conclusion = DeductiveConclusion(
            conclusion=best_explanation,
            deduction_type=DeductionType.ABDUCTIVE,
            confidence=obs.evidence_strength,
            supporting_observations=[obs.statement],
            alternative_conclusions=[
                ("Alternative 1", 0.3),
                ("Alternative 2", 0.2),
            ],
        )
        return conclusion
    
    def _calculate_similarity(self, statement1: str, statement2: str) -> float:
        """Calculate semantic similarity"""
        words1 = set(statement1.lower().split())
        words2 = set(statement2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0


class PerceptionAndDiscernmentEngine:
    """Perceives hidden patterns and deeper meanings"""
    
    def __init__(self):
        self.pattern_library = self._init_pattern_library()
        self.meaning_extraction = self._init_meaning_extraction()
        
    def _init_pattern_library(self) -> Dict[str, Dict[str, Any]]:
        """Library of recognizable patterns"""
        return {
            "projection": {
                "description": "Attributing own feelings to others",
                "indicators": ["you must feel", "they probably think", "everyone knows"],
                "level": DiscernmentLevel.SUBTLE,
            },
            "rationalization": {
                "description": "Justifying behavior post-hoc with logic",
                "indicators": ["because", "obviously", "clearly", "naturally"],
                "level": DiscernmentLevel.HIDDEN,
            },
            "denial": {
                "description": "Refusing to acknowledge reality",
                "indicators": ["that's not true", "that didn't happen", "impossible"],
                "level": DiscernmentLevel.HIDDEN,
            },
            "power_dynamic": {
                "description": "Subtle power imbalances in relationships",
                "indicators": ["you should", "you need to", "trust me"],
                "level": DiscernmentLevel.SUBTLE,
            },
            "avoidance": {
                "description": "Dodging real issues with distraction",
                "indicators": ["anyway", "off-topic", "changing subject"],
                "level": DiscernmentLevel.SUBTLE,
            },
            "inconsistency": {
                "description": "Contradictions between beliefs and actions",
                "indicators": ["but earlier", "you said", "contradiction"],
                "level": DiscernmentLevel.SURFACE,
            },
        }
    
    def _init_meaning_extraction(self) -> Dict[str, List[str]]:
        """Extract hidden meanings"""
        return {
            "urgency_signals": ["need", "must", "immediately", "now", "urgent"],
            "vulnerability": ["afraid", "scared", "uncertain", "lost", "help"],
            "strength": ["confident", "know", "certain", "powerful", "capable"],
            "disconnection": ["alone", "isolated", "understand", "see", "hear me"],
        }
    
    async def perceive_patterns(self, text: str) -> List[DiscernedPattern]:
        """Perceive hidden patterns in text"""
        
        patterns = []
        text_lower = text.lower()
        
        for pattern_name, pattern_data in self.pattern_library.items():
            indicators = pattern_data.get("indicators", [])
            
            matches = sum(1 for indicator in indicators if indicator in text_lower)
            
            if matches > 0:
                confidence = min(1.0, matches / len(indicators))
                
                pattern = DiscernedPattern(
                    pattern_name=pattern_name,
                    discernment_level=pattern_data.get("level", DiscernmentLevel.SURFACE),
                    confidence=confidence,
                    description=pattern_data.get("description", ""),
                    examples=[],
                )
                patterns.append(pattern)
        
        return sorted(patterns, key=lambda x: x.confidence, reverse=True)
    
    async def extract_hidden_meanings(self, text: str) -> Dict[str, Any]:
        """Extract deeper meanings from text"""
        
        meanings = {
            "urgent_needs": [],
            "vulnerabilities": [],
            "strengths": [],
            "connection_needs": [],
            "underlying_emotions": [],
        }
        
        text_lower = text.lower()
        
        for need_word in self.meaning_extraction["urgency_signals"]:
            if need_word in text_lower:
                meanings["urgent_needs"].append(need_word)
        
        for vuln_word in self.meaning_extraction["vulnerability"]:
            if vuln_word in text_lower:
                meanings["vulnerabilities"].append(vuln_word)
        
        for strength_word in self.meaning_extraction["strength"]:
            if strength_word in text_lower:
                meanings["strengths"].append(strength_word)
        
        for connect_word in self.meaning_extraction["disconnection"]:
            if connect_word in text_lower:
                meanings["connection_needs"].append(connect_word)
        
        return meanings
    
    async def discern_truth_from_context(
        self,
        statements: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Discern what's likely true vs. false based on patterns"""
        
        discernment = {
            "likely_true": [],
            "likely_false": [],
            "uncertain": [],
            "hidden_assumptions": [],
            "contradictions": [],
        }
        
        for i, statement in enumerate(statements):
            for j, other in enumerate(statements):
                if i != j:
                    if self._are_contradictory(statement, other):
                        discernment["contradictions"].append((statement, other))
        
        return discernment
    
    def _are_contradictory(self, statement1: str, statement2: str) -> bool:
        """Check if statements contradict"""
        
        if "but" in statement2.lower():
            return True
        
        opposites = [
            ("yes", "no"),
            ("true", "false"),
            ("always", "never"),
            ("everyone", "no one"),
        ]
        
        s1_lower = statement1.lower()
        s2_lower = statement2.lower()
        
        for word1, word2 in opposites:
            if word1 in s1_lower and word2 in s2_lower:
                return True
        
        return False


class InstantPerceptionSystem:
    """Real-time immediate perception"""
    
    def __init__(self):
        self.deduction_engine = RealTimeDeductionEngine()
        self.discernment_engine = PerceptionAndDiscernmentEngine()
        
    async def perceive_instantly(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Instant perception of entire situation"""
        
        text = input_data.get("text", "")
        context = input_data.get("context", {})
        
        observations = [
            Observation(statement=text, evidence_strength=0.8, source_reliability=0.9)
        ]
        
        deductions = await self.deduction_engine.deduce_from_observations(observations)
        
        patterns = await self.discernment_engine.perceive_patterns(text)
        
        hidden_meanings = await self.discernment_engine.extract_hidden_meanings(text)
        
        perception = {
            "immediate_observations": text,
            "logical_deductions": [
                {
                    "conclusion": d.conclusion,
                    "type": d.deduction_type.value,
                    "confidence": d.confidence,
                }
                for d in deductions[:3]
            ],
            "discerned_patterns": [
                {
                    "pattern": p.pattern_name,
                    "level": p.discernment_level.value,
                    "confidence": p.confidence,
                }
                for p in patterns
            ],
            "hidden_meanings": hidden_meanings,
            "what_is_not_said": await self._perceive_absence(text),
        }
        
        return perception
    
    async def _perceive_absence(self, text: str) -> List[str]:
        """Perceive what's conspicuously missing"""
        
        absences = []
        
        if "feel" not in text.lower():
            absences.append("No mention of feelings")
        
        if "because" not in text.lower() and "why" not in text.lower():
            absences.append("No reasoning or explanation")
        
        if "we" not in text.lower() and "you" not in text.lower():
            absences.append("Disconnected language (no relational pronouns)")
        
        return absences
