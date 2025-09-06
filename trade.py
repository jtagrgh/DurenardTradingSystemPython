from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    timestamp: datetime
    price: float
    quantity: float
