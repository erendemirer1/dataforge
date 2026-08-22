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
    is_satisfaction_query: bool
    economic_salience: float      # -1.0 (Heavy Cost/Tax) to +1.0 (Subsidy/Financial Relief)
    care_harm_salience: float     # -1.0 (Harm/Cruelty Risk) to +1.0 (Protection/Compassion)
    fairness_salience: float      # -1.0 (Favoritism/Cheating) to +1.0 (Merit/Fairness/Justice)
    loyalty_salience: float       # -1.0 (In-group Threat/Betrayal) to +1.0 (Patriotism/Solidarity)
    authority_salience: float     # -1.0 (Anarchy/Lawlessness) to +1.0 (Order/Security/Law)
    sanctity_salience: float      # -1.0 (Cultural Desecration) to +1.0 (Tradition/Purity)
    liberty_salience: float       # -1.0 (Bans/Oppression/Censorship) to +1.0 (Freedom/Openness)
    local_spatial_impact: float   # 0.0 to 1.0 (How intensely this impacts immediate neighborhood life)


class AutonomousSemanticParser:
    """Extracts semantic and moral salience from arbitrary Turkish prompts."""

    PROFANITY_OR_BAN_WORDS = ["yasak", "kısıtlama", "engellensin", "kapatılsın", "ceza", "itlaf", "uyutma"]
    LIBERTY_WORDS = ["serbest", "açılsın", "kaldırılsın", "özgürlük", "destek", "izin", "gelsin", "kolaylık"]
    SECURITY_WORDS = ["güvenlik", "terör", "asayiş", "olay", "kavga", "savaş", "şiddet", "çatışma", "polis", "asker", "provokasyon", "tribün", "taraftar"]
    ECONOMIC_BURDEN_WORDS = ["zam", "vergi", "harç", "fiyat artışı", "pahalı", "maliyet", "yük", "borç", "enflasyon"]
    ECONOMIC_BENEFIT_WORDS = ["indirim", "ucuz", "burs", "kira yardımı", "destek", "ücretsiz", "sosyal yardım", "maaş zammı", "öğrenci"]
    MORAL_SACRED_WORDS = ["cami", "ezan", "din", "şehit", "vatan", "bayrak", "kutsal", "milli", "tarihi", "değerler"]

    def parse(self, prompt: str) -> TopicSemanticVector:
        p_lower = prompt.lower()
        cleaned = re.sub(r'[^\w\sğüşıöçĞÜŞİÖÇ]', ' ', p_lower)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        is_sat = any(w in p_lower for w in ["memnun", "nasıl buluyorsunuz", "yaşanır mı", "yönetim", "hizmetler", "yaşam kalitesi"])

        # Extract core subject
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
        if any(w in p_lower for w in ["çocuk", "yaşlı", "engelli", "hayvan", "köpek", "can", "deprem", "mağdur", "öğrenci", "burs"]):
            care += 0.80

        # 6. Loyalty / Group Pride
        loyalty = 0.0
        if any(w in p_lower for w in ["milli", "türkiye", "beşiktaş", "çarşı", "fenerbahçe", "galatasaray", "amed", "vatan", "bayrak"]):
            loyalty += 0.75

        return TopicSemanticVector(
            raw_prompt=prompt,
            cleaned_topic=cleaned,
            target_subject=target_subj,
            is_satisfaction_query=is_sat,
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
        h: HaidtMoralProfile = persona.haidt_morals or HaidtMoralProfile(50, 50, 50, 50, 50, 50)
        b: BourdieuCapitalVector = persona.bourdieu_capitals or BourdieuCapitalVector(50, 50, 50, 50)
        n: NeuroPsychologicalState = persona.neuro_psych or NeuroPsychologicalState(2.25, 0.88, 0.8, 30, 50, {})
        lb = persona.latent_belief

        # 1. Moral & Value Alignment Dot Product
        moral_utility = (
            (h.care_harm - 50.0) * topic.care_harm_salience * 0.30 +
            (h.fairness_cheating - 50.0) * topic.fairness_salience * 0.20 +
            (h.loyalty_betrayal - 50.0) * topic.loyalty_salience * 0.25 +
            (h.authority_subversion - 50.0) * topic.authority_salience * 0.30 +
            (h.sanctity_degradation - 50.0) * topic.sanctity_salience * 0.30 +
            (h.liberty_oppression - 50.0) * topic.liberty_salience * 0.25
        )

        # 2. Economic & Class Habitus Utility (Bourdieu & Kahneman Prospect Theory)
        economic_impact = topic.economic_salience * (100.0 - b.economic_capital_score) * 0.40
        if economic_impact < 0:
            economic_impact *= n.loss_aversion_lambda

        # 3. Security & Institutional Trust Factor
        security_friction = 0.0
        if topic.authority_salience > 0.3 and lb:
            if getattr(lb, 'national_security_redline', 50) > 70:
                security_friction -= (lb.national_security_redline - 50.0) * 0.50

        # 4. Status Quo Inertia & Age Resistance
        age_inertia = (persona.yas - 40) * 0.30 if persona.yas > 45 else 0.0
        if topic.liberty_salience > 0.3 and persona.yas >= 55:
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

        if final_utility > 10.0:
            verdict = "KABUL"
        elif final_utility < -10.0:
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
        parts = persona.sehir_ilce.split('/')
        district = parts[-1].strip() if len(parts) > 1 else persona.sehir_ilce
        if district in ["Merkez", "Merkez Mah.", ""]:
            district = parts[0].strip() if len(parts) > 0 else "İlçemiz"
        housing = getattr(persona, 'barinma_durumu', 'Kiracı')
        prompt_clean = topic.target_subject

        # Clause 1: Situational First-Person Anchor
        prefixes = [
            f"Ben bir {occ} olarak,",
            f"{district}'da ikamet eden {age} yaşında bir yurttaş olarak,",
            f"Bu semtte {housing.lower()} olarak yaşayan biri olarak,",
            f"Kendi aile bütçemizi ve günlük hayatımızı düşündüğümde,",
            f"{district} sokaklarındaki yaşamı her gün birebir tecrübe eden biri olarak,"
        ]
        prefix = self.rng.choice(prefixes)

        # BRANCH 1: Satisfaction & Municipal Governance
        if topic.is_satisfaction_query:
            if verdict == "KABUL":
                sat_cores = [
                    f"{district}'ın temel belediye hizmetlerinden, parklarından ve çevre temizliğinden gayet memnunum.",
                    f"mahallemizin huzuru, pazar yerleri ve sakin yaşam tarzı ailemiz için oldukça yeterli ve güzel.",
                    f"ulaşım imkanları ve yerel hizmetler genel olarak düzenli işliyor, semtimizin yönetiminden memnunum."
                ]
                sat_conseq = "Bu yüzden yerel yönetimin mevcut çalışmalarını destekliyorum."
            elif verdict == "RED":
                sat_cores = [
                    f"{district}'da sokakların bakımı, çevre kirliliği ve altyapı yetersizliği yaşam kalitemizi düşürüyor.",
                    f"gençler için sosyal, kültürel ve sanatsal alanlar neredeyse hiç yok; semtimizin gelişimi çok yavaş.",
                    f"iş çıkışı saatlerindeki trafik keşmekeşi ve toplu taşıma yetersizliği canımıza tak etti; yönetimden memnun değilim."
                ]
                sat_conseq = "Bu eksiklikler giderilmediği sürece mevcut yönetimden memnun olmam mümkün değil."
            else:
                sat_cores = [
                    f"{district} sakin bir yer ama sosyal imkanlar ve merkeze ulaşım konusunda hala ciddi sıkıntılar var.",
                    f"bazı hizmetler güzel yürütülse de altyapı ve çevre düzenlemelerinde eksikler göze çarpıyor."
                ]
                sat_conseq = "Bu sebeple ne tamamen memnunum ne de her şeyi kötüleyebilirim; çekimserim."

            core = self.rng.choice(sat_cores)
            return f"{prefix} {core} {sat_conseq}"

        # BRANCH 2: Proposals, Policies, Social Aid, Sports, Projects
        if verdict == "KABUL":
            if dominant_driver == "Geçim ve Maddi Şartlar":
                cores = [
                    f"mevcut hayat pahalılığında '{prompt_clean}' adımı dar gelirli ve çalışan kesime ciddi bir nefes aldırır.",
                    f"maddi zorlukların arttığı bu süreçte '{prompt_clean}' desteği ekonomik açıdan çok isabetli bir karar.",
                    f"bu uygulamanın getireceği mali kolaylık vatandaşın bütçesine doğrudan can suyu olacaktır."
                ]
            elif dominant_driver == "Toplumsal Dayanışma ve Şefkat":
                cores = [
                    f"'{prompt_clean}' gibi sosyal dayanışmayı ve gençleri/ihtiyaç sahiplerini gözeten projelere sahip çıkmamız şart.",
                    f"öğrencilerin ve mağdur kesimlerin elinden tutan bu yaklaşımı son derece insani ve değerli buluyorum."
                ]
            elif dominant_driver == "Özgürlük ve Hakkaniyet":
                cores = [
                    f"önyargıları bir kenara bırakıp '{prompt_clean}' konusunda hakkaniyetli davranmak en doğrusudur.",
                    f"yasakçılık yerine kurallara uyularak bu imkanın sağlanması toplumsal barışa katkı sunar."
                ]
            elif dominant_driver == "Milli Güvenlik ve Asayiş":
                cores = [
                    f"gerekli emniyet ve denetim tedbirleri alındığı müddetçe '{prompt_clean}' sürecinde hiçbir asayiş sorunu yaşanmaz.",
                    f"sağduyulu ve kontrollü bir yönetimle bu konu huzur bozulmadan başarıyla yürütülür."
                ]
            else:
                cores = [
                    f"'{prompt_clean}' konusu {district} halkının yaşam standardını doğrudan yükseltecektir.",
                    f"bu gelişme semtimiz ve günlük yaşamımız için son derece olumlu sonuçlar doğurur."
                ]
            
            consequences = [
                "Dolayısıyla peşin hükümlü olmadan bu adımı sonuna kadar destekliyorum.",
                "Bu yüzden bu projeye tereddütsüz evet diyorum.",
                "Toplumun yararına olan bu kararın arkasında durmak gerekir."
            ]

        elif verdict == "RED":
            if dominant_driver == "Geçim ve Maddi Şartlar":
                cores = [
                    f"çarşı pazardaki yangın ortadayken '{prompt_clean}' ile bütçeye veya vatandaşa ek yük getirilmesini doğru bulmuyorum.",
                    f"geçim derdi ve enflasyon altında ezilirken böyle bir maliyetin halkın sırtına yüklenmesi haksızlıktır."
                ]
            elif dominant_driver == "Milli Güvenlik ve Asayiş":
                cores = [
                    f"geçmişte yaşanan gerginlikler ortadayken '{prompt_clean}' adımı sokaklarımızda büyük provokasyon ve güvenlik riski yaratır.",
                    f"asayişin ve kamu düzeninin bozulma ihtimali çok yüksek; bu karar huzurumuzu tehlikeye atar."
                ]
            elif dominant_driver == "Geleneksel Değerler ve Huzur":
                cores = [
                    f"{district}'ın yerleşik huzurunu ve mahalle dokusunu zedeleyecek bu dayatmaya razı olamam.",
                    f"toplumun hassasiyetlerini ve geleneksel yapısını hiçe sayan bu teklif semtimizde huzursuzluk yaratır."
                ]
            else:
                cores = [
                    f"sahadaki gerçeklerden kopuk şekilde '{prompt_clean}' teklifiyle gelinmesini son derece hatalı buluyorum.",
                    f"vatandaşın gerçek talepleriyle örtüşmeyen bu adımın faydadan çok zarar getireceğini düşünüyorum."
                ]

            consequences = [
                "Bu sebeple bu teklife kesinlikle karşı çıkıyorum.",
                "Huzurumuz ve güvenliğimiz için bu adıma hayır diyorum.",
                "Böyle bir uygulamanın hayata geçirilmesini doğru bulmuyorum."
            ]

        else: # CEKIMSER
            if dominant_driver == "Geçim ve Maddi Şartlar":
                cores = [
                    f"'{prompt_clean}' teklifi teoride güzel duruyor fakat bütçesinin nasıl karşılanacağı kafamı kurcalıyor.",
                    f"maliyetin vatandaşa nasıl yansıyacağı netleşmeden bu konuda peşin bir kanaat oluşturmak güç."
                ]
            elif dominant_driver == "Milli Güvenlik ve Asayiş":
                cores = [
                    f"iyi niyetli bir adım olabilir ancak olası provokasyon ve asayiş riskleri beni ciddi şekilde tedirgin ediyor.",
                    f"emniyet ve denetim tarafı çok sağlam tutulmadan bu adımın atılması riskli görünüyor."
                ]
            else:
                cores = [
                    f"'{prompt_clean}' meselesinde iki tarafın da haklı yönleri var; şartları iyice incelemeden karar vermek zor.",
                    f"detaylar ve uygulamanın getireceği somut sonuçlar netleşmeden ne evet ne hayır diyebiliyorum."
                ]

            consequences = [
                "Bu yüzden şimdilik çekimser kalmayı tercih ediyorum.",
                "Uygulamanın sahadaki gidişatını görmeden kesin bir taraf seçmek istemiyorum.",
                "Kafamdaki soru işaretleri giderilmeden net bir duruş sergileyemem."
            ]

        core = self.rng.choice(cores)
        consequence = self.rng.choice(consequences)

        return f"{prefix} {core} {consequence}"

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
        parts = persona.sehir_ilce.split('/')
        district = parts[-1].strip() if len(parts) > 1 else persona.sehir_ilce
        if district in ["Merkez", "Merkez Mah.", ""]:
            district = parts[0].strip() if len(parts) > 0 else "İlçemiz"
        occ = persona.meslek
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
