"""
Users schema generator.
Produces complete, realistic Turkish citizen digital twin profiles powered by TÜİK, SGK, BDDK, KKB, UAVT,
and the 7-level Causal DAG synthesizer (60+ additional fields).
"""
from __future__ import annotations

from typing import Any, Optional

from .base import BaseGenerator
from ..engine.profile_builder import ProfileBuilder


class UsersGenerator(BaseGenerator):
    """Generator for the 'users' schema powered by TÜİK & UAVT statistical models + Causal DAG."""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self.builder = ProfileBuilder(self.rng)

    def generate_one(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        record_id: int = kwargs.pop('record_id', self.randint(1, 999_999))
        # build_profile now returns a fully extended dict (core + 60+ causal fields)
        profile = self.builder.build_profile(record_id=record_id, **kwargs)
        return profile
