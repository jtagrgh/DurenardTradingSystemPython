from dataclasses import dataclass
from book_entry import BookEntry
from typing import Optional


@dataclass
class Book:
    bids: list[BookEntry]
    asks: list[BookEntry]

    mid: Optional[float] = None

    best_bid: Optional[BookEntry] = None
    total_bids: float = 0
    average_bid_price: float = 0

    best_ask: Optional[BookEntry] = None
    total_asks: float = 0
    average_ask_price: float = 0


    def __post_init__(self) -> None:
        self.bids.sort(key=lambda e: e.price, reverse=True)
        self.asks.sort(key=lambda e: e.price)

        self.best_bid = self.bids[0] if self.bids else None
        self.total_bids = sum(bid.quantity for bid in self.bids)
        self.average_bid_price = sum(bid.price * bid.quantity for bid in self.bids) / self.total_bids

        self.best_ask = self.asks[0] if self.asks else None
        self.total_asks = sum(ask.quantity for ask in self.asks)
        self.average_ask_price = sum(ask.price * ask.quantity for ask in self.asks) / self.total_asks

        self.mid = (self.best_bid.price + self.best_ask.price) / 2 if self.best_bid and self.best_ask else None
