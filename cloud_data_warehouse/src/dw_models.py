"""Cloud Data Warehouse Models Definition."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class DimCustomer:
    """Dimension: Customer (SCD Type 2)."""
    customer_id: str
    customer_key: int = 0  # Surrogate key
    name: str = ""
    email: str = ""
    segment: str = ""
    region: str = ""
    is_current: bool = True
    valid_from: datetime = field(default_factory=datetime.now)
    valid_to: Optional[datetime] = None

@dataclass
class DimProduct:
    """Dimension: Product (SCD Type 1)."""
    product_id: str
    product_key: int = 0
    name: str = ""
    category: str = ""
    subcategory: str = ""
    price: float = 0.0
    cost: float = 0.0

@dataclass
class FactSales:
    """Fact: Sales Transactions."""
    transaction_id: str
    date_key: int
    customer_key: int
    product_key: int
    amount: float
    quantity: int
    discount: float
    profit: float = 0.0

@dataclass
class AuditLog:
    """Audit: Pipeline Execution Log."""
    run_id: str
    table_name: str
    rows_processed: int
    rows_loaded: int
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
