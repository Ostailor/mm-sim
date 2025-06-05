from __future__ import annotations

import struct
from pathlib import Path

from backend.itch_parser import parse_itch


def test_parse_itch(tmp_path: Path) -> None:
    data = struct.pack(
        ">cQBdI", b"A", 1, 0, 101.0, 10
    )
    file = tmp_path / "sample.itch"
    file.write_bytes(data)
    messages = parse_itch(file)
    assert len(messages) == 1
    msg = messages[0]
    assert msg.order_id == 1
    assert msg.side == 0
    assert msg.price == 101.0
    assert msg.qty == 10
