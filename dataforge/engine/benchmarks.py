"""
Official Macroeconomic and Demographic Benchmarks for Turkey.
Sources:
- TÜİK (Turkish Statistical Institute) 2024/2025 Income & Living Conditions Survey
- BKM (Interbank Card Center) 2024 Card Payment Statistics
- SGK (Social Security Institution) Employment & Wage Distributions
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# TÜİK 2024 GELİR DİLİMLERİ (Income Quintiles & Brackets)
# Net Monthly Individual / Disposable Income (TRY)
# ---------------------------------------------------------------------------
INCOME_SEGMENTS = {
    "alt_gelir": {
        "label": "Alt Gelir / Asgari Ücret",
        "weight": 0.22,  # En alt %20 dilim + asgari ücret tabanı
        "income_range": (17002, 26000),
        "typical_merchants": {
            "market": ["BİM", "A101", "ŞOK", "Hakmar"],
            "giyim": ["LC Waikiki", "DeFacto", "Koton"],
            "restoran": ["Dönerci", "Pide Salonu", "Tavuk Dünyası", "Mahalle Lokantası"],
        },
        "basket_multiplier": 0.65,
    },
    "orta_alt": {
        "label": "Orta-Alt Gelir",
        "weight": 0.26,
        "income_range": (26000, 45000),
        "typical_merchants": {
            "market": ["Migros", "CarrefourSA", "A101", "ŞOK"],
            "giyim": ["LC Waikiki", "Koton", "Mavi", "DeFacto"],
            "restoran": ["Köfteci Yusuf", "Burger King", "Pidem", "Yemeksepeti"],
        },
        "basket_multiplier": 0.95,
    },
    "orta_gelir": {
        "label": "Orta Gelir / Uzman - Memur",
        "weight": 0.28,
        "income_range": (45000, 80000),
        "typical_merchants": {
            "market": ["Migros", "CarrefourSA Gurme", "Metro Grossmarket"],
            "giyim": ["Mavi", "Zara", "Mango", "Boyner", "Colin's"],
            "restoran": ["BigChefs", "Midpoint", "Cookshop", "EspressoLab", "Starbucks"],
        },
        "basket_multiplier": 1.40,
    },
    "orta_ust": {
        "label": "Orta-Üst Gelir / Kıdemli Beyaz Yaka",
        "weight": 0.16,
        "income_range": (80000, 150000),
        "typical_merchants": {
            "market": ["Macrocenter", "CarrefourSA Gurme", "Migros Sanal Market"],
            "giyim": ["Massimo Dutti", "Network", "Beymen Club", "Zara", "Tommy Hilfiger"],
            "restoran": ["Nusr-Et", "Zuma", "Sushico", "Divan", "The House Cafe"],
        },
        "basket_multiplier": 2.20,
    },
    "ust_gelir": {
        "label": "Üst Gelir / Varlıklı",
        "weight": 0.08,
        "income_range": (150000, 450000),
        "typical_merchants": {
            "market": ["Macrocenter", "Özel Şarküteri & Gurme"],
            "giyim": ["Beymen", "Vakko", "Gucci", "Prada", "Hugo Boss"],
            "restoran": ["Mikla", "Sunset Grill & Bar", "Lucca", "Spago", "Papermoon"],
        },
        "basket_multiplier": 4.50,
    },
}

# ---------------------------------------------------------------------------
# TÜİK EĞİTİM VE YAŞA GÖRE MESLEK DAĞILIMI
# ---------------------------------------------------------------------------
OCCUPATIONS_BY_AGE_AND_EDUCATION = {
    "genc_ogrenci": {
        "age_range": (18, 23),
        "titles": [
            "Üniversite Öğrencisi", "Lise Mezunu / Aday", "Part-Time Kasiyer",
            "Moto Kurye", "Garson", "Stajyer", "Freelance İçerik Üreticisi",
            "Müşteri Temsilcisi Asistanı", "Çağrı Merkezi Elemanı"
        ],
        "default_segment": "alt_gelir",
    },
    "genc_profesyonel": {
        "age_range": (24, 32),
        "titles": [
            "Yazılım Geliştirici", "Veri Analisti", "Öğretmen", "Hemşire",
            "Pazarlama Uzmanı", "Muhasebe Uzmanı", "Mimar", "Avukat",
            "İnsan Kaynakları Uzmanı", "Makine Mühendisi", "Saha Satış Temsilcisi",
            "Bankacı", "E-Ticaret Operasyon Uzmanı", "Grafik Tasarımcı"
        ],
        "default_segment": "orta_gelir",
    },
    "deneyimli_kariyer": {
        "age_range": (33, 49),
        "titles": [
            "Kıdemli Yazılım Mimarı", "Mali Müşavir", "Şube Müdürü", "Okul Müdürü",
            "Doktor / Uzman Hekim", "Satış Direktörü", "Fabrika Üretim Müdürü",
            "İnşaat Mühendisi / Proje Müdürü", "Esnaf / İşletme Sahibi", "Avukat / Ortak",
            "Finans Müdürü", "Pazarlama Direktörü", "Devlet Memuru (Kıdemli)"
        ],
        "default_segment": "orta_ust",
    },
    "yonetici_kidemli": {
        "age_range": (50, 64),
        "titles": [
            "Genel Müdür Yardımcısı", "Yönetici Ortak", "Bölge Satış Müdürü",
            "Prof. Dr. / Akademisyen", "Başhekim", "Müteahhit", "Fabrika Sahibi",
            "Kıdemli Danışman", "Kamu Şube Müdürü", "Yeminli Mali Müşavir"
        ],
        "default_segment": "orta_ust",
    },
    "emekli": {
        "age_range": (65, 85),
        "titles": [
            "Emekli Öğretmen", "Emekli Memur", "Emekli İşçi", "Emekli Bankacı",
            "Emekli Mühendis", "Emekli Subay", "Emekli Esnaf", "Emekli Sağlık Çalışanı"
        ],
        "default_segment": "orta_alt",
    },
}

# ---------------------------------------------------------------------------
# BKM (BANKALARARASI KART MERKEZİ) HARCAMA KATEGORİ ORANLARI
# ---------------------------------------------------------------------------
BKM_SPENDING_CATEGORIES = {
    "market": {
        "share": 0.32,  # BKM verisi: %32 gıda & süpermarket
        "base_amount_range": (150, 1800),
        "frequency_per_month": (8, 20),
    },
    "other": {
        "share": 0.15,  # Faturalar, kira, abonelik
        "base_amount_range": (250, 4500),
        "frequency_per_month": (3, 8),
    },
    "transport": {
        "share": 0.12,  # Akaryakıt, toplu taşıma, taksi
        "base_amount_range": (50, 1500),
        "frequency_per_month": (6, 18),
    },
    "restaurant": {
        "share": 0.11,  # Yemeksepeti, restoran, kafe
        "base_amount_range": (100, 1200),
        "frequency_per_month": (4, 15),
    },
    "giyim": {
        "share": 0.10,  # Giyim ve ayakkabı
        "base_amount_range": (350, 3500),
        "frequency_per_month": (1, 4),
    },
    "electronic": {
        "share": 0.09,  # Elektronik ve ev eşyası
        "base_amount_range": (600, 12000),
        "frequency_per_month": (0, 2),
    },
    "health": {
        "share": 0.06,  # Eczane, muayene, sağlık
        "base_amount_range": (100, 1500),
        "frequency_per_month": (1, 4),
    },
    "entertainment": {
        "share": 0.05,  # Sinema, dijital servisler, oyun
        "base_amount_range": (50, 650),
        "frequency_per_month": (2, 6),
    },
}

# ---------------------------------------------------------------------------
# ZAMAN & MAAŞ GÜNÜ HARCAMA ÇARPANLARI (BDDK & BKM Döngüsü)
# ---------------------------------------------------------------------------
TEMPORAL_MULTIPLIERS = {
    "salary_days": {
        "days_of_month": [14, 15, 16, 31, 1, 2],  # Kamu (15'i) & Özel Sektör (1'i)
        "volume_multiplier": 2.20,
        "grocery_multiplier": 1.80,
        "bill_payment_probability": 0.85,
    },
    "weekend": {
        "days": [5, 6],  # Cumartesi, Pazar
        "restaurant_multiplier": 1.90,
        "entertainment_multiplier": 2.10,
        "shopping_multiplier": 1.60,
    },
}
