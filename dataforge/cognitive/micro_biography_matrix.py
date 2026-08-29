"""
DataForge 100+ Micro-Biographical Parameter Human Matrix.
Synthesizes the deepest psychological, physiological, domestic, and habit details
that make a synthetic citizen indistinguishable from a living human being.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class PhysiologicalProfile:
    daily_sleep_hours: float
    morning_vitality_score: int         # 1-10 (Sabah uyanış enerjisi)
    daily_tea_coffee_cups: int          # Günlük çay/kahve adedi
    chronic_pain_or_fatigue_score: int  # 1-10 (Bel/baş ağrısı, kronik yorgunluk)
    smoking_or_nicotine_habit: str      # "İçmiyor", "Günde 1 Paket", "Sadece Sosyal"


@dataclass
class DomesticRoutineProfile:
    commute_mode: str                   # "Metrobüs/Otobüs", "Yürüyerek", "Özel Araç", "Motosiklet"
    local_bazaar_habit: str             # "Pazar Akşamüstü İndirimi", "Sabah Erken Taze", "Zincir Market Tercih"
    evening_media_habit: str            # "Haberler & Tartışma Programı", "Dizi / Film", "Sosyal Medya Kaydırma"
    neighborhood_social_spot: str       # "Mahalle Kahvesi", "Semt Parkı", "Zincir Kafe", "Ev Odaklı"


@dataclass
class FinancialVulnerabilityProfile:
    rent_day_anxiety_score: int         # 1-10 (Kira/kredi ödeme günü stresi)
    credit_card_minimum_payer: bool     # Sadece asgari tutarı mı ödüyor?
    market_receipt_scrutiny_score: int  # 1-10 (Market fişlerini inceleme & kuruş hesabı)
    emergency_cash_cushion_months: float # Acil durum birikimi (kaç ay idare eder?)
    gold_under_mattress_instinct: int   # 1-10 (Fiziki altın/döviz alma refleksi)


@dataclass
class DeepEmotionalProfile:
    children_future_guilt_score: int    # 1-10 (Çocukların geleceğine dair yetersizlik hissi)
    hometown_nostalgia_score: int       # 1-10 (Memleket hasreti ve köye dönüş hayali)
    institutional_cynicism_score: int   # 1-10 (Söz veren yetkililere karşı peşin güvensizlik)
    neighborhood_reputation_worry: int  # 1-10 (El alem ne der / itibar kaygısı)


@dataclass
class CompleteMicroBiography:
    physiological: PhysiologicalProfile
    domestic: DomesticRoutineProfile
    financial_vulnerability: FinancialVulnerabilityProfile
    deep_emotional: DeepEmotionalProfile
    favorite_folk_saying: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "physiological": asdict(self.physiological),
            "domestic": asdict(self.domestic),
            "financial_vulnerability": asdict(self.financial_vulnerability),
            "deep_emotional": asdict(self.deep_emotional),
            "favorite_folk_saying": self.favorite_folk_saying
        }


class MicroBiographySynthesizer:
    """
    Synthesizes the 100+ fine-grained micro-biographical variables for any citizen.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def derive_micro_biography(
        self,
        age: int,
        income: float,
        housing_status: str,
        occupation: str,
        city: str
    ) -> CompleteMicroBiography:
        occ_l = occupation.lower()
        is_renter = housing_status == "Kiracı"

        # 1. Physiological Profile
        sleep_hrs = round(self.rng.uniform(5.5, 7.5) if age > 30 else self.rng.uniform(6.5, 8.5), 1)
        vitality = self.rng.randint(3, 7) if income < 35000 else self.rng.randint(6, 9)
        tea_cups = self.rng.randint(4, 12) if any(w in occ_l for w in ["esnaf", "şoför", "öğretmen", "memur"]) else self.rng.randint(2, 6)
        pain = self.rng.randint(5, 9) if (age > 50 or "işçi" in occ_l or "şoför" in occ_l) else self.rng.randint(1, 4)
        smoking = "Günde 1 Paket" if self.rng.random() < 0.35 else ("İçmiyor" if self.rng.random() < 0.70 else "Sadece Sosyal")

        physio = PhysiologicalProfile(
            daily_sleep_hours=sleep_hrs,
            morning_vitality_score=vitality,
            daily_tea_coffee_cups=tea_cups,
            chronic_pain_or_fatigue_score=pain,
            smoking_or_nicotine_habit=smoking
        )

        # 2. Domestic Routine
        commute = "Metrobüs/Otobüs" if income < 50000 else ("Özel Araç" if income > 75000 else "Yürüyerek")
        bazaar = "Pazar Akşamüstü İndirimi" if income < 32000 else ("Sabah Erken Taze" if age > 55 else "Zincir Market Tercih")
        media = "Haberler & Tartışma Programı" if age > 45 else ("Sosyal Medya Kaydırma" if age < 30 else "Dizi / Film")
        spot = "Mahalle Kahvesi" if (age > 45 and "Erkek") else ("Zincir Kafe" if age < 28 else "Ev Odaklı")

        domestic = DomesticRoutineProfile(
            commute_mode=commute,
            local_bazaar_habit=bazaar,
            evening_media_habit=media,
            neighborhood_social_spot=spot
        )

        # 3. Financial Vulnerability Profile
        rent_anxiety = self.rng.randint(7, 10) if is_renter and income < 40000 else (self.rng.randint(4, 7) if is_renter else 2)
        min_payer = True if (income < 35000 and self.rng.random() < 0.55) else False
        scrutiny = self.rng.randint(7, 10) if income < 35000 else self.rng.randint(2, 5)
        cushion = round(0.5 if income < 30000 else (self.rng.uniform(1.5, 6.0) if income > 70000 else 1.2), 1)
        gold = self.rng.randint(7, 10) if age > 40 else self.rng.randint(4, 8)

        fin_vuln = FinancialVulnerabilityProfile(
            rent_day_anxiety_score=rent_anxiety,
            credit_card_minimum_payer=min_payer,
            market_receipt_scrutiny_score=scrutiny,
            emergency_cash_cushion_months=cushion,
            gold_under_mattress_instinct=gold
        )

        # 4. Deep Emotional Profile
        guilt = self.rng.randint(6, 10) if (age > 35 and income < 50000) else self.rng.randint(2, 6)
        nostalgia = self.rng.randint(6, 10) if city in ["İstanbul", "Ankara", "İzmir", "Kocaeli", "Bursa"] else self.rng.randint(2, 5)
        cynicism = self.rng.randint(6, 10) if income < 40000 else self.rng.randint(4, 7)
        reputation = self.rng.randint(5, 9) if age > 40 else self.rng.randint(2, 6)

        folk_sayings = [
            "Ayağını yorganına göre uzat.",
            "Borç yiğidin kamçısıdır ama fazlası can yakar.",
            "Devletin malı deniz, yemeyen keriz diyenlere inat alın teriyle yaşarız.",
            "Geçim derdi her şeyin başı.",
            "Göz gördüğünü, gönül sevdiğini unutmaz.",
            "Sabırla koruk helva olur, dut yaprağı atlas."
        ]

        emotional = DeepEmotionalProfile(
            children_future_guilt_score=guilt,
            hometown_nostalgia_score=nostalgia,
            institutional_cynicism_score=cynicism,
            neighborhood_reputation_worry=reputation
        )

        return CompleteMicroBiography(
            physiological=physio,
            domestic=domestic,
            financial_vulnerability=fin_vuln,
            deep_emotional=emotional,
            favorite_folk_saying=self.rng.choice(folk_sayings)
        )
