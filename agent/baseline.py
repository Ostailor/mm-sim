from __future__ import annotations

import random

from loguru import logger

from backend.order_book import Order, OrderBook


def random_action(book: OrderBook) -> None:
    """Insert a random order as a baseline strategy."""
    side = random.randint(0, 1)
    price = random.randint(99, 101)
    qty = random.randint(1, 10)
    order = Order(id=random.randint(1, 10000), side=side, price=price, qty=qty)
    logger.debug(f"Baseline agent inserting {order}")
    book.insert(order)

