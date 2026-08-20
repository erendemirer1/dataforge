"""
DataForge Canonical Turkish Sociological Archetypes & Demographic Weights.
Calibrated using TÜİK 2024 Population Data, KONDA Social Strata Reports, and Ipsos Consumer Indices.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class TurkishArchetype:
    archetype_code: str
    archetype_title: str
    population_share_pct: float
    typical_occupations: list[str]
    typical_age_bracket: tuple[int, int]
    dominant_pain_points: list[str]
    speech_patterns: list[str]
    psychological_defense: str
    price_sensitivity: str
    tech_adoption_tier: str


TURKISH_POPULATION_ARCHETYPES: list[TurkishArchetype] = [
    TurkishArchetype(
        archetype_code="ESNAF_TRADITIONAL",
        archetype_title="Geleneksel Mülkiyetçi Esnaf / Zanaatkar",
        population_share_pct=23.5,
        typical_occupations=["Mahalle Bakkalı", "Oto Tamir Ustası", "Berber / Kuaför", "Kasap", "Tesisat Ustası", "Taksici / Minibüsçü"],
        typical_age_bracket=(35, 62),
        dominant_pain_points=[
            "Dükkan kirasının her yıl %100+ artması",
            "Müşterinin kredi kartı istemesi ve yüksek POS komisyonları",
            "Çırak ve kalifiye eleman bulamamak, haftada 60+ saat tezgahta kalmak",
            "Toptancıların vadeli satışı bırakıp nakit veya 7 gün vade istemesi"
        ],
        speech_patterns=[
            "Hocam 5 lira ne la, paket sigara kaç para olmuş.",
            "Yeğenim bana hikaye anlatma, bu alet benim kasama para sokar mı sokmaz mı?",
            "Biz babadan böyle gördük, deftere yazarız iş biter.",
            "Karttan çekerken sonra başımıza dert açmasınlar da."
        ],
        psychological_defense="Alaycılık ve Küçümseme ('Biz bu işin kitabını yazdık, yazılıma gerek yok')",
        price_sensitivity="Çok Yüksek (Nakit Koruyucu)",
        tech_adoption_tier="Geç Benimseyen (Late Majority)"
    ),
    TurkishArchetype(
        archetype_code="WHITE_COLLAR_BURNOUT",
        archetype_title="Tükenmiş & Borçlu Kentli Beyaz Yaka",
        population_share_pct=21.2,
        typical_occupations=["Yazılım Geliştirici", "Pazarlama Uzmanı", "Finans / Denetim Analisti", "İK Uzmanı", "Mimar / Mühendis"],
        typical_age_bracket=(25, 45),
        dominant_pain_points=[
            "Enflasyon karşısında eriyen maaş ve kredi kartı asgari ödeme sarmalı",
            "İstanbul trafiğinde günde 2.5 saat kaybetmek ve evden çalışma haklarının geri alınması",
            "Sürekli toplantılar, bitmeyen Slack/Teams mesajları ve tükenmişlik (burnout)",
            "Kira artışı ve ev sahibi tahliye baskısı"
        ],
        speech_patterns=[
            "Bunun ROI (Yatırım Getirisi) ve SLA garantisi nedir?",
            "KVKK ve veri güvenliği compliance onayından geçmesi lazım.",
            "Bu çeyrek bütçemiz kısıtlı, Q3 başında tekrar sync olalım.",
            "Uygulama güzel ama UX tarafı biraz hantal kalmış."
        ],
        psychological_defense="Entelektüalizasyon (Teknik ve prosedürel kusur bularak reddetme)",
        price_sensitivity="Orta-Yüksek (Statü ve Fayda Odaklı)",
        tech_adoption_tier="Erken Benimseyen (Early Adopter)"
    ),
    TurkishArchetype(
        archetype_code="Z_GEN_PRECARIA",
        archetype_title="Gelecek Kaygılı Genç Z Kuşağı Prekarya",
        population_share_pct=18.4,
        typical_occupations=["Üniversite Öğrencisi", "İşsiz / Mezun", "Kurye", "Garson / Barista", "Stajyer", "Çağrı Merkezi Elemanı"],
        typical_age_bracket=(18, 27),
        dominant_pain_points=[
            "KPSS'de yüksek puan alıp atanamama veya torpil kaygısı",
            "Kira ve yurt fiyatları yüzünden aile evine hapsolma hissi",
            "Yurtdışı vize randevusu alamamak, pasaport harçlarının pahalılığı",
            "Günübirlik harçlıkla yaşamak, ay sonunu değil yarını düşünmek"
        ],
        speech_patterns=[
            "Agalar 5 lira para değil la, bi su parası.",
            "Ghostlamak istemem ama öğrenci indirimi yoksa hayatta sarmadı der silerim.",
            "Bizi de mi söğüşleyecekler yine, net dolandırıcı bunlar.",
            "Deneme sürümü yoksa kartımı hayatta girmem.",
            "Harbi scam duruyor",
            "Kartta limit yok ki çeksinler",
            "Bi denerim sarmazsa iptal"
        ],
        psychological_defense="Şüphecilik ve Alaycı Mizah (Cynical Humor / Meme kültürü)",
        price_sensitivity="Aşırı Yüksek (Harçlık / Sıfır Nakit Seviyesi)",
        tech_adoption_tier="Dijital Yerli (Digital Native)"
    ),
    TurkishArchetype(
        archetype_code="CIVIL_SERVANT_STABLE",
        archetype_title="Garantici & Kuralcı Kamu Memuru",
        population_share_pct=14.8,
        typical_occupations=["Öğretmen", "Polis Memuru", "Zabıta", "Adliye Katibi", "Hemşire / Sağlık Memuru", "Nüfus Memuru"],
        typical_age_bracket=(28, 58),
        dominant_pain_points=[
            "Sabit maaşın piyasa enflasyonu karşısında her ay erimesi",
            "Kurum içi tayin ve rotasyon stresi",
            "Mevzuat dışına çıkma ve soruşturma geçirme korkusu",
            "Lojman ve yan hakların yetersizliği"
        ],
        speech_patterns=[
            "Bu sistemin resmi bir protokolü veya bakanlık onayı var mı?",
            "Biz devlet memuruyuz, başımıza iş açacak gayriresmi şeylere giremeyiz.",
            "Mevzuatta yeri yoksa kurumumuz bunu kabul etmez.",
            "Ay başı maaş yatsın bir değerlendirelim."
        ],
        psychological_defense="Kuralcılık ve Sorumluluktan Kaçınma ('Mevzuat izin vermiyor')",
        price_sensitivity="Yüksek (Fiyat-Performans & Güven Odaklı)",
        tech_adoption_tier="Muhafazakar (Late Majority)"
    ),
    TurkishArchetype(
        archetype_code="RURAL_AGRICULTURE",
        archetype_title="Anadolu Kırsal Üretici & Çiftçi",
        population_share_pct=12.1,
        typical_occupations=["Çiftçi (Tahıl/Sebze/Meyve)", "Büyükbaş/Küçükbaş Hayvancı", "Arıcı", "Köy Muhtarı", "Tarım İşçisi"],
        typical_age_bracket=(35, 68),
        dominant_pain_points=[
            "Mazot, gübre ve yem fiyatlarının hasat gelirini aşması",
            "Kuraklık, don ve iklim dengesizliği",
            "Ziraat Bankası ve Tarım Kredi borçlarının ötelenmesi",
            "TMO'nun açıkladığı taban fiyatın maliyeti karşılamaması"
        ],
        speech_patterns=[
            "Ağa biz topraktan anlarız, ekranla koyun güdülmez.",
            "Tarlanın dönümüne kaç para faydası var onu de sen bana.",
            "Elimle tutmadığım, gözümle görmediğim alete para bağlamam.",
            "Bereketini göreceksek bakarız ama bu sene mahsul zayıf."
        ],
        psychological_defense="Gelenekçilik ve Somutçuluk ('Toprak yalan söylemez, makine aldatır')",
        price_sensitivity="Çok Yüksek (Mevsimsel Nakit Akışı)",
        tech_adoption_tier="Gelenekçi (Laggard)"
    ),
    TurkishArchetype(
        archetype_code="ENTREPRENEUR_WEALTH",
        archetype_title="Yeni Dönem Girişimci & Sermaye Sahibi",
        population_share_pct=10.0,
        typical_occupations=["E-Ticaret Şirketi Sahibi", "Müteahhit", "İhracatçı / Fabrikatör", "Yatırımcı / Kripto Tüccarı"],
        typical_age_bracket=(30, 55),
        dominant_pain_points=[
            "Döviz kuru dalgalanmaları ve ithalat maliyetleri",
            "Vergi dilimleri ve finansmana erişim (kredi faizleri)",
            "Nitelikli personel tutma ve operasyonel verimsizlik",
            "Rakiplerin agresif fiyat kırması"
        ],
        speech_patterns=[
            "Bana zaman kazandırmayacak hiçbir şeye tek kuruş vermem.",
            "Bunu haftaya şirketimde kurabilir miyiz? Hızlı ölçeklenmesi şart.",
            "Ekibimle konuşayım, pilot uygulamayı başlatalım.",
            "Fiyat önemli değil, bana cirodaki artışı göster."
        ],
        psychological_defense="Rasyonalizasyon ve Güç Gösterisi ('Vaktim nakitten daha değerli')",
        price_sensitivity="Düşük (Zaman ve Ölçek Odaklı)",
        tech_adoption_tier="Yenilikçi (Innovator)"
    )
]


class ArchetypeRegistry:
    """Provides weighted archetype sampling matching current Turkish demographic proportions."""

    @classmethod
    def get_weighted_archetype(cls, rng: Optional[random.Random] = None) -> TurkishArchetype:
        r = rng or random.Random()
        weights = [a.population_share_pct for a in TURKISH_POPULATION_ARCHETYPES]
        return r.choices(TURKISH_POPULATION_ARCHETYPES, weights=weights)[0]

    @classmethod
    def find_archetype_by_occupation(cls, occupation: str) -> TurkishArchetype:
        occ_lower = occupation.lower()
        for a in TURKISH_POPULATION_ARCHETYPES:
            if any(t.lower() in occ_lower for t in a.typical_occupations):
                return a
        if any(w in occ_lower for w in ["mühendis", "yazılım", "analist", "müdür", "mimar"]):
            return TURKISH_POPULATION_ARCHETYPES[1]
        elif any(w in occ_lower for w in ["öğrenci", "stajyer", "garson", "kurye", "işsiz"]):
            return TURKISH_POPULATION_ARCHETYPES[2]
        elif any(w in occ_lower for w in ["memur", "öğretmen", "polis", "hemşire"]):
            return TURKISH_POPULATION_ARCHETYPES[3]
        elif any(w in occ_lower for w in ["çiftçi", "arıcı", "tarım", "muhtar"]):
            return TURKISH_POPULATION_ARCHETYPES[4]
        elif any(w in occ_lower for w in ["holding", "ceo", "kurucu", "ihracat"]):
            return TURKISH_POPULATION_ARCHETYPES[5]
        return TURKISH_POPULATION_ARCHETYPES[0]
