from __future__ import annotations

from agent.fixed_spread import fixed_spread_action
from backend.order_book import OrderBook


def test_fixed_spread_action() -> None:
    book = OrderBook()
    fixed_spread_action(book, spread=1.0)
    bids = [o for o in book.orders if o.side == 0]
    asks = [o for o in book.orders if o.side == 1]
    assert len(bids) == 1
    assert len(asks) == 1
    assert asks[0].price - bids[0].price == 1.0
