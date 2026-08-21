"""
DataForge Historical Trauma & Lived Turkish Memory Engine.
Synthesizes deep episodic biographical memories from Turkey's real historical milestones:
- 2001 Bankalar & Devalüasyon Krizi (Batan dükkanlar, hacizler)
- 2018 Kur Şoku & Düğün/Konut Borcu Travması
- 2020 Pandemi & Esnaf Kapanmaları
- 2021-2024 Hiperenflasyon & Barınma/Kira Bunalımı
- 2023 Deprem & Göç/Kayıp Hafızası
- 28 Şubat, Mülakat/Torpil & Askerlik/Şehitlik Hatıraları
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class BiographicalMemory:
    # 1. Yaşadığı En Büyük Ekonomik / Sosyal Kırılma Noktası
    tarihsel_kirilma_ani: str
    
    # 2. Hayatını Değiştiren Ailevi / Bireysel Olay
    bireysel_donum_noktasi: str
    
    # 3. Geleceğe Bakışını Belirleyen Temel Travma
    kisisel_guvenlik_refleksi: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class HistoricalMemoryEngine:
    """Derives contextually consistent historical memories based on age, region, and class."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def generate_biographical_memory(
        self,
        age: int,
        occupation: str,
        social_class: str,
        city: str
    ) -> BiographicalMemory:
        """Synthesizes rich, highly specific biographical milestones."""
        occ_lower = occupation.lower()
        soc_lower = social_class.lower()
        city_lower = city.lower()

        # 1. Historical Crisis Grounding by Age & Background
        if age >= 45:
            if "esnaf" in occ_lower or "ticaret" in occ_lower:
                crisis = "2001 krizinde babasının toptancı dükkanının iflas etmesi ve protesto edilen senetler"
                turning_point = "Kriz sonrası sıfırdan küçük bir dükkan açarak ailesini borç batağından kurtarması"
                reflex = "Bankalara ve çek/senet işlerine asla güvenmeme, sürekli nakit ve altın tutma refleksi"
            elif "memur" in occ_lower or "kamu" in soc_lower:
                crisis = "90'lı yılların yüksek enflasyonunda her ay maaş erimesi ve memur maaş kuyrukları"
                turning_point = "Devlet memuriyetine girerek hayat boyu garanti maaşı ve lojmanı tek sığınak görmesi"
                reflex = "Devlet kurumlarının dışındaki hiçbir özel vaade ve maceraya prim vermeme"
            elif any(w in occ_lower for w in ["şehit", "gazi", "asker", "polis"]):
                crisis = "90'lı yıllarda Güneydoğu dağlarında tertip arkadaşlarını şehit vermesi"
                turning_point = "Gazilik unvanını aldığı gün ailesine verdiği 'bu vatanın onurunu çiğnetmeme' yemini"
                reflex = "Milli birlik ve şehit kanı üzerinden yapılan her türlü siyasi pazarlığa tavizsiz öfke"
            else:
                crisis = "2001 devalüasyonunda tüm birikimlerinin bir gecede yarıya inmesi"
                turning_point = "Taşradan büyükşehre göç edip kooperatiften taksitle ilk evini alması"
                reflex = "Mülk ve gayrimenkulü tek gerçek güvence kabul etme"
        elif 30 <= age < 45:
            if "beyaz yaka" in soc_lower or "mühendis" in occ_lower:
                crisis = "2018 kur şokunda ve pandemi döneminde bir gecede yurtdışı hayallerinin ve dövizli borçlarının patlaması"
                turning_point = "Üniversiteden dereceyle mezun olup ilk işinde asgari ücretin biraz üstüne başlatılması"
                reflex = "Kariyerde liyakat yerine network ve torpilin geçerli olduğunu acı tecrübeyle kabul etme"
            elif any(c in city_lower for c in ["hatay", "maraş", "malatya", "antep", "adıyaman"]):
                crisis = "6 Şubat 2023 depreminde evini ve yakınlarını kaybedip şehri terk etmek zorunda kalması"
                turning_point = "Deprem sonrası yeni bir şehirde konteynerden/kiralık evden sıfırdan hayat kurma mücadelesi"
                reflex = "Yarın ne olacağının garantisi olmadığını bilerek günübirlik güvence arama"
            elif "esnaf" in occ_lower:
                crisis = "2020 pandemisinde dükkanının aylarca kapalı kalması ve biriken kira/POS borçları"
                turning_point = "Borçları ödemek için arabasını satıp kuryelik yaparak ayakta kalması"
                reflex = "Her an yeni bir kriz çıkabilir korkusuyla veresiye ve vadeli iş yapmama"
            else:
                crisis = "2021 sonrasındaki fahiş kira artışlarında ev sahibinin baskısıyla 3 kez ev taşımak zorunda kalması"
                turning_point = "Evlilik masraflarını ödemek için 4 farklı bankadan kredi çekip hala taksit ödemesi"
                reflex = "Gereksiz hiçbir lüks tüketime girmeme, her alışverişte en ucuz marketi arama"
        else: # Genç Kuşak (18-29)
            if "öğrenci" in occ_lower or "yazılım" in occ_lower or "işsiz" in occ_lower:
                crisis = "Üniversiteyi bitirip yüzlerce yere CV attıktan sonra sadece tanıdığı olanların mülakatı geçtiğini görmesi"
                turning_point = "KYK bursunun/kredisinin yurt ücretine bile yetmediğini anlayıp part-time çalışmaya başlaması"
                reflex = "Resmi vaatlere ve 'garanti iş/staj' söylemlerine karşı doğuştan derin bir şüphecilik"
            elif "esnaf" in occ_lower or "çırak" in occ_lower or "kurye" in occ_lower:
                crisis = "Genç yaşta motor kredisi ve kredi kartı asgarisini ödemek için günde 14 saat çalışmak zorunda kalması"
                turning_point = "Okulu bırakıp piyasada sıcak para kazanmanın tek çare olduğunu fark etmesi"
                reflex = "Kitabi kurallara değil, sokakta hızlı nakit döndüren pratik zekaya güvenme"
            else:
                crisis = "Arkadaşlarının birer birer vize alıp yurtdışına gitmesi ve kendisinin pasaport harcını bile karşılayamaması"
                turning_point = "İlk kez tek başına ev tutmaya kalktığında memur kefil ve 3 depozito istendiğinde yaşadığı eziklik"
                reflex = "Geleceğe dair uzun vadeli plan yapmaktan vazgeçip anı kurtarma psikolojisi"

        return BiographicalMemory(
            tarihsel_kirilma_ani=crisis,
            bireysel_donum_noktasi=turning_point,
            kisisel_guvenlik_refleksi=reflex
        )
