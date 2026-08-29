"""
Unit tests for 1-on-1 Socratic InterrogationEngine.
"""
from dataforge.cognitive.interrogation_engine import InterrogationEngine


def test_interrogation_turn():
    engine = InterrogationEngine()
    test_persona = {
        "id": 1,
        "first_name": "Özgür",
        "last_name": "Öztürk",
        "age": 44,
        "occupation": "Elektrik-Elektronik Mühendisi",
        "city": "Ankara",
        "district": "Sincan",
        "monthly_income": 58000.0,
        "housing_status": "Ev Sahibi"
    }

    resp = engine.conduct_interview_turn(
        persona_dict=test_persona,
        user_question="Sincan'daki ulaşım yatırımları hakkında ne düşünüyorsunuz?"
    )

    assert resp.persona_ad_soyad == "Özgür Öztürk"
    assert resp.persona_meslek == "Elektrik-Elektronik Mühendisi"
    assert len(resp.cevap_metni) > 0
    assert len(resp.kullanilan_arguman_tipi) > 0
