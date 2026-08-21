"""
DataForge Full Cognitive Persona & Digital Twin Model.
Synthesizes Demographics + Bourdieu Habitus + Haidt Morals + Neuro-Psychology into a living persona.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass, asdict
from .habitus_matrix import HabitusEngine, SociologicalHabitus
from .neuro_state import NeuroCognitiveEngine, NeuroCognitiveState
from .micro_traits import MicroTraitSynthesizer, CognitiveMicroTraits
from .belief_system import CausalBeliefEngine, LatentBeliefVector
from .historical_memory import HistoricalMemoryEngine, BiographicalMemory
from .deep_causal_framework import DeepCausalFramework, BourdieuCapitalVector, NeuroPsychologicalState, HaidtMoralProfile


@dataclass
class DeepCognitivePersona:
    # 1. Kimlik ve Coğrafya
    id: int
    tckn: str
    ad_soyad: str
    cinsiyet: str
    yas: int
    sehir_ilce: str
    meslek: str
    egitim_durumu: str

    # 2. Somut Finansal Bütçe
    aylik_net_gelir_tl: float
    aylik_sabit_gider_tl: float
    aylik_serbest_harcanabilir_tl: float
    borcluluk_orani: float

    # 3. Sınıf, Habitus ve Ahlak
    habitus: SociologicalHabitus

    # 4. Nörobilişsel Zihin
    neuro: NeuroCognitiveState

    # 5. Bilişsel İnanç ve Değer Vektörü (Causal Latent Belief State)
    latent_belief: LatentBeliefVector

    # 6. Tarihsel Yaşam ve Kriz Hafızası (Episodic Biographical Memory)
    historical_memory: BiographicalMemory

    # 7. Psikolojik Mikro-Nüanslar & Dijital Kimlik
    micro_traits: CognitiveMicroTraits

    # 8. Derin Nedensel Çıkarım Vektörleri
    bourdieu_capitals: Optional[BourdieuCapitalVector] = None
    neuro_psych: Optional[NeuroPsychologicalState] = None
    haidt_morals: Optional[HaidtMoralProfile] = None

    # 9. Psikolojik Derinlik & Günlük Hayat
    en_buyuk_gunluk_derdi: str = ""
    gizli_korkusu: str = ""
    sosyal_statu_kaygisi: str = ""
    konusma_ve_jargon_tarzi: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert persona into hierarchical dictionary."""
        d = asdict(self)
        return d


class CognitivePersonaBuilder:
    """Builds 100% grounded, deeply cognitive, neuro-sociologically complete personas."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.habitus_engine = HabitusEngine(self.rng)
        self.neuro_engine = NeuroCognitiveEngine(self.rng)
        self.micro_trait_engine = MicroTraitSynthesizer(self.rng)
        self.belief_engine = CausalBeliefEngine(self.rng)
        self.memory_engine = HistoricalMemoryEngine(self.rng)
        self.deep_causal = DeepCausalFramework(self.rng)

    def build_from_raw(self, raw_person: dict[str, Any], record_id: int = 1) -> DeepCognitivePersona:
        """Transforms a demographic person dict into a deep cognitive agent."""
        age = int(raw_person.get("yas", 32))
        income = float(raw_person.get("aylik_net_gelir_tl", raw_person.get("aylik_ortalama_gelir_tl", 38000.0)))
        city = raw_person.get("sehir", raw_person.get("sehir_ilce", "İstanbul").split("/")[0].strip())
        district = raw_person.get("ilce", "Merkez")
        occupation = raw_person.get("meslek_rol", raw_person.get("meslek", "Vatandaş"))
        education = raw_person.get("egitim_durumu", "Lise")
        housing_status = raw_person.get("housing_status", "Kiracı")

        # 1. Financial Cashflow Calculation
        fixed_ratio = self.rng.uniform(0.55, 0.78)
        fixed_expenses = round(income * fixed_ratio, 2)
        debt_ratio = round(self.rng.uniform(0.10, 0.45), 2)
        discretionary = round(max(500.0, income - fixed_expenses - (income * debt_ratio * 0.3)), 2)

        # 2. Habitus & Moral Foundations
        habitus = self.habitus_engine.derive_habitus(
            city=city,
            district=district,
            occupation=occupation,
            education_level=education,
            income_tl=income,
            age=age
        )

        # 3. Neuro-Cognitive State
        neuro = self.neuro_engine.derive_neuro_state(
            income_tl=income,
            discretionary_budget_tl=discretionary,
            debt_ratio=debt_ratio,
            age=age,
            social_class=habitus.social_class_stratum,
            cultural_capital=habitus.cultural_capital_score
        )

        # 4. Deep Causal Mathematical Ensembles
        bourdieu_capitals = self.deep_causal.derive_bourdieu_capitals(
            income_tl=income,
            education_level=education,
            occupation=occupation,
            city=city,
            housing_status=housing_status
        )
        neuro_psych = self.deep_causal.derive_neuro_psychology(
            age=age,
            income_tl=income,
            economic_capital=bourdieu_capitals.economic_capital_score,
            discretionary_budget_tl=discretionary
        )
        haidt_morals = self.deep_causal.derive_haidt_moral_matrix(
            age=age,
            education_level=education,
            occupation=occupation,
            cultural_capital=bourdieu_capitals.cultural_capital_score
        )

        # 5. Latent Causal Belief Vector
        latent_belief = self.belief_engine.build_latent_belief_vector(
            occupation=occupation,
            social_class=habitus.social_class_stratum,
            age=age,
            city=city,
            monthly_income=income,
            fixed_expenses=fixed_expenses,
            habitus_moral=asdict(habitus.moral_foundations)
        )

        # 6. Episodic Biographical & Historical Memory
        historical_memory = self.memory_engine.generate_biographical_memory(
            age=age,
            occupation=occupation,
            social_class=habitus.social_class_stratum,
            city=city
        )

        # 7. Micro-Traits & Digital Subculture
        micro_traits = self.micro_trait_engine.generate_micro_traits(
            occupation=occupation,
            social_class=habitus.social_class_stratum,
            age=age,
            city=city
        )

        # 7. Psychological Frustrations & Speech Patterns
        occ_lower = occupation.lower()
        if any(w in occ_lower for w in ["gazi", "şehit", "asker", "astsubay", "uzman çavuş", "polis", "güvenlik"]):
            daily_pain = self.rng.choice([
                "Fiziksel protez/sağlık sorunları ve gazilik haklarının bürokraside yıpranması",
                "Şehit evladının hatırası ve geride kalan ailesinin onurunu koruma mücadelesi",
                "Vatan uğruna can verdikten sonra siyasette şehitlik kavramının ucuzlatılması hissi"
            ])
            hidden_fear = "Şehit kanının siyasi pazarlık konusu yapılması ve gazilerin haklarının gasp edilmesi"
            status_anxiety = "Şehitlik ve gazilik onurunun çiğnenmesi"
            jargon = "Vakar dolu, onurlu, vatansever ve net asker/kamu dili"
        elif any(w in occ_lower for w in ["öğrenci", "oyun", "yazılım", "tasarım", "genç", "stajyer", "çevirmen"]):
            daily_pain = self.rng.choice([
                "Geleceksizlik hissi, mezun olunca iş bulamama ve sosyal alanların daralması",
                "Sürekli getirilen platform yasakları, sansür ve teknolojiye erişim pahalılığı",
                "KYK bursunun hiçbir şeye yetmemesi ve aile evine hapsolma duygusu"
            ])
            hidden_fear = "Gençliğini hiçbir hayalini gerçekleştiremeden bu ülkede heba etmek"
            status_anxiety = "Akranlarının gerisinde kalmak ve çaresizce yerinde saymak"
            jargon = "Samimi, eleştirel, doğrudan ve dijital çağın dili"
        elif "Esnaf" in habitus.social_class_stratum:
            daily_pain = self.rng.choice([
                "Artan dükkan kirası ve toptancı vadelerinin kısalması",
                "Müşterinin sürekli kredi kartı istemesi ve POS komisyonları",
                "İyi eleman/çırak bulamamak, her işe tek başına koşmak"
            ])
            hidden_fear = "İflas edip piyasaya borçlu kalmak, esnaflık itibarını kaybetmek"
            status_anxiety = "Çarşıdaki diğer esnafların yanında küçük düşmek"
            jargon = "Samimi, şüpheci, esnaf argosu ve atasözleriyle harmanlanmış pragmatik dil"
        elif "Beyaz Yaka" in habitus.social_class_stratum:
            daily_pain = self.rng.choice([
                "Sürekli toplantılar, bitmeyen Slack mesajları ve tükenmişlik (burnout)",
                "İstanbul trafiğinde günde 2.5 saat kaybetmek ve kira artış baskısı",
                "Kariyerde tıkanma hissi ve enflasyon karşısında eriyen maaş"
            ])
            hidden_fear = "İşten çıkarılmak ve kredi kartı/konut kredisi borçlarıyla ortada kalmak"
            status_anxiety = "Akranlarının gerisinde kalmak, yetersiz ve başarısız görünmek"
            jargon = "Plaza Türkçesi (Feedback, deadline, ROI, sprint) ve entelektüel eleştirel üslup"
        elif "Kamu" in habitus.social_class_stratum:
            daily_pain = "Ay sonunu getirmek, sabit maaşın enflasyon karşısında erimesi"
            hidden_fear = "Soruşturma geçirmek veya tayinin istenmeyen bir yere çıkması"
            status_anxiety = "Lojman ve kurum içindeki hiyerarşide saygınlığını yitirmek"
            jargon = "Bürokratik, temkinli, kuralcı ve risksiz kamu dili"
        else:
            daily_pain = "Günübirlik iş bulma kaygısı ve ayın 15'inde biten nakit"
            hidden_fear = "Hastalık durumunda ailesine bakamamak ve aç kalmak"
            status_anxiety = "Mahallede ve akrabalar arasında dışlanmak/eziklenmek"
            jargon = "Kısa, net, hayatta kalma odaklı sokak dili"

        return DeepCognitivePersona(
            id=record_id,
            tckn=raw_person.get("tckn", "11111111110"),
            ad_soyad=raw_person.get("ad_soyad", "İsimsiz"),
            cinsiyet=raw_person.get("cinsiyet", "Erkek"),
            yas=age,
            sehir_ilce=raw_person.get("sehir_ilce", f"{city} / {district}"),
            meslek=occupation,
            egitim_durumu=education,
            aylik_net_gelir_tl=income,
            aylik_sabit_gider_tl=fixed_expenses,
            aylik_serbest_harcanabilir_tl=discretionary,
            borcluluk_orani=debt_ratio,
            habitus=habitus,
            neuro=neuro,
            latent_belief=latent_belief,
            historical_memory=historical_memory,
            micro_traits=micro_traits,
            bourdieu_capitals=bourdieu_capitals,
            neuro_psych=neuro_psych,
            haidt_morals=haidt_morals,
            en_buyuk_gunluk_derdi=daily_pain,
            gizli_korkusu=hidden_fear,
            sosyal_statu_kaygisi=status_anxiety,
            konusma_ve_jargon_tarzi=jargon
        )
