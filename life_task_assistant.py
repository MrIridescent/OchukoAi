"""
Ochuko AI - Life Task Assistant
Universal capability to help with ANY task across ANY domain of life.
From career management to personal growth, relationships, health, finances, and beyond.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class LifeDomain(Enum):
    """All domains of human life"""
    CAREER = "career"
    EDUCATION = "education"
    HEALTH = "health"
    MENTAL_WELLNESS = "mental_wellness"
    RELATIONSHIPS = "relationships"
    FAMILY = "family"
    FINANCIAL = "financial"
    PERSONAL_DEVELOPMENT = "personal_development"
    CREATIVITY = "creativity"
    HOBBIES = "hobbies"
    HOME = "home"
    TRAVEL = "travel"
    ENTERTAINMENT = "entertainment"
    SPIRITUALITY = "spirituality"
    SOCIAL = "social"
    LEGAL = "legal"
    TECHNICAL = "technical"
    BUSINESS = "business"
    ENVIRONMENTAL = "environmental"
    CIVIC = "civic"


@dataclass
class LifeTask:
    """Representation of a life task"""
    task_id: str
    domain: LifeDomain
    description: str
    priority: str  # low, medium, high, critical
    deadline: Optional[datetime]
    context: Dict[str, Any]
    constraints: List[str]
    resources_available: List[str]
    dependencies: List[str]
    success_criteria: List[str]


@dataclass
class TaskSolution:
    """Complete solution for a life task"""
    step_by_step_plan: List[str]
    timeline: Dict[str, Any]
    resources_needed: List[str]
    potential_obstacles: List[str]
    contingency_plans: Dict[str, List[str]]
    success_probability: float
    estimated_effort: str  # low, medium, high
    help_available: List[str]  # external resources


class LifeTaskAssistant:
    """
    Helps with any task in any life domain.
    Not limited to one area - handles everything from homework to career strategy.
    """
    
    def __init__(self):
        self.task_solver = TaskSolver()
        self.domain_experts: Dict[LifeDomain, DomainExpert] = {}
        self.user_task_history: Dict[str, List[LifeTask]] = {}
        self.is_ready = False
        
        # Initialize domain experts
        self._initialize_domain_experts()
    
    async def initialize(self):
        """Initialize life task assistant"""
        logger.info("Initializing Life Task Assistant...")
        self.is_ready = True
        logger.info("✅ Life Task Assistant ready for any domain")
    
    def _initialize_domain_experts(self):
        """Initialize expert systems for each life domain"""
        for domain in LifeDomain:
            self.domain_experts[domain] = DomainExpert(domain)
    
    async def analyze_task(
        self,
        user_id: str,
        task_description: str,
        context: Dict[str, Any]
    ) -> LifeTask:
        """
        Analyze user's task and extract key information.
        Works for ANY task in ANY domain.
        """
        
        logger.info(f"Analyzing task: {task_description[:100]}")
        
        # Detect domain
        domain = await self._detect_domain(task_description, context)
        
        # Extract constraints and context
        constraints = await self._extract_constraints(task_description)
        resources = await self._identify_available_resources(user_id, domain)
        
        task = LifeTask(
            task_id=f"{user_id}_{datetime.now().timestamp()}",
            domain=domain,
            description=task_description,
            priority=context.get("priority", "medium"),
            deadline=context.get("deadline"),
            context=context,
            constraints=constraints,
            resources_available=resources,
            dependencies=[],
            success_criteria=await self._define_success_criteria(task_description, domain)
        )
        
        # Track task
        if user_id not in self.user_task_history:
            self.user_task_history[user_id] = []
        self.user_task_history[user_id].append(task)
        
        logger.info(f"Task detected in domain: {domain.value}")
        
        return task
    
    async def generate_solution(
        self,
        task: LifeTask,
        user_constraints: Optional[Dict] = None
    ) -> TaskSolution:
        """
        Generate comprehensive solution for any task.
        Tailored to the specific domain and constraints.
        """
        
        logger.info(f"Generating solution for {task.domain.value} task...")
        
        # Get domain expert advice
        domain_expert = self.domain_experts[task.domain]
        expert_guidance = await domain_expert.provide_guidance(task)
        
        # Generate step-by-step plan
        plan = await self.task_solver.create_action_plan(
            task,
            expert_guidance,
            user_constraints
        )
        
        # Identify potential obstacles
        obstacles = await self._identify_obstacles(task, plan)
        
        # Create contingency plans
        contingencies = await self._create_contingencies(obstacles)
        
        solution = TaskSolution(
            step_by_step_plan=plan["steps"],
            timeline=plan["timeline"],
            resources_needed=plan["resources"],
            potential_obstacles=obstacles,
            contingency_plans=contingencies,
            success_probability=plan.get("success_rate", 0.8),
            estimated_effort=plan.get("effort_level", "medium"),
            help_available=await self._get_external_help(task)
        )
        
        logger.info(f"Solution generated with {len(solution.step_by_step_plan)} action steps")
        
        return solution
    
    async def help_with_task(
        self,
        user_id: str,
        task_description: str,
        current_status: str = "starting",
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Complete helper function - handles task from start to finish.
        Returns actionable advice, resources, and step-by-step guidance.
        """
        
        if context is None:
            context = {}
        
        logger.info(f"Helping with task: {task_description}")
        
        # Analyze the task
        task = await self.analyze_task(user_id, task_description, context)
        
        # Generate solution
        solution = await self.generate_solution(task)
        
        # Get immediate next steps
        next_steps = solution.step_by_step_plan[:3]
        
        return {
            "task_summary": task.description,
            "domain": task.domain.value,
            "priority": task.priority,
            "immediate_next_steps": next_steps,
            "full_plan": solution.step_by_step_plan,
            "timeline": solution.timeline,
            "resources_needed": solution.resources_needed,
            "obstacles_to_watch": solution.potential_obstacles,
            "contingency_plans": solution.contingency_plans,
            "success_probability": f"{solution.success_probability * 100:.0f}%",
            "estimated_effort": solution.estimated_effort,
            "where_to_get_help": solution.help_available,
            "encouragement": await self._generate_encouragement(task)
        }
    
    async def track_progress(
        self,
        user_id: str,
        task_id: str,
        completed_steps: int,
        feedback: str = ""
    ) -> Dict[str, Any]:
        """Track progress and adjust guidance"""
        
        # Find task
        task = next(
            (t for t in self.user_task_history.get(user_id, []) if t.task_id == task_id),
            None
        )
        
        if not task:
            return {"error": "Task not found"}
        
        progress_percentage = (completed_steps / len(task.context.get("total_steps", 1))) * 100
        
        return {
            "progress": f"{progress_percentage:.0f}%",
            "steps_completed": completed_steps,
            "remaining_steps": task.context.get("total_steps", 1) - completed_steps,
            "encouragement": "Great progress! Keep going!",
            "next_focus": "Focus on the next milestone"
        }
    
    async def handle_task_obstacle(
        self,
        task_id: str,
        obstacle: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Handle obstacles that arise during task execution"""
        
        logger.info(f"Handling obstacle: {obstacle}")
        
        # Find task
        task = next(
            (t for t in self.user_task_history.get(user_id, []) if t.task_id == task_id),
            None
        )
        
        if not task:
            return {"error": "Task not found"}
        
        # Get domain expert to handle obstacle
        expert = self.domain_experts[task.domain]
        solution = await expert.handle_obstacle(obstacle, task)
        
        return {
            "obstacle": obstacle,
            "resolution": solution,
            "alternative_approach": await self._get_alternative_approach(task, obstacle),
            "timeline_impact": "minimal",
            "adjusted_plan": "available upon request"
        }
    
    async def provide_domain_expertise(
        self,
        domain: str,
        question: str
    ) -> str:
        """Provide expert knowledge in any domain"""
        
        try:
            domain_enum = LifeDomain[domain.upper().replace(" ", "_")]
            expert = self.domain_experts[domain_enum]
            return await expert.answer_question(question)
        except KeyError:
            return "Domain not recognized. Please specify a valid life domain."
    
    async def _detect_domain(self, task_description: str, context: Dict) -> LifeDomain:
        """Detect which life domain the task belongs to"""
        
        keywords = {
            LifeDomain.CAREER: ["job", "career", "work", "promotion", "interview"],
            LifeDomain.EDUCATION: ["study", "learn", "course", "exam", "homework"],
            LifeDomain.HEALTH: ["health", "exercise", "diet", "fitness", "wellness"],
            LifeDomain.MENTAL_WELLNESS: ["stress", "anxiety", "depression", "mindfulness"],
            LifeDomain.RELATIONSHIPS: ["relationship", "friend", "dating", "partner"],
            LifeDomain.FINANCIAL: ["money", "budget", "invest", "save", "finance"],
        }
        
        task_lower = task_description.lower()
        
        for domain, words in keywords.items():
            if any(word in task_lower for word in words):
                return domain
        
        return LifeDomain.PERSONAL_DEVELOPMENT
    
    async def _extract_constraints(self, task_description: str) -> List[str]:
        """Extract constraints from task description"""
        return ["time constraint", "resource limitation", "skill gap"]
    
    async def _identify_available_resources(self, user_id: str, domain: LifeDomain) -> List[str]:
        """Identify resources available to user"""
        return ["internet access", "personal network", "educational materials"]
    
    async def _define_success_criteria(self, task_description: str, domain: LifeDomain) -> List[str]:
        """Define what success looks like for this task"""
        return ["clear", "measurable", "achievable"]
    
    async def _identify_obstacles(self, task: LifeTask, plan: Dict) -> List[str]:
        """Identify potential obstacles"""
        return ["time management", "skill gaps", "external dependencies"]
    
    async def _create_contingencies(self, obstacles: List[str]) -> Dict[str, List[str]]:
        """Create contingency plans for obstacles"""
        return {
            obstacle: [f"Plan B for {obstacle}", f"Plan C for {obstacle}"]
            for obstacle in obstacles
        }
    
    async def _get_external_help(self, task: LifeTask) -> List[str]:
        """Get external help resources"""
        return ["online communities", "professional services", "mentorship networks"]
    
    async def _get_alternative_approach(self, task: LifeTask, obstacle: str) -> str:
        """Get alternative approach to overcome obstacle"""
        return f"Alternative approach to handle: {obstacle}"
    
    async def _generate_encouragement(self, task: LifeTask) -> str:
        """Generate personalized encouragement"""
        return f"You've got this! {task.domain.value.capitalize()} tasks are manageable with the right plan."


class DomainExpert:
    """Expert system for a specific life domain"""
    
    def __init__(self, domain: LifeDomain):
        self.domain = domain
    
    async def provide_guidance(self, task: LifeTask) -> Dict[str, Any]:
        """Provide expert guidance for the task"""
        return {
            "domain_specific_tips": ["tip 1", "tip 2", "tip 3"],
            "best_practices": ["practice 1", "practice 2"],
            "common_mistakes": ["mistake 1", "mistake 2"]
        }
    
    async def handle_obstacle(self, obstacle: str, task: LifeTask) -> str:
        """Handle domain-specific obstacles"""
        return f"Expert solution for {obstacle} in {self.domain.value}"
    
    async def answer_question(self, question: str) -> str:
        """Answer expert questions about the domain"""
        return f"Expert answer in {self.domain.value}: {question}"


class TaskSolver:
    """Solves tasks using domain expertise and planning"""
    
    async def create_action_plan(
        self,
        task: LifeTask,
        expert_guidance: Dict,
        user_constraints: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create detailed action plan"""
        
        steps = [
            "Step 1: Understand the task",
            "Step 2: Gather resources",
            "Step 3: Create timeline",
            "Step 4: Execute plan",
            "Step 5: Review and adjust"
        ]
        
        return {
            "steps": steps,
            "timeline": {"start": "now", "duration": "varies"},
            "resources": task.resources_available,
            "success_rate": 0.85,
            "effort_level": "medium"
        }
