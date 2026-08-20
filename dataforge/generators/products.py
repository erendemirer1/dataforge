"""
Products schema generator.
Produces realistic Turkish e-commerce product records.
"""
from __future__ import annotations
import string
from datetime import datetime, timedelta
from typing import Any

from .base import BaseGenerator
from ..utils import turkish_data as td

# Price ranges per category (min, max in TRY)
CATEGORY_PRICE_RANGES: dict[str, tuple[float, float]] = {
    'Elektronik': (500.0, 80_000.0),
    'Giyim': (99.0, 5_000.0),
    'Ev & Yaşam': (150.0, 25_000.0),
    'Spor & Outdoor': (200.0, 15_000.0),
    'Kozmetik': (50.0, 2_500.0),
    'Kitap & Müzik': (30.0, 500.0),
    'Gıda & İçecek': (20.0, 800.0),
    'Otomotiv': (100.0, 30_000.0),
}


class ProductsGenerator(BaseGenerator):
    """Generator for the 'products' schema."""

    def _sku(self, category: str, idx: int) -> str:
        prefix = category[:3].upper().replace(' ', 'X').replace('&', 'A')
        suffix = ''.join(
            self.choice(list(string.ascii_uppercase + string.digits))
            for _ in range(6)
        )
        return f"{prefix}-{idx:05d}-{suffix}"

    def generate_one(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        record_id: int = kwargs.get('record_id', self.randint(1, 999_999))

        category = self.choice(list(td.PRODUCT_CATEGORIES.keys()))
        subcategory = self.choice(td.PRODUCT_CATEGORIES[category])
        brand = self.choice(td.BRANDS)

        # Price: category-aware range
        p_min, p_max = CATEGORY_PRICE_RANGES.get(category, (100.0, 10_000.0))
        price = round(self.uniform(p_min, p_max), 2)

        # Discount: 5-40% off, always strictly less than price
        disc_pct = self.uniform(0.05, 0.40)
        discount_price = round(price * (1 - disc_pct), 2)

        stock = self.randint(0, 1_000)
        rating = round(self.uniform(1.0, 5.0), 1)
        review_count = self.randint(0, 10_000)

        sku = self._sku(category, record_id)

        description = (
            f"{brand} markasının {subcategory} kategorisindeki kaliteli ürünü. "
            f"Müşteri puanı: {rating}/5.0. "
            f"Stok: {stock} adet."
        )

        created_days_ago = self.randint(0, 365 * 3)
        created_at = datetime.now() - timedelta(days=created_days_ago)

        return {
            'id': record_id,
            'name': f"{brand} {subcategory} {self.randint(100, 9999)}",
            'category': category,
            'subcategory': subcategory,
            'price': price,
            'discount_price': discount_price,
            'stock': stock,
            'sku': sku,
            'brand': brand,
            'description': description,
            'rating': rating,
            'review_count': review_count,
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def generate(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        return [self.generate_one(record_id=i) for i in range(1, count + 1)]
