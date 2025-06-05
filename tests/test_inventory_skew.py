from __future__ import annotations

from agent.inventory_skew import inventory_skew_action
from backend.order_book import OrderBook


def test_inventory_skew_action() -> None:
    book = OrderBook()
    inventory_skew_action(book, inventory=5.0, spread=1.0, skew_coef=0.1)
    bids = [o for o in book.orders if o.side == 0]
    asks = [o for o in book.orders if o.side == 1]
    assert len(bids) == 1
    assert len(asks) == 1
    # When inventory>0, bid should be lower than ask even after skew
    assert bids[0].price < asks[0].price
