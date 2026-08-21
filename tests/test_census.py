from fastapi.testclient import TestClient
from dataforge.api.app import app
from dataforge.cognitive.census_engine import MunicipalCensusEngine

client = TestClient(app)


def test_municipal_census_engine_direct():
    engine = MunicipalCensusEngine()
    rep = engine.run_census_poll(
        question="Kadıköy rıhtımda elektrikli scooter kullanımı yasaklansın mı?",
        city="İstanbul",
        district="Kadıköy",
        sample_size=200
    )
    assert rep.orneklem_buyuklugu == 200
    assert "Kadıköy" in rep.hedef_bolge
    assert len(rep.ilce_kirilimi) > 0
    assert len(rep.yas_grubu_kirilimi) > 0
    assert len(rep.barinma_durumu_kirilimi) > 0
    assert 0 <= rep.genel_kabul_yuzde <= 100
    assert rep.belediye_stratejik_aksiyon_plani is not None


def test_census_api_endpoint():
    resp = client.post(
        "/api/v1/census/poll",
        json={
            "question": "İstanbulda kentsel dönüşüm kira yardımı 20.000 TLye çıkarılsın mı?",
            "city": "İstanbul",
            "district": "Tümü",
            "sample_size": 300
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "genel_kabul_yuzde" in data
    assert "ilce_kirilimi" in data
    assert "belediye_stratejik_aksiyon_plani" in data
