import pytest
from dataforge.cognitive.deep_causal_framework import DeepCausalFramework
from dataforge.cognitive.cognitive_persona import CognitivePersonaBuilder


def test_deep_causal_framework_bourdieu():
    fw = DeepCausalFramework()
    cap = fw.derive_bourdieu_capitals(
        income_tl=85000.0,
        education_level="Üniversite",
        occupation="Kıdemli Yazılım Mühendisi",
        city="İstanbul",
        housing_status="Ev Sahibi"
    )
    assert cap.economic_capital_score > 50.0
    assert cap.cultural_capital_score > 70.0
    assert cap.composite_class_index > 50.0


def test_deep_causal_prospect_theory():
    fw = DeepCausalFramework()
    neuro = fw.derive_neuro_psychology(
        age=34,
        income_tl=30000.0,
        economic_capital=45.0,
        discretionary_budget_tl=3000.0 # High cortisol scenario
    )
    assert neuro.loss_aversion_lambda >= 2.2 # Extreme loss aversion under distress
    assert neuro.cortisol_stress_level >= 70.0

    # Prospect utility computation
    util = fw.compute_prospect_utility(perceived_gain_tl=100.0, perceived_loss_tl=100.0, neuro=neuro)
    assert util < 0 # Due to loss aversion (loss hurts more than gain feels good)


def test_persona_builder_full_enrichment():
    builder = CognitivePersonaBuilder()
    raw = {
        "yas": 27,
        "aylik_net_gelir_tl": 32000.0,
        "sehir": "İstanbul",
        "ilce": "Kadıköy",
        "meslek": "Grafik Tasarımcı",
        "egitim_durumu": "Üniversite",
        "housing_status": "Kiracı"
    }
    p = builder.build_from_raw(raw)
    assert p.bourdieu_capitals is not None
    assert p.neuro_psych is not None
    assert p.haidt_morals is not None
    assert "Openness" in str(p.neuro_psych.big_five_ocean)
    assert 0 <= p.haidt_morals.liberty_oppression <= 100
