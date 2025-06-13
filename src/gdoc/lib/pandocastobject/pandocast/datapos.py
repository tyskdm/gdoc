"""
datapos.py: DataPos class
"""
from typing import NamedTuple


class Pos(NamedTuple):
    ln: int
    col: int


class DataPos(NamedTuple):
    path: str
    start: Pos
    stop: Pos
