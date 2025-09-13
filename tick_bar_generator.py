from dataclasses import dataclass, field
from typing import Optional
from event import Event
from fsm_agent import FSMAgent
from market_update import MarketUpdate
from transition import Transition
from common_transition_functions import price, always, never, none
from tick_bar import TickBar

@dataclass
class TickBarGenerator(FSMAgent):
    market: str
    length: int
    counter: int = 0
    buffer: list[float] = field(default_factory=list[float])
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None

    def __post_init__(self) -> None:
        self.states.append('EMIT')
        self.name = f'TickBarGenerator_{self.market}_{self.length}'

    def pre_process(self, event: Event) -> None:
        match(event):
            case MarketUpdate():
                self.positions.append(0)
                self.counter = len(self.buffer)
            case _:
                super().pre_process(event)

    def observe(self, event: Event) -> bool:
        match(event):
            case MarketUpdate():
                return self.market == event.security_name
            case _:
                return super().observe(event)

    def set_fsm(self) -> None:
        self.current_state = self.states[-1]

        TTransition = Transition[float,MarketUpdate]

        def calc_to_calc(p: float):
            self.close = p
            self.high = max(self.high, p) if self.high else p
            self.low = min(self.low, p) if self.low else p
            self.buffer.append(p)

        def calc_to_emit(p: float):
            if self.open and self.high and self.low and self.close:
                self.emit(data=TickBar(
                    timestamp=self.timestamps[-1],
                    security=self.market,
                    open=self.open,
                    high=self.high,
                    low=self.low,
                    close=self.close,
                    num_ticks=self.length
                ))

        def emit_to_calc(p: float):
            self.buffer.append(p)
            self.open = p
            self.high = p
            self.low = p
            self.close = p

        self.transitions = [
            TTransition(
                'CALC',
                'CALC',
                price,
                lambda p: self.counter < self.length,
                calc_to_calc
            ),
            TTransition(
                'CALC',
                'EMIT',
                price,
                lambda _: self.counter == self.length,
                calc_to_emit
            ),
            TTransition(
                'EMIT',
                'CALC',
                price,
                always,
                emit_to_calc
            ),
            TTransition(
                'EMIT',
                'EMIT',
                price,
                never,
                none
            )
        ]