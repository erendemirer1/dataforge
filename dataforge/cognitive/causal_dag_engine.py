"""
DataForge Judea Pearl Structural Causal DAG & Counterfactual Intervention Engine.
Implements do-calculus interventions and invariant-preserving forward/backward propagation.
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class CausalInterventionShock:
    variable_name: str
    target_value: float
    description: str


@dataclass
class CausalStateVector:
    sege_index: float
    education_level_rank: int
    gross_income: float
    fixed_expense_ratio: float
    cash_flow_margin: float
    loss_aversion_lambda: float
    moral_care: float
    moral_fairness: float
    moral_loyalty: float
    moral_liberty: float
    policy_utility: float


class StructuralCausalDAG:
    """
    Formal Structural Equation Model (SEM) governing societal decisions.
    Preserves invariant relationships:
    SEGE -> Occupation -> Income -> Expense Pressure -> Loss Aversion -> Policy Decision.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def evaluate_causal_pathway(
        self,
        sege_tier: int,
        age: int,
        education_rank: int,
        base_income: float,
        question_semantic_weights: dict[str, float],
        interventions: Optional[list[CausalInterventionShock]] = None
    ) -> CausalStateVector:
        """
        Computes the structural forward pass through the causal DAG.
        Applies do(X = x) interventions if provided.
        """
        # Exogenous shocks map
        shocks = {i.variable_name: i.target_value for i in (interventions or [])}

        # 1. Structural Equation: Regional SEGE score (1=highest, 6=lowest)
        sege_val = shocks.get("sege_tier", float(sege_tier))
        sege_norm = max(0.1, min(1.0, (7.0 - sege_val) / 6.0))

        # 2. Structural Equation: Income Formation Function f_Y(SEGE, Edu, Age)
        edu_val = shocks.get("education_rank", education_rank)
        edu_multiplier = 0.70 + (edu_val * 0.15)
        raw_income = base_income * edu_multiplier * (0.8 + (sege_norm * 0.4))
        income = shocks.get("income", raw_income)

        # 3. Structural Equation: Fixed Expense Pressure f_E(Income, Inflation, SEGE)
        inflation_multiplier = shocks.get("inflation_index", 1.0)
        base_expense_ratio = (0.85 - (min(income, 120000.0) / 300000.0)) * inflation_multiplier
        expense_ratio = shocks.get("fixed_expense_ratio", max(0.35, min(0.95, base_expense_ratio)))
        cash_flow_margin = max(0.05, 1.0 - expense_ratio)

        # 4. Structural Equation: Kahneman Loss Aversion f_L(CashFlowMargin, Age)
        # Tight cash flow increases loss aversion from baseline 2.25 up to 3.50
        lambda_loss = 2.25 + (1.20 * (1.0 - cash_flow_margin)) + (0.30 if age > 55 else 0.0)
        lambda_loss = shocks.get("loss_aversion_lambda", lambda_loss)

        # 5. Structural Equation: Haidt Moral Weights
        care = shocks.get("moral_care", 60.0 + (15.0 if age < 35 else 5.0))
        fairness = shocks.get("moral_fairness", 65.0 + (10.0 if cash_flow_margin < 0.20 else 0.0))
        loyalty = shocks.get("moral_loyalty", 50.0 + (sege_val * 4.0))
        liberty = shocks.get("moral_liberty", 55.0 + (edu_val * 5.0))

        # 6. Outcome Utility Function
        econ_gain = question_semantic_weights.get("econ_gain", 0.40)
        env_risk = question_semantic_weights.get("env_risk", 0.20)
        fiscal_cost = question_semantic_weights.get("fiscal_cost", 0.30)

        positive_utility = (econ_gain * 1.6) + (liberty / 100.0 * 0.5) + (loyalty / 100.0 * 0.4)
        negative_utility = (env_risk * lambda_loss) + (fiscal_cost * (1.0 / cash_flow_margin) * 0.8) + (care / 100.0 * 0.6)
        net_utility = positive_utility - negative_utility

        return CausalStateVector(
            sege_index=round(sege_norm, 3),
            education_level_rank=int(edu_val),
            gross_income=round(income, 2),
            fixed_expense_ratio=round(expense_ratio, 3),
            cash_flow_margin=round(cash_flow_margin, 3),
            loss_aversion_lambda=round(lambda_loss, 2),
            moral_care=round(care, 1),
            moral_fairness=round(fairness, 1),
            moral_loyalty=round(loyalty, 1),
            moral_liberty=round(liberty, 1),
            policy_utility=round(net_utility, 3)
        )
