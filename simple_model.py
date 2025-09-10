from dataclasses import dataclass, field
from event import Event
from fsm_agent import FSMAgent
from market_update import MarketUpdate
from statistics import mean
from transition import Transition
from common_transition_functions import *


def price(event: MarketUpdate) -> float:
    return event.price


@dataclass(kw_only=True)
class SimpleModel(FSMAgent):
    length: int
    counter: int = 0
    moving_average: float = 0
    name: str = field(init=False)
    transitions: list[Transition[float, MarketUpdate]] = field(init=False)
    states: list[str] = field(init=False)
    current_state: str = field(init=False)

    def __post_init__(self):
        self.name = f'simple_model_{self.length}'
        self.states = ['INIT']

    def pre_process(self, event: Event) -> None:
        match(event):
            case MarketUpdate():
                self.counter = len(self.reval_prices)
                self.moving_average = mean(self.reval_prices[-self.length:])
            case _:
                pass

    def post_process(self, event: Event) -> None:
        match(event):
            case MarketUpdate():
                print(f'Agent <{self.name}> consumed market update with price <{event.price}>')
            case _:
                pass

    def set_fsm(self) -> None:
        TTransition = Transition[float, MarketUpdate]
        self.current_state = self.states[0]
        self.transitions = [
            TTransition(
                initial_state='INIT',
                final_state='INIT',
                sensor=lambda e: e.price,
                predicate=lambda p: self.counter <= self.length,
                actuator=lambda p: self.positions.append(0)),
            TTransition(
                initial_state='INIT',
                final_state='LONG',
                sensor=lambda e: e.price,
                predicate=lambda p: self.counter > self.length and p > self.moving_average,
                actuator=lambda p: self.positions.append(1)
            ),
            TTransition(
                initial_state='INIT',
                final_state='SHORT',
                sensor=lambda e: e.price,
                predicate=lambda p: self.counter > self.length and p <= self.moving_average,
                actuator=lambda p: self.positions.append(-1)
            ),
            TTransition(
                initial_state='LONG',
                final_state='INIT',
                sensor=lambda e: e.price,
                predicate=never,
                actuator=none 
            ),
            TTransition(
                initial_state='LONG',
                final_state='LONG',
                sensor=lambda e: e.price,
                predicate=lambda p: p > self.moving_average,
                actuator=lambda p: self.positions.append(1)
            ),
            TTransition(
                initial_state='LONG',
                final_state='SHORT',
                sensor=lambda e: e.price,
                predicate=lambda p: p <= self.moving_average,
                actuator=lambda p: self.positions.append(-1)
            ),
            TTransition(
                initial_state='SHORT',
                final_state='INIT',
                sensor=lambda e: e.price,
                predicate=never,
                actuator=none
            ),
            TTransition(
                initial_state='SHORT',
                final_state='LONG',
                sensor=price,
                predicate=lambda p: p > self.moving_average,
                actuator=lambda p: self.positions.append(1)
            ),
            TTransition(
                initial_state='SHORT',
                final_state='SHORT',
                sensor=price,
                predicate=lambda p: p <= self.moving_average,
                actuator=lambda p: self.positions.append(-1)
            )
        ]

