from dataclasses import dataclass, field
from statistics import mean
from event import Event


@dataclass
class Bar(Event):
    security: str

    open: float
    high: float
    low: float
    close: float

    pivot: float = field(init=False)
    filled: bool = field(init=False)

    def __post_init__(self) -> None:
        self.pivot = mean((self.open, self.high, self.low, self.close))
        self.filled = self.close >= self.open

