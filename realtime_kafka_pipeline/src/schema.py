"""
Data schemas for Kafka messages
"""
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class StockTick:
    """Raw stock tick data"""
    symbol: str
    timestamp: str
    price: float
    volume: int
    change_percent: float
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StockTick':
        return cls(**data)


@dataclass
class ProcessedTick:
    """Processed stock tick with aggregations"""
    symbol: str
    timestamp: str
    price: float
    volume: int
    change_percent: float
    moving_avg_5: Optional[float] = None
    moving_avg_10: Optional[float] = None
    is_anomaly: bool = False
    anomaly_reason: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Alert:
    """Alert message for anomalies"""
    alert_id: str
    symbol: str
    timestamp: str
    alert_type: str
    severity: str
    message: str
    current_price: float
    threshold_exceeded: float
    
    def to_dict(self) -> dict:
        return asdict(self)
