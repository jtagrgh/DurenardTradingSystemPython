from datetime import datetime
from dataclasses import dataclass, field
from message import Message
from market_update import MarketUpdate
from event import Event
from trade import Trade
from typing import Callable
from trade_stat import TradeStat


@dataclass(kw_only=True)
class Agent():
    name: str
    events_queue: list[Event]
    recipients_list: list[str]

    slippage: Callable[[Event, float], float] = lambda e,p: 0
    compute_trade_states: Callable[[list[Trade]], TradeStat] = lambda x: TradeStat()
    timestamps: list[datetime] = field(default_factory=list[datetime])
    reval_prices: list[float] = field(default_factory=list[float])
    orders: list[float] = field(default_factory=list[float])
    positions: list[float] = field(default_factory=list[float])
    pls: list[float] = field(default_factory=list[float])
    fitnesses: list[float] = field(default_factory=list[float])
    trades: list[Trade] = field(default_factory=list[Trade])
    trade_stats: list[TradeStat] = field(default_factory=list[TradeStat])
    incoming_messages: list[Message] = field(default_factory=list[Message])
    outgoing_messages: list[Message] = field(default_factory=list[Message])

    def observe(self, event: Event) -> bool:
        return True
    
    def pre_process(self, event: Event) -> None:
        pass

    def post_process(self, event: Event) -> None:
        pass

    def update_before(self, event: Event) -> None:
        match(event):
            case MarketUpdate():
                if len(self.timestamps) == 0:
                    self.pls.append(0)
                    self.fitnesses.append(0)
                self.timestamps.append(event.timestamp)
                self.reval_prices.append(event.price)
            case _:
                pass

        self.pre_process(event)

    def update_main(self, event: Event) -> None:
        match(event):
            case MarketUpdate():
                self.positions.append(0)
            case _:
                pass

    def update_after(self, event: Event) -> None:
        match(event):
            case MarketUpdate():
                n_events = len(self.timestamps)
                last_position = self.positions[-1]
                prev_position = 0 if n_events < 2 else self.positions[-2]
                trade_quantity = prev_position - last_position
                last_price = self.reval_prices[-1]
                prev_price = 0 if n_events < 2 else self.reval_prices[-2]
                pl = 0 if n_events < 2 else (prev_price - last_price) * prev_position
                self.pls.append(pl)
                if trade_quantity != 0:
                    self.trades.append(Trade(event.timestamp, self.slippage(event, trade_quantity), trade_quantity))
                    self.trade_stats.append(self.compute_trade_states(self.trades))
            case _:
                pass
        
        self.post_process(event)

    def update(self, event: Event) -> None:
        self.update_before(event)
        self.update_main(event)
        self.update_after(event)

    def consume(self, event: Event) -> None:
        if self.observe(event):
            self.update(event)
        

