"""
Performance Metrics Tracker for AI Video Production System.

Provides detailed performance tracking for agent executions,
API calls, and workflow operations with statistical analysis.
"""

import time
import statistics
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import json
from pathlib import Path

from backend.core.config import get_settings


@dataclass
class MetricDataPoint:
    """Single metric data point."""
    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricStats:
    """Statistical summary of metric data."""
    count: int
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    p95: float  # 95th percentile
    p99: float  # 99th percentile


class PerformanceMetrics:
    """Tracks and analyzes performance metrics."""
    
    def __init__(self):
        self.settings = get_settings()
        self.metrics: Dict[str, List[MetricDataPoint]] = defaultdict(list)
        self._timers: Dict[str, float] = {}
    
    def record(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        Record a metric value.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            labels: Optional labels for metric categorization
        """
        data_point = MetricDataPoint(
            timestamp=datetime.now(),
            value=value,
            labels=labels or {}
        )
        self.metrics[metric_name].append(data_point)
    
    def start_timer(self, timer_name: str):
        """Start a named timer."""
        self._timers[timer_name] = time.time()
    
    def stop_timer(self, timer_name: str, labels: Optional[Dict[str, str]] = None) -> float:
        """
        Stop a named timer and record the duration.
        
        Args:
            timer_name: Name of the timer
            labels: Optional labels
        
        Returns:
            Duration in milliseconds
        """
        if timer_name not in self._timers:
            raise ValueError(f"Timer {timer_name} not started")
        
        start_time = self._timers.pop(timer_name)
        duration_ms = (time.time() - start_time) * 1000
        
        self.record(f"{timer_name}_duration_ms", duration_ms, labels)
        return duration_ms
    
    def get_stats(self, metric_name: str) -> Optional[MetricStats]:
        """
        Get statistical summary for a metric.
        
        Args:
            metric_name: Name of the metric
        
        Returns:
            Statistical summary or None if no data
        """
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return None
        
        values = [dp.value for dp in self.metrics[metric_name]]
        
        if len(values) < 2:
            # Not enough data for statistics
            return MetricStats(
                count=len(values),
                mean=values[0] if values else 0.0,
                median=values[0] if values else 0.0,
                std_dev=0.0,
                min_value=values[0] if values else 0.0,
                max_value=values[0] if values else 0.0,
                p95=values[0] if values else 0.0,
                p99=values[0] if values else 0.0
            )
        
        sorted_values = sorted(values)
        
        return MetricStats(
            count=len(values),
            mean=statistics.mean(values),
            median=statistics.median(values),
            std_dev=statistics.stdev(values),
            min_value=min(values),
            max_value=max(values),
            p95=sorted_values[int(len(sorted_values) * 0.95)],
            p99=sorted_values[int(len(sorted_values) * 0.99)]
        )
    
    def get_recent(self, metric_name: str, limit: int = 10) -> List[MetricDataPoint]:
        """Get recent metric data points."""
        if metric_name not in self.metrics:
            return []
        return self.metrics[metric_name][-limit:]
    
    def export_metrics(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Export all metrics with statistics.
        
        Args:
            output_path: Optional path to save metrics JSON
        
        Returns:
            Dictionary of metrics data
        """
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "metrics": {}
        }
        
        for metric_name, data_points in self.metrics.items():
            stats = self.get_stats(metric_name)
            export_data["metrics"][metric_name] = {
                "count": len(data_points),
                "stats": {
                    "mean": stats.mean if stats else 0,
                    "median": stats.median if stats else 0,
                    "std_dev": stats.std_dev if stats else 0,
                    "min": stats.min_value if stats else 0,
                    "max": stats.max_value if stats else 0,
                    "p95": stats.p95 if stats else 0,
                    "p99": stats.p99 if stats else 0
                } if stats else None,
                "recent_values": [dp.value for dp in self.get_recent(metric_name, 20)]
            }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data
    
    def clear(self):
        """Clear all metrics data."""
        self.metrics.clear()
        self._timers.clear()


# Global metrics instance
_metrics_instance: Optional[PerformanceMetrics] = None


def get_metrics() -> PerformanceMetrics:
    """Get or create global metrics instance."""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = PerformanceMetrics()
    return _metrics_instance


def reset_metrics():
    """Reset global metrics instance."""
    global _metrics_instance
    if _metrics_instance:
        _metrics_instance.clear()
