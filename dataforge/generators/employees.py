"""
Employees schema generator.
Produces realistic corporate employee records with Turkish locale.
"""
from __future__ import annotations
import re
import unicodedata
from datetime import datetime, timedelta
from typing import Any

from .base import BaseGenerator
from ..utils import turkish_data as td


def _email_slug(name: str) -> str:
    """Convert Turkish name to ASCII-safe string for email."""
    replacements = {
        'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's',
        'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c',
    }
    for k, v in replacements.items():
        name = name.replace(k, v)
    name = unicodedata.normalize('NFD', name)
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    return name.lower()


class EmployeesGenerator(BaseGenerator):
    """Generator for the 'employees' schema."""

    def generate_one(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        record_id: int = kwargs.get('record_id', self.randint(1, 999_999))
        all_ids: list[int] = kwargs.get('all_ids', list(range(1, record_id)))

        gender = self.choices(td.GENDERS, weights=td.GENDER_WEIGHTS)[0]
        first_name = self.choice(td.MALE_NAMES if gender == 'Erkek' else td.FEMALE_NAMES)
        last_name = self.choice(td.SURNAMES)

        department = self.choice(list(td.DEPARTMENTS.keys()))
        positions = td.DEPARTMENTS[department]
        position, sal_min, sal_max = self.choice(positions)
        salary = round(self.uniform(sal_min, sal_max), 2)

        domain = self.choice(td.COMPANY_DOMAINS)
        slug_f = _email_slug(first_name)
        slug_l = _email_slug(last_name)
        email = f"{slug_f}.{slug_l}@{domain}"

        hire_days_ago = self.randint(30, 365 * 10)
        hire_date = (datetime.now() - timedelta(days=hire_days_ago)).date().isoformat()

        # manager_id: pick a previous employee or None
        if all_ids and self.rng.random() > 0.1:
            manager_id = self.choice(all_ids)
        else:
            manager_id = None

        operators = ['530', '532', '535', '537', '542', '545', '552', '555']
        op = self.choice(operators)
        phone = f"0{op} {self.randint(100, 999)} {self.randint(10, 99)} {self.randint(10, 99)}"

        city = self.choices(td.CITIES, weights=td.CITY_WEIGHTS)[0]

        return {
            'id': record_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'department': department,
            'position': position,
            'salary': salary,
            'hire_date': hire_date,
            'manager_id': manager_id,
            'phone': phone,
            'city': city,
        }

    def generate(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        records = []
        for i in range(1, count + 1):
            all_ids = list(range(1, i))
            records.append(self.generate_one(record_id=i, all_ids=all_ids))
        return records
