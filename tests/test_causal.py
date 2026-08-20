"""
Tests for DataForge 7-Level Causal DAG & Digital Twin Synthesizer.
Validates sociological, economic, and institutional consistency.
"""
import pytest
from dataforge.generators.users import UsersGenerator


def test_causal_profile_richness():
    gen = UsersGenerator(seed=42)
    profile = gen.generate_one()

    # Must contain 80+ rich causal attributes
    assert len(profile) >= 80

    # 1. Identity & Demographics
    assert "birth_city" in profile
    assert "ethnicity" in profile
    assert "mother_tongue" in profile

    # 2. Education Depth
    assert "education_level_detail" in profile
    assert "has_master" in profile
    assert "foreign_language" in profile

    # 3. Labor & Career Depth
    assert "employment_status_detail" in profile
    assert "company_size" in profile
    assert "work_experience_years" in profile
    assert "annual_bonus_tl" in profile

    # 4. Income & Taxation
    assert "gross_salary_tl" in profile
    assert "net_salary_tl" in profile
    assert "tax_bracket" in profile
    assert "monthly_fixed_expenses_tl" in profile

    # 5. Financial & Investment DNA
    assert "savings_tl" in profile
    assert "gold_holdings_gram" in profile
    assert "stock_portfolio_tl" in profile
    assert "investment_risk_tolerance" in profile

    # 6. Housing Depth
    assert "housing_type_detail" in profile
    assert "housing_sqm" in profile
    assert "heating_type" in profile
    assert "room_count" in profile

    # 7. Mobility Depth
    assert "vehicle_count" in profile
    assert "daily_commute_method" in profile
    assert "commute_time_minutes" in profile

    # 8. Health & Lifestyle Depth
    assert "bmi_value" in profile
    assert "bmi_category" in profile
    assert "smoker_detail" in profile
    assert "supermarket_preference" in profile
    assert "vacation_type" in profile


def test_causal_coherence_rules():
    gen = UsersGenerator(seed=123)
    profiles = gen.generate(50)

    for p in profiles:
        # Rule 1: High School type must be present for Lise/Uni graduates
        if p["education_level_detail"] in ["lise", "universite", "lisansustu"]:
            assert p["high_school_type"] is not None
        else:
            assert p["high_school_type"] is None

        # Rule 2: University name is present if educated at university level
        if p["education_level_detail"] in ["universite", "lisansustu"]:
            assert p["university_name"] is not None
        else:
            assert p["university_name"] is None

        # Rule 3: Work experience cannot exceed age - 15
        assert p["work_experience_years"] <= max(0, p["age"] - 15)

        # Rule 4: Gross salary must be >= Net salary
        assert p["gross_salary_tl"] >= p["net_salary_tl"]

        # Rule 5: Room count consistent with SQM
        if p["housing_sqm"] < 100:
            assert p["room_count"] == "2+1"
        elif p["housing_sqm"] < 150:
            assert p["room_count"] == "3+1"
        else:
            assert p["room_count"] == "4+1"
