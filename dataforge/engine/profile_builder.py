"""
DataForge Person Profile Builder.
Constructs statistically grounded, demographically coherent individual citizen digital twins
derived from TÜİK, SGK, BDDK, KKB, BTK, ISCO-08 labor matrix, and Sanayi Bakanlığı SEGE.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from typing import Any, Optional

from . import benchmarks as bm
from .district_archetypes import get_district_archetype
from .brand_registry import BrandRegistry
from .salary_engine import SalaryEngine
from .labor_matrix import LaborMatrixEngine, PROVINCE_TO_IBBS1
from .household_engine import HouseholdEngine
from .financial_engine import FinancialEngine
from .mobility_engine import MobilityEngine
from .digital_lifestyle_engine import DigitalLifestyleEngine
from .health_profile_engine import HealthProfileEngine
from ..utils import generate_tckn
from ..utils.geo_db import GeoDatabase
from ..utils import turkish_data as td
from ..ml.causal_synthesizer import CausalProfileExtender


@dataclass
class PersonProfile:
    """Demographically, economically, and behaviorally coherent Turkish citizen digital twin."""

    # 1. Demographic Layer (TÜİK & UAVT)
    id: int
    first_name: str
    last_name: str
    gender: str
    age: int
    birthdate: str
    tckn: str
    phone: str
    email: str
    blood_type: str

    # 2. Geographical Layer (UAVT / PTT 2025)
    city: str
    district: str
    neighborhood: str
    postal_code: str
    address: str

    # 3. Socioeconomic & Labor Layer (SEGE, ISCO-08 & TÜİK İBBS-1)
    district_archetype: str
    occupation: str
    education_level: str
    income_segment: str
    income_segment_label: str
    monthly_income: float

    # 4. Household & Family Layer (TÜİK Hanehalkı)
    marital_status: str
    children_count: int
    household_size: int
    housing_status: str

    # 5. Financial & Banking DNA (BDDK & KKB Findeks)
    findeks_credit_score: int
    credit_score_rating: str
    credit_card_limit: float
    savings_preference: str
    has_bes_pension: bool

    # 6. Mobility & Vehicle Layer (TÜİK Taşıt & Trafik)
    driving_license: str
    vehicle_ownership: str
    vehicle_model: Optional[str]
    vehicle_fuel_type: Optional[str]

    # 7. Digital Lifestyle & Telecom Layer (BTK)
    smartphone_model: str
    operating_system: str
    gsm_operator: str
    monthly_data_gb: int
    digital_subscriptions: list[str]

    # 8. Health & Social Security Layer (SGK)
    sgk_category: str
    health_insurance: str

    # 9. Behavioral & Consumer DNA (BKM 2024 & Brand Registry)
    basket_multiplier: float
    preferred_payment_method: str
    preferred_merchants: dict[str, list[str]]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _slugify_name(name: str) -> str:
    """Convert Turkish characters to clean ASCII email prefix."""
    replacements = {
        'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's',
        'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c',
    }
    for tr, en in replacements.items():
        name = name.replace(tr, en)
    return "".join(c for c in name.lower() if c.isalnum())


class ProfileBuilder:
    """Engine that generates statistically validated individual citizen digital twins."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.geo_db = GeoDatabase.get_instance()
        self.brand_registry = BrandRegistry.get_instance()
        self.salary_engine = SalaryEngine.get_instance()
        self.labor_engine = LaborMatrixEngine.get_instance()
        self.household_engine = HouseholdEngine.get_instance()
        self.financial_engine = FinancialEngine.get_instance()
        self.mobility_engine = MobilityEngine.get_instance()
        self.digital_engine = DigitalLifestyleEngine.get_instance()
        self.health_engine = HealthProfileEngine.get_instance()
        self.causal_extender = CausalProfileExtender()

    def build_profile(self, record_id: int = 1, **kwargs: Any) -> dict[str, Any]:
        """Create a full PersonProfile using empirical SEGE, İBBS-1, BDDK, SGK, and TÜİK rules."""
        # 1. Geographic Location & District SEGE Archetype (UAVT / PTT 2025)
        city_req = kwargs.get("city")
        district_req = kwargs.get("district")
        addr_info = self.geo_db.get_random_address(rng=self.rng, city=city_req, district=district_req)

        city_name = addr_info["city"]
        district_name = addr_info["district"]
        archetype = get_district_archetype(district_name, city_name)
        region_code = PROVINCE_TO_IBBS1.get(city_name, "TR1")

        # 2. Age & Birthdate (TÜİK 2024 age pyramid distribution)
        if "age" in kwargs:
            age = kwargs["age"]
        else:
            if archetype.tier == 1:
                age_weights = [0.10, 0.28, 0.35, 0.17, 0.10]
            elif archetype.tier == 3:
                age_weights = [0.20, 0.32, 0.28, 0.15, 0.05]
            else:
                age_weights = [0.15, 0.25, 0.30, 0.20, 0.10]

            age_brackets = [
                (18, 24),
                (25, 34),
                (35, 49),
                (50, 64),
                (65, 80),
            ]
            chosen_bracket = self.rng.choices(age_brackets, weights=age_weights)[0]
            age = self.rng.randint(chosen_bracket[0], chosen_bracket[1])

        current_year = date.today().year
        birth_year = current_year - age
        birth_month = self.rng.randint(1, 12)
        birth_day = self.rng.randint(1, 28)
        birthdate = date(birth_year, birth_month, birth_day).isoformat()

        # 3. Gender & Generational Cohort Name Matching (No 'Berkecan Dede'!)
        gender = kwargs.get("gender") or self.rng.choices(td.GENDERS, weights=td.GENDER_WEIGHTS)[0]
        first_name = kwargs.get("first_name") or td.get_name_by_age_and_gender(gender, age, rng=self.rng)
        last_name = kwargs.get("last_name") or self.rng.choice(td.SURNAMES)

        # 4. Occupation & Education from Empirical Regional Labor Matrix (ISCO-08)
        if "occupation" in kwargs:
            occupation = kwargs["occupation"]
            education_level = kwargs.get("education_level", "Lisans")
        else:
            candidates = self.labor_engine.get_candidate_occupations(
                age=age,
                city=city_name,
                district=district_name,
                sege_tier=archetype.tier,
            )
            chosen_candidate = self.rng.choice(candidates)
            occupation = chosen_candidate["title"]
            education_level = kwargs.get("education_level") or chosen_candidate.get("education", "Lisans")

        # 5. Compensation from Live Salary Engine
        comp = self.salary_engine.calculate_compensation(occupation, age=age, rng=self.rng)
        monthly_income = comp["monthly_income"]
        income_segment = kwargs.get("income_segment") or comp["income_segment"]
        income_segment_label = comp["income_segment_label"]
        basket_multiplier = comp["basket_multiplier"]

        # 6. Household & Family Profile (TÜİK Hanehalkı)
        household = self.household_engine.generate_household(
            age=age,
            income_segment=income_segment,
            region=region_code,
            rng=self.rng,
        )

        # 7. Financial & Credit DNA (BDDK & KKB Findeks)
        financial = self.financial_engine.generate_financial_profile(
            monthly_income=monthly_income,
            income_segment=income_segment,
            age=age,
            occupation=occupation,
            rng=self.rng,
        )

        # 8. Mobility & Vehicles (TÜİK & Karayolları)
        mobility = self.mobility_engine.generate_mobility(
            occupation=occupation,
            income_segment=income_segment,
            age=age,
            is_metro=archetype.is_metro,
            rng=self.rng,
        )

        # 9. Digital Lifestyle & Telecom (BTK)
        digital = self.digital_engine.generate_digital_profile(
            income_segment=income_segment,
            age=age,
            rng=self.rng,
        )

        # 10. Health & Social Security (SGK & Kızılay)
        health = self.health_engine.generate_health_profile(
            occupation=occupation,
            income_segment=income_segment,
            age=age,
            rng=self.rng,
        )

        # 11. Preferred Brands from Dynamic BrandRegistry
        categories = ["market", "giyim", "electronic", "restaurant", "transport", "health", "entertainment", "other"]
        preferred_merchants = {
            cat: self.brand_registry.get_merchants(cat, income_segment=income_segment, is_metro=archetype.is_metro)
            for cat in categories
        }

        # 12. Preferred Payment Method
        if income_segment in ["orta_ust", "ust_gelir"]:
            payment_pref = self.rng.choices(
                ["Kredi Kartı", "Banka Kartı", "Dijital Cüzdan"], weights=[0.75, 0.15, 0.10]
            )[0]
        elif income_segment == "alt_gelir":
            payment_pref = self.rng.choices(
                ["Banka Kartı", "Kredi Kartı", "Kapıda Ödeme", "BNPL"], weights=[0.45, 0.35, 0.10, 0.10]
            )[0]
        else:
            payment_pref = self.rng.choices(
                ["Kredi Kartı", "Banka Kartı", "Havale/EFT", "Dijital Cüzdan"], weights=[0.55, 0.30, 0.10, 0.05]
            )[0]

        # 13. Contact Details & TCKN
        tckn = generate_tckn()
        operators = ['530', '532', '535', '537', '542', '545', '552', '555']
        op = self.rng.choice(operators)
        phone = f"0{op} {self.rng.randint(100, 999)} {self.rng.randint(10, 99)} {self.rng.randint(10, 99)}"

        domain = self.rng.choice(["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "icloud.com", "yandex.com"])
        slug_f = _slugify_name(first_name)
        slug_l = _slugify_name(last_name)
        suffix = self.rng.randint(10, 999) if self.rng.random() > 0.4 else ""
        email = f"{slug_f}.{slug_l}{suffix}@{domain}"

        # Timestamp
        created_days_ago = self.rng.randint(0, 365 * 4)
        created_at = (datetime.now() - timedelta(days=created_days_ago)).strftime('%Y-%m-%d %H:%M:%S')

        # Build core profile dict
        core_profile: dict[str, Any] = dict(
            id=record_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            age=age,
            birthdate=birthdate,
            tckn=tckn,
            phone=phone,
            email=email,
            blood_type=health.blood_type,
            city=addr_info["city"],
            district=addr_info["district"],
            neighborhood=addr_info["neighborhood"],
            postal_code=addr_info["postal_code"],
            address=addr_info["full_address"],
            district_archetype=archetype.label,
            occupation=occupation,
            education_level=education_level,
            income_segment=income_segment,
            income_segment_label=income_segment_label,
            monthly_income=monthly_income,
            marital_status=household.marital_status,
            children_count=household.children_count,
            household_size=household.household_size,
            housing_status=household.housing_status,
            findeks_credit_score=financial.findeks_credit_score,
            credit_score_rating=financial.credit_score_rating,
            credit_card_limit=financial.credit_card_limit,
            savings_preference=financial.savings_preference,
            has_bes_pension=financial.has_bes_pension,
            driving_license=mobility.driving_license,
            vehicle_ownership=mobility.vehicle_ownership,
            vehicle_model=mobility.vehicle_model,
            vehicle_fuel_type=mobility.vehicle_fuel_type,
            smartphone_model=digital.smartphone_model,
            operating_system=digital.operating_system,
            gsm_operator=digital.gsm_operator,
            monthly_data_gb=digital.monthly_data_gb,
            digital_subscriptions=digital.digital_subscriptions,
            sgk_category=health.sgk_category,
            health_insurance=health.health_insurance_type,
            basket_multiplier=basket_multiplier,
            preferred_payment_method=payment_pref,
            preferred_merchants=preferred_merchants,
            created_at=created_at,
        )

        # Causal extension: 60+ additional fields derived from core profile
        extended_profile = self.causal_extender.extend(core_profile, self.rng)
        return extended_profile

