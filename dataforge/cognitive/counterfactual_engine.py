"""
DataForge Real-Time "What-If" Macroeconomic Counterfactual Stress Test Engine.
Propagates dynamic policy, minimum wage, inflation, and rent shocks across synthetic populations
and calculates instant decision transitions (Markov Shift) and cashflow redistributions.
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class CounterfactualShiftReport:
    asgari_ucret_degisim_yuzde: float
    enflasyon_sepet_degisim_yuzde: float
    kira_artis_degisim_yuzde: float
    onceki_kabul_orani_yuzde: float
    yeni_kabul_orani_yuzde: float
    onceki_ret_orani_yuzde: float
    yeni_ret_orani_yuzde: float
    onceki_kararsiz_orani_yuzde: float
    yeni_kararsiz_orani_yuzde: float
    ortalama_serbest_nakit_degisimi_tl: float
    stres_kortizol_endeks_degisimi: float
    en_cok_etkilenen_demografik_kesim: str
    yonetici_stres_ozeti: str
    etkilenen_ornek_yurttaslar: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CounterfactualStressEngine:
    """
    Simulates macroeconomic shocks across synthetic populations in real-time.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def apply_macroeconomic_shock(
        self,
        current_ballots: list[dict[str, Any]],
        delta_asgari_ucret_pct: float = 0.0, # e.g. +30.0%
        delta_enflasyon_pct: float = 0.0,    # e.g. +40.0%
        delta_kira_pct: float = 0.0          # e.g. +50.0%
    ) -> CounterfactualShiftReport:
        """
        Applies macroeconomic changes across all citizens and recalculates cashflows, stress, and votes.
        """
        if not current_ballots:
            # Generate synthetic base if empty
            current_ballots = [
                {
                    "citizen_id": i + 1,
                    "ad_soyad": f"Yurttaş {i+1}",
                    "yas": 35 + (i % 30),
                    "meslek": "Çalışan",
                    "sehir_ilce": "İstanbul / Şişli",
                    "aylik_net_gelir_tl": 35000.0,
                    "barinma_durumu": "Kiracı" if i % 2 == 0 else "Ev Sahibi",
                    "karar": "Kabul Eder / Destekler" if i % 3 == 0 else ("Kesinlikle Reddeder" if i % 3 == 1 else "Kararsız / Çekimser"),
                    "bireysel_dusuncesi_ve_gerekcesi": ""
                }
                for i in range(100)
            ]

        total = len(current_ballots)
        orig_kabul = sum(1 for b in current_ballots if "Kabul" in b.get("karar", ""))
        orig_ret = sum(1 for b in current_ballots if "Red" in b.get("karar", ""))
        orig_kararsiz = total - orig_kabul - orig_ret

        # Macro multipliers
        wage_mult = 1.0 + (delta_asgari_ucret_pct / 100.0)
        inf_mult = 1.0 + (delta_enflasyon_pct / 100.0)
        rent_mult = 1.0 + (delta_kira_pct / 100.0)

        # Cumulative economic pressure index
        economic_pressure_delta = (delta_enflasyon_pct * 0.45) + (delta_kira_pct * 0.40) - (delta_asgari_ucret_pct * 0.35)

        new_kabul = orig_kabul
        new_ret = orig_ret
        new_kararsiz = orig_kararsiz
        cashflow_deltas = []
        updated_citizens = []

        for b in current_ballots:
            income = float(b.get("aylik_net_gelir_tl", 35000.0))
            housing = b.get("barinma_durumu", "Kiracı")
            age = int(b.get("yas", 35))
            occ = b.get("meslek", "Çalışan")
            orig_karar = b.get("karar", "Kararsız / Çekimser")

            # New income (if low/mid income, wage shock applies more)
            is_wage_earner = income <= 45000.0
            new_income = income * (wage_mult if is_wage_earner else 1.0 + (delta_asgari_ucret_pct * 0.3 / 100.0))

            # New expenses
            fixed_exp = income * 0.65
            new_fixed = fixed_exp * inf_mult
            if housing == "Kiracı":
                new_fixed += (income * 0.30) * (rent_mult - 1.0)

            # Cashflow difference
            orig_discretionary = max(500.0, income - fixed_exp)
            new_discretionary = max(0.0, new_income - new_fixed)
            diff_discretionary = new_discretionary - orig_discretionary
            cashflow_deltas.append(diff_discretionary)

            # Kahneman Loss Aversion & Vote Transition
            # If citizen loses cashflow, dissatisfaction rises sharply
            new_karar = orig_karar
            if diff_discretionary < -3000:
                if "Kabul" in orig_karar and self.rng.random() < 0.45:
                    new_karar = "Kesinlikle Reddeder"
                    new_kabul -= 1
                    new_ret += 1
                elif "Kararsız" in orig_karar and self.rng.random() < 0.60:
                    new_karar = "Kesinlikle Reddeder"
                    new_kararsiz -= 1
                    new_ret += 1
            elif diff_discretionary > 4000:
                if "Red" in orig_karar and self.rng.random() < 0.35:
                    new_karar = "Kabul Eder / Destekler"
                    new_ret -= 1
                    new_kabul += 1
                elif "Kararsız" in orig_karar and self.rng.random() < 0.50:
                    new_karar = "Kabul Eder / Destekler"
                    new_kararsiz -= 1
                    new_kabul += 1

            updated_citizens.append({
                "citizen_id": b.get("citizen_id", 1),
                "ad_soyad": b.get("ad_soyad", "Yurttaş"),
                "meslek": occ,
                "onceki_karar": orig_karar,
                "yeni_karar": new_karar,
                "net_gelir_degisimi": f"{new_income - income:+,.0f} TL",
                "serbest_nakit_farki": f"{diff_discretionary:+,.0f} TL",
                "karar_degisti_mi": orig_karar != new_karar
            })

        avg_cashflow_diff = sum(cashflow_deltas) / max(1, len(cashflow_deltas))
        stress_delta = max(-25.0, min(35.0, economic_pressure_delta * 0.6))

        # Affected segment
        if delta_kira_pct > 25:
            worst_hit = "Metropol Kiracıları ve Dar Gelirli Gençler"
        elif delta_enflasyon_pct > 25:
            worst_hit = "Sabit Gelirli Emekliler ve Kalabalık Haneler"
        else:
            worst_hit = "Orta Segment Hizmet Sektörü Çalışanları"

        summary = (
            f"Simüle edilen makroekonomik şok sonucunda hanehalkı serbest harcanabilir nakdinde ortalama "
            f"{avg_cashflow_diff:+,.0f} TL değişim gözlemlendi. Toplumsal stres endeksi {stress_delta:+.1f} puan kaydı; "
            f"kabul oranı %{(orig_kabul/total)*100:.1f}'den %{(new_kabul/total)*100:.1f}'e evrildi."
        )

        return CounterfactualShiftReport(
            asgari_ucret_degisim_yuzde=delta_asgari_ucret_pct,
            enflasyon_sepet_degisim_yuzde=delta_enflasyon_pct,
            kira_artis_degisim_yuzde=delta_kira_pct,
            onceki_kabul_orani_yuzde=round((orig_kabul / total) * 100, 1),
            yeni_kabul_orani_yuzde=round((new_kabul / total) * 100, 1),
            onceki_ret_orani_yuzde=round((orig_ret / total) * 100, 1),
            yeni_ret_orani_yuzde=round((new_ret / total) * 100, 1),
            onceki_kararsiz_orani_yuzde=round((orig_kararsiz / total) * 100, 1),
            yeni_kararsiz_orani_yuzde=round((new_kararsiz / total) * 100, 1),
            ortalama_serbest_nakit_degisimi_tl=round(avg_cashflow_diff, 2),
            stres_kortizol_endeks_degisimi=round(stress_delta, 1),
            en_cok_etkilenen_demografik_kesim=worst_hit,
            yonetici_stres_ozeti=summary,
            etkilenen_ornek_yurttaslar=updated_citizens[:10]
        )
