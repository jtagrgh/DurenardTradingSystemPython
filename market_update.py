from event import Event
from dataclasses import dataclass


@dataclass
class MarketUpdate(Event):
    security_name: str
    price: float