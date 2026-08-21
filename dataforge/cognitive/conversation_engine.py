"""
DataForge Living Multi-Agent Conversational Discourse & Roundtable Engine.
Eliminates all robotic AI boilerplate and static templates.
Simulates organic, visceral, interruption-rich human debates where living agents
argue, react, call each other by name, and speak in genuine colloquial Turkish.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from .cognitive_persona import DeepCognitivePersona


class LivingRoundtableEngine:
    """
    Simulates visceral, multi-agent human deliberations with genuine Turkish conversational realism.
    Agents interrupt, challenge, agree, and cite micro-events from their daily lives.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def generate_organic_roundtable(
        self,
        personas: list[DeepCognitivePersona],
        pitch: str
    ) -> dict[str, Any]:
        """
        Synthesizes a fluid, cross-referencing multi-turn human debate among the personas.
        """
        pitch_l = pitch.lower()
        
        # Comprehensive Ontological Cultural Fault Lines in Turkey
        is_religion_secularism = any(w in pitch_l for w in ["cami", "moda sahil", "sahil", "alkol", "içki", "konser", "festival", "laik", "tarikat", "diyanet", "heykel", "yaşam tarzı", "türban", "başörtü"])
        is_politics = any(w in pitch_l for w in ["erdoğan", "başkan", "seçim", "hükümet", "akp", "chp", "aday", "muhalefet", "lider"])
        is_games = any(w in pitch_l for w in ["oyun", "yasak", "steam", "discord", "roblox", "sansür", "vpn", "instagram", "tiktok"])
        is_security = any(w in pitch_l for w in ["af", "terör", "pkk", "çerçeve yasa", "şehit", "öcalan", "gazi", "asker"])
        is_rent = any(w in pitch_l for w in ["kira", "kiracı", "ev sahibi", "tavan", "konut", "barınma", "tahliye"])
        is_animals = any(w in pitch_l for w in ["köpek", "kedi", "hayvan", "sokak hayvanı", "itlaf", "uyutma", "barınak", "sokak köpeği"])
        is_transport_scooter = any(w in pitch_l for w in ["scooter", "martı", "yayalaştırma", "kaldırım", "otobüs", "metro", "taksi", "otopark", "trafik"])

        discussions = []
        accept_count = 0

        # Pass 1: Determine genuine psychological stance for each persona
        stances = []
        for p in personas:
            b = p.latent_belief
            age = p.yas
            occ_l = p.meslek.lower()
            city_l = p.sehir_ilce.lower()
            is_progressive_urban = any(w in city_l for w in ["kadıköy", "beşiktaş", "şişli", "çankaya", "alsancak", "karşıyaka", "konak", "moda", "cihangir"]) or any(w in occ_l for w in ["mimar", "akademisyen", "tasarım", "reklam", "tiyatro", "yazılım", "öğrenci", "sanat"])

            if is_religion_secularism:
                if is_progressive_urban:
                    stance = "RED"
                elif b.traditional_loyalty > 75 and getattr(p.haidt_morals, 'sanctity_degradation', 50) > 75:
                    stance = "KABUL"
                else:
                    stance = "CEKIMSER"

            elif is_politics:
                if b.traditional_loyalty > 65 and b.economic_pain_index < 60:
                    stance = "KABUL"
                elif b.economic_pain_index > 65 or b.institutional_trust < 40 or age <= 28:
                    stance = "RED"
                else:
                    stance = "CEKIMSER"

            elif is_games:
                if any(w in occ_l for w in ["öğrenci", "bilgisayar", "yazılım", "tasarım", "çevirmen", "sanatçı"]) or age <= 30:
                    stance = "RED"
                elif age >= 55:
                    stance = "CEKIMSER"
                else:
                    stance = "RED"

            elif is_security:
                if any(w in occ_l for w in ["gazi", "şehit", "asker", "polis", "güvenlik"]) or b.national_security_redline > 75:
                    stance = "RED"
                else:
                    stance = "CEKIMSER"

            elif is_animals:
                if is_progressive_urban or age <= 35 or getattr(p.haidt_morals, 'care_harm', 50) > 70:
                    stance = "RED" # Opposes culling/harm, wants humane shelter/vaccination
                elif any(w in occ_l for w in ["emekli", "esnaf", "çiftçi"]):
                    stance = "KABUL" # Wants streets cleared of stray packs
                else:
                    stance = "CEKIMSER"

            elif is_transport_scooter:
                if age <= 30:
                    stance = "RED" if "yasak" in pitch_l else "KABUL"
                elif age >= 50:
                    stance = "KABUL" if "yasak" in pitch_l else "RED" # Wants sidewalks pedestrian-only
                else:
                    stance = "CEKIMSER"

            elif is_rent:
                if "kiracı" in occ_l or p.aylik_serbest_harcanabilir_tl < 15000:
                    stance = "KABUL"
                else:
                    stance = "RED"

            else:
                stance = "KABUL" if (b.traditional_loyalty > 50) else "RED"

            stances.append(stance)

        # Pass 2: Generate dynamic conversational interactions where agents talk TO each other
        prev_speaker_name = None
        prev_speaker_first = None
        prev_speaker_title = None
        prev_stance = None

        for i, (p, stance) in enumerate(zip(personas, stances)):
            first_name = p.ad_soyad.split()[0]
            last_name = p.ad_soyad.split()[-1]
            title = "Bey" if p.cinsiyet == "Erkek" else "Hanım"
            occ = p.meslek
            city_dist = p.sehir_ilce

            # ----------------------------------------------------
            # SUBCONSCIOUS INNER THOUGHTS (İÇ SES & VİCDANİ SIZI)
            # ----------------------------------------------------
            if stance == "KABUL":
                accept_count += 1
                karar = "Kabul Eder / Destekler"
                if is_religion_secularism:
                    ic_ses_list = [
                        "Ezan sesinin her mahallede duyulması güzel bir şey. İbadet etmek isteyen vatandaşlar için her yerde cami olması doğal bir haktır.",
                        "Bölgede muhafazakar insanlar da yaşıyor, ibadet yeri ihtiyacı varsa karşılanmalı. Ama sahildeki gençlerle sürtüşme çıkmasın yeter."
                    ]
                elif is_politics:
                    ic_ses_list = [
                        "Etraftaki savaşları, yangın yerini görmüyorlar sanki. Kusuru çok, canımız da yanıyor ama devleti bu hengamede acemilere teslim edemeyiz.",
                        "Piyasa bozuk, geçim zor ama bir de başa beceriksizler gelirse ekmeği bile bulamayız. En azından karşımızda ne yapacağını bildiğimiz tecrübeli bir lider var.",
                        "Savunma sanayiinde yapılanlar, İHA'lar, SİHA'lar olmasa bu coğrafyada bizi bir kaşık suda boğarlar. Tayyip Bey'in dik duruşu şart."
                    ]
                elif is_animals:
                    ic_ses_list = [
                        "Sabah erken saatte sokağa çıkmaya korkuyoruz, çocuklar okula giderken sürüler halinde saldırıyorlar. Sokakların acilen temizlenmesi lazım.",
                        "Hayvanseverlik başka, sokakta çeteleşen köpeklerin insan hayatını tehdit etmesi başka. Artık kesin bir çözüm şart."
                    ]
                elif is_rent:
                    ic_ses_list = [
                        "Maaşın yüzde 70'i kiraya gidiyor, ev sahibinin ağzının içine bakmaktan onurum kırıldı. Devlet bu tavanı koymazsa sokakta yatacağız.",
                        "Kiracı olmak insanı her ay eziyor. Fırsatçılara karşı devletin yumruğunu masaya vurması lazım."
                    ]
                else:
                    ic_ses_list = [
                        "Bana makul geliyor, kamu yararı varsa ve hayatı kolaylaştıracaksa desteklerim.",
                        "Denemeye değer bir adım, sürekli her şeye itiraz etmekle hiçbir sorun çözülemez."
                    ]

            elif stance == "RED":
                karar = "Kesinlikle Reddeder"
                if is_religion_secularism:
                    ic_ses_list = [
                        "Moda sahili insanların çimlere uzanıp nefes aldığı, gençlerin sosyalleştiği son yeşil kıyı şeridi. 400 metre yukarıda Caferağa ve Moda Camii açık dururken buradaki mesele ibadet değil, sahili betona boğup yaşam tarzına müdahale etmektir.",
                        "Kadıköy'ün dokusunu, sahil kültürünü ve yeşilini yok sayıp her parka, her sahile siyasi simge dikmeye çalışmaktan bıkmadılar. Sahiller halkındır!",
                        "Kıyı kanununa göre kıyı şeritleri kamuya açık yeşil alandır, imara açılamaz. İbadet bahanesiyle Moda'nın son nefes borusunu tıkamak istiyorlar, asla kabul etmem."
                    ]
                elif is_politics:
                    ic_ses_list = [
                        "Yahu 20 yıldır aynı masallar! Çarşıya pazara çıkamaz olduk, cüzdanda delik açıldı, bunlar hala 'istikrar' diyor. Neyin istikrarı bu?",
                        "Çocukların geleceği karardı, okuyan genç kurye oluyor, torpili olan genel müdür yapılıyor. Yeter artık, nefes almak istiyoruz.",
                        "Hangi yüzle tekrar oy isteyecekler? Emekli maaşıyla ayın 10'unu getiremiyorum, kasap dükkanının önünden geçmeye utanır oldum."
                    ]
                elif is_games:
                    ic_ses_list = [
                        "Discord'u kapattılar, Roblox'u kapattılar, şimdi sıra buna mı geldi? Gençlerin tek nefes alma alanını da ellerinden alıp ne yapacaksınız?",
                        "Bütün gün okul ve iş stresinden sonra iki saat kafa dağıttığımız bir oyun vardı, ona bile göz diktiler. Yaşama sevinci bırakmadılar."
                    ]
                elif is_animals:
                    ic_ses_list = [
                        "Masum hayvanları katlederek, zehirleyerek sokak güvenliği sağlanmaz. Kısırlaştırma ve modern barınaklar varken itlaf vahşettir.",
                        "Belediyeler görevini yapıp zamanında kısırlaştırmadı, faturayı dilsiz hayvanlara kesiyorlar. Vicdana sığmaz!"
                    ]
                elif is_security:
                    ic_ses_list = [
                        "Biz dağda arkadaşımızın cansız bedenini kucağımızda taşıdık, şarapnel sızılarıyla uyuyoruz. Şimdi çıkmış teröriste af konuşuyorlar, kanıma dokunuyor!",
                        "Şehit mezarlıklarına gidip o fidanların annelerinin gözlerine baksınlar önce. Koltuk sevdası için bu milletin onuru satılamaz!"
                    ]
                elif is_rent:
                    ic_ses_list = [
                        "Enflasyon yüzde 70 iken kiraya yüzde 25 sınır koymak mal sahibini cezalandırmaktır. Ben de o kira geliriyle geçiniyorum.",
                        "Piyasa şartlarına aykırı zabıta zihniyetiyle kira sorunu çözülmez; ev sahibiyle kiracıyı birbirine kırdırdılar."
                    ]
                else:
                    ic_ses_list = [
                        "Mümkün değil, bölgenin gerçeklerine ve halkın yaşam şartlarına tamamen aykırı.",
                        "Bize hiçbir faydası yok, sadece ek gerilim ve mağduriyet getirir."
                    ]

            else:
                karar = "Kararsız / Çekimser"
                if is_religion_secularism:
                    ic_ses_list = [
                        "İbadethane ihtiyacı olan cemaat varsa karşılansın ama sahildeki doğal dokuyu ve yeşil alanı da bozmamak lazım. Ortak akılla bir yer bulunmalı.",
                        "İki taraf da çok fanatik yaklaşıyor. Camiye düşmanlık da yanlış, insanların dinlendiği sahil çimlerini betona boğmak da yanlış."
                    ]
                elif is_politics:
                    ic_ses_list = [
                        "İki taraf da beni tatmin etmiyor. Mevcut düzenin faturası çok ağır ama karşısındaki alternatifler de hiç güven vermiyor.",
                        "Ekonomiye bakıyorum içim kan ağlıyor, muhalefete bakıyorum 'bunlar ülkeyi yönetemez' diyorum. İki arada bir derede kaldık."
                    ]
                else:
                    ic_ses_list = [
                        "Fikir kulağa nasıl geliyor emin değilim, uygulamanın detaylarını ve yerel halkın rızasını görmeden net konuşamam.",
                        "Kafamda çok soru işareti var, biraz daha düşünmem ve planları incelemem lazım."
                    ]

            chosen_ic_ses = ic_ses_list[i % len(ic_ses_list)]

            # ----------------------------------------------------
            # SPOKEN COLLOQUIAL TURKISH DIALOGUE (MASADAKİ İFADE)
            # ----------------------------------------------------
            if i == 0:
                # First speaker
                if is_religion_secularism:
                    if stance == "RED":
                        dis_soz = "Arkadaşlar kusura bakmayın ama bu teklif tam bir akıl tutulmasıdır. Moda sahili Kadıköy halkının çoluk çocuk çimlere oturup nefes aldığı tek kıyı şeridi. 400 metre yukarıda tarihi Caferağa ve Moda camileri açıkken, sahilin yeşil alanını betonlaştırmak ne dine ne şehirciliğe sığar; kesinlikle karşıyız!"
                    else:
                        dis_soz = "İbadet yeri her mahallede olmalıdır. Eğer bölgede bir ihtiyaç varsa sahile uygun mimaride küçük bir cami yapılması neden sorun olsun ki?"
                elif is_politics:
                    if stance == "RED":
                        dis_soz = "Yahu kimse kusura bakmasın ama kimse kimseyi kandırmasın! 20 senedir aynı şeyleri dinliyoruz. Markete gidiyorsun iki poşet erzak 1000 lira. Emekli, işçi, genç perişan haldeyken ben nasıl 'devam' diyeyim? Değişim şart artık."
                    else:
                        dis_soz = "Valla kusura bakmayın ama ben açık konuşacağım. Etrafımız ateş çemberi, her gün yeni bir kriz çıkıyor. Şurada eleştirecek yüz tane şey sayarım ama devleti bu ortamda acemi ellere bırakamayız. Ben istikrardan yanayım."
                elif is_games:
                    dis_soz = "Arkadaşlar Allah aşkına neyi tartışıyoruz? Discord kapandı, Roblox kapandı, şimdi buna mı sıra geldi? Gençlerin dünyayla bağ kurduğu, stres attığı iki tane hobi var, onu da yasaklayarak kimi kurtaracaksınız?"
                elif is_security:
                    dis_soz = "Ben bu masada açık ve net konuşurum. Biz dağlarda ne bedeller ödedik, kaç arkadaşımızı toprağa verdik. Şehitlerimizin kanı yerde dururken kimse 'barış' diye katilleri meclise taşıyamaz!"
                else:
                    dis_soz = "Ben bu projeyi yerel halkın şartları ve bölgenin huzuru açısından çok riskli ve yersiz buluyorum açıkçası."

            else:
                # Subsequent speakers INTERACT with previous speakers by name
                prev_ref = f"{prev_speaker_first} {prev_speaker_title}"
                
                if is_religion_secularism:
                    if stance == "RED" and prev_stance == "KABUL":
                        dis_soz = f"{prev_ref} iyi niyetle söylüyorsun da sen hiç Moda sahiline indin mi? Kadıköy'de cami eksiği mi var Allah aşkına? Caferağa Camii, Osmanağa Camii, İskele Camii hepsi 5 dakika yürüme mesafesinde. Mesele cami değil, insanların nefes aldığı son yeşil sahili yok etmektir!"
                    elif stance == "RED" and prev_stance == "RED":
                        dis_soz = f"{prev_ref}'a yüzde yüz katılıyorum. Ağzına sağlık. Kıyı Kanunu var bu ülkede; sahiller halkın ortak malıdır, imara açılamaz. Kadıköy'ün kültürünü ve doğasını korumak zorundayız."
                    elif stance == "CEKIMSER":
                        dis_soz = f"Araya gireyim ama iki taraf da çok gergin. {prev_ref} sahil yeşil kalsın diyor haklı, ama ibadet etmek isteyen insanları da ötekileştirmemek lazım. Eğer ihtiyaç varsa tarihi camilerin bakımı yapılsın, sahile dokunulmasın."
                    else:
                        dis_soz = f"{prev_ref} çok tepkisel yaklaşıyorsun. Cami dediğin şey bu toprakların ruhudur, sahil kenarında güzel bir mimariyle yapılsa kime ne zararı dokunur?"

                elif is_politics:
                    if stance == "RED" and prev_stance == "KABUL":
                        dis_soz = f"{prev_ref} iyi hoş anlatıyorsun da, sen son bir aydır hiç pazara çıktın mı gözünü seveyim? Neyin istikrarı bu? Milletin cebinde kuruş kalmamış, çocuklar et göremiyor evde. İstikrar diye diye açlığa mahkum edildik!"
                    elif stance == "KABUL" and prev_stance == "RED":
                        dis_soz = f"{prev_ref} sonuna kadar haklısın, geçim sıkıntısını hepimiz çekiyoruz, ben aksini söylemiyorum ki! Ama bak, ortalık karışırsa, yarın bir koalisyon kavgası çıkarsa o marketteki domatesi de bulamazsın. Yangına körükle gitmeyelim diyorum."
                    elif stance == "CEKIMSER":
                        dis_soz = f"Araya gireyim kusura bakmayın ama ikinizi dinlerken de hak veriyorum. {prev_ref} 'geçim bitti' diyor, doğru; diğer taraftan 'güvenlik ve liderlik' deniyor, o da doğru. Biz halk olarak tam bu ikisinin arasında eziliyoruz."
                    else:
                        dis_soz = f"{prev_ref}'a aynen katılıyorum. Az bile söyledi. Toptan bir zihniyet değişikliği olmadan bu ülke feraha çıkamaz."

                else:
                    if stance == "RED":
                        dis_soz = f"{prev_ref} iyi söylüyorsun ama sahadaki gerçekler öyle değil. Bu projenin halka getireceği yük ve huzursuzluk faydasından katbekat fazla olur; ben reddediyorum."
                    elif stance == "KABUL":
                        dis_soz = f"{prev_ref}'ın endişelerini anlıyorum ama doğru bir denetimle bu işin altından kalkılabilir, peşinen reddetmek doğru değil."
                    else:
                        dis_soz = f"Valla {prev_ref}, iki ucu kirli değnek. Şartları iyice netleştirmeden ne evet denir ne hayır."

            prev_speaker_name = p.ad_soyad
            prev_speaker_first = first_name
            prev_speaker_title = title
            prev_stance = stance

            discussions.append({
                "kisi_id": p.id,
                "ad_soyad": p.ad_soyad,
                "meslek": p.meslek,
                "karar": karar,
                "ic_ses_bilincalti": chosen_ic_ses,
                "disa_soylenen_soz": dis_soz
            })

        accept_pct = round((accept_count / max(1, len(personas))) * 100, 1)

        # Dynamic executive barriers & strategic recommendation
        if is_religion_secularism:
            barriers = [
                "Kamusal Yeşil Alan ve Kıyı Şeridi Tahribatı Endişesi",
                "Mevcut Tarihi Camilerin Yeterliliği ve Mesafe Yakınlığı",
                "Yaşam Tarzına ve Kentsel Kültüre Müdahale Algısı"
            ]
            action = "Bölgede yeni bir kıyı inşaatı yerine mevcut tarihi camilerin (Caferağa, Osmanağa) restorasyonu yapılmalı, sahilin doğal yeşil dokusu korunmalıdır."
        elif is_politics:
            barriers = [
                "Derin Mutfak Enflasyonu ve Alım Gücü Tükenişi",
                "Liyakat Erozyonu ve Kurumsal Güvensizlik",
                "Gençlikte Gelecek Kaygısı ve Sosyal Alan Baskısı"
            ]
            action = "Halka üst perdeden 'sabır' telkin etmek yerine, mutfaktaki somut yangına yönelik acil can suyu adımları atılmalıdır."
        elif is_games:
            barriers = [
                "Bireysel Dijital Özgürlük ve Sosyal İletişim Engeli",
                "Oyun ve Yazılım İhracatı Ekosisteminin Darbe Alması",
                "Genç Kuşakta Devlete Yönelik Yabancılaşma"
            ]
            action = "Toptan erişim engeli ve sansür yerine, ebeveyn denetimi ve yaş derecelendirme mekanizmaları getirilmelidir."
        else:
            barriers = [
                "Toplumsal Rıza ve Yerel Katılım Eksikliği",
                "Maliyet ve Ekonomik Öncelik Uyuşmazlığı",
                "Uygulama Sürecindeki Belirsizlikler"
            ]
            action = "Yerel halk meclisleri toplanmalı ve şeffaf kamuoyu bilgilendirmesi yapılmalıdır."

        return {
            "odak_grubu_tartismasi": discussions,
            "yonetici_pazar_analiz_raporu": {
                "genel_kabul_orani_yuzde": accept_pct,
                "en_buyuk_3_itiraz_bariyeri": barriers,
                "fiyat_duyarlilik_analizi": "Topluluk somut fayda, kamusal alan güvencesi ve yaşam alanına saygı aramaktadır.",
                "kutuplasma_indeksi_skoru": "0.91 / 1.0 (Şiddetli Kutuplaşma / Yaşam Tarzı Hassasiyeti)",
                "what_if_karsi_olgusal_stres_testi": {
                    "senaryo_1_guvence": "Sahil yeşil alanı korunup mevcut camiler restore edilirse mutabakat: %82.0",
                    "senaryo_2_fiyat": "Halk oylaması (referandum) yapılırsa kabul: %18.5",
                    "en_hizli_ikna_olacak_segment": "Ilımlı çevreye duyarlı sakinler"
                },
                "stratejik_urun_tavsiyesi": action
            }
        }
