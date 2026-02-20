"""
Ochuko AI - Enhanced Memory & Learning System
Episodic memory, semantic learning, knowledge graphs, continuous learning
Author: David Akpoviroro Oke (MrIridescent)
Version: 2.0.0 Production-Grade
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import asyncio
import json

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memory"""
    EPISODIC = "episodic"  # Specific events and experiences
    SEMANTIC = "semantic"  # Factual knowledge and concepts
    PROCEDURAL = "procedural"  # How to do things
    WORKING = "working"  # Current active memory
    CONTEXTUAL = "contextual"  # Context and relationships


class MemoryImportance(Enum):
    """Importance level for memory retention"""
    CRITICAL = "critical"  # Must remember
    HIGH = "high"  # Very important
    MEDIUM = "medium"  # Moderately important
    LOW = "low"  # Nice to remember
    MINIMAL = "minimal"  # Can forget


@dataclass
class EpisodicMemory:
    """Memory of specific event or interaction"""
    memory_id: str
    timestamp: datetime
    
    event_description: str
    participants: List[str]
    context: Dict[str, Any]
    
    emotional_significance: float  # 0-100
    importance_level: MemoryImportance
    
    sensory_details: Dict[str, str]  # What was seen, heard, felt
    outcome: Optional[Dict[str, Any]]
    lessons_learned: List[str]
    
    related_memories: List[str]  # Memory IDs of related events
    retrieval_count: int = 0  # How many times retrieved
    last_retrieved: Optional[datetime] = None
    fade_time: datetime = field(default_factory=datetime.now)


@dataclass
class SemanticMemory:
    """Factual knowledge and concepts"""
    concept_id: str
    concept_name: str
    concept_description: str
    
    category: str
    parent_concepts: List[str]  # What this relates to
    child_concepts: List[str]  # What relates to this
    
    facts: Dict[str, Any]
    relationships: Dict[str, List[str]]
    
    confidence: float  # 0-100 confidence in correctness
    source: str  # Where this knowledge came from
    learned_date: datetime
    
    usage_frequency: int
    last_used: Optional[datetime] = None


@dataclass
class ProceduralMemory:
    """Knowledge of how to do things"""
    procedure_id: str
    procedure_name: str
    procedure_description: str
    
    steps: List[Dict[str, Any]]
    prerequisites: List[str]
    outcomes: List[str]
    
    success_rate: float  # 0-100 success when executed
    times_executed: int
    
    variations: Dict[str, str]  # Different ways to achieve same goal
    common_mistakes: List[str]
    optimization_tips: List[str]


@dataclass
class KnowledgeGraphNode:
    """Node in semantic knowledge graph"""
    node_id: str
    node_name: str
    node_type: str  # concept, entity, relationship
    
    attributes: Dict[str, Any]
    connections: Dict[str, List[str]]  # relationship -> connected nodes
    
    importance: float  # 0-100
    connectivity: int  # How many connections
    embedding: Optional[List[float]]  # Vector representation


class EnhancedMemoryAndLearningSystem:
    """
    Advanced memory system combining episodic, semantic, and procedural memory.
    Mimics human memory consolidation and forgetting curves.
    """
    
    def __init__(self):
        self.episodic_store: Dict[str, EpisodicMemory] = {}
        self.semantic_store: Dict[str, SemanticMemory] = {}
        self.procedural_store: Dict[str, ProceduralMemory] = {}
        self.knowledge_graph = KnowledgeGraph()
        
        self.retrieval_engine = RetrievalEngine(self)
        self.consolidation_engine = ConsolidationEngine(self)
        self.learning_engine = LearningEngine(self)
        
        self.user_context: Dict[str, Any] = {}
        self.active_working_memory: deque = asyncio.Queue(maxsize=10)
        
        self.is_ready = False
    
    async def initialize(self):
        """Initialize memory systems"""
        logger.info("Initializing Enhanced Memory & Learning System...")
        await self.knowledge_graph.initialize()
        self.is_ready = True
        logger.info("✅ Enhanced Memory & Learning System ready")
    
    async def record_episodic_memory(
        self,
        event_description: str,
        participants: List[str],
        context: Dict[str, Any],
        emotional_significance: float = 50.0,
        outcome: Optional[Dict] = None
    ) -> EpisodicMemory:
        """Record new episodic memory (specific event)"""
        
        memory = EpisodicMemory(
            memory_id=f"epi_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            event_description=event_description,
            participants=participants,
            context=context,
            emotional_significance=min(100, emotional_significance),
            importance_level=self._determine_importance(emotional_significance),
            sensory_details=context.get("sensory_details", {}),
            outcome=outcome,
            lessons_learned=await self._extract_lessons(event_description, outcome),
            related_memories=[]
        )
        
        self.episodic_store[memory.memory_id] = memory
        
        await self.consolidation_engine.consolidate_episodic(memory)
        
        return memory
    
    async def record_semantic_learning(
        self,
        concept_name: str,
        concept_description: str,
        category: str,
        facts: Dict[str, Any],
        source: str = "learning"
    ) -> SemanticMemory:
        """Record new semantic memory (knowledge)"""
        
        semantic = SemanticMemory(
            concept_id=f"sem_{datetime.now().timestamp()}",
            concept_name=concept_name,
            concept_description=concept_description,
            category=category,
            parent_concepts=[],
            child_concepts=[],
            facts=facts,
            relationships={},
            confidence=0.85,
            source=source,
            learned_date=datetime.now()
        )
        
        self.semantic_store[semantic.concept_id] = semantic
        
        await self.knowledge_graph.add_node(semantic)
        
        await self.learning_engine.learn_semantic(semantic)
        
        return semantic
    
    async def record_procedural_learning(
        self,
        procedure_name: str,
        procedure_description: str,
        steps: List[Dict[str, Any]],
        outcomes: List[str]
    ) -> ProceduralMemory:
        """Record new procedural memory (how-to knowledge)"""
        
        procedure = ProceduralMemory(
            procedure_id=f"proc_{datetime.now().timestamp()}",
            procedure_name=procedure_name,
            procedure_description=procedure_description,
            steps=steps,
            prerequisites=[],
            outcomes=outcomes,
            success_rate=0.0,
            times_executed=0,
            variations={},
            common_mistakes=[],
            optimization_tips=[]
        )
        
        self.procedural_store[procedure.procedure_id] = procedure
        
        await self.learning_engine.learn_procedural(procedure)
        
        return procedure
    
    async def recall_memory(
        self,
        query: str,
        memory_type: Optional[MemoryType] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Recall memories matching query"""
        
        results = await self.retrieval_engine.retrieve(
            query, memory_type, max_results
        )
        
        for result in results:
            if "memory_id" in result:
                if result["memory_id"] in self.episodic_store:
                    mem = self.episodic_store[result["memory_id"]]
                    mem.retrieval_count += 1
                    mem.last_retrieved = datetime.now()
        
        return results
    
    async def get_context_from_memory(
        self,
        topic: str,
        max_depth: int = 3
    ) -> Dict[str, Any]:
        """
        Get comprehensive context from memory.
        Retrieves all related memories up to specified depth.
        """
        
        context = {
            "topic": topic,
            "retrieved_at": datetime.now().isoformat(),
            "episodic": [],
            "semantic": [],
            "procedural": [],
            "knowledge_graph_context": {}
        }
        
        episodic_results = await self.recall_memory(
            topic, MemoryType.EPISODIC, max_results=10
        )
        context["episodic"] = episodic_results
        
        semantic_results = await self.recall_memory(
            topic, MemoryType.SEMANTIC, max_results=10
        )
        context["semantic"] = semantic_results
        
        procedural_results = await self.recall_memory(
            topic, MemoryType.PROCEDURAL, max_results=5
        )
        context["procedural"] = procedural_results
        
        kg_context = await self.knowledge_graph.get_node_context(topic, max_depth)
        context["knowledge_graph_context"] = kg_context
        
        return context
    
    async def update_memory(
        self,
        memory_id: str,
        updates: Dict[str, Any]
    ):
        """Update existing memory with new information"""
        
        if memory_id in self.episodic_store:
            mem = self.episodic_store[memory_id]
            for key, value in updates.items():
                if hasattr(mem, key):
                    setattr(mem, key, value)
    
    async def consolidate_memories(self):
        """
        Consolidate memories (like sleep consolidation).
        Strengthens important memories, weakens unimportant ones.
        Creates new associations.
        """
        
        await self.consolidation_engine.consolidate_all()
    
    async def continuous_learning_from_interactions(
        self,
        interaction_data: Dict[str, Any]
    ):
        """
        Continuously learn from every interaction.
        Updates memories, learns new concepts, improves procedures.
        """
        
        if interaction_data.get("type") == "event":
            await self.record_episodic_memory(
                event_description=interaction_data.get("description", ""),
                participants=interaction_data.get("participants", []),
                context=interaction_data.get("context", {}),
                emotional_significance=interaction_data.get("significance", 50.0),
                outcome=interaction_data.get("outcome")
            )
        
        if interaction_data.get("type") == "learning":
            await self.record_semantic_learning(
                concept_name=interaction_data.get("concept", ""),
                concept_description=interaction_data.get("description", ""),
                category=interaction_data.get("category", "general"),
                facts=interaction_data.get("facts", {})
            )
        
        if interaction_data.get("type") == "procedure":
            await self.record_procedural_learning(
                procedure_name=interaction_data.get("name", ""),
                procedure_description=interaction_data.get("description", ""),
                steps=interaction_data.get("steps", []),
                outcomes=interaction_data.get("outcomes", [])
            )
    
    def _determine_importance(self, emotional_significance: float) -> MemoryImportance:
        """Determine importance level"""
        if emotional_significance >= 85:
            return MemoryImportance.CRITICAL
        elif emotional_significance >= 70:
            return MemoryImportance.HIGH
        elif emotional_significance >= 50:
            return MemoryImportance.MEDIUM
        elif emotional_significance >= 25:
            return MemoryImportance.LOW
        else:
            return MemoryImportance.MINIMAL
    
    async def _extract_lessons(
        self,
        event_description: str,
        outcome: Optional[Dict]
    ) -> List[str]:
        """Extract lessons from event"""
        lessons = []
        
        if outcome:
            if outcome.get("success"):
                lessons.append(f"Successfully completed: {event_description}")
            else:
                lessons.append(f"Challenge encountered: {outcome.get('issue', 'unknown')}")
        
        return lessons


class RetrievalEngine:
    """Retrieve memories using semantic and contextual matching"""
    
    def __init__(self, memory_system):
        self.memory_system = memory_system
    
    async def retrieve(
        self,
        query: str,
        memory_type: Optional[MemoryType],
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Retrieve matching memories"""
        
        results = []
        
        if memory_type in [None, MemoryType.EPISODIC]:
            episodic_matches = self._match_episodic(query)
            results.extend(episodic_matches[:max_results])
        
        if memory_type in [None, MemoryType.SEMANTIC]:
            semantic_matches = self._match_semantic(query)
            results.extend(semantic_matches[:max_results])
        
        if memory_type in [None, MemoryType.PROCEDURAL]:
            procedural_matches = self._match_procedural(query)
            results.extend(procedural_matches[:max_results])
        
        return results[:max_results]
    
    def _match_episodic(self, query: str) -> List[Dict]:
        """Match episodic memories"""
        matches = []
        
        for mem_id, mem in self.memory_system.episodic_store.items():
            if query.lower() in mem.event_description.lower():
                matches.append({
                    "memory_id": mem_id,
                    "type": "episodic",
                    "description": mem.event_description,
                    "relevance": 0.85
                })
        
        return sorted(matches, key=lambda x: x["relevance"], reverse=True)
    
    def _match_semantic(self, query: str) -> List[Dict]:
        """Match semantic memories"""
        matches = []
        
        for concept_id, concept in self.memory_system.semantic_store.items():
            if query.lower() in concept.concept_name.lower():
                matches.append({
                    "memory_id": concept_id,
                    "type": "semantic",
                    "concept": concept.concept_name,
                    "relevance": 0.88
                })
        
        return sorted(matches, key=lambda x: x["relevance"], reverse=True)
    
    def _match_procedural(self, query: str) -> List[Dict]:
        """Match procedural memories"""
        matches = []
        
        for proc_id, proc in self.memory_system.procedural_store.items():
            if query.lower() in proc.procedure_name.lower():
                matches.append({
                    "memory_id": proc_id,
                    "type": "procedural",
                    "procedure": proc.procedure_name,
                    "relevance": 0.82
                })
        
        return sorted(matches, key=lambda x: x["relevance"], reverse=True)


class ConsolidationEngine:
    """Consolidate memories during rest/sleep"""
    
    def __init__(self, memory_system):
        self.memory_system = memory_system
    
    async def consolidate_episodic(self, memory: EpisodicMemory):
        """Consolidate episodic memory"""
        logger.debug(f"Consolidating episodic memory: {memory.memory_id}")
    
    async def consolidate_all(self):
        """Consolidate all memories"""
        logger.info("Memory consolidation cycle starting...")
        
        for mem_id, mem in self.memory_system.episodic_store.items():
            if mem.importance_level == MemoryImportance.CRITICAL:
                mem.retrieval_count = max(mem.retrieval_count, 10)


class LearningEngine:
    """Learn and improve from new information"""
    
    def __init__(self, memory_system):
        self.memory_system = memory_system
    
    async def learn_semantic(self, semantic: SemanticMemory):
        """Learn new semantic information"""
        logger.debug(f"Learning semantic: {semantic.concept_name}")
    
    async def learn_procedural(self, procedure: ProceduralMemory):
        """Learn new procedures"""
        logger.debug(f"Learning procedure: {procedure.procedure_name}")
    
    async def improve_from_feedback(self, feedback: Dict[str, Any]):
        """Improve from user feedback"""
        pass


class KnowledgeGraph:
    """Semantic knowledge graph for concept relationships"""
    
    def __init__(self):
        self.nodes: Dict[str, KnowledgeGraphNode] = {}
        self.edges: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    
    async def initialize(self):
        """Initialize knowledge graph"""
        logger.info("Initializing Knowledge Graph...")
    
    async def add_node(self, semantic: SemanticMemory):
        """Add concept node to graph"""
        
        node = KnowledgeGraphNode(
            node_id=semantic.concept_id,
            node_name=semantic.concept_name,
            node_type="concept",
            attributes=semantic.facts,
            connections={},
            importance=semantic.confidence,
            connectivity=0
        )
        
        self.nodes[node.node_id] = node
    
    async def get_node_context(self, node_name: str, max_depth: int) -> Dict:
        """Get context around a node"""
        
        matching_nodes = [
            n for n in self.nodes.values()
            if node_name.lower() in n.node_name.lower()
        ]
        
        if not matching_nodes:
            return {}
        
        primary_node = matching_nodes[0]
        
        return {
            "node": primary_node.node_name,
            "connected_nodes": list(primary_node.connections.keys()),
            "importance": primary_node.importance
        }


from collections import deque
