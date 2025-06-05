from __future__ import annotations

import random
from typing import Any, Tuple

import numpy as np
from gymnasium import Env, spaces
from loguru import logger

from .order_book import Order, OrderBook


class MarketEnv(Env):
    """Simple market-making environment wrapping the OrderBook."""

    metadata = {"render_modes": []}

    def __init__(self) -> None:
        self.book = OrderBook()
        self.inventory = 0
        self.price = 100.0
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=np.array([-np.inf, -np.inf], dtype=np.float32),
            high=np.array([np.inf, np.inf], dtype=np.float32),
            dtype=np.float32,
        )

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> Tuple[np.ndarray, dict[str, Any]]:
        super().reset(seed=seed)
        self.book = OrderBook()
        self.inventory = 0
        self.price = 100.0
        obs = np.array([self.price, self.inventory], dtype=np.float32)
        return obs, {}

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        if action in (0, 1):
            bid_id = random.randint(1, 1_000_000)
            self.book.insert(Order(bid_id, 0, self.price - 0.5, 1))
            logger.debug(f"Placed bid {bid_id} at {self.price - 0.5}")
        if action in (0, 2):
            ask_id = random.randint(1, 1_000_000)
            self.book.insert(Order(ask_id, 1, self.price + 0.5, 1))
            logger.debug(f"Placed ask {ask_id} at {self.price + 0.5}")

        if random.random() < 0.5:
            side = random.randint(0, 1)
            trades = self.book.match_market(side, 1)
            if trades:
                qty = trades[0].qty
                if side == 0:
                    self.inventory -= qty
                else:
                    self.inventory += qty

        self.price += float(np.random.normal(0, 0.1))
        reward = -abs(self.inventory) * 0.01
        obs = np.array([self.price, self.inventory], dtype=np.float32)
        return obs, reward, False, False, {}
