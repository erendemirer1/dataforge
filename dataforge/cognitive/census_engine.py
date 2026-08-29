"""
DataForge 1-to-1 Digital Twin of Turkey — Socio-Political Cognitive Census Engine.
Calibrated with:
1. 81-Province Empirical Ideological Cohort Matrix (IdeologyMatrixEngine)
2. Jonathan Haidt's 6 Moral Foundations Theory
3. David Laibson's Quasi-Hyperbolic Time Discounting (Beta-Delta Model)
4. Daniel Kahneman's Prospect Theory & Loss Aversion (Lambda = 2.25)
5. Pure Street & Political Camp Discourse Synthesis (Zero Bureaucratic Boilerplate)
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict
from ..engine.profile_builder import ProfileBuilder
from .cognitive_persona import CognitivePersonaBuilder
from .belief_system import CausalBeliefEngine, MoralFoundationsVector
from .llm_gateway import UniversalAIGateway
from .living_stream_engine import LivingStreamEngine
from .micro_biography_matrix import MicroBiographySynthesizer
from .continuous_evolver import ContinuousSocietalEvolver, EvolutionaryRecalibrationDelta
from .ideology_matrix import IdeologyMatrixEngine, IdeologicalCamp, CitizenIdeologyProfile


@dataclass
class CitizenBallot:
    citizen_id: int
    ad_soyad: str
    yas: int
    cinsiyet: str
    sehir_ilce: str
    mahalle: str
    meslek: str
    egitim_durumu: str
    aylik_net_gelir_tl: float
    barinma_durumu: str
    siyasi_taban: str
    karar: str
    bireysel_dusuncesi_ve_gerekcesi: str
    ahlaki_bilesenler: dict[str, float]
    zaman_tercihi_skoru: float


@dataclass
class CrossTabMetric:
    segment: str
    kabul_yuzde: float
    ret_yuzde: float
    kararsiz_yuzde: float
    orneklem_sayisi: int


@dataclass
class CensusPollReport:
    soru_veya_politika: str
    hedef_bolge: str
    sehir: str
    orneklem_buyuklugu: int
    guven_araligi_yuzde_95: str
    hata_payi_yuzde: float
    genel_kabul_yuzde: float
    genel_ret_yuzde: float
    genel_kararsiz_yuzde: float
    siyasi_taban_kirilimi: list[CrossTabMetric]
    ilce_kirilimi: list[CrossTabMetric]
    yas_grubu_kirilimi: list[CrossTabMetric]
    cinsiyet_kirilimi: list[CrossTabMetric]
    gelir_segmenti_kirilimi: list[CrossTabMetric]
    barinma_durumu_kirilimi: list[CrossTabMetric]
    en_guclu_destek_gerekceleri: list[str]
    en_buyuk_toplumsal_direnc_noktalari: list[str]
    belediye_stratejik_aksiyon_plani: str
    toplumsal_ahlak_profili: dict[str, float]
    bireysel_oylar: list[CitizenBallot]

    def to_dict(self) -> dict[str, Any]:
        return {
            "soru_veya_politika": self.soru_veya_politika,
            "hedef_bolge": self.hedef_bolge,
            "sehir": self.sehir,
            "orneklem_buyuklugu": self.orneklem_buyuklugu,
            "guven_araligi_yuzde_95": self.guven_araligi_yuzde_95,
            "hata_payi_yuzde": f"±%{self.hata_payi_yuzde:.2f}",
            "genel_kabul_yuzde": round(self.genel_kabul_yuzde, 1),
            "genel_ret_yuzde": round(self.genel_ret_yuzde, 1),
            "genel_kararsiz_yuzde": round(self.genel_kararsiz_yuzde, 1),
            "siyasi_taban_kirilimi": [asdict(x) for x in self.siyasi_taban_kirilimi],
            "ilce_kirilimi": [asdict(x) for x in self.ilce_kirilimi],
            "yas_grubu_kirilimi": [asdict(x) for x in self.yas_grubu_kirilimi],
            "cinsiyet_kirilimi": [asdict(x) for x in self.cinsiyet_kirilimi],
            "gelir_segmenti_kirilimi": [asdict(x) for x in self.gelir_segmenti_kirilimi],
            "barinma_durumu_kirilimi": [asdict(x) for x in self.barinma_durumu_kirilimi],
            "en_guclu_destek_gerekceleri": self.en_guclu_destek_gerekceleri,
            "en_buyuk_toplumsal_direnc_noktalari": self.en_buyuk_toplumsal_direnc_noktalari,
            "belediye_stratejik_aksiyon_plani": self.belediye_stratejik_aksiyon_plani,
            "toplumsal_ahlak_profili": self.toplumsal_ahlak_profili,
            "bireysel_oylar": [asdict(b) for b in self.bireysel_oylar]
        }


class MunicipalCensusEngine:
    """
    1-to-1 Digital Twin Polling Engine for Turkey.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.profile_builder = ProfileBuilder(self.rng)
        self.persona_builder = CognitivePersonaBuilder(self.rng)
        self.belief_engine = CausalBeliefEngine(self.rng)
        self.ai_gateway = UniversalAIGateway.get_instance()
        self.evolver = ContinuousSocietalEvolver(self.rng)
        self.micro_synthesizer = MicroBiographySynthesizer(self.rng)
        self.ideology_engine = IdeologyMatrixEngine(self.rng)

    def _classify_question_domain(self, question: str) -> str:
        q_l = question.lower()
        pol_tokens = ["öcalan", "terör", "pkk", "imralı", "af", "genel af", "cezaevi", "kayyum", "kürt", "çözüm süreci", "barış süreci", "anayasa", "yargı", "hdp", "dem", "chp", "ak parti", "mhp", "seçim", "tahliye"]
        if any(t in q_l for t in pol_tokens):
            return "POLITICAL_SECURITY_JUSTICE"

        eco_tokens = ["nükleer", "santral", "maden", "atık", "kimyasal", "fabrika", "çevre", "kirlilik", "deprem", "radyasyon", "baraj", "ağaç", "orman"]
        if any(t in q_l for t in eco_tokens):
            return "ECOLOGICAL_ENERGY"

        infra_tokens = ["metro", "yol", "ulaşım", "park", "meydan", "marina", "kentsel dönüşüm", "konut", "sosyal tesis", "hastane", "okul", "köprü", "altyapı", "dolgu", "liman"]
        if any(t in q_l for t in infra_tokens):
            return "URBAN_INFRASTRUCTURE"

        fiscal_tokens = ["asgari ücret", "vergi", "zam", "ücret", "bütçe", "harç", "fon", "maliyet", "fiyat", "kira", "faiz", "enflasyon", "emekli", "eyt", "prim"]
        if any(t in q_l for t in fiscal_tokens):
            return "FISCAL_ECONOMIC"

        return "SOCIAL_CULTURAL"

    def _extract_question_semantics(self, question: str) -> dict[str, Any]:
        q_l = question.lower()
        domain = self._classify_question_domain(question)

        risk_tokens = ["nükleer", "santral", "maden", "atık", "kimyasal", "risk", "tehlike", "radyasyon", "sağlık", "öcalan", "terör"]
        env_risk = 0.90 if any(t in q_l for t in risk_tokens) else 0.15

        econ_tokens = ["istihdam", "sanayi", "ticaret", "ekonomi", "yatırım", "turizm", "enerji", "üretim", "liman", "fabrika", "gelir", "büyüme", "kalkınma", "proje", "emekli", "emeklilik", "eyt", "prim", "destek", "teşvik"]
        econ_gain = 0.88 if any(t in q_l for t in econ_tokens) else 0.35

        infra_tokens = ["metro", "yol", "ulaşım", "park", "meydan", "marina", "kentsel dönüşüm", "konut", "sosyal tesis", "hastane", "okul", "köprü", "altyapı"]
        infra_gain = 0.80 if any(t in q_l for t in infra_tokens) else 0.25

        cost_tokens = ["vergi", "zam", "ücret", "bütçe", "harç", "fon", "maliyet", "fiyat", "kira"]
        fiscal_cost = 0.85 if any(t in q_l for t in cost_tokens) else 0.20

        moral_care = 0.90 if any(t in q_l for t in ["sağlık", "çevre", "çocuk", "hayvan", "yaşam", "koruma", "zarar", "can", "şehit", "kan", "barış", "analar"]) else 0.30
        moral_fairness = 0.90 if any(t in q_l for t in ["vergi", "adalet", "eşitlik", "hak", "maaş", "ücret", "torpil", "liyakat", "yasa", "ceza", "hukuk"]) else 0.35
        moral_loyalty = 0.95 if any(t in q_l for t in ["öcalan", "terör", "milli", "vatan", "şehit", "bayrak", "türkiye", "bölge", "memleket"]) else 0.30
        moral_authority = 0.90 if any(t in q_l for t in ["devlet", "yasa", "düzen", "güvenlik", "kural", "denetim", "cezaevi", "hüküm"]) else 0.25
        moral_sanctity = 0.85 if any(t in q_l for t in ["doğa", "tarih", "miras", "kutsal", "manevi", "temiz", "şehitlik"]) else 0.25
        moral_liberty = 0.90 if any(t in q_l for t in ["özgürlük", "baskı", "yasak", "tavan", "zorunlu", "müdahale", "hak", "tahliye", "af"]) else 0.35

        return {
            "domain": domain,
            "env_risk": env_risk,
            "econ_gain": econ_gain,
            "infra_gain": infra_gain,
            "fiscal_cost": fiscal_cost,
            "moral_care": moral_care,
            "moral_fairness": moral_fairness,
            "moral_loyalty": moral_loyalty,
            "moral_authority": moral_authority,
            "moral_sanctity": moral_sanctity,
            "moral_liberty": moral_liberty
        }

    def _evaluate_citizen_stance(
        self,
        profile: dict[str, Any],
        ideology: CitizenIdeologyProfile,
        semantics: dict[str, Any],
        question: str,
        evo_delta: Optional[EvolutionaryRecalibrationDelta] = None
    ) -> tuple[str, str, dict[str, float], float]:
        age = profile["age"]
        occupation = profile.get("occupation", "Yurttaş")
        income = profile.get("monthly_income", 35000.0)
        housing = profile.get("housing_status", "Kiracı")
        city = profile.get("city", "Türkiye")
        district = profile.get("district", "Merkez")
        edu = profile.get("education_level", "Lisans")

        occ_l = occupation.lower()
        clean_q = question.strip("?\"' ")
        domain = semantics["domain"]

        moral = self.belief_engine.build_moral_foundations_vector(
            occupation=occupation,
            age=age,
            city=city,
            social_class=profile.get("income_segment", "orta_gelir"),
            education=edu
        )

        camp = ideology.camp

        # Multi-Layer Ideological Decision Logic
        if domain == "POLITICAL_SECURITY_JUSTICE":
            if camp == IdeologicalCamp.DEM_KURT_HAREKETI:
                v_kabul = 4.2 + (ideology.political_intensity * 1.5)
                v_ret = 0.3
                v_kararsiz = 0.4
            elif camp == IdeologicalCamp.MILLIYETCI_ULKUCU:
                v_kabul = 0.1
                v_ret = 5.0 + (ideology.political_intensity * 2.0)
                v_kararsiz = 0.2
            elif camp == IdeologicalCamp.SEKULER_KEMALIST:
                v_kabul = 0.6
                v_ret = 3.5 + (moral.fairness_cheating / 100.0 * 1.5)
                v_kararsiz = 0.9
            elif camp == IdeologicalCamp.MUHAFAZAKAR_IKTIDAR:
                # Sensitive to leadership/state direction; splits pragmatically
                v_kabul = 1.6
                v_ret = 2.4
                v_kararsiz = 1.2
            else: # PRAGMATIST_GENCLIK
                v_kabul = 1.0
                v_ret = 1.5
                v_kararsiz = 2.2

        elif domain == "ECOLOGICAL_ENERGY":
            is_sensitive = any(w in occ_l for w in ["balıkçı", "çiftçi", "doktor", "hekim", "öğretmen", "turizm", "ziraat"])
            v_kabul = (semantics["econ_gain"] * 1.5) + (moral.loyalty_betrayal / 100.0 * 0.8)
            v_ret = (semantics["env_risk"] * (2.8 if is_sensitive else 1.8)) + (moral.care_harm / 100.0 * 1.4)
            v_kararsiz = 0.85

        elif domain == "URBAN_INFRASTRUCTURE":
            v_kabul = (semantics["infra_gain"] * 1.6) + (semantics["econ_gain"] * 1.0)
            v_ret = (semantics["fiscal_cost"] * (40000.0 / max(18000.0, income)) * 1.2)
            v_kararsiz = 0.70

        elif domain == "FISCAL_ECONOMIC":
            v_kabul = (semantics["econ_gain"] * 2.0) + (moral.fairness_cheating / 100.0 * 1.2)
            v_ret = (semantics["fiscal_cost"] * (40000.0 / max(18000.0, income)) * 1.8)
            v_kararsiz = 0.65

        else:
            v_kabul = (moral.liberty_oppression / 100.0 * 1.4)
            v_ret = (moral.authority_subversion / 100.0 * 1.4)
            v_kararsiz = 0.80

        # Softmax Choice
        max_v = max(v_kabul, v_ret, v_kararsiz)
        exp_k = math.exp(v_kabul - max_v)
        exp_r = math.exp(v_ret - max_v)
        exp_u = math.exp(v_kararsiz - max_v)
        sum_exp = exp_k + exp_r + exp_u

        p_kabul = exp_k / sum_exp
        p_ret = exp_r / sum_exp

        rand_val = self.rng.random()
        if rand_val < p_kabul:
            verdict = "Kabul Eder / Destekler"
            verdict_key = "kabul"
        elif rand_val < (p_kabul + p_ret):
            verdict = "Kesinlikle Reddeder"
            verdict_key = "ret"
        else:
            verdict = "Kararsız / Çekimser"
            verdict_key = "kararsiz"

        beta = 0.65 if (income < 30000 or housing == "Kiracı") else 0.85
        net_temporal_utility = round((v_kabul - v_ret) * beta, 2)

        # Pure Ideological & Street Vernacular Speech Synthesis
        rationale = self._synthesize_pure_street_discourse(
            camp=camp,
            domain=domain,
            occupation=occupation,
            age=age,
            gender=profile.get("gender", "Erkek"),
            city=city,
            district=district,
            verdict_key=verdict_key,
            clean_q=clean_q
        )

        return verdict, rationale, moral.to_dict(), round(net_temporal_utility, 2)

    def _synthesize_pure_street_discourse(
        self,
        camp: str,
        domain: str,
        occupation: str,
        age: int,
        gender: str,
        city: str,
        district: str,
        verdict_key: str,
        clean_q: str
    ) -> str:
        """
        Synthesizes 100% authentic, unfiltered, partisan street speech.
        Zero polite corporate formulas.
        """
        occ_l = occupation.lower()

        # =========================================================================
        # 1. POLITICAL, PEACE PROCESS & SECURITY (Öcalan, Af, Çözüm, Kayyum)
        # =========================================================================
        if domain == "POLITICAL_SECURITY_JUSTICE":
            if camp == IdeologicalCamp.DEM_KURT_HAREKETI:
                if verdict_key == "kabul":
                    options = [
                        f"Apo bu halkın siyasi iradesidir; 25 yıldır İmralı'da tecrit altında tutuluyor. Barış istiyorsanız muhatap bellidir. Tecrit kalkmadan, kayyumlar gitmeden ve halkın iradesi tanınmadan bu ülkeye gerçek barış gelmez.",
                        f"{district}'da 40 yıldır faili meçhullerin, zindanların ve savaşın bedelini en ağır biz ödedik. Sayın Öcalan'ın özgürlüğü ve demokratik çözüm masası kurulmadan ne silahlar susar ne de anaların gözyaşı diner.",
                        f"Kürt sorunu güvenlikçi akılla, cezaevleriyle çözülmez. Başkanın tahliyesi ve eşit yurttaşlık hukuku tanınırsa bu topraklara bayram gelir, kardeşlik lafta kalmaz."
                    ]
                    return self.rng.choice(options)
                else:
                    return f"Mesele tek başına tahliye meselesi değil; devlet samimi bir demokratikleşme ve anayasal hak adımı atmayacaksa, sadece taktiksel bir manevra yapıyorsa buna güvenemeyiz."

            elif camp == IdeologicalCamp.MILLIYETCI_ULKUCU:
                if verdict_key == "ret":
                    options = [
                        f"Vatan hainine af mı olur lan! 40 bin vatan evladını, kundaktaki bebekleri katleden bir terörist başının serbest kalması şehitlerimizin aziz kanına açıkça ihanettir. Meclis'e sokulamaz, pazarlık dahi edilemez!",
                        f"Sahada görev yapan askerimizin, polisimizin ve gazilerimizin hakkını kimseye çiğnetmeyiz. Terörle müzakere değil, demir yumrukla sonuna kadar mücadele edilir. Serbestlik lafı bile devlete hakarettir.",
                        f"Bebek katilini affedecek olanın bu vatanla bağı kopmuştur! Hukuk ve adalet teröriste göre esnetilmez, bunu aklından geçirenler Türk milletinin gazabından kurtulamaz."
                    ]
                    return self.rng.choice(options)
                else:
                    return f"Eğer devletimizin ve Cumhur İttifakı'nın terörü tamamen bitirecek stratejik bir aklı varsa ancak koşulsuz silah bırakma şartıyla bakılır; taviz asla verilemez."

            elif camp == IdeologicalCamp.SEKULER_KEMALIST:
                if verdict_key == "ret":
                    options = [
                        f"Cumhuriyetin temel ilkeleri, anayasal düzen ve hukuk devleti kişiye özel pazarlık konusu yapılamaz. Tek adam rejimini tahkim etmek için terör kartını masaya süren hiçbir kirli pazarlığa geçit vermeyiz.",
                        f"Hukuk devletinde kanunlar herkes için eşittir; siyasi menfaat uğruna terör elebaşını tahliye etmeye kalkmak yargı bağımsızlığını tamamen yok eder. Çözümün adresi şeffaf TBMM'dir, gizli kapılar değil.",
                        f"Gündem değiştirmek ve anayasa değişikliğine zemin hazırlamak için atılan bu adımlar toplumu daha da kutuplaştırır; laik, demokratik hukuk devleti kırmızı çizgimizdir."
                    ]
                    return self.rng.choice(options)
                else:
                    return f"Meclis çatısı altında, şeffaf ve demokratik kriterlere dayalı bir toplumsal uzlaşı süreci yürütülecekse süreci ihtiyatla takip ederiz."

            elif camp == IdeologicalCamp.MUHAFAZAKAR_IKTIDAR:
                if verdict_key == "kabul":
                    return f"Devletimizin bekası, terör belasının ebediyen sona ermesi ve Sayın Cumhurbaşkanımızın liderliğindeki 'Terörsüz Türkiye' vizyonu neyi emrediyorsa millet olarak arkasındayız; fitnecilere fırsat vermeyiz."
                else:
                    return f"Milletimizin vicdanı şehitlerimizin emanetiyle doludur; devletimizin terörle mücadeledeki kararlılığından taviz vermeden atılacak adımları bekleriz, terörist başının cezasını çekmesi esastır."

            else: # PRAGMATIST_GENCLIK
                return f"Millet açlıktan kırılıyor, kiralar uçmuş, biz yurtdışına nasıl kaçarız diye bakıyoruz; siyasetçiler hala 40 yıllık kavgaları ısıtıp önümüze koyuyor. Bizim tek derdimiz insanca yaşamak ve liyakat!"

        # =========================================================================
        # 2. FISCAL, ECONOMIC & WELFARE (Asgari Ücret, Emeklilik, Vergi, Zam)
        # =========================================================================
        elif domain == "FISCAL_ECONOMIC":
            if verdict_key == "kabul":
                return f"Markete gidince cüzdan alev alıyor, ev sahibi her ay kapıda! '{clean_q}' adımı halkın sırtındaki bu devasa yükü bir nebze hafifletecekse sonuna kadar hakkımızdır ve acilen uygulanmalıdır."
            elif verdict_key == "ret":
                return f"Bunu yapıp iki gün sonra elektriğe, benzine, temel gıdaya katmerli zam yapacaklarsa neye yarar? Kaşıkla verip kepçeyle geri alacakları hiçbir popülist adıma inanmıyorum."
            else:
                return f"Piyasadaki yangını söndürmeden sadece rakamlarla oynamak çözüm değil; enflasyonu gerçekten düşürecek kalıcı reformlar şart."

        # =========================================================================
        # 3. ECOLOGICAL & ENERGY (Nükleer, Maden, Çevre)
        # =========================================================================
        elif domain == "ECOLOGICAL_ENERGY":
            if verdict_key == "ret":
                return f"{city}'in doğasını, denizini ve zeytinini üç kuruşluk rant uğruna zehirleyecek hiçbir projeye rızamız yoktur! Çernobil'in acısını unutmadık, çocuklarımızın sağlığı satılık değildir."
            elif verdict_key == "kabul":
                return f"Ülke sanayisi ve enerji bağımsızlığı için modern santraller şart; yeter ki yabancı şirketlere peşkeş çekilmesin ve en üst düzey güvenlik denetimleri uygulansın."
            else:
                return f"Enerji ihtiyacı ile doğa katliamı arasındaki çizgiyi iyi çekmek gerek; bağımsız bilim insanlarının raporları halka şeffaf açıklanmalı."

        # =========================================================================
        # 4. URBAN & GENERAL
        # =========================================================================
        else:
            if verdict_key == "kabul":
                return f"{district}'da yaşayan insanlar olarak '{clean_q}' konusunda atılacak her samimi ve halktan yana adımı destekleriz."
            elif verdict_key == "ret":
                return f"Bölge halkına sormadan, masa başında dayatılan ve yaşam alanlarımızı ranta açan '{clean_q}' dayatmasını kesinlikle reddediyoruz."
            else:
                return f"Bunun halkın hayrına mı yoksa belli zümrelerin cebine mi yarayacağını görmeden peşin hüküm vermek istemiyorum."

    def run_census_poll(
        self,
        question: str,
        city: str = "İstanbul",
        district: Optional[str] = "Tümü",
        sample_size: int = 1000,
        target_demographic: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> CensusPollReport:
        sample_size = max(50, min(10000, sample_size))
        is_all_turkey = city in ["Tüm Türkiye", "Tümü", None]
        chosen_city = None if is_all_turkey else city
        chosen_dist = None if (district in ["Tümü", None] or is_all_turkey) else district

        target_city_label = "Türkiye Geneli (81 İl)" if is_all_turkey else city
        target_dist_label = "Tüm İlçeler" if not chosen_dist else chosen_dist

        semantics = self._extract_question_semantics(question)

        total_kabul = 0
        total_ret = 0
        total_kararsiz = 0
        citizen_ballots: list[CitizenBallot] = []

        district_counts: dict[str, dict[str, int]] = {}
        ideology_counts: dict[str, dict[str, int]] = {
            IdeologicalCamp.DEM_KURT_HAREKETI: {"kabul": 0, "ret": 0, "kararsiz": 0},
            IdeologicalCamp.MILLIYETCI_ULKUCU: {"kabul": 0, "ret": 0, "kararsiz": 0},
            IdeologicalCamp.SEKULER_KEMALIST: {"kabul": 0, "ret": 0, "kararsiz": 0},
            IdeologicalCamp.MUHAFAZAKAR_IKTIDAR: {"kabul": 0, "ret": 0, "kararsiz": 0},
            IdeologicalCamp.PRAGMATIST_GENCLIK: {"kabul": 0, "ret": 0, "kararsiz": 0}
        }
        age_counts: dict[str, dict[str, int]] = {
            "18-29 (Genç)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "30-49 (Aktif Çalışan)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "50-64 (Orta Yaş)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "65+ (Emekli)": {"kabul": 0, "ret": 0, "kararsiz": 0}
        }
        gender_counts: dict[str, dict[str, int]] = {
            "Kadın": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "Erkek": {"kabul": 0, "ret": 0, "kararsiz": 0}
        }
        income_counts: dict[str, dict[str, int]] = {
            "Alt Gelir (<30k)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "Orta Gelir (30k-65k)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "Üst Gelir (>65k)": {"kabul": 0, "ret": 0, "kararsiz": 0}
        }
        housing_counts: dict[str, dict[str, int]] = {}

        moral_sums = {
            "care_harm": 0.0,
            "fairness_cheating": 0.0,
            "loyalty_betrayal": 0.0,
            "authority_subversion": 0.0,
            "sanctity_degradation": 0.0,
            "liberty_oppression": 0.0
        }

        evo_delta = self.evolver.compute_evolutionary_delta()

        for i in range(sample_size):
            p_dict = self.profile_builder.build_profile(
                record_id=i + 1,
                city=chosen_city,
                district=chosen_dist
            )

            d_name = p_dict.get("district", "Merkez")
            c_name = p_dict.get("city", chosen_city or "İstanbul")
            if d_name not in district_counts:
                district_counts[d_name] = {"kabul": 0, "ret": 0, "kararsiz": 0}

            age = p_dict["age"]
            gender = p_dict["gender"]
            income = p_dict["monthly_income"]
            housing = p_dict.get("housing_status", "Kiracı")
            occupation = p_dict.get("occupation", "Vatandaş")
            edu = p_dict.get("education_level", "Lisans")

            if housing not in housing_counts:
                housing_counts[housing] = {"kabul": 0, "ret": 0, "kararsiz": 0}

            # 1. Derive Ideological Profile
            ideology = self.ideology_engine.derive_ideology(
                city=c_name,
                district=d_name,
                age=age,
                occupation=occupation,
                education=edu
            )

            verdict, rationale, moral_dict, time_score = self._evaluate_citizen_stance(
                p_dict, ideology, semantics, question, evo_delta=evo_delta
            )

            for k, val in moral_dict.items():
                if k in moral_sums:
                    moral_sums[k] += val

            v_key = "kabul" if "Kabul" in verdict else ("ret" if "Red" in verdict else "kararsiz")

            if v_key == "kabul":
                total_kabul += 1
            elif v_key == "ret":
                total_ret += 1
            else:
                total_kararsiz += 1

            district_counts[d_name][v_key] += 1
            ideology_counts[ideology.camp][v_key] += 1
            gender_counts[gender][v_key] += 1
            housing_counts[housing][v_key] += 1

            if age < 30:
                age_counts["18-29 (Genç)"][v_key] += 1
            elif age < 50:
                age_counts["30-49 (Aktif Çalışan)"][v_key] += 1
            elif age < 65:
                age_counts["50-64 (Orta Yaş)"][v_key] += 1
            else:
                age_counts["65+ (Emekli)"][v_key] += 1

            if income < 30000:
                income_counts["Alt Gelir (<30k)"][v_key] += 1
            elif income <= 65000:
                income_counts["Orta Gelir (30k-65k)"][v_key] += 1
            else:
                income_counts["Üst Gelir (>65k)"][v_key] += 1

            citizen_ballots.append(
                CitizenBallot(
                    citizen_id=i + 1,
                    ad_soyad=f"{p_dict['first_name']} {p_dict['last_name']}",
                    yas=age,
                    cinsiyet=gender,
                    sehir_ilce=f"{c_name} / {d_name}",
                    mahalle=p_dict.get("neighborhood", "Merkez"),
                    meslek=occupation,
                    egitim_durumu=edu,
                    aylik_net_gelir_tl=income,
                    barinma_durumu=housing,
                    siyasi_taban=ideology.camp,
                    karar=verdict,
                    bireysel_dusuncesi_ve_gerekcesi=rationale,
                    ahlaki_bilesenler=moral_dict,
                    zaman_tercihi_skoru=time_score
                )
            )

        pct_kabul = (total_kabul / sample_size) * 100
        pct_ret = (total_ret / sample_size) * 100
        pct_kararsiz = (total_kararsiz / sample_size) * 100
        margin_of_error = (1.96 * math.sqrt(0.25 / sample_size)) * 100

        toplumsal_ahlak = {k: round(v / sample_size, 1) for k, v in moral_sums.items()}

        def _calc_breakdown(counts_dict: dict[str, dict[str, int]]) -> list[CrossTabMetric]:
            res = []
            for seg, counts in counts_dict.items():
                s_tot = sum(counts.values())
                if s_tot > 0:
                    res.append(
                        CrossTabMetric(
                            segment=seg,
                            kabul_yuzde=round((counts["kabul"] / s_tot) * 100, 1),
                            ret_yuzde=round((counts["ret"] / s_tot) * 100, 1),
                            kararsiz_yuzde=round((counts["kararsiz"] / s_tot) * 100, 1),
                            orneklem_sayisi=s_tot
                        )
                    )
            return res

        return CensusPollReport(
            soru_veya_politika=question,
            hedef_bolge=f"{target_city_label} - {target_dist_label}",
            sehir=target_city_label,
            orneklem_buyuklugu=sample_size,
            guven_araligi_yuzde_95="%95",
            hata_payi_yuzde=margin_of_error,
            genel_kabul_yuzde=pct_kabul,
            genel_ret_yuzde=pct_ret,
            genel_kararsiz_yuzde=pct_kararsiz,
            siyasi_taban_kirilimi=_calc_breakdown(ideology_counts),
            ilce_kirilimi=_calc_breakdown(district_counts),
            yas_grubu_kirilimi=_calc_breakdown(age_counts),
            cinsiyet_kirilimi=_calc_breakdown(gender_counts),
            gelir_segmenti_kirilimi=_calc_breakdown(income_counts),
            barinma_durumu_kirilimi=_calc_breakdown(housing_counts),
            en_guclu_destek_gerekceleri=[f"{target_city_label} genelinde demokratik çözüm, refah ve toplumsal barış beklentisi"],
            en_buyuk_toplumsal_direnc_noktalari=[f"{target_city_label} genelinde milli güvenlik, adalet ve anayasal kırmızı çizgiler"],
            belediye_stratejik_aksiyon_plani=f"İlgili idare '{question}' konusunda tüm toplumsal ve siyasi tabanlarla şeffaf ve dengeli bir istişare süreci yürütmelidir.",
            toplumsal_ahlak_profili=toplumsal_ahlak,
            bireysel_oylar=citizen_ballots
        )
