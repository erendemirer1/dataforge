"""
DataForge Neuro-Cognitive State & Behavioral Economics Engine.
Simulates biochemical drives (Dopamine, Cortisol, Amygdala),
Kahneman's System 1 & System 2 processing, and Freudian psychological ego defense mechanisms.
"""
from __future__ import annotations

import random
from typing import Optional
from dataclasses import dataclass


@dataclass
class NeuroCognitiveState:
    dopamine_reward_seeking: float     # Ödül & Yenilik Açlığı (0-100)
    cortisol_chronic_stress: float     # Geçim & Yaşam Stresi (0-100)
    amygdala_threat_reactivity: float  # Dolandırılma & Tehlike Hassasiyeti (0-100)
    loss_aversion_coefficient: float   # Kayıptan Kaçınma Katsayısı (1.2x - 3.5x)
    status_quo_inertia: float          # Alışkanlıkları Değiştirmeme Direnci (0-100)
    cognitive_fatigue_level: float     # Zihinsel Yorgunluk / Karar Felci (0-100)
    ego_defense_mechanism: str         # Rasyonalizasyon, Yansıtma, İnkar, Entelektüalizasyon, Alaycılık
    decision_style: str                # Sezgisel/Dürtüsel (Sistem 1), Aşırı Analitik (Sistem 2), Şüpheci Defansif, Sosyal Onay Bağımlısı
    price_guilt_threshold_tl: float    # Vicdan azabı duymadan harcayabileceği maksimum tek seferlik limit


class NeuroCognitiveEngine:
    """Calculates deep neuropsychological states conditioned on financial reality, age, and habitus."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def derive_neuro_state(
        self,
        income_tl: float,
        discretionary_budget_tl: float,
        debt_ratio: float,
        age: int,
        social_class: str,
        cultural_capital: float
    ) -> NeuroCognitiveState:
        """Derives mutually-coherent neuro-psychological state."""
        
        # 1. Cortisol (Stress) Calculation (Financial debt & survival constraints)
        base_stress = 40.0
        if debt_ratio > 0.4:
            base_stress += 25.0
        if discretionary_budget_tl < 3000:
            base_stress += 25.0
        if "Prekarya" in social_class:
            base_stress += 15.0
        cortisol = min(98.0, max(15.0, base_stress + self.rng.uniform(-10, 10)))

        # 2. Dopamine (Reward & Novelty seeking)
        if age < 30 and cultural_capital > 60:
            dopamine = round(self.rng.uniform(65, 95), 1)
        elif "Esnaf" in social_class:
            dopamine = round(self.rng.uniform(35, 65), 1) # Esnaf nakit sever, fantezi sevmez
        elif age > 55:
            dopamine = round(self.rng.uniform(20, 50), 1)
        else:
            dopamine = round(self.rng.uniform(40, 75), 1)

        # 3. Amygdala & Threat Reactivity (Suspicion & Fear of being scammed)
        if "Esnaf" in social_class or "Taşra" in social_class:
            amygdala = round(self.rng.uniform(70, 95), 1) # Yabancıya ve dijital tekliflere aşırı şüpheci
        elif cultural_capital > 80:
            amygdala = round(self.rng.uniform(35, 65), 1) # Rasyonel sorgular ama paranoyak değildir
        else:
            amygdala = round(self.rng.uniform(50, 85), 1)

        # 4. Kahneman Loss Aversion Coefficient (Standard human is ~2.0x, stressed is ~3.2x)
        if cortisol > 70:
            loss_aversion = round(self.rng.uniform(2.5, 3.5), 2)
        elif cultural_capital > 75:
            loss_aversion = round(self.rng.uniform(1.4, 2.0), 2)
        else:
            loss_aversion = round(self.rng.uniform(1.8, 2.6), 2)

        # 5. Status Quo Inertia
        if age > 45 or "Geleneksel" in social_class:
            inertia = round(self.rng.uniform(75, 98), 1)
        elif age < 28:
            inertia = round(self.rng.uniform(25, 55), 1)
        else:
            inertia = round(self.rng.uniform(50, 80), 1)

        # 6. Ego Defense Mechanism
        if cultural_capital > 75:
            ego_defense = self.rng.choice([
                "Entelektüalizasyon (Teknik kusur bularak reddetme)",
                "Rasyonalizasyon (Maliyet-fayda analiziyle kendini haklı çıkarma)"
            ])
            decision_style = "Aşırı Analitik & Sorgulayıcı (Sistem 2)"
        elif "Esnaf" in social_class:
            ego_defense = self.rng.choice([
                "Alaycılık ve Küçümseme ('Biz bu işin kitabını yazdık')",
                "Yansıtma ('Millet parayı buldu bize mi satıyor?')"
            ])
            decision_style = "Şüpheci & Pazarlıkçı (Sistem 1 + Defansif)"
        elif "Prekarya" in social_class:
            ego_defense = "İnkar & Kaçınma ('Bizim öyle lüks işlerle işimiz olmaz')"
            decision_style = "Dürtüsel & Kaçak (Hayatta Kalma Modu)"
        else:
            ego_defense = "Rasyonalizasyon (İhtiyacım yoktu diyerek geçiştirme)"
            decision_style = "Sosyal Onay & Güven Arayıcısı"

        # 7. Price Guilt Threshold (Vicdan Azabı Sınırı)
        price_guilt = round(max(250.0, discretionary_budget_tl * self.rng.uniform(0.10, 0.25)), 2)

        return NeuroCognitiveState(
            dopamine_reward_seeking=dopamine,
            cortisol_chronic_stress=round(cortisol, 1),
            amygdala_threat_reactivity=amygdala,
            loss_aversion_coefficient=loss_aversion,
            status_quo_inertia=inertia,
            cognitive_fatigue_level=round(self.rng.uniform(30, 85), 1),
            ego_defense_mechanism=ego_defense,
            decision_style=decision_style,
            price_guilt_threshold_tl=price_guilt
        )
