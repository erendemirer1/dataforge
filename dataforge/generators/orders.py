"""
Orders schema generator.
Produces realistic e-commerce order records with referential integrity support and behavioral user profiles.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional

from .base import BaseGenerator
from ..engine import ProfileBuilder, PersonProfile
from ..utils import turkish_data as td


class OrdersGenerator(BaseGenerator):
    """Generator for the 'orders' schema."""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self.profile_builder = ProfileBuilder(self.rng)
        self._user_profiles_cache: dict[int, PersonProfile] = {}

    def _order_number(self, idx: int) -> str:
        return f"ORD-{datetime.now().year}-{idx:08d}"

    def generate_one(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        record_id: int = kwargs.get('record_id', self.randint(1, 999_999))
        user_ids: list[int] = kwargs.get('user_ids', [])
        product_ids: list[int] = kwargs.get('product_ids', [])

        user_id = self.choice(user_ids) if user_ids else self.randint(1, 1000)
        product_id = self.choice(product_ids) if product_ids else self.randint(1, 500)

        # Get or create PersonProfile for this user_id
        if user_id not in self._user_profiles_cache:
            self._user_profiles_cache[user_id] = self.profile_builder.build_profile(record_id=user_id)

        profile = self._user_profiles_cache[user_id]

        quantity = self.randint(1, 5)
        # Unit price scaled slightly by income segment
        base_price = self.uniform(50.0, 3500.0) * profile.get("basket_multiplier", 1.0)
        unit_price = round(base_price, 2)
        total_price = round(quantity * unit_price, 2)

        status = self.choices(td.ORDER_STATUSES, weights=td.ORDER_STATUS_WEIGHTS)[0]
        payment_method = profile.get("preferred_payment_method", "Kredi Kartı")
        shipping_address = profile.get("address", "")

        created_days_ago = self.randint(0, 730)
        created_at = datetime.now() - timedelta(days=created_days_ago)

        # updated_at is always >= created_at
        updated_offset = timedelta(hours=self.randint(0, 72))
        updated_at = created_at + updated_offset
        if updated_at > datetime.now():
            updated_at = datetime.now()

        return {
            'id': record_id,
            'order_number': self._order_number(record_id),
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
            'status': status,
            'payment_method': payment_method,
            'shipping_address': shipping_address,
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def generate(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        return [self.generate_one(record_id=i, **kwargs) for i in range(1, count + 1)]
