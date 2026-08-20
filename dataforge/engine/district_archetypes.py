"""
DataForge District Archetypes & Socio-Economic Characterization Engine.
Classifies Turkish districts based on Sanayi ve Teknoloji Bakanlığı SEGE (Sosyo-Ekonomik Gelişmişlik Sıralaması)
and TÜİK demographic distributions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# SEGE TIER 1: METROPOL ELİT & YÜKSEK EĞİTİM
# ---------------------------------------------------------------------------
TIER_1_DISTRICTS = {
    # İstanbul
    "Kadıköy", "Beşiktaş", "Şişli", "Bakırköy", "Sarıyer", "Üsküdar",
    "Ataşehir", "Maltepe", "Beyoğlu", "Adalar",
    # Ankara
    "Çankaya", "Gölbaşı",
    # İzmir
    "Karşıyaka", "Konak", "Bornova", "Urla", "Çeşme", "Güzelbahçe",
    # Bursa, Antalya, Eskişehir, Muğla
    "Nilüfer", "Muratpaşa", "Konyaaltı", "Tepebaşı", "Bodrum", "Marmaris", "Fethiye",
}

# ---------------------------------------------------------------------------
# SEGE TIER 2: GELİŞMİŞ İL MERKEZLERİ & MEMUR / HİZMET
# ---------------------------------------------------------------------------
TIER_2_DISTRICTS = {
    # İstanbul
    "Kartal", "Pendik", "Ümraniye", "Bahçelievler", "Beylikdüzü", "Zeytinburnu", "Fatih",
    # Ankara
    "Yenimahalle", "Etimesgut", "Keçiören", "Mamak", "Altındağ", "Sincan",
    # İzmir
    "Buca", "Bayraklı", "Çiğli", "Gaziemir", "Karabağlar", "Menemen",
    # Diğer Büyükşehir Merkezleri
    "Osmangazi", "Yıldırım", "Seyhan", "Çukurova", "Yüreğir",
    "Selçuklu", "Meram", "Karatay", "Melikgazi", "Kocasinan",
    "İlkadım", "Atakum", "Ortahisar", "Odunpazarı", "İzmit", "Adapazarı",
    "Pamukkale", "Merkezefendi", "Süleymanpaşa", "Antakya", "İskenderun",
}

# ---------------------------------------------------------------------------
# SEGE TIER 3: SANAYİ, ÜRETİM & GENÇ NÜFUS
# ---------------------------------------------------------------------------
TIER_3_DISTRICTS = {
    # İstanbul & Marmara Sanayi
    "Esenyurt", "Bağcılar", "Küçükçekmece", "Sultangazi", "Gaziosmanpaşa", "Esenler", "Arnavutköy", "Tuzla",
    "Gebze", "Darıca", "Çayırova", "Dilovası", "Körfez",
    "Çorlu", "Çerkezköy", "Kapaklı", "İnegöl", "Gemlik", "Mustafakemalpaşa",
    # Anadolu Sanayi Merkezleri
    "Şahinbey", "Şehitkamil", "Torbalı", "Aliağa", "Kemalpaşa",
    "Tarsus", "Akdeniz", "Toroslar", "Ceyhan", "Körfez",
}


@dataclass
class DistrictArchetype:
    tier: int
    label: str
    is_metro: bool
    income_weights: dict[str, float]
    education_weights: dict[str, float]
    occupations: list[str]


def get_district_archetype(district: str, city: str = "") -> DistrictArchetype:
    """Analyze SEGE tier and return demographic modifier for the district."""
    # 1. Check Tier 1
    if district in TIER_1_DISTRICTS:
        return DistrictArchetype(
            tier=1,
            label="Metropol Elit & İnovasyon",
            is_metro=True,
            income_weights={
                "alt_gelir": 0.05,
                "orta_alt": 0.15,
                "orta_gelir": 0.30,
                "orta_ust": 0.35,
                "ust_gelir": 0.15,
            },
            education_weights={
                "Lise": 0.15,
                "Lisans": 0.55,
                "Yüksek Lisans / Doktora": 0.30,
            },
            occupations=[
                "Yazılım Mimarı", "Mimar", "Doktor / Uzman Hekim", "Akademisyen / Profesör",
                "Avukat / Hukuk Danışmanı", "Pazarlama Direktörü", "Finans Yöneticisi",
                "Yatırım Uzmanı", "Kreatif Direktör", "Genel Müdür Yardımcısı", "Kıdemli Danışman",
            ],
        )

    # 2. Check Tier 2
    if district in TIER_2_DISTRICTS or city in ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Eskişehir"] and "Merkez" in district:
        return DistrictArchetype(
            tier=2,
            label="Gelişmiş İl Merkezi & Memur/Hizmet",
            is_metro=True,
            income_weights={
                "alt_gelir": 0.15,
                "orta_alt": 0.30,
                "orta_gelir": 0.40,
                "orta_ust": 0.12,
                "ust_gelir": 0.03,
            },
            education_weights={
                "Lise": 0.35,
                "Ön Lisans": 0.15,
                "Lisans": 0.45,
                "Yüksek Lisans / Doktora": 0.05,
            },
            occupations=[
                "Öğretmen", "Devlet Memuru", "Bankacı", "Hemşire",
                "Saha Satış Uzmanı", "Mali Müşavir", "İnsan Kaynakları Uzmanı",
                "Makine Mühendisi", "Şube Müdürü", "Esnaf / Mağaza Müdürü",
            ],
        )

    # 3. Check Tier 3
    if district in TIER_3_DISTRICTS:
        return DistrictArchetype(
            tier=3,
            label="Sanayi & Üretim Merkezi",
            is_metro=True,
            income_weights={
                "alt_gelir": 0.35,
                "orta_alt": 0.45,
                "orta_gelir": 0.17,
                "orta_ust": 0.03,
                "ust_gelir": 0.00,
            },
            education_weights={
                "İlkokul/Ortaokul": 0.25,
                "Lise / Meslek Lisesi": 0.55,
                "Ön Lisans / Lisans": 0.20,
            },
            occupations=[
                "Fabrika Teknisyeni", "CNC Operatörü", "Usta / Formen",
                "Lojistik Sevkiyat Görevlisi", "Kamyon / Tır Şoförü", "Moto Kurye",
                "Market Kasiyeri", "Kaynak Ustası", "Depo Sorumlusu", "Oto Tamir Ustası",
            ],
        )

    # 4. Tier 4 (Anadolu Kırsal, Tarım & Yerel Kasaba)
    return DistrictArchetype(
        tier=4,
        label="Anadolu Kırsal & Tarım / Esnaf Kasabası",
        is_metro=False,
        income_weights={
            "alt_gelir": 0.55,  # Asgari ücret ve tarım tabanı
            "orta_alt": 0.35,
            "orta_gelir": 0.10,
            "orta_ust": 0.00,
            "ust_gelir": 0.00,
        },
        education_weights={
            "İlkokul/Ortaokul": 0.55,
            "Lise": 0.35,
            "Lisans": 0.10,
        },
        occupations=[
            "Çiftçi / Ziraatçı", "Esnaf / Bakkal", "Ziraat Teknisyeni",
            "Traktör & Tarım Makinesi Operatörü", "Hayvan Yetiştiricisi",
            "İnşaat Ustası", "Minibüs / Taksi Şoförü", "Orman İşçisi",
            "Köy Muhtarı / İdari Personel", "Belediye Hizmet Personeli",
        ],
    )
