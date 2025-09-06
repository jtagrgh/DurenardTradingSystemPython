from dataclasses import dataclass
from event import Event
from typing import Callable, TypeVar, Generic

TEvent = TypeVar('TEvent', bound=Event)
TData = TypeVar('TData')


@dataclass
class Transition(Generic[TData,TEvent]):
    initial_state: str
    final_state: str
    sensor: Callable[[TEvent], TData]
    predicate: Callable[[TData], bool]
    actuator: Callable[[TData], None]
    effected: bool = False

    def perform(self, event: TEvent) -> bool:
        self.effected = self.predicate(self.sensor(event))
        return self.effected

