from dataclasses import dataclass
from transition import Transition
from event import Event
from typing import Any


@dataclass(kw_only=True)
class FSM():
    current_state: str
    transitions: list[Transition[Any,Any]]

    def operate_fsm(self, event: Event) -> None:
        applicable_transitions = [t for t in self.transitions if t.initial_state == self.current_state]
        effected_transition = [t for t in applicable_transitions if t.perform(event)][0]
        effected_transition.actuator(effected_transition.sensor(event))
        self.current_state = effected_transition.final_state
        
