from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import struct
from typing import List

from loguru import logger


@dataclass
class AddOrder:
    """Simplified ITCH Add Order message."""

    order_id: int
    side: int
    price: float
    qty: int

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation."""
        return {
            "type": "A",
            "order_id": self.order_id,
            "side": self.side,
            "price": self.price,
            "qty": self.qty,
        }


def parse_itch(path: Path) -> List[AddOrder]:
    """Parse a very small subset of TotalView-ITCH messages.

    Parameters
    ----------
    path:
        Binary file containing ITCH messages encoded in a simplified format.

    Returns
    -------
    list[AddOrder]
        Parsed Add Order messages.
    """
    messages: List[AddOrder] = []
    with path.open("rb") as f:
        while True:
            header = f.read(1)
            if not header:
                break
            msg_type = header.decode("ascii")
            if msg_type == "A":
                data = f.read(21)
                if len(data) < 21:
                    logger.warning("Truncated message encountered")
                    break
                order_id, side, price, qty = struct.unpack(
                    ">QBdI", data
                )
                messages.append(
                    AddOrder(order_id=order_id, side=side, price=price, qty=qty)
                )
            else:
                logger.debug(f"Unknown message type {msg_type}; skipping")
                break
    return messages
