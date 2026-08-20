"""
Tests for DataForge Machine Learning Generative Model & Evaluator.
"""
import pytest
import numpy as np
import pandas as pd
from dataforge.ml import TabularCopulaML, MLEvaluator


def test_copula_ml_fit_sample():
    # Create sample real dataset (e.g. Kızılay donor dataset)
    np.random.seed(42)
    n = 200
    age = np.random.randint(18, 65, size=n)
    income = age * 1200.0 + np.random.normal(5000, 2000, size=n)
    blood_types = np.random.choice(["A Rh(+)", "0 Rh(+)", "B Rh(+)", "AB Rh(+)"], size=n)
    cities = np.random.choice(["İstanbul", "Ankara", "İzmir", "Bursa"], size=n)

    df_real = pd.DataFrame({
        "age": age,
        "income": income,
        "blood_type": blood_types,
        "city": cities,
    })

    # 1. Fit ML Generative Copula
    model = TabularCopulaML(random_state=42)
    model.fit(df_real)
    assert model.is_fitted

    # 2. Sample Synthetic Data
    df_synthetic = model.sample(count=150)
    assert len(df_synthetic) == 150
    assert list(df_synthetic.columns) == list(df_real.columns)

    # 3. Evaluate Fidelity and Privacy
    report = MLEvaluator.evaluate(df_real, df_synthetic)
    assert report["overall_fidelity_score"] >= 70.0
    assert report["correlation_similarity_score"] >= 70.0
    assert report["privacy_protection_score"] >= 95.0
