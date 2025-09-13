from dataclasses import dataclass
from bar import Bar

@dataclass
class TickBar(Bar):
    num_ticks: int
