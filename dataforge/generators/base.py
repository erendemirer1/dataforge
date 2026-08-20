"""
Base generator class for all DataForge generators.
"""
from __future__ import annotations
import random
from abc import ABC, abstractmethod
from typing import Any


class BaseGenerator(ABC):
    """Abstract base class that all schema generators must inherit from."""

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)

    @abstractmethod
    def generate_one(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a single record. Override in subclasses."""
        ...

    def generate(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        """Generate *count* records."""
        return [self.generate_one(**kwargs) for _ in range(count)]

    # -----------------------------------------------------------------------
    # Convenience helpers
    # -----------------------------------------------------------------------
    def choice(self, seq: list) -> Any:
        return self.rng.choice(seq)

    def choices(self, seq: list, weights: list | None = None, k: int = 1) -> list:
        return self.rng.choices(seq, weights=weights, k=k)

    def randint(self, a: int, b: int) -> int:
        return self.rng.randint(a, b)

    def uniform(self, a: float, b: float) -> float:
        return self.rng.uniform(a, b)

    def randfloat(self, a: float, b: float, decimals: int = 2) -> float:
        return round(self.rng.uniform(a, b), decimals)
