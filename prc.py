from dataclasses import dataclass
from market_update import MarketUpdate


@dataclass
class PRC(MarketUpdate):
    volume: float

