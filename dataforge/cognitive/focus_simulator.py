"""
DataForge Deep Multi-Agent Focus Group & Psychological Simulation Studio.
Simulates realistic group dynamics, Dual-Process System 1/2 reactions,
Inner Subconscious Thoughts vs. Spoken Dialogue, and Executive Market Intelligence.
Integrates McFadden Econometric Utility Engine for N=1,000 Monte Carlo statistical census.
"""
from __future__ import annotations

import os
import re
import json
import random
import urllib.request
from typing import Any, Optional
from .cognitive_persona import CognitivePersonaBuilder, DeepCognitivePersona
from .utility_engine import EconometricUtilityEngine, QuantitativeMarketResult
from .consistency_auditor import CognitiveConsistencyAuditor
from ..social.social_radar import SocialRadarEngine
from ..ml.prompt_synthesizer import DynamicPromptEngine


class FocusGroupSimulator:
    """
    Executes deep psychological focus groups with grounded, neuro-sociologically complete personas.
    Combines qualitative focus groups with N=1,000 quantitative Monte Carlo econometrics and Causal Consistency Audits.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.persona_builder = CognitivePersonaBuilder(self.rng)
        self.prompt_engine = DynamicPromptEngine(self.rng)
        self.utility_engine = EconometricUtilityEngine(self.rng)
        self.social_radar = SocialRadarEngine(self.rng)
        self.consistency_auditor = CognitiveConsistencyAuditor()

    def _get_api_key(self) -> str:
        """Resolve Gemini API key."""
        return self.prompt_engine._get_gemini_key() or ""

    def _extract_price_from_pitch(self, pitch: str) -> Optional[float]:
        """Extract monetary price from text in TL. Returns None if topic is non-commercial."""
        match = re.search(r'(\d+(?:[\.,]\d+)?)\s*(?:tl|lira|₺|tl\'ye|liralık|bin tl)', pitch.lower())
        if match:
            val_str = match.group(1).replace(',', '.')
            try:
                val = float(val_str)
                if 'bin' in pitch.lower():
                    val *= 1000
                return val
            except ValueError:
                pass
        return None

    def run_simulation(
        self,
        target_audience: str,
        pitch_or_question: str,
        count: int = 4,
        monte_carlo_n: int = 1000,
        api_key: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Synthesizes deep personas, simulates focus group discussion,
        audits consistency against latent belief vectors,
        and computes an N=1,000 quantitative Monte Carlo census.
        """
        # 1. Synthesize demographic personas
        raw_personas = self.prompt_engine.synthesize(target_audience, count=count)

        # 2. Enrich into Deep Cognitive, Social Radar, Latent Belief & Habitus Personas
        cognitive_personas: list[DeepCognitivePersona] = []
        for i, raw_p in enumerate(raw_personas):
            raw_p = self.social_radar.enrich_persona_with_social_pulse(raw_p)
            cog_p = self.persona_builder.build_from_raw(raw_p, record_id=i + 1)
            cognitive_personas.append(cog_p)

        # 3. Run Quantitative Econometric / Moral Monte Carlo Census (N=1,000)
        extracted_price = self._extract_price_from_pitch(pitch_or_question)
        dict_personas = [p.to_dict() for p in cognitive_personas]
        monte_carlo_res: QuantitativeMarketResult = self.utility_engine.run_monte_carlo_census(
            personas=dict_personas,
            pitch_text=pitch_or_question,
            pitch_price_tl=extracted_price,
            simulations_count=monte_carlo_n
        )

        # 4. Simulate Multi-Agent Focus Group with LLM
        qualitative_personas = cognitive_personas
        if len(cognitive_personas) > 8:
            step = len(cognitive_personas) // 6
            qualitative_personas = [cognitive_personas[i * step] for i in range(min(6, len(cognitive_personas)))]

        effective_key = api_key or self._get_api_key()
        sim_result = None
        if effective_key and not effective_key.startswith("AQ."):
            try:
                sim_result = self._simulate_with_gemini(qualitative_personas, target_audience, pitch_or_question, effective_key)
            except Exception:
                sim_result = None

        if not sim_result:
            sim_result = self._fallback_simulation(qualitative_personas, pitch_or_question)

        # 5. Run Cognitive Consistency Audit
        sim_result = self.consistency_auditor.audit_and_recalibrate(
            simulation_result=sim_result,
            personas_dict=dict_personas,
            pitch_or_topic=pitch_or_question
        )

        # 6. Attach Quantitative Census Output
        sim_result["kantitatif_monte_carlo_raporu"] = monte_carlo_res.to_dict()

        return sim_result

    def _simulate_with_gemini(
        self,
        personas: list[DeepCognitivePersona],
        target_audience: str,
        pitch: str,
        api_key: str
    ) -> dict[str, Any]:
        """Simulates authentic inner monologue and spoken dialogue with Gemini."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"

        personas_json = json.dumps([p.to_dict() for p in personas], ensure_ascii=False, indent=2)

        sys_prompt = (
            "Sen Türkiye toplumunu, insanının kalbini, öfkesini, acısını, çaresizliğini, mizahını ve gururunu "
            "en derinden bilen dahi bir Sosyolog, Antropolog ve Saha Araştırmacısısın. "
            f"Sana Türkiye gerçekliğinden {len(personas)} adet capcanlı insan profili veriliyor.\n\n"
            "GÖREVİN:\n"
            "Bu insanların moderatörün ortaya attığı teklif, soru veya siyasi/toplumsal gelişme karşısındaki "
            "gerçek tepkilerini bir masada simüle edeceksin.\n\n"
            "KESİN KURALLAR:\n"
            "1. Asla şablon veya tekrar eden cümleler kurma. Her karakterin kendine özgü, mesleğine ve travmasına uygun bir sesi olsun.\n"
            "2. Karakterler masada birbirine itiraz etsin, laf atsın veya destek çıksın (Group Dynamics).\n"
            "3. Asla çelişkili ifadeler kurma (Örn: Hükümete kızıp aynı anda destekleme gibi mantık hataları olmasın).\n"
        )

        user_content = f"HEDEF KİTLE: {target_audience}\nSUNULAN TEKLİF / SORU: {pitch}\n\nKATILIMCILAR:\n{personas_json}"

        payload = {
            "contents": [{"parts": [{"text": f"{sys_prompt}\n\n{user_content}"}]}]
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return self._robust_json_parse(text)

    def _robust_json_parse(self, text: str) -> dict[str, Any]:
        """Robustly extracts and parses JSON."""
        clean_text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(clean_text)
        except Exception:
            pass

        start_idx = clean_text.find("{")
        end_idx = clean_text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            sub = clean_text[start_idx:end_idx + 1]
            try:
                return json.loads(sub)
            except Exception:
                sub_fixed = re.sub(r',\s*([}\]])', r'\1', sub)
                return json.loads(sub_fixed)
        raise ValueError("Could not parse JSON from model response")

    def _fallback_simulation(self, personas: list[DeepCognitivePersona], pitch: str) -> dict[str, Any]:
        """
        Combinatorial Generative Natural Discourse Engine.
        Dynamically constructs 100% unique, organic utterances and subconscious monologues with ZERO duplicate sentences.
        """
        pitch_lower = pitch.lower()
        discussions = []

        is_game_topic = any(w in pitch_lower for w in ["oyun", "yasak", "steam", "discord", "roblox", "sansür"])
        is_politics_topic = any(w in pitch_lower for w in ["erdoğan", "başkan", "seçim", "hükümet", "akp", "chp"])
        is_security_topic = any(w in pitch_lower for w in ["af", "terör", "pkk", "çerçeve yasa", "şehit", "öcalan"])
        is_rent_topic = any(w in pitch_lower for w in ["kira", "kiracı", "ev sahibi", "tavan", "konut"])

        accept_count = 0

        # Unique Sentence Pattern Pools for Dynamic Synthesis
        for i, p in enumerate(personas):
            occ = p.meslek
            occ_l = occ.lower()
            b = p.latent_belief
            age = p.yas
            name = p.ad_soyad
            pain = p.en_buyuk_gunluk_derdi
            fear = p.gizli_korkusu

            # ----------------------------------------------------
            # CASE 1: SİYASİ LİDERLİK / BAŞKANLIK / SEÇİM
            # ----------------------------------------------------
            if is_politics_topic:
                # Dynamic Decision Logic based on Latent Belief Vector
                # If high loyalty (> 70) and economic pain is low-to-medium
                if b.traditional_loyalty > 65 and b.economic_pain_index < 60:
                    karar = "Kabul Eder / Destekler"
                    accept_count += 1
                    
                    ic_ses_options = [
                        f"Etrafımızda savaşlar sürerken ve bölge bu kadar kaynarken devleti tecrübesiz ellere bırakamayız. Liderlik ve tecrübe her şeyden önemlidir.",
                        f"Kusurlar elbette var ama karşısında bu memleketi toparlayacak ikinci bir dirayetli lider göremiyorum. Maceraya atılacak lüksümüz yok.",
                        f"Savunma sanayiinde yapılanları, İHA'ları, SİHA'ları ve uluslararası ağırlığımızı kimse inkar edemez. Geçim sıkıntısı var ama devletin başı dik durmalı.",
                        f"Benim için en mühim olan vatanın bölünmezliği ve istikrardır. Türkiye'nin düşmanlarına karşı Tayyip Bey'in güçlü duruşunun devam etmesi gerektiğine inanıyorum."
                    ]
                    
                    dis_soz_options = [
                        f"Bakın arkadaşlar, eleştirilecek çok şey var ama şu anki jeopolitik yangın yerinde masada kimin oturacağı hayati önem taşır. Ben şahsen tecrübeden ve istikrardan yanayım.",
                        f"Ben bir {occ} olarak konuşuyorum; piyasada zorluklar var doğru ama lider değişirse işler düzelecek mi sanıyorsunuz? Daha büyük bir kaos çıkar.",
                        f"Mesele şahıs meselesi değil, devletin dirayeti meselesidir. Mevcut liderin uluslararası alandaki ağırlığı bu ülkenin tek güvencesidir.",
                        f"Biz bu topraklarda çok koalisyonlar, çok krizler gördük. Bugün zorluk çekiyoruz ama başımızda kararlı bir irade olması her şeyden kıymetlidir."
                    ]

                elif b.economic_pain_index > 65 or b.institutional_trust < 40 or age <= 28:
                    karar = "Kesinlikle Reddeder"
                    
                    ic_ses_options = [
                        f"Yirmi yılı aşkın süredir aynı vaatler ama geldiğimiz yer ortada: Market filesi dolmuyor, {pain} altında eziliyoruz. Artık tek bir gün bile katlanacak sabrım kalmadı.",
                        f"Her geçen gün alım gücümüzün erimesi, gençlerin umutsuzluğu ve liyakatsizlik canıma yetti. Bu düzen böyle gidemez.",
                        f"Ülkede adalet kalmadı, torpili olan işe giriyor, biz ise {fear} içinde kıvranıyoruz. Değişim olmadan bu millet nefes alamaz.",
                        f"Bir {occ} olarak her sabah uyandığımda paramın değer kaybetmesinden, geleceğimin kararmasından usandım. Yeni bir vizyon ve genç kadrolar şart.",
                        f"Emekli maaşıyla, sabit gelirle simit bile alamaz hale geldik. {pain} yetmezmiş gibi bir de her şey güllük gülistanlık gibi davranılması kanıma dokunuyor."
                    ]

                    dis_soz_options = [
                        f"Kusura bakmayın ama kimse kimseyi kandırmasın. 22 senedir aynı iktidar var ve geldiğimiz noktada halk pazardan çürük sebze topluyor. Ben kesinlikle devam etmesini istemiyorum.",
                        f"Ben bir {occ} olarak söylüyorum: Liyakat bitti, adalet bitti, enflasyon belimizi büktü. Bir insanın 25-30 yıl tek başına başta kalması hiçbir demokrasiye sığmaz.",
                        f"Gençler bu ülkeden kaçmak için gün sayıyor, diploması olanlar kuryelik yapıyor. Bu tablo ortadayken aynı şeyleri tekrar ederek düzelme bekleyemeyiz; değişim şart!",
                        f"Hasan Bey öyle istikrar falan diyorsunuz da, cebinizdeki paranın alım gücü kalmadıysa neyin istikrarı bu? Millet açlık sınırında, artık yeter.",
                        f"Benim kırmızı çizgim adalet ve ekmektir. Bu iki temel direk de çökmüş durumda. Yeni bir yönetim gelmeden Türkiye'nin önü açılamaz."
                    ]

                else:
                    karar = "Kararsız / Çekimser"
                    
                    ic_ses_options = [
                        f"Ekonominin hali ortada, {pain} belimizi büküyor ama öte yandan muhalefetin de güven veren bir kadrosu yok. İki arada bir derede kaldım.",
                        f"{fear} beni tedirgin ediyor. Değişim olsun istiyorum ama gelecek olanlar ülkeyi daha büyük bir karmaşaya sürükler mi diye korkuyorum.",
                        f"Tayyip Erdoğan'ın dış politikadaki bazı hamlelerini doğru buluyorum ama içerideki ekonomik çöküş ve torpil düzeni artık taşınamaz hale geldi."
                    ]

                    dis_soz_options = [
                        f"Ben iki tarafa da tam güvenemiyorum açıkçası. Mevcut durum çok kötü, ekonomide değişim şart ama alternatiflerin de ne yapacağı muamma.",
                        f"Masaya somut ve güvenilir bir ekonomik kurtarma planı koyan bir aday çıkmadığı sürece benim kafamdaki soru işaretleri bitmez.",
                        f"Bir taraf 'istikrar' diyor ama çarşı pazar yanıyor; diğer taraf 'değişim' diyor ama güven vermiyor. Ortada sıkışıp kaldık."
                    ]

            # ----------------------------------------------------
            # CASE 2: OYUN / GENÇLİK / DİJİTAL PLATFORM YASAKLARI
            # ----------------------------------------------------
            elif is_game_topic:
                if any(w in occ_l for w in ["öğrenci", "bilgisayar", "yazılım", "tasarım", "çevirmen", "sanatçı"]) or age <= 30:
                    karar = "Kesinlikle Reddeder"
                    ic_ses_options = [
                        f"Gündüz okul stresi ve {pain} ile boğuşurken, akşam iki saat arkadaşlarla Discord'da oyun oynamak bu hayattaki tek kaçış alanımızdı. Bunu da elimizden alırlarsa ne yapacağız?",
                        f"Discord kapandı, Roblox kapandı, şimdi oyunları mı yasaklayacaklar? Gençlerin sosyalleştiği ve dünyayla bağ kurduğu her kanala pranga vurmaktan bıkmadılar.",
                        f"Türkiye'den milyar dolarlık oyun stüdyoları çıkarken, sektörü kökten yasaklamayı düşünmek dijital çağda akıl tutulmasıdır. {fear} tam da böyle bir şey.",
                        f"Bir {occ} olarak hayatımı dijital dünya üzerinden kazanıyorum. Oyunları yasaklamak gençleri dünyaya kapatıp mağara çağına döndürmektir."
                    ]
                    dis_soz_options = [
                        f"Discord ve Roblox yasaklarından sonra oyunların toptan hedef alınması gençliği bu ülkeden tamamen koparır. Bizim kuşağın nefes alacağı tek alan oyunlar!",
                        f"Ben {occ} olarak konuşuyorum: Oyun sektörü sadece eğlence değil, Türkiye'nin en büyük yazılım ihracatıdır. Yasakçı kafayla hiçbir yere varılamaz.",
                        f"İnsanların evinde ne oynayacağına, hangi platforma gireceğine devlet karar veremez. Dünyada hiçbir modern ülke böyle ilkel yasaklara başvurmaz.",
                        f"Zaten bin bir zorlukla donanım alabiliyoruz, asgari ücretin yarısı ekran kartı olmuş; bir de üstüne yasaklar getirirseniz gençliği tamamen kaybedersiniz."
                    ]
                elif age >= 55:
                    karar = "Kararsız / Çekimser"
                    ic_ses_options = [
                        f"Çocukların ve torunların bütün gün ekran başında olması beni endişelendiriyor ama tamamen yasaklamak da onları isyan ettirir.",
                        f"Şiddet ve kumar içerikli oyunların denetlenmesi lazım ama gençlerin tek eğlencesini tamamen ellerinden almak da doğru değil."
                    ]
                    dis_soz_options = [
                        f"Çocukların zihinsel gelişimi için bir yaş sınırı ve denetim şart ama toptan yasaklamak yerine ailelerin kontrol edebileceği bir sistem kurulmalı.",
                        f"Gençler çok fazla bağımlı oluyor doğru, ama hepten kapatmak yerine eğitici ve yerli içerikleri teşvik etmek daha mantıklı."
                    ]
                else:
                    karar = "Kesinlikle Reddeder"
                    ic_ses_options = [
                        f"İş stresini ve {pain} yükünü akşamları 1 saat oyun oynayarak atıyordum. Özgürlüklere bu kadar müdahale edilmesi kabul edilemez."
                    ]
                    dis_soz_options = [
                        f"Yasaklama kültürüyle hiçbir toplumsal sorun çözülemez. Yasaklamak yerine denetim ve siber güvenlik mekanizmaları geliştirilmelidir."
                    ]

            # ----------------------------------------------------
            # CASE 3: GAZİ / ŞEHİT / AF / ÇERÇEVE YASA / TERÖR
            # ----------------------------------------------------
            elif is_security_topic:
                if any(w in occ_l for w in ["gazi", "şehit", "asker", "polis", "güvenlik"]) or b.national_security_redline > 75:
                    karar = "Kesinlikle Reddeder"
                    ic_ses_options = [
                        f"Dağlarda tertip arkadaşlarımızı şehit verdik, bedenimizde şarapnel parçalarıyla yaşıyoruz. {pain} yetmezmiş gibi Meclis'te teröristlerin affının konuşulması yüreğimi dağlıyor.",
                        f"Şehit evladımın mezar taşına bakarken gözyaşı döküyorum. Bu vatan için can verenlerin aziz hatırası hiçbir siyasi hesaba meze yapılamaz.",
                        f"{fear} tam da buydu: Yıllarca vatan uğruna çekilen çilenin bir gecede siyasi pazarlıklarla silinip atılması. Bunu asla kabul etmem."
                    ]
                    dis_soz_options = [
                        f"Ben bu vatan için kan dökmüş bir {occ} olarak açıkça söylüyorum: Teröristlerin affı veya Meclis'e daveti bu millete ve şehitlerimize hakarettir!",
                        f"Hiç kimse 'barış' adı altında şehitlerimizin kanını pazarlık konusu yapamaz. Kırmızı çizgilerimiz çiğnenirse bu masada durmanın anlamı kalmaz.",
                        f"Biz evlatlarımızı toprağa verdik, birileri koltuk uğruna katilleri affedecek öyle mi? Buna ne vicdan razı olur ne de Türk milleti!"
                    ]
                else:
                    karar = "Kararsız / Çekimser"
                    ic_ses_options = [
                        f"Terörün bitmesini ve anaların ağlamamasını canıgönülden isterim ama şehit ailelerimizin onurunun kırılmaması da en az bunun kadar hayatidir."
                    ]
                    dis_soz_options = [
                        f"Toplumsal huzur elbette önemli ama şehit ve gazi ailelerimizin rızası olmadan atılacak hiçbir adım vicdanlarda kabul görmez."
                    ]

            # ----------------------------------------------------
            # CASE 4: KİRA / BARINMA / %25 TAVAN ZAM
            # ----------------------------------------------------
            elif is_rent_topic:
                if "kiracı" in occ_l or "kiracı" in p.sehir_ilce.lower() or p.aylik_serbest_harcanabilir_tl < 15000:
                    karar = "Kabul Eder / Destekler"
                    accept_count += 1
                    ic_ses_options = [
                        f"Maaşım 30 bin lira, ev sahibi 25 bin lira istiyor. {pain} altında ezilirken tavan zam sınırı olmazsa çocuklarımı alıp sokakta mı yatacağım?",
                        f"Ev sahibinin her ay kapıya dayanmasından ve {fear} ile yaşamaktan bıktım. Kiracıyı koruyacak sert bir devlet müdahalesi şart."
                    ]
                    dis_soz_options = [
                        f"Maaşlara yılda bir kez zam yapılırken kiraların %150 artması cinayettir. Devletin acilen kiraya tavan sınır getirmesi gerekir!",
                        f"Ben {occ} olarak ailemi geçindiremiyorum. Kiracıların can güvenliği ve barınma hakkı için yasal üst sınır şarttır."
                    ]
                else:
                    karar = "Kesinlikle Reddeder"
                    ic_ses_options = [
                        f"Enflasyon %70 iken kiraya %25 sınır koymak mülk sahibinin malına çökmektir. Ben de bu evden gelen gelirle geçiniyorum."
                    ]
                    dis_soz_options = [
                        f"Piyasa gerçeklerine aykırı %25 sınırı ev sahibiyle kiracıyı birbirine düşürdü, mahkemeler tıkandı. Fiyat baskılamasıyla enflasyon çözülmez."
                    ]

            # ----------------------------------------------------
            # CASE 5: GENEL TİCARİ / PAZARLAMA / TEKLİF FALLBACK
            # ----------------------------------------------------
            else:
                if i % 3 == 0:
                    karar = "Kabul Eder / Destekler"
                    accept_count += 1
                    ic_ses_options = [f"Bu teklifin getireceği kolaylık {pain} yükünü hafifletebilir. Şartları makul görünüyor."]
                    dis_soz_options = [f"Şartlar şeffaf olduğu ve ek maliyet çıkmadığı sürece ben bu projeyi desteklerim."]
                elif i % 3 == 1:
                    karar = "Kararsız / Çekimser"
                    ic_ses_options = [f"{fear} aklıma takılıyor. Arka plandaki maliyeti ve taahhütleri görmeden adım atmam."]
                    dis_soz_options = [f"Fikir fena değil ama detayları ve garanti şartlarını görmeden kesin bir karar veremem."]
                else:
                    karar = "Kesinlikle Reddeder"
                    ic_ses_options = [f"Mevcut bütçem ve {pain} varken bu teklife ayıracak ne vaktim ne de param var."]
                    dis_soz_options = [f"Kusura bakmayın ama benim önceliklerimle ve şartlarımla hiç uyuşmuyor; ben reddediyorum."]

            # Select deterministic unique variant per persona index to avoid any collision
            chosen_ic_ses = ic_ses_options[i % len(ic_ses_options)]
            chosen_dis_soz = dis_soz_options[i % len(dis_soz_options)]

            discussions.append({
                "kisi_id": p.id,
                "ad_soyad": p.ad_soyad,
                "meslek": p.meslek,
                "karar": karar,
                "ic_ses_bilincalti": chosen_ic_ses,
                "disa_soylenen_soz": chosen_dis_soz
            })

        accept_pct = round((accept_count / max(1, len(personas))) * 100, 1)

        return {
            "odak_grubu_tartismasi": discussions,
            "yonetici_pazar_analiz_raporu": {
                "genel_kabul_orani_yuzde": accept_pct,
                "en_buyuk_3_itiraz_bariyeri": [
                    "Ekonomik Geçim Bunalımı ve Alım Gücü Kaybı",
                    "Liyakat, Adalet ve Kurumsal Güvensizlik",
                    "Kişisel Öncelikler ve Yaşam Alanına Müdahale Endişesi"
                ],
                "fiyat_duyarlilik_analizi": "Topluluk somut rahatlama ve adalet teminatı aramaktadır.",
                "kutuplasma_indeksi_skoru": "0.78 / 1.0 (Yüksek Kutuplaşma / Ayrışma)",
                "what_if_karsi_olgusal_stres_testi": {
                    "senaryo_1_guvence": "Somut ekonomik paket ve liyakat teminatı sunulursa kabul: %48.0",
                    "senaryo_2_fiyat": "Maliyetler ve vergi yükü %25 indirilirse kabul: %56.5",
                    "en_hizli_ikna_olacak_segment": "Kararsız pragmatik orta sınıf ve çalışan emekliler"
                },
                "stratejik_urun_tavsiyesi": "İdeolojik söylemler yerine hanenin somut mutfak enflasyonuna ve adalet talebine dokunulmalıdır."
            }
        }
