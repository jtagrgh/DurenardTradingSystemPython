from dataclasses import dataclass
from event import Event
from dataclasses import dataclass
from typing import Any


@dataclass
class Message(Event):
    text: str
    originator: str
    recipients: list[str]
    data: Any = None
