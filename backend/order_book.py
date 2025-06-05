from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
from loguru import logger
from numba import njit


@dataclass
class Order:
    """Represents a limit order."""

    id: int
    side: int  # 0 = bid, 1 = ask
    price: float
    qty: int


class OrderBook:
    """A simple order book with numba-accelerated matching."""

    def __init__(self) -> None:
        self.orders: List[Order] = []

    def insert(self, order: Order) -> None:
        """Insert a new order."""
        logger.debug(f"Inserting {order}")
        self.orders.append(order)

    def modify(self, order_id: int, qty: int) -> None:
        """Modify an existing order quantity."""
        for o in self.orders:
            if o.id == order_id:
                logger.debug(f"Modifying order {order_id} qty {qty}")
                o.qty = qty
                return
        logger.warning(f"Order {order_id} not found")

    def cancel(self, order_id: int) -> None:
        """Cancel an order by id."""
        logger.debug(f"Canceling order {order_id}")
        self.orders = [o for o in self.orders if o.id != order_id]

    def match_market(self, side: int, qty: int) -> List[Order]:
        """Match a market order against the book."""
        if not self.orders:
            return []
        prices = np.array([o.price for o in self.orders], dtype=np.float64)
        quantities = np.array([o.qty for o in self.orders], dtype=np.int64)
        sides = np.array([o.side for o in self.orders], dtype=np.int64)
        matched_qty = _match(prices, quantities, sides, side, qty)
        matched: List[Order] = []
        for i, m in enumerate(matched_qty):
            if m > 0:
                matched.append(Order(self.orders[i].id, self.orders[i].side, self.orders[i].price, int(m)))
                self.orders[i].qty -= int(m)
        self.orders = [o for o in self.orders if o.qty > 0]
        return matched


@njit
def _match(prices: np.ndarray, quantities: np.ndarray, sides: np.ndarray, side: int, qty: int) -> np.ndarray:
    """Numba-accelerated matching algorithm."""
    matched = np.zeros_like(quantities)
    remaining = qty
    for i in range(len(prices)):
        if remaining <= 0:
            break
        if sides[i] != side:
            trade_qty = min(quantities[i], remaining)
            matched[i] = trade_qty
            remaining -= trade_qty
    return matched

