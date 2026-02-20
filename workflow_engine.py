"""
Phase 4: Autonomous Workflow Engine
DAG-based task orchestration with dependencies, retries, and monitoring
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio
import uuid

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


@dataclass
class TaskResult:
    """Result of task execution"""
    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    retries: int = 0


@dataclass
class WorkflowTask:
    """Individual task in workflow"""
    id: str
    name: str
    func: Callable
    dependencies: List[str] = field(default_factory=list)
    retry_count: int = 3
    timeout_seconds: int = 300
    skip_on_failure: bool = False
    metadata: Dict = field(default_factory=dict)


@dataclass
class WorkflowDAG:
    """Directed Acyclic Graph of tasks"""
    id: str
    name: str
    tasks: Dict[str, WorkflowTask] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_task(self, task: WorkflowTask) -> WorkflowTask:
        """Add task to DAG"""
        self.tasks[task.id] = task
        logger.info("Task added to DAG", task_id=task.id, dag_id=self.id)
        return task
    
    def add_dependency(self, task_id: str, depends_on: str) -> bool:
        """Add dependency between tasks"""
        if task_id not in self.tasks or depends_on not in self.tasks:
            return False
        
        self.tasks[task_id].dependencies.append(depends_on)
        logger.info("Dependency added", task_id=task_id, depends_on=depends_on)
        return True
    
    def get_task_order(self) -> List[str]:
        """Topological sort to get execution order"""
        visited = set()
        result = []
        
        def visit(task_id: str):
            if task_id in visited:
                return
            visited.add(task_id)
            
            for dep in self.tasks[task_id].dependencies:
                visit(dep)
            
            result.append(task_id)
        
        for task_id in self.tasks:
            visit(task_id)
        
        return result
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate DAG for cycles and missing dependencies"""
        for task_id, task in self.tasks.items():
            for dep in task.dependencies:
                if dep not in self.tasks:
                    return False, f"Missing dependency: {dep} for task {task_id}"
        
        order = self.get_task_order()
        if len(order) != len(self.tasks):
            return False, "Circular dependency detected"
        
        return True, None


class WorkflowExecutor:
    """Execute workflow DAG"""
    
    def __init__(self):
        self.results: Dict[str, TaskResult] = {}
        self.execution_history: List[Dict] = []
    
    async def execute_task(self, task: WorkflowTask) -> TaskResult:
        """Execute single task with retries"""
        result = TaskResult(
            task_id=task.id,
            status=TaskStatus.PENDING,
            start_time=datetime.utcnow()
        )
        
        for attempt in range(task.retry_count):
            try:
                result.status = TaskStatus.RUNNING
                logger.info(
                    "Task starting",
                    task_id=task.id,
                    attempt=attempt + 1
                )
                
                if attempt > 0:
                    result.status = TaskStatus.RETRYING
                    await asyncio.sleep(2 ** attempt)
                
                task_coro = task.func()
                if asyncio.iscoroutine(task_coro):
                    result.result = await asyncio.wait_for(
                        task_coro,
                        timeout=task.timeout_seconds
                    )
                else:
                    result.result = task_coro
                
                result.status = TaskStatus.COMPLETED
                result.retries = attempt
                logger.info("Task completed", task_id=task.id, retries=attempt)
                break
            
            except asyncio.TimeoutError:
                result.error = f"Timeout after {task.timeout_seconds}s"
                logger.warning("Task timeout", task_id=task.id)
            
            except Exception as e:
                result.error = str(e)
                if attempt == task.retry_count - 1:
                    result.status = TaskStatus.FAILED
                    logger.error("Task failed", task_id=task.id, error=str(e))
        
        result.end_time = datetime.utcnow()
        result.duration_ms = (
            (result.end_time - result.start_time).total_seconds() * 1000
        )
        
        return result
    
    async def execute_dag(self, dag: WorkflowDAG) -> Dict[str, TaskResult]:
        """Execute entire workflow DAG"""
        valid, error = dag.validate()
        if not valid:
            logger.error("DAG validation failed", error=error)
            return {}
        
        execution_start = datetime.utcnow()
        logger.info("DAG execution starting", dag_id=dag.id, task_count=len(dag.tasks))
        
        task_order = dag.get_task_order()
        
        for task_id in task_order:
            task = dag.tasks[task_id]
            
            skip = False
            for dep in task.dependencies:
                if self.results[dep].status == TaskStatus.FAILED:
                    if not task.skip_on_failure:
                        skip = True
                        break
            
            if skip:
                result = TaskResult(
                    task_id=task.id,
                    status=TaskStatus.SKIPPED,
                    start_time=datetime.utcnow(),
                    end_time=datetime.utcnow()
                )
                logger.info("Task skipped", task_id=task.id)
            else:
                result = await self.execute_task(task)
            
            self.results[task_id] = result
        
        execution_end = datetime.utcnow()
        execution_duration = (execution_end - execution_start).total_seconds()
        
        completed = sum(1 for r in self.results.values() if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in self.results.values() if r.status == TaskStatus.FAILED)
        
        summary = {
            "dag_id": dag.id,
            "total_tasks": len(dag.tasks),
            "completed": completed,
            "failed": failed,
            "duration_seconds": execution_duration,
            "timestamp": execution_end.isoformat()
        }
        self.execution_history.append(summary)
        
        logger.info(
            "DAG execution completed",
            dag_id=dag.id,
            completed=completed,
            failed=failed,
            duration=execution_duration
        )
        
        return self.results
    
    def get_results(self, task_id: str) -> Optional[TaskResult]:
        """Get results for specific task"""
        return self.results.get(task_id)
    
    def get_execution_summary(self) -> Dict:
        """Get summary of all executions"""
        return {
            "total_executions": len(self.execution_history),
            "executions": self.execution_history[-10:]
        }


class WorkflowOrchestrator:
    """High-level workflow management"""
    
    def __init__(self):
        self.dags: Dict[str, WorkflowDAG] = {}
        self.executor = WorkflowExecutor()
    
    def create_workflow(self, name: str) -> WorkflowDAG:
        """Create new workflow"""
        dag = WorkflowDAG(
            id=str(uuid.uuid4()),
            name=name
        )
        self.dags[dag.id] = dag
        logger.info("Workflow created", dag_id=dag.id, name=name)
        return dag
    
    def get_workflow(self, dag_id: str) -> Optional[WorkflowDAG]:
        """Get workflow by ID"""
        return self.dags.get(dag_id)
    
    async def execute_workflow(self, dag_id: str) -> Dict[str, TaskResult]:
        """Execute workflow"""
        dag = self.dags.get(dag_id)
        if not dag:
            logger.error("Workflow not found", dag_id=dag_id)
            return {}
        
        return await self.executor.execute_dag(dag)
    
    def list_workflows(self) -> List[Dict]:
        """List all workflows"""
        return [
            {
                "id": dag.id,
                "name": dag.name,
                "task_count": len(dag.tasks),
                "created_at": dag.created_at.isoformat()
            }
            for dag in self.dags.values()
        ]


global_workflow_orchestrator = WorkflowOrchestrator()
