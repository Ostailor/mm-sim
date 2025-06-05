from __future__ import annotations

import random

from loguru import logger

from backend.order_book import Order, OrderBook
from .fixed_spread import mid_price


def inventory_skew_action(
    book: OrderBook,
    inventory: float,
    spread: float = 1.0,
    skew_coef: float = 0.1,
) -> None:
    """Place orders skewed by inventory.

    Parameters
    ----------
    book:
        Order book to trade against.
    inventory:
        Current signed inventory; positive means long.
    spread:
        Base spread in price units.
    skew_coef:
        Price adjustment per unit inventory.
    """
    mid = mid_price(book)
    adj = inventory * skew_coef
    bid_price = mid - spread / 2 - adj
    ask_price = mid + spread / 2 - adj
    book.insert(Order(random.randint(1, 1_000_000), 0, bid_price, 1))
    book.insert(Order(random.randint(1, 1_000_000), 1, ask_price, 1))
    logger.debug(
        f"Inventory skew bid {bid_price:.2f}, ask {ask_price:.2f}, inventory {inventory}"
    )
