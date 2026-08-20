"""
DataForge Vehicle & Mobility Engine.
Simulates driver license classes, vehicle ownership, car models, and fuel types
conditioned on TÜİK motor vehicle statistics, occupation, income, and district archetype.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class MobilityProfile:
    driving_license: str
    vehicle_ownership: str
    vehicle_model: Optional[str]
    vehicle_fuel_type: Optional[str]


class MobilityEngine:
    """Calculates realistic mobility and vehicle ownership profiles."""

    _instance: Optional["MobilityEngine"] = None

    @classmethod
    def get_instance(cls) -> "MobilityEngine":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_mobility(
        self,
        occupation: str,
        income_segment: str,
        age: int,
        is_metro: bool = True,
        rng: Optional[random.Random] = None,
    ) -> MobilityProfile:
        """Generate statistically coherent vehicle and transportation profile."""
        if rng is None:
            rng = random.Random()

        # 1. Driving License Class (Karayolları Trafik Kanunu)
        if "TIR" in occupation or "Kamyon" in occupation:
            license_class = "CE / E (Ağır Vasıta / TIR)"
        elif "Otobüs" in occupation or "Metrobüs" in occupation:
            license_class = "D (Otobüs / Toplu Taşıma)"
        elif "Kurye" in occupation or "Motosiklet" in occupation:
            license_class = "A2 (Motosiklet)"
        elif age < 19:
            license_class = rng.choices(["Yok", "B (Otomobil)"], weights=[0.70, 0.30])[0]
        else:
            license_class = rng.choices(["B (Otomobil)", "B + A2", "Yok"], weights=[0.82, 0.10, 0.08])[0]

        # 2. Vehicle Ownership & Model
        has_vehicle = True
        vehicle_type = "Otomobil"
        vehicle_model = None
        fuel = None

        if "Kurye" in occupation:
            vehicle_type = "Motosiklet"
            vehicle_model = rng.choice(["Honda Dio 110", "Yamaha NMAX 155", "RKS Bitter 50", "Honda PCX 125"])
            fuel = "Benzin"
        elif "Çiftçi" in occupation or "Ziraat" in occupation:
            vehicle_type = "Traktör / Ticari"
            vehicle_model = rng.choice(["New Holland T4", "Massey Ferguson 240", "Fiat Doblo 1.6 Multijet", "Ford Transit Courier"])
            fuel = "Dizel"
        elif "Taksi" in occupation:
            vehicle_type = "Ticari Taksi"
            vehicle_model = rng.choice(["Fiat Egea 1.4 Fire (Taksi)", "Renault Megane 1.5 dCi", "Toyota Corolla Hibrit"])
            fuel = rng.choice(["LPG / Benzin", "Hibrit", "Dizel"])
        elif income_segment == "ust_gelir":
            vehicle_type = "Lüks Otomobil / SUV"
            vehicle_model = rng.choice([
                "TOGG T10X V2 Uzun Menzil", "BMW 320i M Sport", "Mercedes-Benz C200",
                "Volvo XC60 Recharge", "Audi A6 Sedan", "Porsche Macan"
            ])
            fuel = rng.choice(["Hibrit / Elektrikli", "Benzin", "Dizel"])
        elif income_segment == "orta_ust":
            vehicle_type = "C/D Segment Otomobil / SUV"
            vehicle_model = rng.choice([
                "Volkswagen Passat / Tiguan", "Skoda Octavia 1.5 eTSI", "Peugeot 3008",
                "Toyota Corolla Hibrit", "Chery Tiggo 8 Pro", "Hyundai Tucson"
            ])
            fuel = rng.choice(["Hibrit / Elektrikli", "Benzin", "Dizel"])
        elif income_segment == "orta_gelir":
            vehicle_type = "B/C Segment Otomobil"
            vehicle_model = rng.choice([
                "Fiat Egea Sedan 1.4", "Renault Clio 1.0 TCe", "Renault Megane Sedan",
                "Hyundai i20", "Ford Focus", "Dacia Duster"
            ])
            fuel = rng.choice(["Benzin", "LPG / Benzin", "Dizel"])
        else:  # alt_gelir, orta_alt
            if rng.random() < 0.55:
                vehicle_type = "Yok (Toplu Taşıma / Kart)"
                vehicle_model = "Yok (İstanbulkart / EGO / İzmirim Kart)"
                fuel = None
                has_vehicle = False
            else:
                vehicle_type = "Ekonomik / Ticari"
                vehicle_model = rng.choice(["Fiat Doblo 1.3 Multijet", "Renault Symbol", "Hyundai Accent Era", "Mondial 125 Motosiklet"])
                fuel = rng.choice(["LPG / Benzin", "Dizel"])

        return MobilityProfile(
            driving_license=license_class,
            vehicle_ownership=vehicle_type,
            vehicle_model=vehicle_model,
            vehicle_fuel_type=fuel,
        )
