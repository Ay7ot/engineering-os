"""Core arithmetic helpers."""

from typing import Iterable, Optional


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def divide(a: float, b: float) -> float:
    """Return a divided by b."""
    if b == 0:
        raise ValueError("b must not be zero")
    return a / b


def average(values: Iterable[float]) -> Optional[float]:
    """Return the arithmetic mean, or None for an empty iterable."""
    items = list(values)
    if not items:
        return None
    return sum(items) / len(items)
