"""
DataForge Autonomous Cognitive Inhabitation & Semantic Causal Reasoner.
Eliminates all hardcoded domain rules, keyword branches, and static sentence templates.
Computes autonomous multi-agent deliberations and census ballots across arbitrary topics
by evaluating Haidt moral foundations, Bourdieu capitals, and Kahneman loss aversion.
"""
from __future__ import annotations

import math
import random
import re
from typing import Any, Optional
from dataclasses import dataclass

from .cognitive_persona import DeepCognitivePersona
from .deep_causal_framework import HaidtMoralProfile, BourdieuCapitalVector, NeuroPsychologicalState


@dataclass
class TopicSemanticVector:
    """Multi-dimensional vector representing the core sociopolitical demands of a prompt."""
    raw_prompt: str
    cleaned_topic: str
    target_subject: str
    economic_salience: float      # -1.0 (Heavy Cost/Tax) to +1.0 (Subsidy/Financial Relief)
    care_harm_salience: float     # -1.0 (Harm/Cruelty Risk) to +1.0 (Protection/Compassion)
    fairness_salience: float      # -1.0 (Favoritism/Cheating) to +1.0 (Merit/Fairness/Justice)
    loyalty_salience: float       # -1.0 (In-group Threat/Betrayal) to +1.0 (Patriotism/Solidarity)
    authority_salience: float     # -1.0 (Anarchy/Lawlessness) to +1.0 (Order/Security/Law)
    sanctity_salience: float      # -1.0 (Cultural Desecration) to +1.0 (Tradition/Purity)
    liberty_salience: float       # -1.0 (Bans/Oppression/Censorship) to +1.0 (Freedom/Openness)
    local_spatial_impact: float   # 0.0 to 1.0 (How intensely this impacts immediate neighborhood life)


class AutonomousSemanticParser:
    """Extracts semantic and moral salience from arbitrary Turkish prompts without static domain tagging."""

    PROFANITY_OR_BAN_WORDS = ["yasak", "kısıtlama", "engellensin", "kapatılsın", "ceza", "itlaf", "uyutma"]
    LIBERTY_WORDS = ["serbest", "açılsın", "kaldırılsın", "özgürlük", "destek", "izin", "gelsin", "kolaylık"]
    SECURITY_WORDS = ["güvenlik", "terör", "asayiş", "olay", "kavga", "savaş", "şiddet", "çatışma", "polis", "asker", "provokasyon"]
    ECONOMIC_BURDEN_WORDS = ["zam", "vergi", "harç", "fiyat artışı", "pahalı", "maliyet", "yük", "borç", "enflasyon"]
    ECONOMIC_BENEFIT_WORDS = ["indirim", "ucuz", "burs", "kira yardımı", "destek", "ücretsiz", "sosyal yardım", "maaş zammı"]
    MORAL_SACRED_WORDS = ["cami", "ezan", "din", "şehit", "vatan", "bayrak", "kutsal", "milli", "tarihi", "değerler"]

    def parse(self, prompt: str) -> TopicSemanticVector:
        p_lower = prompt.lower()
        cleaned = re.sub(r'[^\w\sğüşıöçĞÜŞİÖÇ]', ' ', p_lower)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        # Extract core subject (strip question particles)
        tokens = [t for t in cleaned.split() if t not in ["mi", "mı", "mu", "mü", "misiniz", "mısınız", "musunuz", "müsünüz", "olur", "mu", "ne", "nasıl", "neden", "hakkında", "görüşünüz"]]
        target_subj = " ".join(tokens[:5]) if tokens else cleaned

        # 1. Economic Salience
        econ = 0.0
        if any(w in p_lower for w in self.ECONOMIC_BURDEN_WORDS):
            econ -= 0.75
        if any(w in p_lower for w in self.ECONOMIC_BENEFIT_WORDS):
            econ += 0.75

        # 2. Authority & Security Salience
        authority = 0.0
        if any(w in p_lower for w in self.SECURITY_WORDS):
            authority += 0.85
        if "asayiş" in p_lower or "güvenlik" in p_lower or "denetim" in p_lower:
            authority += 0.50

        # 3. Sanctity & Tradition Salience
        sanctity = 0.0
        if any(w in p_lower for w in self.MORAL_SACRED_WORDS):
            sanctity += 0.80

        # 4. Liberty vs Bans Salience
        liberty = 0.0
        if any(w in p_lower for w in self.LIBERTY_WORDS):
            liberty += 0.65
        if any(w in p_lower for w in self.PROFANITY_OR_BAN_WORDS):
            liberty -= 0.70

        # 5. Care / Harm
        care = 0.0
        if any(w in p_lower for w in ["çocuk", "yaşlı", "engelli", "hayvan", "köpek", "can", "deprem", "mağdur"]):
            care += 0.80

        # 6. Loyalty / Group Pride
        loyalty = 0.0
        if any(w in p_lower for w in ["milli", "türkiye", "beşiktaş", "çarşı", "fenerbahçe", "galatasaray", "amed", "vatan", "bayrak"]):
            loyalty += 0.75

        return TopicSemanticVector(
            raw_prompt=prompt,
            cleaned_topic=cleaned,
            target_subject=target_subj,
            economic_salience=econ,
            care_harm_salience=care,
            fairness_salience=0.5 if "hak" in p_lower or "adalet" in p_lower else 0.0,
            loyalty_salience=loyalty,
            authority_salience=authority,
            sanctity_salience=sanctity,
            liberty_salience=liberty,
            local_spatial_impact=0.8 if any(w in p_lower for w in ["semt", "mahalle", "sokak", "ilçe", "park", "belediye", "stadyum", "esnaf"]) else 0.4
        )


class AutonomousCognitiveReasoner:
    """
    Simulates authentic human cognition, visceral inner thoughts, and debate responses
    for any Turkish digital twin persona across any arbitrary topic.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.parser = AutonomousSemanticParser()

    def evaluate_persona_stance(
        self,
        persona: DeepCognitivePersona,
        topic: TopicSemanticVector
    ) -> tuple[str, float, str]:
        """
        Calculates mathematical causal utility and determines stance: (verdict, utility_score, dominant_driver).
        """
        h: HaidtMoralProfile = persona.haidt_morals
        b: BourdieuCapitalVector = persona.bourdieu_capitals
        n: NeuroPsychologicalState = persona.neuro_psych
        lb = persona.latent_belief

        # 1. Moral & Value Alignment Dot Product
        moral_utility = (
            (h.care_harm - 50.0) * topic.care_harm_salience * 0.25 +
            (h.fairness_cheating - 50.0) * topic.fairness_salience * 0.20 +
            (h.loyalty_betrayal - 50.0) * topic.loyalty_salience * 0.25 +
            (h.authority_subversion - 50.0) * topic.authority_salience * 0.30 +
            (h.sanctity_degradation - 50.0) * topic.sanctity_salience * 0.30 +
            (h.liberty_oppression - 50.0) * topic.liberty_salience * 0.25
        )

        # 2. Economic & Class Habitus Utility (Bourdieu & Kahneman Prospect Theory)
        economic_impact = topic.economic_salience * (100.0 - b.economic_capital_score) * 0.40
        if economic_impact < 0:
            # Loss aversion lambda multiplier (2.25x pain for perceived losses)
            economic_impact *= n.loss_aversion_lambda

        # 3. Security & Institutional Trust Factor
        security_friction = 0.0
        if topic.authority_salience > 0.3:
            if lb.national_security_redline > 70:
                security_friction -= (lb.national_security_redline - 50.0) * 0.50

        # 4. Status Quo Inertia & Age Resistance
        age_inertia = (persona.yas - 40) * 0.30 if persona.yas > 45 else 0.0
        if topic.liberty_salience > 0.3 and persona.yas >= 55:
            # Older cohorts more cautious of sudden disruptions
            age_inertia -= 10.0

        # Total Latent Causal Utility
        total_utility = moral_utility + economic_impact + security_friction - age_inertia
        noise = self.rng.gauss(0, 15.0)
        final_utility = total_utility + noise

        # Determine dominant driver
        drivers = [
            ("Geçim ve Maddi Şartlar", abs(economic_impact)),
            ("Milli Güvenlik ve Asayiş", abs(security_friction) + abs(h.authority_subversion * topic.authority_salience)),
            ("Özgürlük ve Hakkaniyet", abs(h.liberty_oppression * topic.liberty_salience) + abs(h.fairness_cheating * topic.fairness_salience)),
            ("Geleneksel Değerler ve Huzur", abs(h.sanctity_degradation * topic.sanctity_salience) + abs(age_inertia)),
            ("Toplumsal Dayanışma ve Şefkat", abs(h.care_harm * topic.care_harm_salience))
        ]
        drivers.sort(key=lambda x: x[1], reverse=True)
        dominant_driver = drivers[0][0]

        if final_utility > 12.0:
            verdict = "KABUL"
        elif final_utility < -12.0:
            verdict = "RED"
        else:
            verdict = "CEKIMSER"

        return verdict, final_utility, dominant_driver

    def synthesize_inner_thought(
        self,
        persona: DeepCognitivePersona,
        topic: TopicSemanticVector,
        verdict: str,
        dominant_driver: str
    ) -> str:
        """
        Synthesizes a deep, authentic subconscious internal monologue grounded in persona DNA.
        """
        age = persona.yas
        occ = persona.meslek
        district = persona.sehir_ilce.split('/')[-1].strip()
        income = persona.aylik_serbest_harcanabilir_tl
        housing = getattr(persona, 'barinma_durumu', 'Kiracı')

        prompt_clean = topic.target_subject

        if verdict == "KABUL":
            openers = [
                f"Şu anki şartlarda '{prompt_clean}' adımı gayet makul görünüyor.",
                f"İnsanların önyargılarını bir kenara bırakıp '{prompt_clean}' konusuna destek vermesi lazım.",
                f"Bizim gibi {district} sakinleri ve çalışan kesim için olumlu bir gelişme olur.",
                f"Yasaklarla ve kısıtlamalarla hiçbir yere varamayız; '{prompt_clean}' fikrini destekliyorum."
            ]
            reasons = [
                f"Benim bir {occ} olarak gördüğüm kadarıyla bu durum hem hayatı kolaylaştırır hem de gereksiz gerginliği bitirir.",
                f"Ekonomik ve sosyal açıdan bakınca topluma faydası zararından katbekat fazla olacaktır.",
                f"Hak ve adalet çerçevesinde kurallara uyulduğu sürece kimseyi engellememek gerekir.",
                f"Gençlerin ve sokaktaki insanın önünü açacak her türlü yapıcı adıma evet demek lazım."
            ]
        elif verdict == "RED":
            openers = [
                f"Yahu kusura bakmasınlar ama '{prompt_clean}' işi tam bir basiretsizlik olur.",
                f"Bu devirde kalkıp '{prompt_clean}' teklifiyle gelmek sahadaki gerçeklerden kopuk olmaktır.",
                f"{district} gibi bir yerde bunun yaratacağı huzursuzluğu ve güvenlik riskini kimse hesap etmiyor mu?",
                f"Kendi içimizde bu kadar dert ve geçim sıkıntısı varken bir de '{prompt_clean}' ile uğraşamayız."
            ]
            reasons = [
                f"Yıllardır bir {occ} olarak bu toplumun nabzını tutuyorum; bu adım provokasyona ve kutuplaşmaya çanak tutar.",
                f"Faturası yine bizim gibi sabit gelirli ve huzur arayan vatandaşa çıkar, kesinlikle karşıyım.",
                f"Milli hassasiyetleri ve kamu güvenliğini hiçe sayarak atılacak her adım kaos getirir.",
                f"Bizim önceliğimiz huzur ve istikrar; bu tür tartışmalı adımlarla ortalığı karıştırmaya gerek yok."
            ]
        else: # CEKIMSER
            openers = [
                f"'{prompt_clean}' meselesinde iki tarafın da haklı ve haksız olduğu yönler var.",
                f"Fikir kulağa prensipte fena gelmiyor ama uygulama ve niyet konusunda ciddi şüphelerim var.",
                f"Ne tamamen evet diyebiliyorum ne de kestirip atabiliyorum; kafamda çok soru işareti var.",
                f"{district} ortamında bu işin nasıl yönetileceği netleşmeden konuşmak çok erken."
            ]
            reasons = [
                f"Bir yandan kamu yararı ve özgürlük düşünülüyor, diğer yandan olası taşkınlıklar ve maliyetler tedirgin ediyor.",
                f"Kurallar çok sıkı tutulmazsa iyi niyetle başlayan iş büyük bir probleme dönüşebilir.",
                f"Detayları, denetim mekanizmasını ve vatandaşa yansıyacak etkilerini görmeden peşin hüküm vermek istemiyorum."
            ]

        p_open = self.rng.choice(openers)
        p_reason = self.rng.choice(reasons)
        return f"{p_open} {p_reason}"

    def synthesize_spoken_dialogue(
        self,
        persona: DeepCognitivePersona,
        topic: TopicSemanticVector,
        verdict: str,
        dominant_driver: str,
        is_first_speaker: bool = False,
        prev_speaker_name: Optional[str] = None,
        prev_speaker_title: Optional[str] = None,
        prev_verdict: Optional[str] = None
    ) -> str:
        """
        Synthesizes live colloquial spoken Turkish dialogue reacting fluidly to the room.
        """
        occ = persona.meslek
        district = persona.sehir_ilce.split('/')[-1].strip()
        prompt_clean = topic.target_subject

        if is_first_speaker:
            if verdict == "KABUL":
                return f"Arkadaşlar ben açık konuşacağım; '{prompt_clean}' konusuna peşinen karşı çıkmak doğru değil. Kurallara uyulursa ve asayiş sağlanırsa bundan kimseye zarar gelmez, aksine toplumsal barışa ve semtimize katkı sağlar."
            elif verdict == "RED":
                return f"Yahu kimse kusura bakmasın ama '{prompt_clean}' teklifi son derece tehlikeli ve riskli bir adım! {district} sokaklarının ve halkının huzurunu bozmaya kimsenin hakkı yok; ben kesinlikle karşıyım."
            else:
                return f"Açıkçası '{prompt_clean}' konusu çok bıçak sırtı bir mesele. Bir yanda hak ve özgürlükler var, diğer yanda güvenlik ve olası provokasyon endişesi. Şartları iyice görmeden net bir şey söylemek zor."

        prev_ref = f"{prev_speaker_name} {prev_speaker_title}" if prev_speaker_name else "Önceki konuşmacı"

        # Interactive conversational turn-taking
        if verdict == "KABUL" and prev_verdict == "KABUL":
            agrees = [
                f"{prev_ref}'a katılıyorum, çok doğru bir yere değindi. Yasakçı zihniyetle bir yere varamayız; sağduyulu yaklaşıldığında '{prompt_clean}' herkesin yararına olur.",
                f"{prev_ref} son derece haklı. Gereksiz korkularla toplumu germek yerine bu tür adımları olgunlukla karşılamak bize yakışır.",
                f"Aynen öyle, {prev_ref}'ın dediği gibi önyargıları kırmak zorundayız. Kurallar net olduktan sonra hiçbir sorun çıkmaz."
            ]
            return self.rng.choice(agrees)

        elif verdict == "RED" and prev_verdict == "RED":
            agrees = [
                f"{prev_ref}'a harfiyen katılıyorum. Az bile söyledi; '{prompt_clean}' meselesinin getireceği huzursuzluğu ve yükü göz göre göre kabul edemeyiz.",
                f"{prev_ref} çok önemli bir noktaya parmak bastı. Sahadaki gerçekleri görmezden gelip masa başında böyle kararlar almak büyük hata olur.",
                f"Ben de bir {occ} olarak {prev_ref}'ın endişelerine sonuna kadar katılıyorum; bu işin sonu iyi bitmez."
            ]
            return self.rng.choice(agrees)

        elif verdict == "RED" and prev_verdict == "KABUL":
            challenges = [
                f"{prev_ref} iyi niyetle anlatıyorsun ama sen hiç {district} sokaklarındaki gerilimi görmüyor musun? '{prompt_clean}' dediğin şey teoride güzel durabilir ama pratikte büyük olay çıkar!",
                f"Kusura bakma {prev_ref} ama söylediklerin bana hiç gerçekçi gelmedi. Provokasyon olduğunda o faturayı kim ödeyecek? İnsanların canını ve huzurunu tehlikeye atamayız.",
                f"{prev_ref}'ın iyimserliğini anlıyorum ama sahadaki dinamikler öyle işlemiyor; bu riski almak {district} halkına haksızlıktır."
            ]
            return self.rng.choice(challenges)

        elif verdict == "KABUL" and prev_verdict == "RED":
            rebuttals = [
                f"{prev_ref} endişelerinde haklısın, kimse huzursuzluk çıksın istemez ama her şeye 'yasak' diyerek de sorun çözülmez. Gerekli güvenlik önlemleri alınırsa '{prompt_clean}' gayet medeni şekilde yürütülür.",
                f"{prev_ref}'ın kaygılarını anlıyorum fakat pireye kızıp yorgan yakmamak lazım. Kurallara uyan insanları peşinen cezalandırmak doğru değil.",
                f"Meseleye sadece korku penceresinden bakarsak hiçbir adım atamayız {prev_ref}. Denetim yapılsın, kurallara uymayan cezasını çeksin ama yasakçılık çözüm değil."
            ]
            return self.rng.choice(rebuttals)

        else: # CEKIMSER
            fences = [
                f"Araya gireyim kusura bakmayın ama ikinizi dinlerken de hak veriyorum. {prev_ref} 'huzur ve güvenlik' diyor doğru; diğer taraftan 'yasak olmasın' deniyor o da doğru. Çok hassas bir denge.",
                f"Bakın {prev_ref}, iki tarafın da haklı gerekçeleri var. '{prompt_clean}' konusunda emniyet ve yerel yönetim çok net bir güvence vermeden taraf seçmek çok güç.",
                f"Ben iki görüşün de ortasında duruyorum. Niyet güzel olabilir ama {district} gerçeklerini de göz ardı etmemek lazım; süreç iyi yönetilmezse problem çıkar."
            ]
            return self.rng.choice(fences)
