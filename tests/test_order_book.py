from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from backend.order_book import Order, OrderBook


def test_insert_modify_cancel() -> None:
    book = OrderBook()
    order = Order(id=1, side=0, price=100.0, qty=10)
    book.insert(order)
    assert len(book.orders) == 1

    book.modify(1, 5)
    assert book.orders[0].qty == 5

    book.cancel(1)
    assert not book.orders


def test_market_match() -> None:
    book = OrderBook()
    book.insert(Order(id=1, side=0, price=100.0, qty=5))
    book.insert(Order(id=2, side=1, price=101.0, qty=5))
    trades = book.match_market(side=0, qty=5)
    assert trades[0].qty == 5
