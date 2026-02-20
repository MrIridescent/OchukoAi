"""
Per-Subsystem Health Monitoring
Real-time status tracking, alerting, and metrics
Detailed component health with recovery actions
"""

from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class HealthStatus(Enum):
    """Health status levels"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


@dataclass
class HealthMetric:
    """Health metric for a component"""
    name: str
    status: HealthStatus
    last_check: datetime
    check_interval_seconds: int
    error_message: Optional[str] = None
    recovery_attempted: bool = False
    metrics: Dict[str, Any] = None


class SubsystemMonitor:
    """Monitor for a single subsystem"""
    
    def __init__(
        self,
        name: str,
        check_interval: int = 10,
        failure_threshold: int = 3
    ):
        self.name = name
        self.check_interval = check_interval
        self.failure_threshold = failure_threshold
        self.status = HealthStatus.HEALTHY
        self.last_check = datetime.utcnow()
        self.consecutive_failures = 0
        self.check_history: list = []
        self.recovery_actions: list = []
    
    async def check_health(self, check_func: Callable) -> HealthMetric:
        """Run health check"""
        try:
            result = await check_func() if hasattr(check_func, '__await__') else check_func()
            
            self.consecutive_failures = 0
            self.status = HealthStatus.HEALTHY
            
            self.check_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pass",
                "result": result
            })
            
            logger.debug(f"Health check passed: {self.name}")
            
            return HealthMetric(
                name=self.name,
                status=HealthStatus.HEALTHY,
                last_check=datetime.utcnow(),
                check_interval_seconds=self.check_interval,
                metrics=result
            )
        
        except Exception as e:
            self.consecutive_failures += 1
            error_msg = str(e)
            
            self.check_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "status": "fail",
                "error": error_msg
            })
            
            if self.consecutive_failures >= self.failure_threshold:
                self.status = HealthStatus.CRITICAL
                logger.critical(f"Health check CRITICAL: {self.name} - {error_msg}")
            elif self.consecutive_failures >= 2:
                self.status = HealthStatus.UNHEALTHY
                logger.error(f"Health check FAILED: {self.name} - {error_msg}")
            else:
                self.status = HealthStatus.DEGRADED
                logger.warning(f"Health check DEGRADED: {self.name} - {error_msg}")
            
            return HealthMetric(
                name=self.name,
                status=self.status,
                last_check=datetime.utcnow(),
                check_interval_seconds=self.check_interval,
                error_message=error_msg
            )
    
    async def attempt_recovery(self, recovery_func: Callable) -> bool:
        """Attempt to recover subsystem"""
        try:
            logger.info(f"Attempting recovery for {self.name}")
            
            result = await recovery_func() if hasattr(recovery_func, '__await__') else recovery_func()
            
            self.consecutive_failures = 0
            self.status = HealthStatus.HEALTHY
            
            self.recovery_actions.append({
                "timestamp": datetime.utcnow().isoformat(),
                "action": "recovery",
                "result": "success"
            })
            
            logger.info(f"Recovery succeeded for {self.name}")
            return True
        
        except Exception as e:
            logger.error(f"Recovery failed for {self.name}: {str(e)}")
            
            self.recovery_actions.append({
                "timestamp": datetime.utcnow().isoformat(),
                "action": "recovery",
                "result": "failed",
                "error": str(e)
            })
            
            return False


class HealthMonitoringSystem:
    """
    System-wide health monitoring:
    - Per-subsystem health checks
    - Automatic recovery attempts
    - Health dashboards
    - Alert generation
    - Historical tracking
    """
    
    def __init__(self):
        self.monitors: Dict[str, SubsystemMonitor] = {}
        self.last_overall_check = datetime.utcnow()
        self.check_history: list = []
        
        logger.info("HealthMonitoringSystem initialized")
    
    def register_subsystem(
        self,
        name: str,
        check_interval: int = 10
    ) -> SubsystemMonitor:
        """Register a subsystem for monitoring"""
        monitor = SubsystemMonitor(name, check_interval)
        self.monitors[name] = monitor
        
        logger.info(f"Subsystem registered: {name}")
        return monitor
    
    async def check_all_subsystems(self) -> Dict[str, HealthMetric]:
        """Check health of all subsystems"""
        results = {}
        
        for name, monitor in self.monitors.items():
            metric = HealthMetric(
                name=name,
                status=monitor.status,
                last_check=monitor.last_check,
                check_interval_seconds=monitor.check_interval
            )
            results[name] = metric
        
        overall_status = self._calculate_overall_status(results)
        
        self.check_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "subsystems": len(results),
            "overall_status": overall_status.value,
            "results": {k: {"status": v.status.value} for k, v in results.items()}
        })
        
        logger.info(
            "System health check completed",
            overall_status=overall_status.value,
            subsystems=len(results)
        )
        
        return results
    
    def _calculate_overall_status(self, results: Dict[str, HealthMetric]) -> HealthStatus:
        """Calculate overall system status"""
        if any(m.status == HealthStatus.CRITICAL for m in results.values()):
            return HealthStatus.CRITICAL
        elif any(m.status == HealthStatus.UNHEALTHY for m in results.values()):
            return HealthStatus.UNHEALTHY
        elif any(m.status == HealthStatus.DEGRADED for m in results.values()):
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY
    
    async def get_health_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive health dashboard"""
        all_checks = await self.check_all_subsystems()
        overall = self._calculate_overall_status(all_checks)
        
        dashboard = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": overall.value,
            "subsystems": {
                name: {
                    "status": metric.status.value,
                    "last_check": metric.last_check.isoformat(),
                    "error": metric.error_message
                }
                for name, metric in all_checks.items()
            },
            "check_history_size": len(self.check_history),
            "last_successful_check": self.last_overall_check.isoformat()
        }
        
        return dashboard
    
    async def generate_alert(self, subsystem: str, status: HealthStatus):
        """Generate alert for subsystem status change"""
        if status in (HealthStatus.UNHEALTHY, HealthStatus.CRITICAL):
            logger.critical(
                f"Health alert: {subsystem} is {status.value}",
                subsystem=subsystem,
                alert_level="critical"
            )
