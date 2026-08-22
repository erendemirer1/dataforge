"""
Unit tests for CounterfactualStressEngine.
"""
from dataforge.cognitive.counterfactual_engine import CounterfactualStressEngine


def test_counterfactual_macro_shock():
    engine = CounterfactualStressEngine()
    sample_ballots = [
        {
            "citizen_id": i + 1,
            "ad_soyad": f"Yurttaş {i+1}",
            "yas": 30 + i,
            "meslek": "Mühendis",
            "sehir_ilce": "İstanbul / Kadıköy",
            "aylik_net_gelir_tl": 30000.0,
            "barinma_durumu": "Kiracı",
            "karar": "Kabul Eder / Destekler",
            "bireysel_dusuncesi_ve_gerekcesi": "Mevcut durumu destekliyorum."
        }
        for i in range(50)
    ]

    report = engine.apply_macroeconomic_shock(
        current_ballots=sample_ballots,
        delta_asgari_ucret_pct=0.0,
        delta_enflasyon_pct=40.0,
        delta_kira_pct=50.0
    )

    assert report.enflasyon_sepet_degisim_yuzde == 40.0
    assert report.kira_artis_degisim_yuzde == 50.0
    assert report.yeni_ret_orani_yuzde >= report.onceki_ret_orani_yuzde
    assert len(report.etkilenen_ornek_yurttaslar) > 0
