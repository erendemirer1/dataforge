"""
Transactions schema generator.
Produces realistic financial transaction records grounded in BKM & BDDK Turkish banking distributions.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

from .base import BaseGenerator
from ..engine import BehaviorEngine, ProfileBuilder, PersonProfile
from ..utils import turkish_data as td


class TransactionsGenerator(BaseGenerator):
    """Generator for the 'transactions' schema powered by BKM macroeconomic rules."""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self.engine = BehaviorEngine(self.rng)
        self.profile_builder = ProfileBuilder(self.rng)
        self._user_profiles_cache: dict[int, PersonProfile] = {}

    def generate_one(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        record_id: int = kwargs.get('record_id', self.randint(1, 999_999))
        user_ids: list[int] = kwargs.get('user_ids', [])
        user_id = self.choice(user_ids) if user_ids else self.randint(1, 1000)

        # Get or create PersonProfile for this user_id
        if user_id not in self._user_profiles_cache:
            self._user_profiles_cache[user_id] = self.profile_builder.build_profile(record_id=user_id)

        profile = self._user_profiles_cache[user_id]
        tx = self.engine.generate_transaction_for_profile(
            profile=profile,
            transaction_index=record_id,
        )

        return {
            'id': tx['id'],
            'transaction_id': tx['transaction_id'],
            'user_id': tx['user_id'],
            'amount': tx['amount'],
            'currency': tx['currency'],
            'type': tx['type'],
            'category': tx['category'],
            'description': tx['description'],
            'balance_after': tx['balance_after'],
            'created_at': tx['created_at'],
        }

    def generate(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        return [self.generate_one(record_id=i, **kwargs) for i in range(1, count + 1)]
