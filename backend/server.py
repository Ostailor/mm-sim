from __future__ import annotations

from fastapi import FastAPI
from loguru import logger

from .order_book import OrderBook, Order

app = FastAPI()
book = OrderBook()


@app.post("/insert")
async def insert_order(order: Order) -> dict:
    """Insert an order into the book."""
    book.insert(order)
    return {"status": "ok"}


@app.post("/modify/{order_id}/{qty}")
async def modify_order(order_id: int, qty: int) -> dict:
    """Modify an existing order."""
    book.modify(order_id, qty)
    return {"status": "ok"}


@app.post("/cancel/{order_id}")
async def cancel_order(order_id: int) -> dict:
    """Cancel an order."""
    book.cancel(order_id)
    return {"status": "ok"}


@app.post("/market/{side}/{qty}")
async def market_order(side: int, qty: int) -> dict:
    """Execute a market order."""
    matched = book.match_market(side, qty)
    logger.info(f"Matched {matched}")
    return {"trades": [m.__dict__ for m in matched]}

