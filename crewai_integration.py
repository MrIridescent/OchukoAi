"""
CrewAI Multi-Agent Orchestration Integration
Enables Ochuko AI to orchestrate multiple specialized AI agents
Each agent has specific role, expertise, and tools
Author: David Akpoviroro Oke (MrIridescent)
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Predefined agent roles in the crew"""
    ANALYST = "analyst"
    STRATEGIST = "strategist"
    RESEARCHER = "researcher"
    ENGINEER = "engineer"
    ARCHITECT = "architect"
    SECURITY_EXPERT = "security_expert"
    DATA_SCIENTIST = "data_scientist"
    FORECASTER = "forecaster"
    SYNTHESIZER = "synthesizer"
    QUALITY_ASSURANCE = "quality_assurance"


class AgentBackend(Enum):
    """Supported LLM backends for agents"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    LOCAL = "local"


@dataclass
class Tool:
    """Tool definition for an agent"""
    name: str
    description: str
    func: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    async def execute(self, **kwargs) -> Any:
        """Execute the tool"""
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(**kwargs)
        else:
            return self.func(**kwargs)


@dataclass
class Agent:
    """
    CrewAI Agent - Autonomous AI agent with specific role
    """
    id: str
    role: AgentRole
    name: str
    goal: str
    backstory: str
    backend: AgentBackend = AgentBackend.OPENAI
    model: str = "gpt-4"
    temperature: float = 0.7
    tools: List[Tool] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    
    def add_tool(self, tool: Tool):
        """Add a tool to the agent's toolkit"""
        self.tools.append(tool)
        logger.info(f"Agent {self.name} acquired tool: {tool.name}")
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a specific tool"""
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    result = await tool.execute(**kwargs)
                    self.memory[f"tool_{tool_name}_{datetime.now().isoformat()}"] = result
                    return result
                except Exception as e:
                    logger.error(f"Tool execution failed: {tool_name}: {e}")
                    return None
        return None
    
    def get_context(self) -> Dict:
        """Get agent's current context"""
        return {
            "id": self.id,
            "role": self.role.value,
            "name": self.name,
            "goal": self.goal,
            "backstory": self.backstory,
            "available_tools": [t.name for t in self.tools],
            "memory_size": len(self.memory),
            "performance_metrics": self.performance_metrics
        }


@dataclass
class Task:
    """
    CrewAI Task - Specific task for an agent or crew
    """
    id: str
    description: str
    agent: Agent
    expected_output: str
    dependencies: List[str] = field(default_factory=list)
    priority: int = 0
    status: str = "pending"
    result: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    async def execute(self, context: Dict = None) -> Dict:
        """Execute the task"""
        self.status = "running"
        logger.info(f"Executing task: {self.description} (Agent: {self.agent.name})")
        
        try:
            result = {
                "task_id": self.id,
                "agent": self.agent.name,
                "description": self.description,
                "status": "completed",
                "output": f"Task completed by {self.agent.name}: {self.expected_output}",
                "timestamp": datetime.now().isoformat()
            }
            self.result = result["output"]
            self.status = "completed"
            return result
        except Exception as e:
            self.status = "failed"
            logger.error(f"Task execution failed: {e}")
            return {
                "task_id": self.id,
                "status": "failed",
                "error": str(e)
            }


@dataclass
class CrewConfig:
    """Configuration for a CrewAI crew"""
    name: str
    description: str
    verbose: bool = True
    async_execution: bool = True
    memory_enabled: bool = True
    hierarchical_mode: bool = False
    manager_agent: Optional[Agent] = None
    max_iterations: int = 10
    timeout: int = 300


class Crew:
    """
    CrewAI Crew - Orchestrates multiple agents
    Manages agent collaboration, task execution, and knowledge sharing
    """
    
    def __init__(self, config: CrewConfig):
        self.config = config
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[Task] = []
        self.task_history: List[Dict] = []
        self.shared_memory: Dict[str, Any] = {}
        self.execution_log: List[str] = []
        self.created_at = datetime.now()
        
    def add_agent(self, agent: Agent) -> Agent:
        """Add an agent to the crew"""
        self.agents[agent.id] = agent
        self.execution_log.append(f"Agent added: {agent.name} ({agent.role.value})")
        logger.info(f"Crew '{self.config.name}' now has agent: {agent.name}")
        return agent
    
    def add_task(self, task: Task) -> Task:
        """Add a task to the crew's task queue"""
        self.tasks.append(task)
        self.execution_log.append(f"Task added: {task.description}")
        logger.info(f"Task added to crew '{self.config.name}': {task.description}")
        return task
    
    async def execute_sequential(self) -> Dict:
        """Execute all tasks sequentially"""
        self.execution_log.append(f"Starting sequential execution at {datetime.now()}")
        results = []
        
        for task in self.tasks:
            # Check dependencies
            if task.dependencies:
                for dep_id in task.dependencies:
                    dep_task = next((t for t in self.tasks if t.id == dep_id), None)
                    if dep_task and dep_task.status != "completed":
                        self.execution_log.append(f"Task {task.id} waiting for dependency {dep_id}")
                        continue
            
            result = await task.execute(context=self.shared_memory)
            results.append(result)
            self.task_history.append(result)
            
            self.shared_memory[f"task_{task.id}"] = result
        
        return {
            "crew": self.config.name,
            "status": "completed",
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks if t.status == "completed"]),
            "results": results,
            "execution_time": (datetime.now() - self.created_at).total_seconds()
        }
    
    async def execute_parallel(self) -> Dict:
        """Execute all tasks in parallel"""
        self.execution_log.append(f"Starting parallel execution at {datetime.now()}")
        
        async def execute_task_wrapper(task: Task):
            return await task.execute(context=self.shared_memory)
        
        tasks_to_execute = [execute_task_wrapper(task) for task in self.tasks]
        results = await asyncio.gather(*tasks_to_execute, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.task_history.append({"error": str(result)})
            else:
                self.task_history.append(result)
                self.shared_memory[f"task_{self.tasks[i].id}"] = result
        
        return {
            "crew": self.config.name,
            "status": "completed",
            "total_tasks": len(self.tasks),
            "completed_tasks": len([r for r in results if not isinstance(r, Exception)]),
            "results": [r for r in results if not isinstance(r, Exception)],
            "execution_time": (datetime.now() - self.created_at).total_seconds()
        }
    
    async def execute_hierarchical(self) -> Dict:
        """Execute tasks in hierarchical mode with manager agent"""
        if not self.config.manager_agent:
            logger.error("Hierarchical mode requires a manager agent")
            return {"status": "error", "message": "Manager agent not configured"}
        
        self.execution_log.append(f"Starting hierarchical execution at {datetime.now()}")
        
        manager = self.config.manager_agent
        self.execution_log.append(f"Manager agent: {manager.name} ({manager.role.value})")
        
        results = []
        for task in self.tasks:
            result = await task.execute(context=self.shared_memory)
            results.append(result)
        
        return {
            "crew": self.config.name,
            "manager": manager.name,
            "status": "completed",
            "results": results,
            "execution_time": (datetime.now() - self.created_at).total_seconds()
        }
    
    async def execute(self) -> Dict:
        """Execute crew based on configured mode"""
        try:
            if self.config.hierarchical_mode:
                return await self.execute_hierarchical()
            elif self.config.async_execution:
                return await self.execute_parallel()
            else:
                return await self.execute_sequential()
        except Exception as e:
            logger.error(f"Crew execution failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_status(self) -> Dict:
        """Get current crew status"""
        return {
            "name": self.config.name,
            "agents": len(self.agents),
            "tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks if t.status == "completed"]),
            "shared_memory_size": len(self.shared_memory),
            "execution_log_entries": len(self.execution_log),
            "uptime": (datetime.now() - self.created_at).total_seconds()
        }


class CrewManager:
    """
    Manages multiple CrewAI crews
    Coordinates crews, handles inter-crew communication
    """
    
    def __init__(self):
        self.crews: Dict[str, Crew] = {}
        self.global_memory: Dict[str, Any] = {}
        self.execution_history: List[Dict] = []
        
    def create_crew(self, config: CrewConfig) -> Crew:
        """Create a new crew"""
        crew = Crew(config)
        self.crews[config.name] = crew
        logger.info(f"Crew created: {config.name}")
        return crew
    
    def get_crew(self, crew_name: str) -> Optional[Crew]:
        """Get a crew by name"""
        return self.crews.get(crew_name)
    
    async def execute_crew(self, crew_name: str) -> Dict:
        """Execute a specific crew"""
        crew = self.crews.get(crew_name)
        if not crew:
            return {"status": "error", "message": f"Crew '{crew_name}' not found"}
        
        result = await crew.execute()
        self.execution_history.append({
            "crew": crew_name,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        return result
    
    async def execute_all_crews(self) -> Dict:
        """Execute all crews in parallel"""
        tasks = [self.execute_crew(name) for name in self.crews.keys()]
        results = await asyncio.gather(*tasks)
        
        return {
            "status": "completed",
            "crews_executed": len(self.crews),
            "results": {name: result for name, result in zip(self.crews.keys(), results)},
            "timestamp": datetime.now().isoformat()
        }
    
    def get_global_status(self) -> Dict:
        """Get status of all crews"""
        return {
            "total_crews": len(self.crews),
            "crews": {name: crew.get_status() for name, crew in self.crews.items()},
            "global_memory_size": len(self.global_memory),
            "execution_history_entries": len(self.execution_history)
        }


def create_standard_crew(crew_name: str = "UniversalAI_Crew") -> Crew:
    """Factory function to create a standard crew with predefined agents"""
    
    config = CrewConfig(
        name=crew_name,
        description="Multi-agent crew for comprehensive analysis and decision-making",
        verbose=True,
        async_execution=True,
        memory_enabled=True,
        hierarchical_mode=False
    )
    
    crew = Crew(config)
    
    analyst = Agent(
        id="analyst_1",
        role=AgentRole.ANALYST,
        name="Data Analyst",
        goal="Analyze data and provide insights",
        backstory="Expert in data analysis with 10+ years experience"
    )
    
    strategist = Agent(
        id="strategist_1",
        role=AgentRole.STRATEGIST,
        name="Strategic Planner",
        goal="Develop comprehensive strategies",
        backstory="Strategic thinker with experience in multiple domains"
    )
    
    researcher = Agent(
        id="researcher_1",
        role=AgentRole.RESEARCHER,
        name="Research Specialist",
        goal="Conduct thorough research",
        backstory="Research expert with access to global knowledge"
    )
    
    synthesizer = Agent(
        id="synthesizer_1",
        role=AgentRole.SYNTHESIZER,
        name="Knowledge Synthesizer",
        goal="Synthesize information from multiple sources",
        backstory="Expert at connecting disparate information"
    )
    
    crew.add_agent(analyst)
    crew.add_agent(strategist)
    crew.add_agent(researcher)
    crew.add_agent(synthesizer)
    
    return crew
