"""
Phase 4: Advanced Anomaly Detection System
Real-time behavioral anomalies, statistical outliers, and pattern-based detection
"""

from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import math

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class StatisticalAnomalyDetector:
    """Detect anomalies using statistical methods (Z-score, IQR)"""
    
    def __init__(self, window_size: int = 100, z_threshold: float = 3.0):
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.data: Dict[str, list] = defaultdict(list)
    
    def add_observation(self, metric: str, value: float):
        """Add observation to metric"""
        self.data[metric].append(value)
        if len(self.data[metric]) > self.window_size:
            self.data[metric].pop(0)
    
    def is_anomaly_zscore(self, metric: str, value: float) -> Tuple[bool, float]:
        """Detect anomaly using Z-score"""
        if len(self.data[metric]) < 2:
            return False, 0.0
        
        mean = statistics.mean(self.data[metric])
        stdev = statistics.stdev(self.data[metric])
        
        if stdev == 0:
            return False, 0.0
        
        z_score = abs((value - mean) / stdev)
        is_anomaly = z_score > self.z_threshold
        
        return is_anomaly, z_score
    
    def is_anomaly_iqr(self, metric: str, value: float) -> Tuple[bool, float]:
        """Detect anomaly using Interquartile Range"""
        if len(self.data[metric]) < 4:
            return False, 0.0
        
        sorted_data = sorted(self.data[metric])
        q1 = sorted_data[len(sorted_data) // 4]
        q3 = sorted_data[3 * len(sorted_data) // 4]
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        is_anomaly = value < lower_bound or value > upper_bound
        distance = min(abs(value - lower_bound), abs(value - upper_bound))
        
        return is_anomaly, distance


class BehavioralAnomalyDetector:
    """Detect behavioral anomalies based on pattern analysis"""
    
    def __init__(self):
        self.patterns: Dict[str, Dict] = defaultdict(lambda: {"normal": [], "anomalies": []})
        self.behavior_baseline: Dict[str, float] = {}
        self.deviation_threshold = 0.3  # 30% deviation
    
    def learn_pattern(self, entity: str, behavior: str, frequency: float):
        """Learn normal behavior pattern"""
        if entity not in self.behavior_baseline:
            self.behavior_baseline[entity] = frequency
        
        self.patterns[entity]["normal"].append({
            "behavior": behavior,
            "frequency": frequency,
            "timestamp": datetime.utcnow()
        })
    
    def detect_behavior_anomaly(self, entity: str, behavior: str, frequency: float) -> Tuple[bool, float]:
        """Detect anomalous behavior"""
        if entity not in self.behavior_baseline:
            return False, 0.0
        
        baseline = self.behavior_baseline[entity]
        deviation = abs(frequency - baseline) / baseline if baseline != 0 else 0
        
        is_anomaly = deviation > self.deviation_threshold
        
        if is_anomaly:
            self.patterns[entity]["anomalies"].append({
                "behavior": behavior,
                "frequency": frequency,
                "deviation": deviation,
                "timestamp": datetime.utcnow()
            })
            logger.warning(
                "Behavioral anomaly detected",
                entity=entity,
                behavior=behavior,
                deviation=deviation
            )
        
        return is_anomaly, deviation


class TimeSeriesAnomalyDetector:
    """Detect anomalies in time series data"""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.timeseries: Dict[str, list] = defaultdict(list)
    
    def add_point(self, metric: str, value: float):
        """Add time series point"""
        self.timeseries[metric].append(value)
        if len(self.timeseries[metric]) > self.window_size * 2:
            self.timeseries[metric].pop(0)
    
    def detect_spike(self, metric: str) -> Tuple[bool, float]:
        """Detect spike in time series"""
        if len(self.timeseries[metric]) < self.window_size:
            return False, 0.0
        
        recent = self.timeseries[metric][-1]
        historical = self.timeseries[metric][:-1]
        
        mean = statistics.mean(historical)
        stdev = statistics.stdev(historical) if len(historical) > 1 else 0
        
        if stdev == 0:
            return False, 0.0
        
        spike_magnitude = (recent - mean) / stdev
        
        return abs(spike_magnitude) > 2.5, abs(spike_magnitude)
    
    def detect_trend_change(self, metric: str) -> Tuple[bool, float]:
        """Detect change in trend"""
        if len(self.timeseries[metric]) < self.window_size:
            return False, 0.0
        
        recent = self.timeseries[metric][-self.window_size:]
        previous = self.timeseries[metric][-2*self.window_size:-self.window_size]
        
        recent_trend = statistics.mean(recent)
        previous_trend = statistics.mean(previous)
        
        if previous_trend == 0:
            change = 0.0
        else:
            change = abs((recent_trend - previous_trend) / previous_trend)
        
        return change > 0.25, change


class AnomalyDetectionSystem:
    """Unified anomaly detection system"""
    
    def __init__(self):
        self.statistical = StatisticalAnomalyDetector()
        self.behavioral = BehavioralAnomalyDetector()
        self.timeseries = TimeSeriesAnomalyDetector()
        
        self.detection_results: List[Dict] = []
        self.anomaly_count = 0
    
    def check_for_anomalies(
        self,
        metric: str,
        value: float,
        entity: Optional[str] = None,
        behavior: Optional[str] = None
    ) -> Dict:
        """Check metric for anomalies using all detectors"""
        results = {
            "metric": metric,
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "anomalies_detected": [],
            "risk_score": 0.0
        }
        
        risk_score = 0.0
        
        self.statistical.add_observation(metric, value)
        is_anomaly_z, z_score = self.statistical.is_anomaly_zscore(metric, value)
        if is_anomaly_z:
            results["anomalies_detected"].append({
                "type": "statistical_zscore",
                "score": z_score
            })
            risk_score += min(0.5, z_score / 10)
        
        is_anomaly_iqr, iqr_distance = self.statistical.is_anomaly_iqr(metric, value)
        if is_anomaly_iqr:
            results["anomalies_detected"].append({
                "type": "statistical_iqr",
                "distance": iqr_distance
            })
            risk_score += 0.3
        
        if entity and behavior:
            self.behavioral.learn_pattern(entity, behavior, value)
        
        self.timeseries.add_point(metric, value)
        is_spike, magnitude = self.timeseries.detect_spike(metric)
        if is_spike:
            results["anomalies_detected"].append({
                "type": "spike",
                "magnitude": magnitude
            })
            risk_score += 0.4
        
        is_trend_change, change = self.timeseries.detect_trend_change(metric)
        if is_trend_change:
            results["anomalies_detected"].append({
                "type": "trend_change",
                "change_percentage": change * 100
            })
            risk_score += 0.2
        
        results["risk_score"] = min(1.0, risk_score)
        
        if results["anomalies_detected"]:
            self.anomaly_count += 1
            logger.warning(
                "Anomalies detected",
                metric=metric,
                count=len(results["anomalies_detected"]),
                risk_score=results["risk_score"]
            )
        
        self.detection_results.append(results)
        return results
    
    def get_anomaly_summary(self) -> Dict:
        """Get summary of detected anomalies"""
        return {
            "total_anomalies": self.anomaly_count,
            "total_checks": len(self.detection_results),
            "anomaly_rate": self.anomaly_count / max(1, len(self.detection_results))
        }


global_anomaly_detector = AnomalyDetectionSystem()
