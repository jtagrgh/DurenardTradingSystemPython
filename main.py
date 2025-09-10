from event import Event
from agent import Agent
from simple_model_comm import SimpleModelComm
from market_update import MarketUpdate
from datetime import datetime


events: list[Event] = [
    MarketUpdate(datetime.now(), 'AAPL', 0),
    MarketUpdate(datetime.now(), 'TSLA', 0),

    MarketUpdate(datetime.now(), 'AAPL', 1),
    MarketUpdate(datetime.now(), 'TSLA', -1),

    MarketUpdate(datetime.now(), 'AAPL', 2),
    MarketUpdate(datetime.now(), 'TSLA', -2),

    MarketUpdate(datetime.now(), 'AAPL', 2),
    MarketUpdate(datetime.now(), 'TSLA', 1),

    MarketUpdate(datetime.now(), 'AAPL', 2),
    MarketUpdate(datetime.now(), 'TSLA', 1),

    MarketUpdate(datetime.now(), 'AAPL', 2),
    MarketUpdate(datetime.now(), 'TSLA', 1),

    MarketUpdate(datetime.now(), 'AAPL', -4),
    MarketUpdate(datetime.now(), 'TSLA', 1),
]

events = events[::-1]

a1 = SimpleModelComm(length=2, market='AAPL', events_queue=events, recipients_list=[])
a2 = SimpleModelComm(length=2, market='TSLA', events_queue=events, recipients_list=[])

a1.recipients_list.append(a2.name)
a2.recipients_list.append(a1.name)

agents: list[Agent] = [a1, a2]

while len(events) > 0:
    event = events.pop()
    for agent in agents:
        agent.consume(event)
    print()