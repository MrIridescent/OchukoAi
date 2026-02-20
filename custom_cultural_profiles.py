"""
Custom Cultural Profiles Manager for Ochuko AI v5.0
Users define their own cultural context and communication norms
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class CultureDimension(Enum):
    """Cultural dimensions (based on Hofstede, Trompenaars, etc.)"""
    POWER_DISTANCE = "power_distance"
    INDIVIDUALISM_COLLECTIVISM = "individualism_collectivism"
    UNCERTAINTY_AVOIDANCE = "uncertainty_avoidance"
    MASCULINITY_FEMININITY = "masculinity_femininity"
    TIME_ORIENTATION = "time_orientation"
    INDULGENCE_RESTRAINT = "indulgence_restraint"
    DIRECTNESS_INDIRECTNESS = "directness_indirectness"
    CONTEXT_LEVEL = "context_level"
    EMOTIONAL_EXPRESSIVENESS = "emotional_expressiveness"
    SPACE_ORIENTATION = "space_orientation"
    AUTHORITY_RESPECT = "authority_respect"
    HARMONY_CONFRONTATION = "harmony_confrontation"


class ValueSystem(Enum):
    """Value systems"""
    COLLECTIVIST = "collectivist"
    INDIVIDUALIST = "individualist"
    EGALITARIAN = "egalitarian"
    HIERARCHICAL = "hierarchical"
    COMMUNAL = "communal"
    MARKET_BASED = "market_based"
    HONOR_BASED = "honor_based"
    DIGNITY_BASED = "dignity_based"
    RIGHTS_BASED = "rights_based"


@dataclass
class CulturalValue:
    """A specific cultural value"""
    name: str
    importance: float  # 0-1
    description: str
    how_it_affects_communication: str
    rituals_or_expressions: List[str] = field(default_factory=list)


@dataclass
class CommunicationNorm:
    """Communication expectation in this culture"""
    context: str = ""  # formal, casual, family, professional, etc.
    greeting_style: str = ""
    directness_level: str = "moderate"  # very_direct, direct, moderate, indirect, very_indirect
    emotional_expression: str = "moderate"  # reserved, moderate, expressive, very_expressive
    silence_meaning: str = ""
    personal_space: str = "45-120cm"  # cm distance
    eye_contact: str = "appropriate"  # required, appropriate, avoided
    appropriate_topics: List[str] = field(default_factory=list)
    taboo_topics: List[str] = field(default_factory=list)
    time_orientation: str = "monochronic"  # monochronic, polychronic
    decision_making_style: str = "individual"  # individual, consensus, hierarchical


@dataclass
class CustomCulturalProfile:
    """User-defined cultural profile"""
    user_id: str
    profile_name: str
    created_date: datetime = field(default_factory=datetime.now)
    cultural_dimensions: Dict[CultureDimension, float] = field(default_factory=dict)
    value_systems: List[ValueSystem] = field(default_factory=list)
    core_values: List[CulturalValue] = field(default_factory=list)
    communication_norms: Dict[str, CommunicationNorm] = field(default_factory=dict)
    taboos: List[str] = field(default_factory=list)
    sacred_practices: List[str] = field(default_factory=list)
    family_structure: str = field(default="")
    age_respect_level: float = 0.5
    gender_role_expectations: Dict[str, str] = field(default_factory=dict)
    conflict_resolution_style: str = field(default="")
    concept_of_time: str = field(default="")
    spiritual_orientation: str = field(default="")
    celebration_traditions: List[str] = field(default_factory=list)
    food_customs: List[str] = field(default_factory=list)
    clothing_customs: List[str] = field(default_factory=list)
    greeting_customs: List[str] = field(default_factory=list)
    mourning_customs: List[str] = field(default_factory=list)


class CulturalProfileBuilder:
    """Guides users in creating their cultural profile"""
    
    def __init__(self):
        self.dimension_descriptions = self._init_dimension_descriptions()
        self.value_system_descriptions = self._init_value_descriptions()
        
    def _init_dimension_descriptions(self) -> Dict[CultureDimension, str]:
        """Descriptions of cultural dimensions"""
        return {
            CultureDimension.POWER_DISTANCE: "How much hierarchy and inequality is acceptable?",
            CultureDimension.INDIVIDUALISM_COLLECTIVISM: "Are personal or group needs more important?",
            CultureDimension.UNCERTAINTY_AVOIDANCE: "How comfortable with unpredictability and ambiguity?",
            CultureDimension.MASCULINITY_FEMININITY: "Achievement-focused or relationship-focused?",
            CultureDimension.TIME_ORIENTATION: "Focus on past, present, or future?",
            CultureDimension.INDULGENCE_RESTRAINT: "Gratification or self-control?",
            CultureDimension.DIRECTNESS_INDIRECTNESS: "Blunt or tactful communication?",
            CultureDimension.CONTEXT_LEVEL: "Low context (explicit) or high context (implicit)?",
            CultureDimension.EMOTIONAL_EXPRESSIVENESS: "Reserved or expressive emotions?",
            CultureDimension.SPACE_ORIENTATION: "Personal space preferences?",
            CultureDimension.AUTHORITY_RESPECT: "Respect for authority and age?",
            CultureDimension.HARMONY_CONFRONTATION: "Seek harmony or address conflict directly?",
        }
    
    def _init_value_descriptions(self) -> Dict[ValueSystem, str]:
        """Descriptions of value systems"""
        return {
            ValueSystem.COLLECTIVIST: "Group harmony and family loyalty valued above individual achievement",
            ValueSystem.INDIVIDUALIST: "Personal autonomy and self-actualization valued above collective harmony",
            ValueSystem.EGALITARIAN: "Equality and fairness in all relationships",
            ValueSystem.HIERARCHICAL: "Natural order and proper ranks respected",
            ValueSystem.COMMUNAL: "Sharing and interdependence emphasized",
            ValueSystem.MARKET_BASED: "Economic exchange and competition as social basis",
            ValueSystem.HONOR_BASED: "Family/group reputation and shame/honor as core values",
            ValueSystem.DIGNITY_BASED: "Individual worth and respect as foundation",
            ValueSystem.RIGHTS_BASED: "Universal rights and individual entitlements",
        }
    
    async def create_profile_interactively(
        self,
        user_id: str,
        profile_name: str,
        responses: Dict[str, Any]
    ) -> CustomCulturalProfile:
        """Create profile from user responses"""
        
        profile = CustomCulturalProfile(
            user_id=user_id,
            profile_name=profile_name
        )
        
        profile.cultural_dimensions = await self._process_dimensions(responses)
        profile.value_systems = await self._process_values(responses)
        profile.core_values = await self._process_core_values(responses)
        profile.communication_norms = await self._process_communication_norms(responses)
        profile.taboos = responses.get("taboos", [])
        profile.sacred_practices = responses.get("sacred_practices", [])
        profile.family_structure = responses.get("family_structure", "")
        profile.conflict_resolution_style = responses.get("conflict_resolution", "")
        profile.concept_of_time = responses.get("time_concept", "")
        profile.spiritual_orientation = responses.get("spiritual_orientation", "")
        profile.celebration_traditions = responses.get("celebrations", [])
        profile.food_customs = responses.get("food_customs", [])
        profile.clothing_customs = responses.get("clothing_customs", [])
        profile.greeting_customs = responses.get("greeting_customs", [])
        profile.mourning_customs = responses.get("mourning_customs", [])
        
        return profile
    
    async def _process_dimensions(self, responses: Dict) -> Dict[CultureDimension, float]:
        """Process dimension responses"""
        dimensions = {}
        
        for dimension in CultureDimension:
            value = responses.get(dimension.value, 0.5)
            dimensions[dimension] = min(1.0, max(0.0, value))
        
        return dimensions
    
    async def _process_values(self, responses: Dict) -> List[ValueSystem]:
        """Process value system selections"""
        values = []
        
        selected = responses.get("value_systems", [])
        for value_name in selected:
            try:
                values.append(ValueSystem[value_name.upper()])
            except KeyError:
                pass
        
        return values
    
    async def _process_core_values(self, responses: Dict) -> List[CulturalValue]:
        """Process core values"""
        core_values = []
        
        values_data = responses.get("core_values", [])
        for value_data in values_data:
            cv = CulturalValue(
                name=value_data.get("name", ""),
                importance=value_data.get("importance", 0.5),
                description=value_data.get("description", ""),
                how_it_affects_communication=value_data.get("communication_impact", ""),
                rituals_or_expressions=value_data.get("rituals", [])
            )
            core_values.append(cv)
        
        return core_values
    
    async def _process_communication_norms(self, responses: Dict) -> Dict[str, CommunicationNorm]:
        """Process communication norms"""
        norms = {}
        
        contexts = responses.get("communication_contexts", {})
        for context, data in contexts.items():
            norm = CommunicationNorm(
                context=context,
                greeting_style=data.get("greeting", ""),
                directness_level=data.get("directness", "moderate"),
                emotional_expression=data.get("emotion_expression", "moderate"),
                silence_meaning=data.get("silence_meaning", ""),
                personal_space=data.get("personal_space", "45-120 cm"),
                eye_contact=data.get("eye_contact", "appropriate"),
                appropriate_topics=data.get("appropriate_topics", []),
                taboo_topics=data.get("taboo_topics", []),
                time_orientation=data.get("time_orientation", "monochronic"),
                decision_making_style=data.get("decision_style", "")
            )
            norms[context] = norm
        
        return norms


class CulturalProfileManager:
    """Manages user cultural profiles"""
    
    def __init__(self):
        self.builder = CulturalProfileBuilder()
        self.profiles = {}
        self.profile_history = {}
        
    async def create_new_profile(
        self,
        user_id: str,
        profile_name: str,
        responses: Dict[str, Any]
    ) -> CustomCulturalProfile:
        """Create new cultural profile"""
        
        profile = await self.builder.create_profile_interactively(
            user_id, profile_name, responses
        )
        
        profile_key = f"{user_id}:{profile_name}"
        self.profiles[profile_key] = profile
        
        if user_id not in self.profile_history:
            self.profile_history[user_id] = []
        self.profile_history[user_id].append(profile)
        
        return profile
    
    def get_profile(self, user_id: str, profile_name: str) -> Optional[CustomCulturalProfile]:
        """Get a specific profile"""
        profile_key = f"{user_id}:{profile_name}"
        return self.profiles.get(profile_key)
    
    def get_all_profiles(self, user_id: str) -> List[CustomCulturalProfile]:
        """Get all profiles for user"""
        return self.profile_history.get(user_id, [])
    
    async def get_communication_recommendations(
        self,
        profile: CustomCulturalProfile,
        context: str
    ) -> Dict[str, Any]:
        """Get communication recommendations based on profile"""
        
        norm = profile.communication_norms.get(context)
        
        if not norm:
            norm = profile.communication_norms.get("general", None)
        
        recommendations = {
            "greeting": norm.greeting_style if norm else "respectful salutation",
            "directness": norm.directness_level if norm else "moderate",
            "emotional_expression": norm.emotional_expression if norm else "moderate",
            "personal_space": norm.personal_space if norm else "standard",
            "eye_contact": norm.eye_contact if norm else "appropriate",
            "topics_to_embrace": norm.appropriate_topics if norm else [],
            "topics_to_avoid": norm.taboo_topics if norm else [],
            "time_orientation": norm.time_orientation if norm else "monochronic",
            "avoid_these_completely": profile.taboos,
            "honor_these_practices": profile.sacred_practices,
        }
        
        return recommendations
    
    async def detect_communication_style_match(
        self,
        profile: CustomCulturalProfile,
        interaction_style: Dict[str, Any]
    ) -> float:
        """How well does an interaction style match the profile?"""
        
        match_score = 0.0
        
        if interaction_style.get("directness") == profile.communication_norms.get(
            "general", CustomCulturalProfile("", "").communication_norms.get(
                "general", CommunicationNorm(context="general")
            )
        ).directness_level:
            match_score += 0.3
        
        if interaction_style.get("emotional_expression") == profile.communication_norms.get(
            "general", CustomCulturalProfile("", "").communication_norms.get(
                "general", CommunicationNorm(context="general")
            )
        ).emotional_expression:
            match_score += 0.3
        
        value_alignment = sum(
            1 for vs in profile.value_systems
            if vs.value in str(interaction_style.get("values", []))
        ) / max(1, len(profile.value_systems))
        match_score += value_alignment * 0.4
        
        return min(1.0, match_score)
    
    async def get_adaptation_suggestions(
        self,
        profile: CustomCulturalProfile,
        current_interaction: Dict[str, Any]
    ) -> List[str]:
        """Get suggestions for adapting communication"""
        
        suggestions = []
        
        for value in profile.core_values:
            if value.importance > 0.7:
                suggestions.append(f"Honor: {value.name}")
        
        general_norm = profile.communication_norms.get("general")
        if general_norm and general_norm.directness_level == "indirect":
            suggestions.append("Use indirect, tactful language")
        
        if any("respect" in str(s).lower() for s in profile.sacred_practices):
            suggestions.append("Show respect for established order")
        
        if profile.conflict_resolution_style == "harmony-focused":
            suggestions.append("Seek harmonious resolution over winning")
        
        return suggestions[:5]
