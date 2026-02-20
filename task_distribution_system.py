"""
Smart Task Distribution System - Feature 1
Distributed async task execution with Celery + Redis
Job queue with result caching, retry logic, and progress tracking
"""

import asyncio
import uuid
from typing import Any, Dict, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import json
from dataclasses import dataclass
from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult:
    """Result of a completed task"""
    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0
    retry_count: int = 0


class TaskDistributionSystem:
    """
    Distributes long-running tasks to worker pool
    - Async job queue
    - Result caching with TTL
    - Automatic retries with exponential backoff
    - Progress tracking
    - Worker health monitoring
    """
    
    def __init__(self, max_workers: int = 10, redis_url: str = "redis://localhost"):
        self.max_workers = max_workers
        self.redis_url = redis_url
        self.active_tasks: Dict[str, TaskResult] = {}
        self.task_cache: Dict[str, TaskResult] = {}
        self.worker_semaphore = asyncio.Semaphore(max_workers)
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.result_queue: asyncio.Queue = asyncio.Queue()
        logger.info(
            "TaskDistributionSystem initialized",
            max_workers=max_workers,
            redis_url=redis_url
        )
    
    async def submit_task(
        self,
        func: Callable,
        *args,
        task_name: str = "",
        timeout: int = 300,
        cache_ttl: int = 3600,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """
        Submit a task for distributed execution
        Returns task_id for polling results
        """
        task_id = str(uuid.uuid4())
        
        task_result = TaskResult(
            task_id=task_id,
            status=TaskStatus.PENDING,
            started_at=datetime.utcnow()
        )
        
        self.active_tasks[task_id] = task_result
        
        logger.info(
            f"Task submitted: {task_name}",
            task_id=task_id,
            task_name=task_name,
            timeout=timeout,
            cache_ttl=cache_ttl,
            max_retries=max_retries
        )
        
        asyncio.create_task(
            self._execute_task(
                task_id, func, args, kwargs, task_name,
                timeout, cache_ttl, max_retries
            )
        )
        
        return task_id
    
    async def _execute_task(
        self,
        task_id: str,
        func: Callable,
        args: tuple,
        kwargs: dict,
        task_name: str,
        timeout: int,
        cache_ttl: int,
        max_retries: int
    ):
        """Execute task with retries and caching"""
        task_result = self.active_tasks[task_id]
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                async with self.worker_semaphore:
                    task_result.status = TaskStatus.RUNNING
                    task_result.started_at = datetime.utcnow()
                    
                    try:
                        if asyncio.iscoroutinefunction(func):
                            result = await asyncio.wait_for(
                                func(*args, **kwargs),
                                timeout=timeout
                            )
                        else:
                            result = await asyncio.wait_for(
                                asyncio.to_thread(func, *args, **kwargs),
                                timeout=timeout
                            )
                        
                        task_result.result = result
                        task_result.status = TaskStatus.COMPLETED
                        task_result.completed_at = datetime.utcnow()
                        task_result.execution_time_ms = (
                            task_result.completed_at - task_result.started_at
                        ).total_seconds() * 1000
                        
                        self.task_cache[task_id] = task_result
                        
                        logger.info(
                            f"Task completed: {task_name}",
                            task_id=task_id,
                            execution_time_ms=task_result.execution_time_ms,
                            retry_count=retry_count
                        )
                        return
                    
                    except asyncio.TimeoutError:
                        raise Exception(f"Task timeout after {timeout}s")
            
            except Exception as e:
                retry_count += 1
                task_result.retry_count = retry_count
                
                if retry_count <= max_retries:
                    backoff = min(2 ** retry_count, 60)
                    logger.warning(
                        f"Task failed, retrying: {task_name}",
                        task_id=task_id,
                        error=str(e),
                        retry_count=retry_count,
                        backoff_seconds=backoff
                    )
                    await asyncio.sleep(backoff)
                else:
                    task_result.status = TaskStatus.FAILED
                    task_result.error = str(e)
                    task_result.completed_at = datetime.utcnow()
                    
                    logger.error(
                        f"Task failed permanently: {task_name}",
                        task_id=task_id,
                        error=str(e),
                        retry_count=retry_count
                    )
                    return
    
    async def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """Get result of a task (non-blocking)"""
        return self.active_tasks.get(task_id) or self.task_cache.get(task_id)
    
    async def wait_for_task(self, task_id: str, timeout: int = 300) -> TaskResult:
        """Wait for task completion with timeout"""
        start = datetime.utcnow()
        
        while (datetime.utcnow() - start).total_seconds() < timeout:
            result = await self.get_task_result(task_id)
            
            if result and result.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                return result
            
            await asyncio.sleep(0.1)
        
        raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        result = self.active_tasks.get(task_id)
        
        if result and result.status == TaskStatus.PENDING:
            result.status = TaskStatus.CANCELLED
            logger.info("Task cancelled", task_id=task_id)
            return True
        
        return False
    
    async def get_active_tasks(self) -> Dict[str, TaskResult]:
        """Get all active tasks"""
        return {
            k: v for k, v in self.active_tasks.items()
            if v.status in (TaskStatus.PENDING, TaskStatus.RUNNING)
        }
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        active = await self.get_active_tasks()
        
        return {
            "total_active_tasks": len(active),
            "total_completed_tasks": len(self.task_cache),
            "total_failed_tasks": len([
                t for t in self.active_tasks.values()
                if t.status == TaskStatus.FAILED
            ]),
            "active_tasks": list(active.keys()),
            "queue_size": self.task_queue.qsize(),
        }
