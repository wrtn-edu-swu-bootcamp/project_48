"""
성능 모니터링 서비스
"""
import time
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import statistics

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """성능 메트릭 데이터"""
    operation: str
    duration: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PerformanceMonitor:
    """성능 모니터링 시스템"""
    
    def __init__(self):
        """모니터 초기화"""
        self.metrics: Dict[str, list] = defaultdict(list)
        self._max_samples = 1000  # 각 작업당 최대 샘플 수
    
    def record(self, operation: str, duration: float, metadata: Optional[Dict[str, Any]] = None):
        """성능 메트릭 기록"""
        metric = PerformanceMetrics(
            operation=operation,
            duration=duration,
            metadata=metadata or {}
        )
        
        self.metrics[operation].append(metric)
        
        # 최대 샘플 수 제한
        if len(self.metrics[operation]) > self._max_samples:
            self.metrics[operation].pop(0)
        
        # 느린 작업 경고
        if duration > 1.0:
            logger.warning(
                f"느린 작업 감지: {operation} - {duration:.2f}s",
                extra={"metadata": metadata}
            )
    
    def get_stats(self, operation: str) -> Optional[Dict[str, Any]]:
        """작업별 통계 조회"""
        if operation not in self.metrics or not self.metrics[operation]:
            return None
        
        durations = [m.duration for m in self.metrics[operation]]
        
        return {
            "operation": operation,
            "count": len(durations),
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "min": min(durations),
            "max": max(durations),
            "stdev": statistics.stdev(durations) if len(durations) > 1 else 0,
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """모든 작업의 통계 조회"""
        return {
            operation: self.get_stats(operation)
            for operation in self.metrics
            if self.get_stats(operation)
        }
    
    def reset(self, operation: Optional[str] = None):
        """메트릭 초기화"""
        if operation:
            self.metrics[operation] = []
        else:
            self.metrics.clear()
    
    def timer(self, operation: str, metadata: Optional[Dict[str, Any]] = None):
        """컨텍스트 매니저로 작업 시간 측정"""
        return _PerformanceTimer(self, operation, metadata)


class _PerformanceTimer:
    """성능 측정 컨텍스트 매니저"""
    
    def __init__(self, monitor: PerformanceMonitor, operation: str, metadata: Optional[Dict[str, Any]]):
        self.monitor = monitor
        self.operation = operation
        self.metadata = metadata
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.monitor.record(self.operation, duration, self.metadata)


# 전역 모니터 인스턴스
_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """성능 모니터 싱글톤 인스턴스 반환"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor
