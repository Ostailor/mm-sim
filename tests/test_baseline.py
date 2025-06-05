from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from agent.baseline import random_action
from backend.order_book import OrderBook


def test_random_action() -> None:
    book = OrderBook()
    random_action(book)
    assert book.orders
