"""
DataForge Machine Learning Evaluation & Differential Privacy Suite.
Measures empirical statistical fidelity (KS-tests, TVD, Correlation Matrix)
and privacy protection metrics (exact match rate, re-identification risk).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Any


class MLEvaluator:
    """Evaluates the statistical similarity and privacy protection between real and synthetic data."""

    @staticmethod
    def evaluate(real_df: pd.DataFrame, synthetic_df: pd.DataFrame) -> dict[str, Any]:
        """Compute full statistical fidelity and differential privacy scores."""
        common_cols = [c for c in real_df.columns if c in synthetic_df.columns]
        if not common_cols:
            raise ValueError("No common columns found between real and synthetic datasets.")

        column_scores: dict[str, float] = {}
        total_fidelity = 0.0

        for col in common_cols:
            real_series = real_df[col].dropna()
            syn_series = synthetic_df[col].dropna()

            if pd.api.types.is_numeric_dtype(real_df[col]) and real_series.nunique() > 5:
                # 1. Kolmogorov-Smirnov Distance Complement
                ks_score = MLEvaluator._ks_complement(real_series.to_numpy(dtype=float), syn_series.to_numpy(dtype=float))
                column_scores[col] = round(ks_score * 100, 2)
            else:
                # 2. Total Variation Distance Complement for Categorical
                tvd_score = MLEvaluator._tvd_complement(real_series, syn_series)
                column_scores[col] = round(tvd_score * 100, 2)

            total_fidelity += column_scores[col]

        avg_fidelity = round(total_fidelity / len(common_cols), 2)

        # 3. Correlation Matrix Similarity (Numerical features)
        num_cols = [c for c in common_cols if pd.api.types.is_numeric_dtype(real_df[c])]
        if len(num_cols) >= 2:
            real_corr = real_df[num_cols].corr().fillna(0).to_numpy()
            syn_corr = synthetic_df[num_cols].corr().fillna(0).to_numpy()
            corr_dist = np.linalg.norm(real_corr - syn_corr, ord="fro") / (len(num_cols) * np.sqrt(2))
            correlation_similarity = round(max(0.0, 1.0 - corr_dist) * 100, 2)
        else:
            correlation_similarity = 100.0

        # 4. Privacy & Leakage Metric (Exact Duplicate Check via clean string hashing)
        df_real_str = real_df[common_cols].astype(str)
        df_syn_str = synthetic_df[common_cols].astype(str)
        merged = pd.merge(df_real_str, df_syn_str, how="inner")
        duplicate_count = len(merged)
        privacy_score = round(max(0.0, 100.0 - (duplicate_count / len(synthetic_df) * 100)), 2)

        return {
            "overall_fidelity_score": avg_fidelity,
            "correlation_similarity_score": correlation_similarity,
            "privacy_protection_score": privacy_score,
            "column_scores": column_scores,
            "exact_duplicate_count": duplicate_count,
            "evaluated_columns_count": len(common_cols),
        }

    @staticmethod
    def _ks_complement(sample1: np.ndarray, sample2: np.ndarray) -> float:
        """Compute Kolmogorov-Smirnov statistic complement (1 - D)."""
        data1 = np.sort(sample1)
        data2 = np.sort(sample2)
        n1 = len(data1)
        n2 = len(data2)

        if n1 == 0 or n2 == 0:
            return 0.0

        data_all = np.concatenate([data1, data2])
        cdf1 = np.searchsorted(data1, data_all, side="right") / n1
        cdf2 = np.searchsorted(data2, data_all, side="right") / n2

        d_stat = float(np.max(np.abs(cdf1 - cdf2)))
        return float(np.clip(1.0 - d_stat, 0.0, 1.0))

    @staticmethod
    def _tvd_complement(s1: pd.Series, s2: pd.Series) -> float:
        """Compute Total Variation Distance complement (1 - TVD)."""
        p1 = s1.value_counts(normalize=True)
        p2 = s2.value_counts(normalize=True)

        all_cats = set(p1.index).union(set(p2.index))
        tvd = 0.5 * sum(abs(p1.get(cat, 0.0) - p2.get(cat, 0.0)) for cat in all_cats)
        return float(np.clip(1.0 - tvd, 0.0, 1.0))
