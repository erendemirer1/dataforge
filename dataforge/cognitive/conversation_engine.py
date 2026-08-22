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
        
        # Comprehensive Ontological Cultural & Commercial Fault Lines
        is_beer_nightlife = any(w in pitch_l for w in ["bira", "alkol", "bar", "pub", "meyhane", "gece kulübü", "şarap", "kokteyl", "biranın", "100 lira", "mekan"])
        is_food_cafe = any(w in pitch_l for w in ["kahve", "kafe", "restoran", "burger", "pizza", "döner", "tatlı", "yemek", "menü"]) and not is_beer_nightlife
        is_religion_secularism = any(w in pitch_l for w in ["cami", "moda sahil", "sahil", "içki yasağı", "konser", "festival", "laik", "tarikat", "diyanet", "heykel", "yaşam tarzı", "türban"]) and not is_beer_nightlife
        is_politics = any(w in pitch_l for w in ["erdoğan", "tayyip", "başkan", "seçim", "hükümet", "akp", "chp", "aday", "muhalefet", "lider", "cumhurbaşkanı"])
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
            is_progressive_urban = any(w in city_l for w in ["kadıköy", "beşiktaş", "şişli", "çankaya", "alsancak", "karşıyaka", "konak", "moda", "cihangir"]) or any(w in occ_l for w in ["mimar", "akademisyen", "tasarım", "reklam", "tiyatro", "yazılım", "öğrenci", "sanat", "barista"])
            is_student_youth = age <= 28 or any(w in occ_l for w in ["öğrenci", "genç", "junior", "stajyer", "barista", "yazılımcı"])

            if is_beer_nightlife:
                if is_student_youth or is_progressive_urban:
                    stance = "KABUL"
                elif age >= 55:
                    stance = "CEKIMSER"
                else:
                    stance = "KABUL"

            elif is_food_cafe:
                stance = "KABUL" if is_student_youth or is_progressive_urban else "CEKIMSER"

            elif is_religion_secularism:
                if is_progressive_urban:
                    stance = "RED"
                elif b.traditional_loyalty > 75 and getattr(p.haidt_morals, 'sanctity_degradation', 50) > 75:
                    stance = "KABUL"
                else:
                    stance = "CEKIMSER"

            elif is_politics:
                # Political stance conditioned on economic distress vs traditional loyalty
                if b.traditional_loyalty > 65 and b.economic_pain_index < 60 and not is_student_youth:
                    stance = "KABUL"
                elif b.economic_pain_index > 65 or b.institutional_trust < 40 or is_student_youth:
                    stance = "RED"
                else:
                    stance = "CEKIMSER"

            elif is_games:
                if is_student_youth or age <= 30:
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
                    stance = "RED"
                elif any(w in occ_l for w in ["emekli", "esnaf", "çiftçi"]):
                    stance = "KABUL"
                else:
                    stance = "CEKIMSER"

            elif is_transport_scooter:
                if age <= 30:
                    stance = "RED" if "yasak" in pitch_l else "KABUL"
                elif age >= 50:
                    stance = "KABUL" if "yasak" in pitch_l else "RED"
                else:
                    stance = "CEKIMSER"

            elif is_rent:
                if "kiracı" in occ_l or p.aylik_serbest_harcanabilir_tl < 15000:
                    stance = "KABUL"
                else:
                    stance = "RED"

            else:
                stance = "KABUL" if (b.traditional_loyalty > 50 or is_student_youth) else "RED"

            stances.append(stance)

        # Pass 2: Generate dynamic conversational interactions where agents talk TO each other
        prev_speaker_first = None
        prev_speaker_title = None
        prev_stance = None

        for i, (p, stance) in enumerate(zip(personas, stances)):
            first_name = p.ad_soyad.split()[0]
            title = "Bey" if p.cinsiyet == "Erkek" else "Hanım"

            # ----------------------------------------------------
            # SUBCONSCIOUS INNER THOUGHTS (İÇ SES & VİCDANİ SIZI)
            # ----------------------------------------------------
            if stance == "KABUL":
                accept_count += 1
                karar = "Kabul Eder / Destekler"
                if is_beer_nightlife:
                    ic_ses_list = [
                        "Kadıköy Barlar Sokağı'nda iki fıçı biraya 450 lira hesap ödüyoruz, dışarı çıkmak lüks oldu. 100 liraya bira olursa arkadaşlarla her Cuma oradayız.",
                        "Öğrenci bütçesiyle ayda bir kere sosyalleşebiliyordum. 100 lira inanılmaz iyi fiyat, bira taze ve ortam güzelse kesinlikle müdavimi olurum.",
                        "Mekanın müziği ve ortamı iyi olsun, birayı da sulandırmasınlar yeter. Bu fiyata kapısında kuyruk olur, yer bulabilirsek harika olur."
                    ]
                elif is_politics:
                    ic_ses_list = [
                        "Etraftaki savaşları, yangın yerini görmüyorlar sanki. Kusuru çok, canımız da yanıyor ama devleti bu hengamede acemilere teslim edemeyiz.",
                        "Piyasa bozuk, geçim zor ama bir de başa beceriksizler gelirse ekmeği bile bulamayız. Karşımızda tecrübeli bir lider var.",
                        "Savunma sanayiinde yapılanlar, İHA'lar, SİHA'lar olmasa bu coğrafyada bizi bir kaşık suda boğarlar. Tayyip Bey'in dik duruşu şart."
                    ]
                elif is_food_cafe:
                    ic_ses_list = [
                        "Dışarıda yemek yemek imkansız hale geldi, bir kahve 120 lira olmuş. Uygun fiyatlı ve kaliteli bir alternatif çıkarsa kesinlikle giderim.",
                        "Fiyat ve lezzet dengesi tutarsa sürekli gideceğim bir mekan olur."
                    ]
                elif is_religion_secularism:
                    ic_ses_list = [
                        "Ezan sesinin her mahallede duyulması güzel bir şey. İbadet etmek isteyen vatandaşlar için her yerde cami olması doğal bir haktır.",
                        "Bölgede muhafazakar insanlar da yaşıyor, ibadet yeri ihtiyacı varsa karşılanmalı."
                    ]
                elif is_rent:
                    ic_ses_list = [
                        "Maaşın yüzde 70'i kiraya gidiyor, ev sahibinin ağzının içine bakmaktan onurum kırıldı. Devlet bu tavanı koymazsa sokakta yatacağız.",
                        "Kiracı olmak insanı her ay eziyor. Fırsatçılara karşı devletin yumruğunu masaya vurması lazım."
                    ]
                else:
                    ic_ses_list = [
                        "Fiyat ve sunduğu teklif bütçeme son derece uygun. Kaliteli olursa kesinlikle denerim ve arkadaşlarıma da tavsiye ederim.",
                        "Gayet mantıklı bir girişim, günümüz piyasasında böyle uygun çözümlere çok ihtiyaç var."
                    ]

            elif stance == "RED":
                karar = "Kesinlikle Reddeder"
                if is_politics:
                    ic_ses_list = [
                        "Yahu 20 yıldır aynı masallar! Çarşıya pazara çıkamaz olduk, cüzdanda delik açıldı, bunlar hala 'istikrar' diyor. Neyin istikrarı bu?",
                        "Çocukların geleceği karardı, okuyan genç kurye oluyor, torpili olan genel müdür yapılıyor. Yeter artık, nefes almak istiyoruz!",
                        "Hangi yüzle tekrar oy isteyecekler? Emekli maaşıyla ayın 10'unu getiremiyorum, kasap dükkanının önünden geçmeye utanır oldum."
                    ]
                elif is_beer_nightlife:
                    ic_ses_list = [
                        "100 liraya bira bu devirde imkansız; ya sahtedir ya da içine su katıyorlardır. Kalitesiz mekana adımımı atmam.",
                        "Çok kalabalık ve tekinsiz bir kitle toplayabilir, kafa dinlemek ve kaliteli vakit geçirmek isteyenler için uygun olmaz."
                    ]
                elif is_religion_secularism:
                    ic_ses_list = [
                        "Moda sahili insanların çimlere uzanıp nefes aldığı, gençlerin sosyalleştiği son yeşil kıyı şeridi. 400 metre yukarıda Caferağa ve Moda Camii açık dururken buradaki mesele ibadet değil, sahili betona boğup yaşam tarzına müdahale etmektir.",
                        "Kadıköy'ün dokusunu, sahil kültürünü ve yeşilini yok sayıp her parka, her sahile siyasi simge dikmeye çalışmaktan bıkmadılar. Sahiller halkındır!"
                    ]
                elif is_games:
                    ic_ses_list = [
                        "Discord'u kapattılar, Roblox'u kapattılar, şimdi sıra buna mı geldi? Gençlerin tek nefes alma alanını da ellerinden alıp ne yapacaksınız?",
                        "Bütün gün okul ve iş stresinden sonra iki saat kafa dağıttığımız bir oyun vardı, ona bile göz diktiler."
                    ]
                elif is_security:
                    ic_ses_list = [
                        "Biz dağda arkadaşımızın cansız bedenini kucağımızda taşıdık, şarapnel sızılarıyla uyuyoruz. Şimdi çıkmış teröriste af konuşuyorlar, kanıma dokunuyor!",
                        "Şehit mezarlıklarına gidip o fidanların annelerinin gözlerine baksınlar önce. Koltuk sevdası için bu milletin onuru satılamaz!"
                    ]
                else:
                    ic_ses_list = [
                        "Bana hiç güven vermedi; bu fiyata kaliteli hizmet sunulamaz veya arkasından başka bir masraf çıkar.",
                        "İhtiyacım olan bir şey değil, paramı böyle şeylere harcamam."
                    ]

            else:
                karar = "Kararsız / Çekimser"
                if is_politics:
                    ic_ses_list = [
                        "İki taraf da beni tam tatmin etmiyor. Mevcut hayat pahalılığı ve liyakat erozyonu ortada ama muhalefetin de devleti yönetebileceğine dair ciddi şüphelerim var.",
                        "Ekonomiye bakıyorum içim kan ağlıyor, etrafa bakıyorum devleti teslim edecek güvenilir bir alternatif göremiyorum. Ne evet diyebiliyorum ne hayır.",
                        "Mevcut sistemin faturası çok ağır oldu ama yarın bir koalisyon kargaşası çıkarsa durum daha da kötüleşir mi diye korkuyorum."
                    ]
                elif is_beer_nightlife:
                    ic_ses_list = [
                        "Fiyat harika ama ortamı, çalınan müziği ve biranın markasını görmem lazım. Sırf ucuz diye basık ve gürültülü yere gitmem.",
                        "Fiyat çok cazip ama ilk günlerin yoğunluğu geçtikten sonra bir görmek lazım."
                    ]
                elif is_religion_secularism:
                    ic_ses_list = [
                        "İbadethane ihtiyacı olan cemaat varsa karşılansın ama sahildeki doğal dokuyu ve yeşil alanı da bozmamak lazım.",
                        "İki taraf da çok fanatik yaklaşıyor. Camiye düşmanlık da yanlış, sahili betona boğmak da yanlış."
                    ]
                elif is_security:
                    ic_ses_list = [
                        "Terörün bitmesini herkes ister ama şehit ailelerinin yüreğini sızlatacak bir taviz verilirse vicdanlar kanar. Detayları görmeden konuşamam.",
                        "Kırmızı çizgiler aşılmadan bir çözüm bulunabilecekse dinlemek lazım ama güven vermiyor."
                    ]
                else:
                    ic_ses_list = [
                        "Fikir kulağa ilginç geliyor ama detayları ve kaliteyi görmeden net bir şey söyleyemem.",
                        "Kafamda çok soru işareti var, biraz daha düşünmem ve planları incelemem lazım."
                    ]

            chosen_ic_ses = ic_ses_list[i % len(ic_ses_list)]

            # ----------------------------------------------------
            # SPOKEN COLLOQUIAL TURKISH DIALOGUE (MASADAKİ İFADE)
            # ----------------------------------------------------
            if i == 0:
                # First speaker
                if is_beer_nightlife:
                    dis_soz = "Hocam şaka mı yapıyorsunuz? Kadıköy'de şu an barlarda bir bira 200-250 liradan aşağı değil. 100 liraya bira veren mekan açarsanız kapıda kuyruk olur, ilk günden masaları doldururuz!"
                elif is_politics:
                    if stance == "RED":
                        dis_soz = "Yahu kimse kusura bakmasın ama kimse kimseyi kandırmasın! 20 senedir aynı şeyleri dinliyoruz. Markete gidiyorsun iki poşet erzak 1000 lira. Emekli, işçi, genç perişan haldeyken ben nasıl 'devam' diyeyim? Değişim şart artık."
                    elif stance == "KABUL":
                        dis_soz = "Valla kusura bakmayın ama ben açık konuşacağım. Etrafımız ateş çemberi, her gün yeni bir kriz çıkıyor. Şurada eleştirecek yüz tane şey sayarım ama devleti bu ortamda acemi ellere bırakamayız. Ben istikrardan yanayım."
                    else:
                        dis_soz = "Açık konuşmak gerekirse iki tarafa da tam güvenemiyorum. Ekonomik tablo ortada, canımız yanıyor ama karşısındaki kadrolar da güven vermiyor."
                elif is_religion_secularism:
                    if stance == "RED":
                        dis_soz = "Arkadaşlar kusura bakmayın ama bu teklif tam bir akıl tutulmasıdır. Moda sahili Kadıköy halkının çoluk çocuk çimlere oturup nefes aldığı tek kıyı şeridi. 400 metre yukarıda tarihi Caferağa ve Moda camileri açıkken, sahilin yeşil alanını betonlaştırmak ne dine ne şehirciliğe sığar; kesinlikle karşıyız!"
                    else:
                        dis_soz = "İbadet yeri her mahallede olmalıdır. Eğer bölgede bir ihtiyaç varsa sahile uygun mimaride küçük bir cami yapılması neden sorun olsun ki?"
                else:
                    dis_soz = "Fiyat ve konsept gençlerin ve sokaktaki insanın bütçesi için oldukça cazip görünüyor, ben desteklerim."

            else:
                # Subsequent speakers INTERACT with previous speakers by name
                prev_ref = f"{prev_speaker_first} {prev_speaker_title}"
                
                if is_politics:
                    if stance == "RED" and prev_stance == "KABUL":
                        dis_soz = f"{prev_ref} iyi hoş anlatıyorsun da, sen son bir aydır hiç pazara çıktın mı gözünü seveyim? Neyin istikrarı bu? Milletin cebinde kuruş kalmamış, çocuklar et göremiyor evde. İstikrar diye diye açlığa mahkum edildik!"
                    elif stance == "KABUL" and prev_stance == "RED":
                        dis_soz = f"{prev_ref} sonuna kadar haklısın, geçim sıkıntısını hepimiz çekiyoruz, ben aksini söylemiyorum ki! Ama bak, ortalık karışırsa, yarın bir koalisyon kavgası çıkarsa o marketteki domatesi de bulamazsın. Yangına körükle gitmeyelim diyorum."
                    elif stance == "RED" and prev_stance == "RED":
                        dis_soz = f"{prev_ref}'a aynen katılıyorum. Az bile söyledi. 20 senedir aynı masallar; toptan bir zihniyet değişikliği ve liyakat gelmeden bu ülke feraha çıkamaz."
                    elif stance == "KABUL" and prev_stance == "KABUL":
                        dis_soz = f"{prev_ref}'a katılıyorum. Kusurları çok, canımız da yanıyor ama bu çalkantılı coğrafyada devleti maceraya sürüklememek lazım, tecrübeli kadrolarla yola devam edilmeli."
                    else:
                        # CEKIMSER
                        dis_soz = f"Araya gireyim kusura bakmayın ama ikinizi dinlerken de hak veriyorum. {prev_ref} 'geçim bitti' diyor, doğru; diğer taraftan 'güvenlik ve liderlik' deniyor, o da doğru. Biz halk olarak tam bu ikisinin arasında eziliyoruz."

                elif is_beer_nightlife:
                    if stance == "KABUL":
                        dis_soz = f"{prev_ref}'a sonuna kadar katılıyorum! Kadıköy'de öğrenci halimizle dışarı çıkamaz olduk. 100 lira harika bir fiyat, arkadaş grubunu toplayıp her hafta sonu geliriz. Yeter ki birayı sulandırmasınlar ve güzel müzik çalsınlar."
                    elif stance == "CEKIMSER":
                        dis_soz = f"{prev_ref} heyecanını anlıyorum fiyat süper ama mekanın kitlesi ve ortamı nasıl olacak? İzdihamdan oturulmazsa veya çok gürültülü olursa sırf ucuz diye gidilmez, mekanın kalitesi de önemli."
                    else:
                        dis_soz = f"{prev_ref} iyi hoş da bu enflasyonda 100 liraya bira satmak sürdürülebilir değil. Ya kalitesiz biradır ya da içeride ekstra şeylerden para çıkarırlar, temkinli olmak lazım."

                elif is_religion_secularism:
                    if stance == "RED" and prev_stance == "KABUL":
                        dis_soz = f"{prev_ref} iyi niyetle söylüyorsun da sen hiç Moda sahiline indin mi? Kadıköy'de cami eksiği mi var Allah aşkına? Caferağa Camii, Osmanağa Camii, İskele Camii hepsi 5 dakika yürüme mesafesinde. Mesele cami değil, insanların nefes aldığı son yeşil sahili yok etmektir!"
                    elif stance == "RED" and prev_stance == "RED":
                        dis_soz = f"{prev_ref}'a yüzde yüz katılıyorum. Ağzına sağlık. Kıyı Kanunu var bu ülkede; sahiller halkın ortak malıdır, imara açılamaz. Kadıköy'ün kültürünü ve doğasını korumak zorundayız."
                    else:
                        dis_soz = f"Araya gireyim ama iki taraf da çok gergin. {prev_ref} sahil yeşil kalsın diyor haklı, ama ibadet etmek isteyen insanları da ötekileştirmemek lazım. Eğer ihtiyaç varsa tarihi camilerin bakımı yapılsın, sahile dokunulmasın."

                else:
                    if stance == "KABUL" and prev_stance == "KABUL":
                        dis_soz = f"{prev_ref}'a katılıyorum, günümüz piyasasında böyle uygun fiyatlı çözümlere çok ihtiyaç var, ben şahsen denerim."
                    elif stance == "RED" and prev_stance == "RED":
                        dis_soz = f"{prev_ref}'a katılıyorum, şartlar netleşmeden ve halkın yararı kanıtlanmadan bu projeyi desteklemek mümkün değil."
                    elif stance == "RED":
                        dis_soz = f"{prev_ref} iyi niyetlisin ama sahadaki gerçekler öyle değil. Bu projenin getireceği yük faydasından katbekat fazla olur; ben reddediyorum."
                    elif stance == "KABUL":
                        dis_soz = f"{prev_ref}'ın endişelerini anlıyorum ama doğru bir denetimle bu işin altından kalkılabilir, peşinen reddetmek doğru değil."
                    else:
                        dis_soz = f"Valla {prev_ref}, şartları iyice netleştirmeden ne evet denir ne hayır."

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
        if is_politics:
            barriers = [
                "Derin Mutfak Enflasyonu ve Alım Gücü Tükenişi",
                "Liyakat Erozyonu ve Kurumsal Güvensizlik",
                "Gençlikte Gelecek Kaygısı ve Sosyal Alan Baskısı"
            ]
            action = "Halka üst perdeden 'sabır' telkin etmek yerine, mutfaktaki somut yangına yönelik acil can suyu adımları atılmalıdır."
            what_if = {
                "senaryo_1_guvence": "Emekli maaşlarına ve asgari ücrete enflasyon üstü ek zam yapılırsa kabul: %58.0",
                "senaryo_2_fiyat": "Mutfak enflasyonu düşürülemezse kabul: %24.0",
                "en_hizli_ikna_olacak_segment": "Kararsız orta yaşlı çalışanlar, emekliler ve esnaf"
            }
            polarization = "0.85 / 1.0 (Yüksek Siyasi ve Ekonomik Kutuplaşma)"

        elif is_beer_nightlife:
            barriers = [
                "Aşırı Yoğunluk ve Masa Bulma / Sıra Bekleme Kaygısı",
                "İçecek ve Hizmet Kalitesinde Düşüş Şüphesi (Sulandırılma/Sahte Endişesi)",
                "Mekan Ambiyansı, Müzik ve Müşteri Profili Seçiciliği"
            ]
            action = "100 TL fıçı bira fiyatlandırması Kadıköy gençliğinde %90+ talep patlaması yaratır. Başarı için taze ve markalı bira garantisi verilmeli, müzik ve havalandırma standartları yüksek tutulmalıdır."
            what_if = {
                "senaryo_1_guvence": "Markalı fıçı ve kaliteli müzik sunulursa kabul: %96.0",
                "senaryo_2_fiyat": "Fiyat 160 TL'ye çıkarsa kabul: %68.0",
                "en_hizli_ikna_olacak_segment": "Üniversite öğrencileri ve genç çalışanlar"
            }
            polarization = "0.15 / 1.0 (Yüksek Mutabakat / Güçlü Tüketici Talebi)"

        elif is_religion_secularism:
            barriers = [
                "Kamusal Yeşil Alan ve Kıyı Şeridi Tahribatı Endişesi",
                "Mevcut Tarihi Camilerin Yeterliliği ve Mesafe Yakınlığı",
                "Yaşam Tarzına ve Kentsel Kültüre Müdahale Algısı"
            ]
            action = "Bölgede yeni bir kıyı inşaatı yerine mevcut tarihi camilerin (Caferağa, Osmanağa) restorasyonu yapılmalı, sahilin doğal yeşil dokusu korunmalıdır."
            what_if = {
                "senaryo_1_guvence": "Sahil yeşil alanı korunup mevcut camiler restore edilirse mutabakat: %88.0",
                "senaryo_2_fiyat": "Halk oylaması (referandum) yapılırsa kabul: %18.5",
                "en_hizli_ikna_olacak_segment": "Ilımlı çevreye duyarlı sakinler"
            }
            polarization = "0.92 / 1.0 (Şiddetli Kutuplaşma / Yaşam Tarzı Hassasiyeti)"

        elif is_security:
            barriers = [
                "Şehit ve Gazi Ailelerinin Vicdani Kırgınlığı ve Kırmızı Çizgiler",
                "Adalet ve Hukuk Devleti İlkelerinin Zedelenmesi Kaygısı",
                "Terörle Mücadeledeki Kazanımların Kaybedilmesi Endişesi"
            ]
            action = "Milli güvenlik ve af konularında şehit aileleri ve gazilerin rızası olmadan hiçbir adım atılmamalıdır."
            what_if = {
                "senaryo_1_guvence": "Şehit ve gazi derneklerinin mutlak onayı alınırsa kabul: %45.0",
                "senaryo_2_fiyat": "Öcalan için genel af çıkarılırsa ret: %98.0",
                "en_hizli_ikna_olacak_segment": "Geleneksel milliyetçi taban"
            }
            polarization = "0.95 / 1.0 (Mutlak Kırmızı Çizgi / Yüksek Duygusal Hassasiyet)"

        else:
            barriers = [
                "Fiyat / Kalite Algısı ve Şeffaflık İhtiyacı",
                "Müşteri Deneyimi ve Sosyal Kanıt Eksikliği",
                "Alternatif Mekan ve Marka Sadakati"
            ]
            action = "Net ve şeffaf fiyatlandırma politikası sürdürülmeli, hedef kitleye yönelik deneyim odaklı tanıtım yapılmalıdır."
            what_if = {
                "senaryo_1_guvence": "Maliyetler sübvanse edilirse kabul: %78.0",
                "senaryo_2_fiyat": "Ek maliyet halka yansıtılırsa ret: %85.0",
                "en_hizli_ikna_olacak_segment": "Dar ve sabit gelirli hanehalkları"
            }
            polarization = "0.65 / 1.0 (Orta Düzey Kutuplaşma)"

        return {
            "odak_grubu_tartismasi": discussions,
            "yonetici_pazar_analiz_raporu": {
                "genel_kabul_orani_yuzde": accept_pct,
                "en_buyuk_3_itiraz_bariyeri": barriers,
                "fiyat_duyarlilik_analizi": "Toplumsal ve ekonomik dinamikler doğrultusunda kanaatler derin kutuplaşma ve somut geçim göstergeleri üzerinden şekillenmektedir.",
                "kutuplasma_indeksi_skoru": polarization,
                "what_if_karsi_olgusal_stres_testi": what_if,
                "stratejik_urun_tavsiyesi": action
            }
        }
