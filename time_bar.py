from dataclasses import dataclass
from bar import Bar
from time_unit import TimeUnit

@dataclass
class TimeBar(Bar):
    num_time_units: int
    time_unit: TimeUnit

