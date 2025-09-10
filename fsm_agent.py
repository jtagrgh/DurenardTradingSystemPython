from dataclasses import dataclass
from event import Event
from fsm import FSM
from agent import Agent
from market_update import MarketUpdate


@dataclass(kw_only=True)
class FSMAgent(FSM, Agent):
    states: list[str]

    def set_fsm(self) -> None:
        pass

    def update_main(self, event: Event) -> None:
        self.set_fsm()

        match(event):
            case MarketUpdate():
                self.operate_fsm(event)
                self.states.append(self.current_state)
            case _:
                pass
            