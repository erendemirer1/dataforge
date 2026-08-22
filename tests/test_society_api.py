"""
Unit tests for Synthetic Society OS REST endpoints.
"""
from fastapi.testclient import TestClient
from dataforge.api.app import app

client = TestClient(app)


def test_interrogate_endpoint():
    payload = {
        "persona_dict": {
            "id": 1,
            "first_name": "Can",
            "last_name": "Yılmaz",
            "age": 28,
            "occupation": "Yazılımcı",
            "city": "İstanbul",
            "district": "Kadıköy",
            "monthly_income": 65000.0,
            "housing_status": "Kiracı"
        },
        "user_question": "Kadıköy'deki kira fiyatları hakkında ne düşünüyorsun?",
        "conversation_history": []
    }
    resp = client.post("/api/v1/society/interrogate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "persona_ad_soyad" in data
    assert "cevap_metni" in data
    assert "bilincalti_refleksi" in data


def test_gis_heatmap_endpoint():
    resp = client.get("/api/v1/society/gis-heatmap")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert "plaka_kodu" in data[0]


def test_export_report_endpoint():
    payload = {
        "report_data": {
            "soru_veya_politika": "Kadıköy Kentsel Dönüşüm Desteği",
            "hedef_bolge": "İstanbul (Kadıköy)",
            "orneklem_buyuklugu": 1000,
            "genel_kabul_yuzde": 65.0,
            "genel_ret_yuzde": 25.0,
            "genel_kararsiz_yuzde": 10.0
        }
    }
    resp = client.post("/api/v1/society/export-report", json=payload)
    assert resp.status_code == 200
    assert "DATAFORGE // RESMİ YÖNETİCİ BRİFİ" in resp.text
