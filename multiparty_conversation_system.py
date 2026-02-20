"""
Multi-Party Conversation System for Ochuko AI v5.0
Handles group dynamics, conversation flow, and collective intelligence
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class ParticipantRole(Enum):
    """Roles in group conversation"""
    LEADER = "leader"
    FACILITATOR = "facilitator"
    CONTRIBUTOR = "contributor"
    LISTENER = "listener"
    CHALLENGER = "challenger"
    SUPPORTER = "supporter"
    MEDIATOR = "mediator"
    OBSERVER = "observer"


class GroupDynamicPattern(Enum):
    """Patterns in group interaction"""
    COLLABORATIVE = "collaborative"
    COMPETITIVE = "competitive"
    HIERARCHICAL = "hierarchical"
    EGALITARIAN = "egalitarian"
    COALITION = "coalition"
    FRAGMENTED = "fragmented"
    UNIFIED = "unified"
    POLARIZED = "polarized"


@dataclass
class Participant:
    """Individual in group conversation"""
    user_id: str
    name: str
    role: ParticipantRole = ParticipantRole.CONTRIBUTOR
    emotional_state: str = "neutral"
    contribution_count: int = 0
    speaking_time: float = 0.0  # seconds
    engagement_level: float = 0.5
    influence_score: float = 0.5
    alignment_with_group: float = 0.5
    recent_messages: List[str] = field(default_factory=list)
    micro_expressions: List[str] = field(default_factory=list)


@dataclass
class ConversationTurn:
    """Individual message in conversation"""
    participant_id: str
    timestamp: datetime
    message: str
    emotion_expressed: str
    intent: str
    response_to: Optional[str] = None
    received_reactions: Dict[str, int] = field(default_factory=dict)
    impact_score: float = 0.0


@dataclass
class GroupDynamics:
    """Analysis of group interaction patterns"""
    conversation_id: str
    participants: Dict[str, Participant] = field(default_factory=dict)
    conversation_turns: List[ConversationTurn] = field(default_factory=list)
    dominant_pattern: GroupDynamicPattern = GroupDynamicPattern.COLLABORATIVE
    psychological_safety: float = 0.5
    participation_balance: float = 0.5
    idea_diversity: float = 0.5
    conflict_level: float = 0.0
    alignment_level: float = 0.5
    collective_intelligence: float = 0.5
    power_distribution: Dict[str, float] = field(default_factory=dict)
    subgroups: List[List[str]] = field(default_factory=list)
    unspoken_tensions: List[str] = field(default_factory=list)


class ParticipantAnalyzer:
    """Analyzes individual participants in groups"""
    
    def __init__(self):
        self.role_indicators = self._init_role_indicators()
        
    def _init_role_indicators(self) -> Dict[ParticipantRole, List[str]]:
        """Indicators of different roles"""
        return {
            ParticipantRole.LEADER: ["lead", "suggest", "direction", "let's", "should"],
            ParticipantRole.FACILITATOR: ["what do you think", "everyone", "include", "balance"],
            ParticipantRole.CONTRIBUTOR: ["idea", "think", "perspective", "suggest"],
            ParticipantRole.LISTENER: ["makes sense", "agree", "right", "yeah"],
            ParticipantRole.CHALLENGER: ["but", "disagree", "what about", "consider"],
            ParticipantRole.SUPPORTER: ["support", "agree", "great point", "exactly"],
            ParticipantRole.MEDIATOR: ["both", "understand", "perspective", "bridge"],
        }
    
    async def infer_role(self, participant: Participant) -> ParticipantRole:
        """Infer role from behavior"""
        
        messages_text = " ".join(participant.recent_messages).lower()
        role_scores = {}
        
        for role, indicators in self.role_indicators.items():
            score = sum(1 for indicator in indicators if indicator in messages_text)
            role_scores[role] = score
        
        if not any(role_scores.values()):
            return ParticipantRole.CONTRIBUTOR
        
        return max(role_scores, key=role_scores.get)
    
    async def assess_engagement(self, participant: Participant) -> float:
        """How engaged is participant?"""
        
        engagement = 0.0
        
        engagement += min(participant.contribution_count / 10, 1.0) * 0.4
        engagement += min(participant.speaking_time / 600, 1.0) * 0.3
        
        if len(participant.recent_messages) > 0:
            engagement += 0.3
        
        return min(1.0, engagement)
    
    async def assess_influence(self, participant: Participant, all_responses: List[str]) -> float:
        """How much influence does participant have?"""
        
        mention_count = sum(
            1 for response in all_responses
            if participant.name.lower() in response.lower() or 
               f"@{participant.user_id}" in response
        )
        
        influence = min(mention_count / 10, 1.0) * 0.4
        influence += min(participant.contribution_count / 20, 1.0) * 0.6
        
        return min(1.0, influence)


class GroupDynamicsAnalyzer:
    """Analyzes group-level patterns"""
    
    def __init__(self):
        self.participant_analyzer = ParticipantAnalyzer()
        
    async def analyze_group_dynamics(
        self,
        conversation: GroupDynamics
    ) -> GroupDynamics:
        """Complete group dynamics analysis"""
        
        for participant in conversation.participants.values():
            participant.role = await self.participant_analyzer.infer_role(participant)
            participant.engagement_level = await self.participant_analyzer.assess_engagement(participant)
        
        conversation.dominant_pattern = await self._detect_pattern(conversation)
        conversation.psychological_safety = await self._assess_psychological_safety(conversation)
        conversation.participation_balance = await self._assess_participation_balance(conversation)
        conversation.idea_diversity = await self._assess_idea_diversity(conversation)
        conversation.conflict_level = await self._assess_conflict_level(conversation)
        conversation.alignment_level = await self._assess_alignment_level(conversation)
        conversation.collective_intelligence = await self._assess_collective_intelligence(conversation)
        conversation.power_distribution = await self._analyze_power_distribution(conversation)
        conversation.subgroups = await self._identify_subgroups(conversation)
        conversation.unspoken_tensions = await self._detect_tensions(conversation)
        
        return conversation
    
    async def _detect_pattern(self, conversation: GroupDynamics) -> GroupDynamicPattern:
        """Detect overall pattern"""
        
        collaborative_indicators = ["agree", "build on", "support", "together"]
        competitive_indicators = ["but", "disagree", "instead", "versus"]
        
        turns_text = " ".join([turn.message for turn in conversation.conversation_turns]).lower()
        
        collab_count = sum(1 for indicator in collaborative_indicators if indicator in turns_text)
        comp_count = sum(1 for indicator in competitive_indicators if indicator in turns_text)
        
        if collab_count > comp_count * 2:
            return GroupDynamicPattern.COLLABORATIVE
        elif comp_count > collab_count:
            return GroupDynamicPattern.COMPETITIVE
        else:
            return GroupDynamicPattern.EGALITARIAN
    
    async def _assess_psychological_safety(self, conversation: GroupDynamics) -> float:
        """Do people feel safe expressing divergent views?"""
        
        safety = 0.0
        
        if conversation.dominant_pattern in [
            GroupDynamicPattern.COLLABORATIVE,
            GroupDynamicPattern.EGALITARIAN
        ]:
            safety += 0.6
        
        if len(conversation.unspoken_tensions) == 0:
            safety += 0.4
        else:
            safety -= len(conversation.unspoken_tensions) * 0.1
        
        return min(1.0, max(0.0, safety))
    
    async def _assess_participation_balance(self, conversation: GroupDynamics) -> float:
        """Are people contributing equally?"""
        
        if len(conversation.participants) == 0:
            return 0.5
        
        contributions = [p.contribution_count for p in conversation.participants.values()]
        
        if not contributions or sum(contributions) == 0:
            return 0.0
        
        avg = sum(contributions) / len(contributions)
        variance = sum((c - avg) ** 2 for c in contributions) / len(contributions)
        std_dev = variance ** 0.5
        
        if avg == 0:
            return 0.0
        
        imbalance = std_dev / avg
        balance = 1.0 - min(imbalance / 2, 1.0)
        
        return max(0.0, balance)
    
    async def _assess_idea_diversity(self, conversation: GroupDynamics) -> float:
        """How diverse are the ideas?"""
        
        if len(conversation.conversation_turns) == 0:
            return 0.0
        
        intents = [turn.intent for turn in conversation.conversation_turns]
        unique_intents = len(set(intents))
        
        diversity = min(unique_intents / 10, 1.0)
        
        return diversity
    
    async def _assess_conflict_level(self, conversation: GroupDynamics) -> float:
        """How much conflict or disagreement?"""
        
        conflict_words = ["disagree", "but", "however", "versus", "against", "problem"]
        
        turns_text = " ".join([turn.message for turn in conversation.conversation_turns]).lower()
        
        conflict_count = sum(1 for word in conflict_words if word in turns_text)
        
        conflict = min(conflict_count / 10, 1.0)
        
        return conflict
    
    async def _assess_alignment_level(self, conversation: GroupDynamics) -> float:
        """How aligned is the group?"""
        
        if len(conversation.participants) == 0:
            return 0.5
        
        alignment_scores = [
            p.alignment_with_group for p in conversation.participants.values()
        ]
        
        avg_alignment = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.5
        
        return avg_alignment
    
    async def _assess_collective_intelligence(self, conversation: GroupDynamics) -> float:
        """Is the group producing better ideas together?"""
        
        diversity = await self._assess_idea_diversity(conversation)
        safety = await self._assess_psychological_safety(conversation)
        balance = await self._assess_participation_balance(conversation)
        
        collective_intelligence = (diversity * 0.3 + safety * 0.4 + balance * 0.3)
        
        return collective_intelligence
    
    async def _analyze_power_distribution(
        self,
        conversation: GroupDynamics
    ) -> Dict[str, float]:
        """Who holds power in the group?"""
        
        power = {}
        
        for participant in conversation.participants.values():
            participant_power = (
                participant.influence_score * 0.5 +
                participant.engagement_level * 0.3 +
                (1.0 if participant.role in [ParticipantRole.LEADER, ParticipantRole.FACILITATOR] else 0) * 0.2
            )
            power[participant.user_id] = participant_power
        
        return power
    
    async def _identify_subgroups(self, conversation: GroupDynamics) -> List[List[str]]:
        """Are there smaller coalitions?"""
        
        subgroups = []
        
        for p1 in conversation.participants.values():
            for p2 in conversation.participants.values():
                if p1.user_id < p2.user_id:
                    overlap = 0
                    for msg1 in p1.recent_messages:
                        for msg2 in p2.recent_messages:
                            if len(set(msg1.split()) & set(msg2.split())) > 3:
                                overlap += 1
                    
                    if overlap > 2:
                        subgroups.append([p1.user_id, p2.user_id])
        
        return subgroups
    
    async def _detect_tensions(self, conversation: GroupDynamics) -> List[str]:
        """What unspoken tensions exist?"""
        
        tensions = []
        
        for p1 in conversation.participants.values():
            for p2 in conversation.participants.values():
                if p1.user_id != p2.user_id:
                    if p1.alignment_with_group < 0.4 and p2.alignment_with_group > 0.8:
                        tensions.append(f"Tension between {p1.user_id} and {p2.user_id}")
        
        return tensions[:3]


class MultiPartyConversationSystem:
    """Main system for handling group conversations"""
    
    def __init__(self):
        self.group_analyzer = GroupDynamicsAnalyzer()
        self.active_conversations = {}
        
    async def process_group_message(
        self,
        conversation_id: str,
        participant_id: str,
        message: str,
        emotion: Optional[str] = None,
        intent: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process message in group conversation"""
        
        if conversation_id not in self.active_conversations:
            self.active_conversations[conversation_id] = GroupDynamics(
                conversation_id=conversation_id
            )
        
        conversation = self.active_conversations[conversation_id]
        
        if participant_id not in conversation.participants:
            conversation.participants[participant_id] = Participant(
                user_id=participant_id,
                name=participant_id
            )
        
        participant = conversation.participants[participant_id]
        participant.recent_messages.append(message)
        participant.contribution_count += 1
        participant.emotional_state = emotion or "neutral"
        
        turn = ConversationTurn(
            participant_id=participant_id,
            timestamp=datetime.now(),
            message=message,
            emotion_expressed=emotion or "neutral",
            intent=intent or "contribute"
        )
        
        conversation.conversation_turns.append(turn)
        
        updated_conversation = await self.group_analyzer.analyze_group_dynamics(conversation)
        self.active_conversations[conversation_id] = updated_conversation
        
        return {
            "conversation_id": conversation_id,
            "dominant_pattern": updated_conversation.dominant_pattern.value,
            "psychological_safety": updated_conversation.psychological_safety,
            "collective_intelligence": updated_conversation.collective_intelligence,
            "tensions": updated_conversation.unspoken_tensions,
        }
    
    async def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get summary of group conversation"""
        
        if conversation_id not in self.active_conversations:
            return {}
        
        conv = self.active_conversations[conversation_id]
        
        return {
            "participants": len(conv.participants),
            "turn_count": len(conv.conversation_turns),
            "pattern": conv.dominant_pattern.value,
            "safety": conv.psychological_safety,
            "balance": conv.participation_balance,
            "diversity": conv.idea_diversity,
            "conflict": conv.conflict_level,
            "collective_intelligence": conv.collective_intelligence,
            "power_holders": [
                uid for uid, power in conv.power_distribution.items()
                if power > 0.6
            ][:3],
        }
    
    async def get_recommendations_for_facilitator(self, conversation_id: str) -> List[str]:
        """Get recommendations for group facilitator"""
        
        if conversation_id not in self.active_conversations:
            return []
        
        conv = self.active_conversations[conversation_id]
        recommendations = []
        
        if conv.participation_balance < 0.5:
            recommendations.append("Some voices are dominating. Invite quieter members to share.")
        
        if conv.psychological_safety < 0.5:
            recommendations.append("Create more psychological safety by validating diverse views.")
        
        if conv.conflict_level > 0.7:
            recommendations.append("Consider addressing conflict directly and respectfully.")
        
        if conv.idea_diversity < 0.3:
            recommendations.append("Encourage more diverse perspectives to strengthen collective intelligence.")
        
        if len(conv.unspoken_tensions) > 2:
            recommendations.append("Address unspoken tensions to improve group cohesion.")
        
        return recommendations
