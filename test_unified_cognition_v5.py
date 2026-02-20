"""
Test Suite for Unified Cognition v5.0
Verifies all systems operational and integrated
"""

import pytest
import asyncio
from multidimensional_reasoning_engines import (
    MultiDimensionalReasoningSystem,
    RationalReasoningEngine,
    RelationalReasoningEngine,
    SubjectiveReasoningEngine,
    ObjectiveReasoningEngine,
)
from unified_cognition_v5 import UnifiedCognitionV5


@pytest.mark.asyncio
class TestRationalReasoningEngine:
    """Tests for rational reasoning"""
    
    async def test_rational_reasoning_initialization(self):
        """Test rational engine initializes"""
        engine = RationalReasoningEngine()
        assert engine.logical_operators is not None
        assert "AND" in engine.logical_operators
    
    @pytest.mark.asyncio
    async def test_rational_reasoning_produces_perspective(self):
        """Test rational reasoning produces valid perspective"""
        engine = RationalReasoningEngine()
        perspective = await engine.reason_rationally("If A then B")
        
        assert perspective.perspective_type.value == "rational"
        assert perspective.validity > 0.9
        assert len(perspective.logic_chain) > 0
    
    @pytest.mark.asyncio
    async def test_logical_fallacy_detection(self):
        """Test detection of logical fallacies"""
        engine = RationalReasoningEngine()
        fallacies = await engine.identify_logical_fallacies(
            "Everyone says this is true, so obviously it must be correct"
        )
        
        assert len(fallacies) > 0
        assert any("authority" in f.lower() for f in fallacies)


@pytest.mark.asyncio
class TestRelationalReasoningEngine:
    """Tests for relational reasoning"""
    
    async def test_relational_reasoning_initialization(self):
        """Test relational engine initializes"""
        engine = RelationalReasoningEngine()
        assert engine.relational_values is not None
        assert "care" in engine.relational_values
    
    @pytest.mark.asyncio
    async def test_relational_reasoning_produces_perspective(self):
        """Test relational reasoning produces valid perspective"""
        engine = RelationalReasoningEngine()
        perspective = await engine.reason_relationally(
            "How to communicate difficult news"
        )
        
        assert perspective.perspective_type.value == "relational"
        assert perspective.completeness > 0.8
        assert "relationship" in perspective.reasoning.lower()
    
    @pytest.mark.asyncio
    async def test_relationship_dynamics_analysis(self):
        """Test analysis of relationship dynamics"""
        engine = RelationalReasoningEngine()
        dynamics = await engine.analyze_relationship_dynamics(
            "I understand how you feel and I care about our relationship"
        )
        
        assert "trust_signals" in dynamics
        assert len(dynamics["trust_signals"]) > 0


@pytest.mark.asyncio
class TestSubjectiveReasoningEngine:
    """Tests for subjective reasoning"""
    
    async def test_subjective_reasoning_initialization(self):
        """Test subjective engine initializes"""
        engine = SubjectiveReasoningEngine()
        assert engine.subjective_frameworks is not None
        assert "personal_values" in engine.subjective_frameworks
    
    @pytest.mark.asyncio
    async def test_subjective_reasoning_produces_perspective(self):
        """Test subjective reasoning produces valid perspective"""
        engine = SubjectiveReasoningEngine()
        perspective = await engine.reason_subjectively(
            "What matters to me in this decision?"
        )
        
        assert perspective.perspective_type.value == "subjective"
        assert perspective.completeness > 0.8
    
    @pytest.mark.asyncio
    async def test_personal_meaning_extraction(self):
        """Test extraction of personal meaning"""
        engine = SubjectiveReasoningEngine()
        meaning = await engine.extract_personal_meaning(
            "This experience taught me the value of patience and connection"
        )
        
        assert "lessons" in meaning or "values" in meaning


@pytest.mark.asyncio
class TestObjectiveReasoningEngine:
    """Tests for objective reasoning"""
    
    async def test_objective_reasoning_initialization(self):
        """Test objective engine initializes"""
        engine = ObjectiveReasoningEngine()
        assert engine.evidence_standards is not None
        assert "scientific" in engine.evidence_standards
    
    @pytest.mark.asyncio
    async def test_objective_reasoning_produces_perspective(self):
        """Test objective reasoning produces valid perspective"""
        engine = ObjectiveReasoningEngine()
        perspective = await engine.reason_objectively(
            "Climate change",
            ["IPCC reports show 97% consensus", "Temperature data verified"]
        )
        
        assert perspective.perspective_type.value == "objective"
        assert perspective.validity > 0.95
    
    @pytest.mark.asyncio
    async def test_evidence_quality_evaluation(self):
        """Test evaluation of evidence quality"""
        engine = ObjectiveReasoningEngine()
        evaluation = await engine.evaluate_evidence_quality([
            "Peer-reviewed study shows X",
            "Experts agree on Y",
            "I heard that Z"
        ])
        
        assert "evidence_rating" in evaluation
        assert evaluation["total_evidence_quality"] > 0.5


@pytest.mark.asyncio
class TestMultiDimensionalReasoningSystem:
    """Tests for integrated reasoning system"""
    
    async def test_multidimensional_system_initialization(self):
        """Test system initializes all engines"""
        system = MultiDimensionalReasoningSystem()
        
        assert system.rational is not None
        assert system.relational is not None
        assert system.subjective is not None
        assert system.objective is not None
    
    @pytest.mark.asyncio
    async def test_comprehensive_reasoning_produces_integrated_result(self):
        """Test comprehensive reasoning"""
        system = MultiDimensionalReasoningSystem()
        integrated = await system.reason_comprehensively(
            "Should I make this difficult life change?"
        )
        
        assert integrated.topic == "Should I make this difficult life change?"
        assert integrated.rational_perspective is not None
        assert integrated.relational_perspective is not None
        assert integrated.subjective_perspective is not None
        assert integrated.objective_perspective is not None
        assert len(integrated.synthesis) > 0
        assert integrated.depth_achieved > 0.5
    
    @pytest.mark.asyncio
    async def test_tension_identification(self):
        """Test identification of tensions between perspectives"""
        system = MultiDimensionalReasoningSystem()
        integrated = await system.reason_comprehensively(
            "Career vs. family"
        )
        
        assert isinstance(integrated.tensions, list)


@pytest.mark.asyncio
class TestUnifiedCognitionV5:
    """Tests for complete unified cognition system"""
    
    async def test_unified_cognition_initialization(self):
        """Test unified cognition initializes"""
        cognition = UnifiedCognitionV5()
        await cognition.initialize_superintelligent_mind()
        
        assert cognition.system_health["overall_superintelligence"] > 0.85
    
    @pytest.mark.asyncio
    async def test_complete_moment_processing(self):
        """Test processing of complete cognitive moment"""
        cognition = UnifiedCognitionV5()
        
        moment = await cognition.process_complete_moment(
            user_id="test_user",
            text_input="I'm struggling with this decision",
            voice_data={
                "pitch": 110,
                "volume": 60,
                "speed": 140,
                "rhythm": "hesitant"
            },
            facial_data={
                "expression": "thoughtful",
                "confidence": 0.75
            },
            cultural_profile="Western_individualist"
        )
        
        assert moment.perceived_input is not None
        assert moment.emotional_context is not None
        assert moment.rational_reasoning is not None
        assert moment.relational_reasoning is not None
        assert moment.depth_of_understanding > 0.5
    
    @pytest.mark.asyncio
    async def test_human_like_response_generation(self):
        """Test generation of human-like response"""
        cognition = UnifiedCognitionV5()
        
        moment = await cognition.process_complete_moment(
            user_id="test_user",
            text_input="I feel lost",
        )
        
        response = await cognition.generate_human_like_response(moment)
        
        assert "text" in response
        assert "emotional_tone" in response
        assert "transparency" in response
        assert len(response["text"]) > 50
    
    @pytest.mark.asyncio
    async def test_moment_insights_extraction(self):
        """Test extraction of insights from cognitive moment"""
        cognition = UnifiedCognitionV5()
        
        moment = await cognition.process_complete_moment(
            user_id="test_user",
            text_input="I'm anxious about the future",
        )
        
        insights = await cognition.get_moment_insights(moment)
        
        assert "what_matters_most" in insights
        assert "hidden_needs" in insights
        assert "growth_opportunity" in insights
        assert isinstance(insights["hidden_needs"], list)
    
    @pytest.mark.asyncio
    async def test_system_health_assessment(self):
        """Test system health assessment"""
        cognition = UnifiedCognitionV5()
        await cognition.initialize_superintelligent_mind()
        
        health = await cognition.assess_system_health()
        
        assert health["overall_superintelligence"] > 0.85
        assert all(v > 0.85 for v in health.values())


@pytest.mark.asyncio
async def test_integration_full_workflow():
    """Test complete workflow from input to response"""
    
    cognition = UnifiedCognitionV5()
    await cognition.initialize_superintelligent_mind()
    
    moment = await cognition.process_complete_moment(
        user_id="integration_test",
        text_input="I'm struggling with confidence in my abilities",
        voice_data={"pitch": 115, "volume": 55, "speed": 130},
        cultural_profile="Collectivist_Eastern"
    )
    
    response = await cognition.generate_human_like_response(moment)
    
    insights = await cognition.get_moment_insights(moment)
    
    assert moment.depth_of_understanding > 0.6
    assert len(response["text"]) > 0
    assert len(insights["hidden_needs"]) > 0
    
    print("\n✅ Full integration test passed")
    print(f"   - Cognitive depth: {moment.depth_of_understanding:.2f}")
    print(f"   - Response quality: {moment.confidence_level:.2f}")
    print(f"   - Insights extracted: {len(insights['hidden_needs'])}")


@pytest.mark.asyncio
async def test_multidimensional_reasoning_on_complex_topic():
    """Test multidimensional reasoning on complex real-world topic"""
    
    system = MultiDimensionalReasoningSystem()
    
    topic = "Should artificial intelligence be regulated?"
    
    integrated = await system.reason_comprehensively(topic)
    
    assert integrated.rational_perspective.validity > 0.85
    assert integrated.relational_perspective.completeness > 0.8
    assert integrated.subjective_perspective.completeness > 0.7
    assert integrated.objective_perspective.validity > 0.9
    assert len(integrated.synthesis) > 100
    assert len(integrated.tensions) > 0
    assert len(integrated.unified_understanding) > 100
    assert integrated.depth_achieved > 0.7


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
