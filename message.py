from dataclasses import dataclass
from event import Event
from dataclasses import dataclass


@dataclass
class Message(Event):
    text: str