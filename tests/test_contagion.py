"""
Unit tests for SocialContagionEngine and Watts-Strogatz cascade dynamics.
"""
from dataforge.cognitive.social_contagion import SocialContagionEngine


def test_social_contagion_cascade():
    engine = SocialContagionEngine()
    sample_ballots = [
        {"citizen_id": i+1, "yas": 20 + (i % 50), "meslek": "Mühendis", "sehir_ilce": "İstanbul / Kadıköy"}
        for i in range(100)
    ]

    report = engine.simulate_information_cascade(
        headline_or_rumor="Kadıköy rıhtımda yeni bir kültür merkezi açılıyor",
        ballots=sample_ballots,
        virality_strength=0.70
    )

    assert report.hedef_topluluk_buyuklugu == 100
    assert len(report.zaman_adimlari) == 5
    assert report.viral_katsayi_r0_zirve > 0.0
    assert report.nihai_doygunluk_orani_yuzde >= 0.0
