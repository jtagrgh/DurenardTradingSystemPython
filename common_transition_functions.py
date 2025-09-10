from typing import Any
from market_update import MarketUpdate

def none(_: Any) -> None:
    pass

def never(_: Any) -> bool:
    return False

def price (event: MarketUpdate) -> float:
    return event.price
