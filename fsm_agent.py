from dataclasses import dataclass
from event import Event
from fsm import FSM
from agent import Agent
from market_update import MarketUpdate


@dataclass
class FSMAgent(FSM, Agent):
    states: list[str]

    def set_fsm(self) -> None:
        pass

    def update_main(self, event: Event) -> None:
        match(event):
            case MarketUpdate():
                self.set_fsm()
                self.operate_fsm(event)
                self.states.append(self.current_state)
            case _:
                pass