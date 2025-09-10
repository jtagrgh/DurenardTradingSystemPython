from dataclasses import dataclass
from event import Event
from simple_model import SimpleModel
from market_update import MarketUpdate
from message import Message
from transition import Transition
from common_transition_functions import price,never,none


@dataclass(kw_only=True)
class SimpleModelComm(SimpleModel):
    market: str
    unblock_short: int = -1
    unblock_long: int = 1

    def __post_init__(self):
        super().__post_init__()
        self.name += f'_{self.market}'
        self.emit('INIT')

    def pre_process(self, event: Event) -> None:
        match(event):
            case Message():
                if event.text == 'INIT':
                    self.unblock_short, self.unblock_long = (0,0)
                elif event.text == 'LONG':
                    self.unblock_short, self.unblock_long = (-1,0)
                elif event.text == 'SHORT':
                    self.unblock_short, self.unblock_long = (0,1)
                else:
                    pass
            case _:
                super().pre_process(event)

    def observe(self, event: Event) -> bool:
        match(event):
            case MarketUpdate():
                return event.security_name == self.market
            case _:
                return super().observe(event)

    def to_long_actuator(self) -> None:
        self.positions.append(self.unblock_long)
        self.emit('LONG')

    def to_short_actuator(self) -> None:
        self.positions.append(self.unblock_short)
        self.emit('SHORT')

    def set_fsm(self) -> None:
        self.current_state = self.states[0]
        self.transitions = [
            Transition[float,MarketUpdate](
                initial_state='INIT',
                final_state='INIT',
                sensor=price,
                predicate=lambda p: self.counter <= self.length,
                actuator=lambda p: self.positions.append(0)
            ),
            Transition[float,MarketUpdate](
                initial_state='INIT',
                final_state='LONG',
                sensor=price,
                predicate=lambda p: self.counter > self.length and p > self.moving_average,
                actuator=lambda p: self.to_long_actuator()
            ),
            Transition[float,MarketUpdate](
                initial_state='INIT',
                final_state='SHORT',
                sensor=price,
                predicate=lambda p: self.counter > self.length and p <= self.moving_average,
                actuator=lambda p: self.to_short_actuator()
            ),
            Transition[float,MarketUpdate](
                initial_state='LONG',
                final_state='INIT',
                sensor=price,
                predicate=never,
                actuator=none
            ),
            Transition[float,MarketUpdate](
                initial_state='LONG',
                final_state='LONG',
                sensor=price,
                predicate=lambda p: p > self.moving_average,
                actuator=lambda p: self.positions.append(self.unblock_long)
            ),
            Transition[float,MarketUpdate](
                initial_state='LONG',
                final_state='SHORT',
                sensor=price,
                predicate=lambda p: p <= self.moving_average,
                actuator=lambda p: self.to_short_actuator()
            ),
            Transition[float,MarketUpdate](
                initial_state='SHORT',
                final_state='INIT',
                sensor=price,
                predicate=never,
                actuator=none
            ),
            Transition[float,MarketUpdate](
                initial_state='SHORT',
                final_state='LONG',
                sensor=price,
                predicate=lambda p: p > self.moving_average,
                actuator=lambda p: self.to_long_actuator()
            ),
            Transition[float,MarketUpdate](
                initial_state='SHORT',
                final_state='SHORT',
                sensor=price,
                predicate=lambda p: p <= self.moving_average,
                actuator=lambda p: self.positions.append(self.unblock_short)
            )
        ]
            
    

