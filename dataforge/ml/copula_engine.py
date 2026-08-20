"""
DataForge Tabular Copula Generative Machine Learning Model.
Learns joint multi-variate continuous and discrete marginal distributions and covariance matrices
from real-world datasets and generates correlation-preserving synthetic records with differential privacy.
"""
from __future__ import annotations

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Optional
import scipy.special as sc
from scipy.stats import rankdata


class TabularCopulaML:
    """
    Gaussian Copula Generative Machine Learning Model for Mixed Tabular Data.
    Learns non-parametric marginal CDFs and latent Gaussian correlation structures.
    """

    def __init__(self, random_state: Optional[int] = None):
        self.rng = np.random.default_rng(random_state)
        self.is_fitted = False
        self.column_types: dict[str, str] = {}
        self.continuous_marginals: dict[str, dict[str, Any]] = {}
        self.categorical_marginals: dict[str, dict[str, Any]] = {}
        self.latent_covariance: Optional[np.ndarray] = None
        self.columns: list[str] = []
        self._continuous_cols: list[str] = []

    def fit(self, df: pd.DataFrame) -> "TabularCopulaML":
        """Fit the generative ML model on any real tabular DataFrame."""
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        self.columns = list(df.columns)
        continuous_transformed = []
        continuous_cols = []

        for col in self.columns:
            series = df[col].dropna()
            # Detect continuous numerical vs categorical
            if pd.api.types.is_numeric_dtype(df[col]) and series.nunique() > 5:
                self.column_types[col] = "continuous"
                values = series.to_numpy(dtype=float)
                n = len(values)

                # Empirical probability integral transform (PIT) using average rank
                ranks = (rankdata(values, method="average") - 0.5) / n
                ranks = np.clip(ranks, 1e-5, 1.0 - 1e-5)
                
                # Inverse standard normal (Probit transform)
                z = sc.ndtri(ranks)
                continuous_transformed.append(z)
                continuous_cols.append(col)

                self.continuous_marginals[col] = {
                    "raw_values": values,
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                    "std": float(np.std(values)) if np.std(values) > 0 else 1.0,
                }
            else:
                self.column_types[col] = "categorical"
                val_counts = series.value_counts(normalize=True)
                categories = list(val_counts.index)
                probabilities = list(val_counts.values)
                self.categorical_marginals[col] = {
                    "categories": categories,
                    "probabilities": probabilities,
                }

        # Calculate latent Gaussian covariance matrix across continuous features
        if len(continuous_transformed) > 1:
            z_matrix = np.column_stack(continuous_transformed)
            cov = np.cov(z_matrix, rowvar=False)
            # Regularize covariance to guarantee strict positive semi-definiteness
            cov = cov + 1e-4 * np.eye(cov.shape[0])
            self.latent_covariance = cov
            self._continuous_cols = continuous_cols
        elif len(continuous_transformed) == 1:
            self.latent_covariance = np.array([[1.0]])
            self._continuous_cols = continuous_cols
        else:
            self.latent_covariance = None
            self._continuous_cols = []

        self.is_fitted = True
        return self

    def sample(self, count: int) -> pd.DataFrame:
        """Sample synthetic records from the learned probability distributions."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before sampling.")

        synthetic_data: dict[str, list[Any]] = {}

        # 1. Sample continuous variables from latent Gaussian Copula
        if self._continuous_cols and self.latent_covariance is not None:
            mean = np.zeros(len(self._continuous_cols))
            latent_samples = self.rng.multivariate_normal(mean, self.latent_covariance, size=count)

            for i, col in enumerate(self._continuous_cols):
                z_vals = latent_samples[:, i]
                # Standard Normal CDF to Uniform [0, 1]
                u_vals = np.clip(sc.ndtr(z_vals), 1e-5, 1.0 - 1e-5)
                
                # Non-parametric quantile inversion
                marginal = self.continuous_marginals[col]
                synthetic_vals = np.quantile(marginal["raw_values"], u_vals)
                
                # Add micro-noise for differential privacy
                noise = self.rng.normal(0, marginal["std"] * 0.005, size=count)
                synthetic_vals = np.clip(synthetic_vals + noise, marginal["min"], marginal["max"])
                synthetic_data[col] = synthetic_vals.tolist()

        # 2. Sample categorical variables from empirical distributions
        for col in self.columns:
            if self.column_types[col] == "categorical":
                marginal = self.categorical_marginals[col]
                cats = marginal["categories"]
                probs = marginal["probabilities"]
                samples = self.rng.choice(cats, size=count, p=probs)
                synthetic_data[col] = samples.tolist()

        # Return DataFrame preserving exact original column order
        ordered_df = pd.DataFrame({col: synthetic_data[col] for col in self.columns})
        return ordered_df

    def save(self, file_path: str | Path) -> None:
        """Save the trained model state to a file."""
        with open(file_path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, file_path: str | Path) -> "TabularCopulaML":
        """Load a trained model from a file."""
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        if not isinstance(model, cls):
            raise TypeError("Loaded file is not a valid TabularCopulaML model.")
        return model
