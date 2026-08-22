"""
Unit tests for SelfCalibrationEngine and Bayesian Active Inference.
"""
from dataforge.cognitive.self_calibration import SelfCalibrationEngine


def test_kl_divergence_computation():
    engine = SelfCalibrationEngine()
    p = {"A": 0.5, "B": 0.5}
    q = {"A": 0.5, "B": 0.5}
    kl = engine.compute_kl_divergence(p, q)
    assert kl == 0.0

    q_diff = {"A": 0.8, "B": 0.2}
    kl_diff = engine.compute_kl_divergence(p, q_diff)
    assert kl_diff > 0.0


def test_poll_calibration_evaluation():
    engine = SelfCalibrationEngine()
    metric = engine.evaluate_poll_calibration(
        sim_kabul_pct=42.0,
        sim_ret_pct=44.0,
        sim_kararsiz_pct=14.0,
        topic_type="municipal_service"
    )
    assert metric.calibration_accuracy_score >= 95.0
    assert metric.kl_divergence >= 0.0

    health = engine.get_global_engine_health()
    assert "bayesian_kalibrasyon_skoru" in health
