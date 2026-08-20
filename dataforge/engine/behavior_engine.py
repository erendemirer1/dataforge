"""
DataForge Behavior Engine.
Executes behavioral rules based on BKM, BDDK, and TÜİK empirical distributions.
Conditions transactions, orders, and timestamps on the individual's PersonProfile.
"""
from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

from . import benchmarks as bm
from .profile_builder import PersonProfile, ProfileBuilder
from ..utils import turkish_data as td



class BehaviorEngine:
    """Simulates realistic financial and consumer transactions aligned with BKM & BDDK stats."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.profile_builder = ProfileBuilder(self.rng)

    def generate_transaction_for_profile(
        self,
        profile: PersonProfile,
        transaction_index: int = 1,
        base_date: Optional[datetime] = None,
        running_balance: float = 0.0,
    ) -> dict[str, Any]:
        """Generate a realistic transaction coherent with the individual's income and habits."""
        if base_date is None:
            # Random date within the last 180 days
            days_ago = self.rng.randint(0, 180)
            tx_time = datetime.now() - timedelta(
                days=days_ago,
                hours=self.rng.randint(0, 23),
                minutes=self.rng.randint(0, 59),
                seconds=self.rng.randint(0, 59),
            )
        else:
            tx_time = base_date

        day_of_month = tx_time.day
        is_salary_day = day_of_month in bm.TEMPORAL_MULTIPLIERS["salary_days"]["days_of_month"]
        is_weekend = tx_time.weekday() in bm.TEMPORAL_MULTIPLIERS["weekend"]["days"]

        # Select spending category according to BKM 2024 distribution
        categories = list(bm.BKM_SPENDING_CATEGORIES.keys())
        shares = [bm.BKM_SPENDING_CATEGORIES[c]["share"] for c in categories]

        # On salary days, increase probability of grocery (market) and bill payments (other)
        if is_salary_day:
            cat_weights = [
                share * 1.8 if c == "market" else share * 2.0 if c == "other" else share
                for c, share in zip(categories, shares)
            ]
        elif is_weekend:
            cat_weights = [
                share * 1.9 if c in ["restaurant", "entertainment"] else share
                for c, share in zip(categories, shares)
            ]
        else:
            cat_weights = shares

        category = self.rng.choices(categories, weights=cat_weights)[0]
        cat_info = bm.BKM_SPENDING_CATEGORIES[category]

        # Calculate amount based on BKM baseline * PersonProfile basket multiplier
        min_amt, max_amt = cat_info["base_amount_range"]
        raw_amt = self.rng.uniform(min_amt, max_amt) * profile.get("basket_multiplier", 1.0)

        # Add weekend / salary multiplier
        if is_salary_day and category == "market":
            raw_amt *= 1.35
        elif is_weekend and category == "restaurant":
            raw_amt *= 1.25

        amount = round(raw_amt, 2)

        # Select merchant & description tailored to profile's income segment
        preferred_merchants = profile.get("preferred_merchants", {})
        if category in preferred_merchants and preferred_merchants[category]:
            merchant = self.rng.choice(preferred_merchants[category])
        else:
            default_merchants = {
                "market": "Migros",
                "other": "Turkcell Fatura / İSKİ",
                "transport": "Opet Akaryakıt",
                "restaurant": "Yemeksepeti Restoran",
                "giyim": "Mavi",
                "electronic": "Hepsiburada Teknoloji",
                "health": "Merkez Eczanesi",
                "entertainment": "Netflix / Spotify",
            }
            merchant = default_merchants.get(category, "Alışveriş")

        if category in td.TRANSACTION_DESCRIPTIONS and td.TRANSACTION_DESCRIPTIONS[category]:
            description = self.rng.choice(td.TRANSACTION_DESCRIPTIONS[category])
        else:
            description = f"{merchant} Harcaması"

        # Balance management
        new_balance = round(running_balance - amount, 2)
        if new_balance < 0:
            # Simulate salary deposit if balance drops below threshold
            deposit_amt = profile.get("monthly_income", 30000)
            new_balance = round(new_balance + deposit_amt, 2)

        return {
            "id": transaction_index,
            "transaction_id": str(uuid.uuid4()),
            "user_id": profile.get("id", 1),
            "amount": amount,
            "currency": "TRY",
            "type": "debit",
            "category": category,
            "merchant": merchant,
            "description": description,
            "balance_after": new_balance,
            "created_at": tx_time.strftime("%Y-%m-%d %H:%M:%S"),
            # Statistical metadata for analytics
            "_income_segment": profile.get("income_segment", "orta_gelir"),
            "_is_salary_day": is_salary_day,
        }

