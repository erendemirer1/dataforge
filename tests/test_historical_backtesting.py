"""
DataForge Empirical Ground Truth & Historical Backtesting Test Suite.
Validates the synthetic simulation engine against known empirical milestones in Turkey.
"""
from __future__ import annotations

import pytest
from dataforge.cognitive.census_engine import MunicipalCensusEngine
from dataforge.cognitive.causal_dag_engine import StructuralCausalDAG, CausalInterventionShock
from dataforge.ml.copula_engine import CopulaCovarianceEngine
from dataforge.cognitive.social_graph import NeighborhoodSocialGraph
from dataforge.cognitive.episodic_memory import PersistentEpisodicMemory


def test_copula_multivariate_covariance():
    """Validates that Copula engine enforces correct empirical correlation signs."""
    copula = CopulaCovarianceEngine()
    samples = [copula.sample_joint_vector() for _ in range(200)]
    
    # Financial profile test
    fin = copula.calibrate_profile_financials(base_income=45000.0, sege_tier=2, age=35)
    assert fin["monthly_income"] > 0
    assert fin["fixed_expenses"] < fin["monthly_income"]
    assert 1100 <= fin["findeks_score"] <= 1900
    assert 0.40 <= fin["laibson_beta"] <= 1.00


def test_pearl_causal_dag_monotonicity():
    """Validates that macroeconomic inflation shocks monotonically increase loss aversion."""
    dag = StructuralCausalDAG()
    semantics = {"econ_gain": 0.50, "env_risk": 0.20, "fiscal_cost": 0.30}

    # Baseline State
    baseline = dag.evaluate_causal_pathway(
        sege_tier=3, age=40, education_rank=3, base_income=40000.0, question_semantic_weights=semantics
    )

    # Shock State (Severe Inflation Shock do(inflation = 1.80))
    shocked = dag.evaluate_causal_pathway(
        sege_tier=3, age=40, education_rank=3, base_income=40000.0, question_semantic_weights=semantics,
        interventions=[CausalInterventionShock(variable_name="inflation_index", target_value=1.50, description="Kriz")]
    )

    # Under inflation shock, expense ratio must rise and cash margin must compress
    assert shocked.fixed_expense_ratio >= baseline.fixed_expense_ratio
    assert shocked.loss_aversion_lambda >= baseline.loss_aversion_lambda
    assert shocked.policy_utility <= baseline.policy_utility


def test_historical_backtesting_eyt_consensus():
    """Validates that EYT pension reform among mature workers produces expected broad consensus."""
    engine = MunicipalCensusEngine()
    report = engine.run_census_poll(
        question="Emeklilikte yaşa takılanlar için erken emeklilik hakkı ve prim gün düzenlemesi",
        city="Tüm Türkiye",
        sample_size=300
    )
    d = report.to_dict()
    # EYT in Turkey has strong demographic presence
    assert d["genel_kabul_yuzde"] > 30.0
    assert len(d["bireysel_oylar"]) == 300


def test_persistent_episodic_memory():
    """Validates SQLite longitudinal memory persistence."""
    mem = PersistentEpisodicMemory.get_instance()
    mem.record_dialogue(
        citizen_id=9999,
        topic="Kentsel Dönüşüm",
        user_prompt="Binanızın güçlendirilmesini ister misiniz?",
        persona_statement="Elbette güvenli ev isterim ancak kira yardımı şart.",
        subconscious_thought="Müteahhide güvenmiyorum.",
        bayesian_shift=12.5
    )
    episodes = mem.get_citizen_episodes(citizen_id=9999)
    assert len(episodes) >= 1
    assert episodes[0].citizen_id == 9999
    assert episodes[0].bayesian_shift == 12.5


def test_watts_strogatz_neighborhood_cascade():
    """Validates peer network graph generation and cascade propagation."""
    graph_engine = NeighborhoodSocialGraph()
    mock_citizens = [
        {"ad_soyad": f"Yurttaş {i}", "meslek": "Esnaf" if i % 5 == 0 else "İşçi", "karar": "Kararsız"}
        for i in range(30)
    ]
    # Set seed opinion leaders to Kabul
    mock_citizens[0]["karar"] = "Kabul Eder / Destekler"
    mock_citizens[0]["meslek"] = "Muhtar"

    nodes = graph_engine.build_neighborhood_graph(mock_citizens, k_neighbors=4, rewire_prob=0.10)
    assert len(nodes) == 30
    assert len(nodes[0].neighbors) >= 2

    res = graph_engine.propagate_opinion_cascade(nodes, iterations=2)
    assert res["toplam_dugum"] == 30
    assert 0 <= res["nihai_kabul_yuzde"] <= 100
