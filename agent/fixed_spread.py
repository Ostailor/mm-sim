from __future__ import annotations

import random

from loguru import logger

from backend.order_book import Order, OrderBook


def mid_price(book: OrderBook, default: float = 100.0) -> float:
    bids = [o.price for o in book.orders if o.side == 0]
    asks = [o.price for o in book.orders if o.side == 1]
    if not bids or not asks:
        return default
    return (max(bids) + min(asks)) / 2


def fixed_spread_action(book: OrderBook, spread: float = 1.0) -> None:
    """Place bid and ask around the mid price."""
    mid = mid_price(book)
    bid_price = mid - spread / 2
    ask_price = mid + spread / 2
    book.insert(Order(random.randint(1, 1_000_000), 0, bid_price, 1))
    book.insert(Order(random.randint(1, 1_000_000), 1, ask_price, 1))
    logger.debug(f"Fixed spread bid {bid_price}, ask {ask_price}")
