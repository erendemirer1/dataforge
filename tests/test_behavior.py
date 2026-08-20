"""
Tests for DataForge Behavior Engine and ProfileBuilder.
Validates statistical grounding against TÜİK and BKM distributions.
Now uses dict-based profile access (build_profile returns dict).
"""
import pytest
from dataforge.engine import ProfileBuilder, BehaviorEngine, benchmarks as bm
from dataforge.generators.users import UsersGenerator
from dataforge.generators.transactions import TransactionsGenerator
from dataforge.generators.orders import OrdersGenerator


def test_person_profile_demographic_coherence():
    builder = ProfileBuilder()
    profile = builder.build_profile(record_id=1)

    # 1. Age and birthdate must match
    from datetime import date
    current_year = date.today().year
    birth_year = int(profile["birthdate"].split('-')[0])
    assert current_year - birth_year == profile["age"]

    # 2. Income must be positive and above minimum threshold
    assert profile["monthly_income"] >= 8000.0
    assert profile["income_segment"] in bm.INCOME_SEGMENTS

    # 3. TCKN must be 11 digits
    assert len(profile["tckn"]) == 11
    assert profile["tckn"][0] != '0'

    # 4. Address must follow official format
    assert ' Mah. ' in profile["address"]
    assert ' / ' in profile["address"]


def test_occupation_age_coherence():
    builder = ProfileBuilder()

    # Student / Youth (<23)
    young_profile = builder.build_profile(record_id=1, age=20)
    assert young_profile["age"] == 20
    assert young_profile["income_segment"] in ["alt_gelir", "orta_alt", "orta_gelir"]

    # Retiree (>65)
    senior_profile = builder.build_profile(record_id=2, age=70)
    assert senior_profile["age"] == 70
    assert any(w in senior_profile["occupation"] for w in ["Emekli", "Muhtar", "Çiftçi", "Usta"])


def test_behavior_engine_transactions():
    engine = BehaviorEngine()
    builder = ProfileBuilder()
    profile = builder.build_profile(record_id=10)

    tx = engine.generate_transaction_for_profile(profile, transaction_index=1)

    assert tx["user_id"] == 10
    assert tx["amount"] > 0
    assert tx["category"] in bm.BKM_SPENDING_CATEGORIES
    assert tx["currency"] == "TRY"
    assert tx["type"] == "debit"


def test_users_generator_behavioral_fields():
    gen = UsersGenerator()
    users = gen.generate(10)

    assert len(users) == 10
    for u in users:
        assert "occupation" in u
        assert "income_segment" in u
        assert "monthly_income" in u
        assert u["monthly_income"] >= 10000.0
        # Digital Twin Attributes
        assert "blood_type" in u
        assert "marital_status" in u
        assert "findeks_credit_score" in u
        assert 900 <= u["findeks_credit_score"] <= 1900
        assert "credit_card_limit" in u
        assert u["credit_card_limit"] > 0
        assert "driving_license" in u
        assert "smartphone_model" in u
        assert "sgk_category" in u
        # Causal extension fields
        assert "education_level_detail" in u
        assert "housing_type_detail" in u
        assert "bmi_category" in u
        assert "supermarket_preference" in u


def test_orders_generator_profile_sync():
    gen = OrdersGenerator()
    orders = gen.generate(5)

    assert len(orders) == 5
    for o in orders:
        assert "ORD-" in o["order_number"]
        assert o["total_price"] > 0
        assert " Mah. " in o["shipping_address"]


def test_district_sege_characterization():
    builder = ProfileBuilder()

    # Tier 1 (Kadıköy) -> Higher education & elite occupations
    kadikoy = builder.build_profile(record_id=1, city="İstanbul", district="Kadıköy", age=35)
    assert kadikoy["city"] == "İstanbul"
    assert kadikoy["district"] == "Kadıköy"
    assert kadikoy["district_archetype"] == "Metropol Elit & İnovasyon"

    # Tier 4 (Çobanlar) -> Rural occupations
    cobanlar = builder.build_profile(record_id=2, city="Afyonkarahisar", district="Çobanlar", age=40)
    assert cobanlar["city"] == "Afyonkarahisar"
    assert cobanlar["district"] == "Çobanlar"
    assert cobanlar["district_archetype"] == "Anadolu Kırsal & Tarım / Esnaf Kasabası"


def test_brand_registry_dynamic_selection():
    from dataforge.engine import BrandRegistry
    reg = BrandRegistry.get_instance()

    # Premium brands in metro
    metro_brands = reg.get_merchants(category="market", income_segment="ust_gelir", is_metro=True)
    assert "Macrocenter" in metro_brands or "CarrefourSA Gurme" in metro_brands

    # Budget brands in non-metro
    rural_brands = reg.get_merchants(category="market", income_segment="alt_gelir", is_metro=False)
    assert "BİM" in rural_brands or "A101" in rural_brands
    # Macrocenter should NOT exist in non-metro rural pool
    assert "Macrocenter" not in rural_brands
