"""
Turkish locale data for DataForge synthetic data generation.
Contains 200+ entries for names, cities, addresses, brands, and more.
"""
from __future__ import annotations
from typing import Any


# ---------------------------------------------------------------------------
# AGE-COHORT GENERATIONAL MALE NAMES
# ---------------------------------------------------------------------------

# Traditional Senior Generation (60-85+ ya): 1940-1965 doğumlular
MALE_NAMES_SENIOR = [
    "Mehmet", "Mustafa", "Ahmet", "Ali", "Hüseyin", "Hasan", "İbrahim", "İsmail",
    "Osman", "Süleyman", "Halil", "Ramazan", "Mahmut", "Recep", "Şaban", "Kazım",
    "Muzaffer", "Hikmet", "Necati", "Celal", "Nuri", "Şevket", "Fahri", "Dursun",
    "Kemal", "Sabri", "Sadık", "Salih", "Zeki", "Hayati", "Kadir", "Şakir",
    "Enver", "Rıza", "Hamdi", "Lütfi", "Tevfik", "Bedri", "Ziya", "Rasim",
    "Tahsin", "Niyazi", "Veli", "Galip", "İlyas", "Şerafettin", "Adil", "Cevdet",
    "Fikret", "Bahri", "Vecdi", "Davut", "Abdurrahman", "Bayram", "Hamza", "İhsan",
]

# Middle Generation / X & Y (35-59 yaş): 1965-1990 doğumlular
MALE_NAMES_MIDDLE = [
    "Murat", "Hakan", "Serkan", "Erkan", "Volkan", "Gökhan", "Tolga", "Onur",
    "Barış", "Özgür", "Uğur", "Alper", "Cenk", "Cihan", "Bülent", "Levent",
    "Koray", "Tuncay", "Engin", "Selim", "Sinan", "Metin", "Çetin", "Serdar",
    "Kenan", "Erdem", "Zafer", "Tayfun", "Birol", "Şenol", "Erol", "Soner",
    "Taner", "İlker", "Tanju", "Oktay", "Olcay", "Önder", "Cüneyt", "Ferhat",
    "Fatih", "Oğuzhan", "Burak", "Cem", "Caner", "Haluk", "Ufuk", "Güven",
    "Teoman", "Yalçın", "Altan", "Dinçer", "Savaş", "Tarık",
]

# Young & Gen Z Generation (18-34 yaş): 1990-2008 doğumlular
MALE_NAMES_YOUNG = [
    "Berk", "Berkecan", "Batuhan", "Berke", "Ege", "Emre", "Arda", "Kaan",
    "Doruk", "Mert", "Can", "Alp", "Kerem", "Efe", "Emir", "Eren",
    "Bartu", "Sarp", "Yağız", "Poyraz", "Bora", "Rüzgar", "Utku", "Deniz",
    "Atlas", "Kuzey", "Çınar", "Baran", "Atakan", "Göktürk", "Alptuğ", "Meriç",
    "Görkem", "Berkay", "Yiğit", "Tuna", "Toprak", "Furkan", "Alperen", "Enes",
    "Umut", "Yasin", "Göktuğ", "Orkun", "Polat", "Egemen",
]

MALE_NAMES = MALE_NAMES_SENIOR + MALE_NAMES_MIDDLE + MALE_NAMES_YOUNG

# ---------------------------------------------------------------------------
# AGE-COHORT GENERATIONAL FEMALE NAMES
# ---------------------------------------------------------------------------

# Traditional Senior Generation (60-85+ yaş): 1940-1965 doğumlular
FEMALE_NAMES_SENIOR = [
    "Fatma", "Ayşe", "Emine", "Hatice", "Meryem", "Şerife", "Sultan", "Hanife",
    "Fadime", "Hacer", "Havva", "Zeliha", "Cemile", "Ayten", "Müşerref", "Saadet",
    "Muazzez", "Naciye", "Şaziye", "Şükran", "Leman", "Meliha", "Sabahat", "Neriman",
    "Semiha", "Bedriye", "Kadriye", "Mediha", "Nazife", "Şadiye", "Vasfiye", "Dürdane",
    "Nermin", "Kamuran", "Saliha", "Gülsüm", "Remziye", "Makbule", "Behiye", "Feride",
    "Huriye", "Lütviye", "Ünzile", "Vesile", "Pembe", "Raziye", "Ümmühan", "Azize",
    "Zehra", "Vahide", "Hayriye", "Latife",
]

# Middle Generation / X & Y (35-59 yaş): 1965-1990 doğumlular
FEMALE_NAMES_MIDDLE = [
    "Dilek", "Arzu", "Ebru", "Burcu", "Pınar", "Özlem", "Berna", "Banu",
    "Sibel", "Filiz", "Hülya", "Neslihan", "Nuray", "Tülay", "Gülay", "Sevil",
    "Sevinç", "Nilgün", "Belgin", "Gülşen", "Yasemin", "Çiğdem", "Aslı", "Başak",
    "Meltem", "İlknur", "Aynur", "Şule", "Esin", "Funda", "Yonca", "Demet",
    "Selda", "Seda", "Hande", "Yeşim", "Esra", "Şebnem", "Serap", "Ümran",
    "Oya", "Perihan", "Reyhan", "Güzide", "Nihal", "Selma", "Neşe", "Jale",
    "Berrak", "Leyla", "Melek", "Zülal", "Derya", "Gamze",
]

# Young & Gen Z Generation (18-34 yaş): 1990-2008 doğumlular
FEMALE_NAMES_YOUNG = [
    "Melisa", "Selin", "İrem", "Ceren", "Dilara", "Melis", "Doğa", "Derin",
    "Defne", "Duru", "Bade", "Ela", "Lara", "Nil", "Su", "Beren",
    "Nehir", "Ilgın", "Simge", "Pelin", "Damla", "Yağmur", "Tuana", "Aleyna",
    "Ecem", "Beste", "Berfin", "Helin", "Hazal", "Açelya", "Irmak", "Mira",
    "Masal", "Alara", "Ece", "İdil", "Mina", "Cansu", "Miray", "Nazlı",
    "Elçin", "Feyza", "Tuğçe", "İlayda", "Ceyda", "Büşra", "Merve", "Elif",
    "Zeynep", "Bahar", "Efsun", "Fulya", "Gözde", "Aylin",
]

FEMALE_NAMES = FEMALE_NAMES_SENIOR + FEMALE_NAMES_MIDDLE + FEMALE_NAMES_YOUNG


def get_name_by_age_and_gender(gender: str, age: int, rng=None) -> str:
    """Sample authentic generational first name matching demographic cohort (No 'Berkecan Dede'!)."""
    if rng is None:
        import random
        rng = random.Random()

    is_male = (gender == "Erkek")

    if age >= 60:
        # 88% Traditional Senior, 12% Middle
        pool = MALE_NAMES_SENIOR if is_male else FEMALE_NAMES_SENIOR
        alt_pool = MALE_NAMES_MIDDLE if is_male else FEMALE_NAMES_MIDDLE
        return rng.choice(pool) if rng.random() < 0.88 else rng.choice(alt_pool)
    elif age >= 35:
        # 85% Middle Gen, 10% Senior, 5% Young
        pool = MALE_NAMES_MIDDLE if is_male else FEMALE_NAMES_MIDDLE
        alt_pool = MALE_NAMES_SENIOR if is_male else FEMALE_NAMES_SENIOR
        return rng.choice(pool) if rng.random() < 0.85 else rng.choice(alt_pool)
    else:
        # 88% Young / Gen Z, 12% Classic/Middle
        pool = MALE_NAMES_YOUNG if is_male else FEMALE_NAMES_YOUNG
        alt_pool = MALE_NAMES_MIDDLE if is_male else FEMALE_NAMES_MIDDLE
        return rng.choice(pool) if rng.random() < 0.88 else rng.choice(alt_pool)

# ---------------------------------------------------------------------------
# SURNAMES (80 entries)
# ---------------------------------------------------------------------------
SURNAMES = [
    "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Yıldırım",
    "Öztürk", "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç", "Aslan",
    "Çetin", "Erdoğan", "Koç", "Kurt", "Özkan", "Şimşek", "Polat",
    "Kaplan", "Turan", "Aktaş", "Karataş", "Keskin", "Güneş", "Korkmaz",
    "Demirci", "Çakır", "Bulut", "Duman", "Aksoy", "Güler", "Güven",
    "Bozkurt", "Avcı", "Yavuz", "Toprak", "Dinç", "Karadeniz", "Sağlam",
    "Kara", "Ateş", "Bilgin", "Çoban", "Erdem", "Fidan", "Göktürk",
    "İlhan", "Kırmızı", "Mutlu", "Nar", "Ören",
    "Pala", "Rüzgar", "Sarı", "Taş", "Uçar", "Vardar", "Yeni",
    "Zengin", "Alpay", "Bayrak", "Ceylan", "Dağ", "Erol", "Gündüz",
    "Horoz", "İpek", "Kıran", "Leblebici", "Mercan", "Nalbant",
    "Olgun", "Parlak", "Reis", "Solmaz", "Temiz", "Uysal", "Vural",
    "Yaman", "Zorlu",
]

# ---------------------------------------------------------------------------
# 81 TURKISH PROVINCES
# ---------------------------------------------------------------------------
CITIES = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara",
    "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl",
    "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı",
    "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan",
    "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
    "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir",
    "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli",
    "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin",
    "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya",
    "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
    "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat",
    "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman",
    "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük",
    "Kilis", "Osmaniye", "Düzce",
]

# Population weights (approx. proportional to real distribution)
CITY_WEIGHTS = [
    0.026, 0.007, 0.009, 0.006, 0.004, 0.068,  # Adana -> Ankara
    0.031, 0.002, 0.013, 0.015, 0.003, 0.003,  # Antalya -> Bingöl
    0.004, 0.004, 0.003, 0.038, 0.006, 0.002,  # Bitlis -> Çankırı
    0.006, 0.012, 0.021, 0.005, 0.007, 0.003,  # Çorum -> Erzincan
    0.009, 0.011, 0.025, 0.005, 0.002,          # Erzurum -> Gümüşhane
    0.003, 0.019, 0.005, 0.022, 0.185, 0.052,  # Hakkari -> İzmir
    0.003, 0.004, 0.017, 0.004, 0.003, 0.024,  # Kars -> Kocaeli
    0.027, 0.007, 0.009, 0.017, 0.014, 0.010,  # Konya -> Mardin
    0.012, 0.005, 0.004, 0.004, 0.009, 0.004,  # Muğla -> Rize
    0.012, 0.016, 0.004, 0.003, 0.007, 0.013,  # Sakarya -> Tekirdağ
    0.007, 0.010, 0.001, 0.025, 0.004, 0.013,  # Tokat -> Van
    0.005, 0.007, 0.005, 0.001, 0.003, 0.003,  # Yozgat -> Kırıkkale
    0.007, 0.006, 0.003, 0.001, 0.002, 0.003,  # Batman -> Yalova
    0.003, 0.002, 0.006, 0.005                  # Karabük -> Düzce
]

# ---------------------------------------------------------------------------
# ALL 81 CITIES -> REAL DISTRICTS (İLÇELER)
# ---------------------------------------------------------------------------
CITY_DISTRICTS: dict[str, list[str]] = {
    "Adana": ["Seyhan", "Yüreğir", "Çukurova", "Sarıçam", "Ceyhan", "Kozan", "İmamoğlu", "Karataş", "Pozantı"],
    "Adıyaman": ["Merkez", "Kahta", "Besni", "Gölbaşı", "Gerger", "Sincik", "Çelikhan"],
    "Afyonkarahisar": ["Merkez", "Sandıklı", "Dinar", "Bolvadin", "Sinanpaşa", "Emirdağ", "Şuhut", "Çay"],
    "Ağrı": ["Merkez", "Doğubayazıt", "Patnos", "Diyadin", "Eleşkirt", "Tutak", "Taşlıçay"],
    "Amasya": ["Merkez", "Merzifon", "Suluova", "Taşova", "Gümüşhacıköy", "Göynücek"],
    "Ankara": ["Çankaya", "Keçiören", "Yenimahalle", "Mamak", "Etimesgut", "Sincan", "Altındağ", "Pursaklar", "Gölbaşı", "Polatlı", "Çubuk", "Kahramankazan", "Beypazarı"],
    "Antalya": ["Muratpaşa", "Kepez", "Konyaaltı", "Alanya", "Manavgat", "Serik", "Döşemealtı", "Kumluca", "Kaş", "Kemer", "Gazipaşa"],
    "Artvin": ["Merkez", "Hopa", "Borçka", "Yusufeli", "Arhavi", "Şavşat", "Kemalpaşa"],
    "Aydın": ["Efeler", "Kuşadası", "Söke", "Nazilli", "Didim", "İncirliova", "Çine", "Germencik"],
    "Balıkesir": ["Karesi", "Altıeylül", "Bandırma", "Edremit", "Gönen", "Ayvalık", "Burhaniye", "Erdek"],
    "Bilecik": ["Merkez", "Bozüyük", "Osmaneli", "Söğüt", "Gölpazarı", "Pazaryeri"],
    "Bingöl": ["Merkez", "Genç", "Solhan", "Karlıova", "Adaklı", "Kiğı"],
    "Bitlis": ["Tatvan", "Merkez", "Güroymak", "Ahlat", "Hizan", "Mutki", "Adilcevaz"],
    "Bolu": ["Merkez", "Gerede", "Mengen", "Mudurnu", "Göynük", "Yeniçağa"],
    "Burdur": ["Merkez", "Bucak", "Gölhisar", "Yeşilova", "Tefenni", "Ağlasun"],
    "Bursa": ["Osmangazi", "Nilüfer", "Yıldırım", "İnegöl", "Gemlik", "Mustafakemalpaşa", "Mudanya", "Gürsu", "Kestel", "Orhangazi"],
    "Çanakkale": ["Merkez", "Biga", "Çan", "Gelibolu", "Ayvacık", "Ezine", "Yenice", "Bozcaada"],
    "Çankırı": ["Merkez", "Çerkeş", "Ilgaz", "Orta", "Şabanözü", "Kurşunlu"],
    "Çorum": ["Merkez", "Sungurlu", "Osmancık", "İskilip", "Alaca", "Bayat"],
    "Denizli": ["Pamukkale", "Merkezefendi", "Çivril", "Acıpayam", "Tavas", "Honaz", "Sarayköy"],
    "Diyarbakır": ["Bağlar", "Kayapınar", "Yenişehir", "Sur", "Bismil", "Ergani", "Silvan", "Çınar"],
    "Edirne": ["Merkez", "Keşan", "Uzunköprü", "İpsala", "Havsa", "Enez"],
    "Elazığ": ["Merkez", "Kovancılar", "Karakoçan", "Palu", "Baskil", "Maden", "Keban"],
    "Erzincan": ["Merkez", "Tercan", "Üzümlü", "Çayırlı", "İliç", "Kemaliye", "Refahiye"],
    "Erzurum": ["Yakutiye", "Palandöken", "Aziziye", "Horasan", "Oltu", "Pasinler"],
    "Eskişehir": ["Odunpazarı", "Tepebaşı", "Sivrihisar", "Çifteler", "Seyitgazi", "Alpu"],
    "Gaziantep": ["Şahinbey", "Şehitkamil", "Nizip", "İslahiye", "Nurdağı", "Oğuzeli"],
    "Giresun": ["Merkez", "Bulancak", "Espiye", "Görele", "Tirebolu", "Şebinkarahisar"],
    "Gümüşhane": ["Merkez", "Kelkit", "Şiran", "Kürtün", "Torul"],
    "Hakkari": ["Yüksekova", "Merkez", "Şemdinli", "Çukurca", "Derecik"],
    "Hatay": ["Antakya", "İskenderun", "Defne", "Dörtyol", "Samandağ", "Kırıkhan", "Reyhanlı", "Arsuz"],
    "Isparta": ["Merkez", "Yalvaç", "Eğirdir", "Şarkikaraağaç", "Gelendost", "Keçiborlu"],
    "Mersin": ["Yenişehir", "Akdeniz", "Mezitli", "Toroslar", "Tarsus", "Erdemli", "Silifke", "Anamur"],
    "İstanbul": [
        "Kadıköy", "Beşiktaş", "Şişli", "Üsküdar", "Maltepe", "Kartal", "Pendik",
        "Ataşehir", "Bakırköy", "Beyoğlu", "Fatih", "Sarıyer", "Beylikdüzü",
        "Bahçelievler", "Zeytinburnu", "Ümraniye", "Tuzla", "Büyükçekmece",
        "Başakşehir", "Küçükçekmece", "Esenyurt", "Gaziosmanpaşa", "Eyüpsultan",
        "Kağıthane", "Sultangazi", "Avcılar", "Bağcılar", "Bayrampaşa", "Beykoz",
        "Çekmeköy", "Esenler", "Güngören", "Sancaktepe", "Sultanbeyli", "Şile"
    ],
    "İzmir": [
        "Konak", "Karşıyaka", "Bornova", "Buca", "Çiğli", "Gaziemir",
        "Bayraklı", "Karabağlar", "Balçova", "Narlıdere", "Güzelbahçe",
        "Urla", "Çeşme", "Seferihisar", "Menderes", "Torbalı", "Kemalpaşa",
        "Menemen", "Aliağa", "Foça", "Dikili", "Bergama", "Ödemiş", "Tire"
    ],
    "Kars": ["Merkez", "Kağızman", "Sarıkamış", "Selim", "Digor", "Arpaçay"],
    "Kastamonu": ["Merkez", "Tosya", "Taşköprü", "Cide", "İnebolu", "Araç"],
    "Kayseri": ["Melikgazi", "Kocasinan", "Talas", "Develi", "Yahyalı", "Bünyan", "Pınarbaşı", "İncesu"],
    "Kırklareli": ["Merkez", "Lüleburgaz", "Babaeski", "Vize", "Pınarhisar"],
    "Kırşehir": ["Merkez", "Kaman", "Mucur", "Çiçekdağı"],
    "Kocaeli": ["İzmit", "Gebze", "Darıca", "Körfez", "Gölcük", "Derince", "Çayırova", "Kartepe", "Başiskele", "Karamürsel"],
    "Konya": ["Selçuklu", "Meram", "Karatay", "Ereğli", "Akşehir", "Beyşehir", "Cihanbeyli", "Kulu", "Seydişehir", "Ilgın", "Çumra"],
    "Kütahya": ["Merkez", "Tavşanlı", "Simav", "Gediz", "Emet"],
    "Malatya": ["Yeşilyurt", "Battalgazi", "Doğanşehir", "Akçadağ", "Darende", "Hekimhan"],
    "Manisa": ["Yunusemre", "Şehzadeler", "Akhisar", "Turgutlu", "Salihli", "Soma", "Alaşehir", "Saruhanlı"],
    "Kahramanmaraş": ["Onikişubat", "Dulkadiroğlu", "Elbistan", "Afşin", "Türkoğlu", "Pazarcık", "Göksun"],
    "Mardin": ["Artuklu", "Kızıltepe", "Midyat", "Nusaybin", "Derik", "Mazıdağı"],
    "Muğla": ["Bodrum", "Fethiye", "Milas", "Menteşe", "Marmaris", "Ortaca", "Yatağan", "Dalaman", "Datça"],
    "Muş": ["Merkez", "Bulanık", "Malazgirt", "Varto", "Hasköy"],
    "Nevşehir": ["Merkez", "Ürgüp", "Avanos", "Gülşehir", "Derinkuyu", "Kozaklı"],
    "Niğde": ["Merkez", "Bor", "Çiftlik", "Ulukışla"],
    "Ordu": ["Altınordu", "Ünye", "Fatsa", "Gölköy", "Kumru", "Korgan", "Perşembe"],
    "Rize": ["Merkez", "Çayeli", "Ardeşen", "Pazar", "Fındıklı", "Güneysu"],
    "Sakarya": ["Adapazarı", "Serdivan", "Akyazı", "Erenler", "Hendek", "Karasu", "Sapanca", "Geyve"],
    "Samsun": ["İlkadım", "Atakum", "Canik", "Bafra", "Çarşamba", "Tekkeköy", "Vezirköprü", "Terme", "Havza"],
    "Siirt": ["Merkez", "Kurtalan", "Pervari", "Baykan", "Şirvan"],
    "Sinop": ["Merkez", "Boyabat", "Gerze", "Ayancık", "Durağan"],
    "Sivas": ["Merkez", "Şarkışla", "Yıldızeli", "Suşehri", "Zara", "Gemerek", "Kangal"],
    "Tekirdağ": ["Süleymanpaşa", "Çorlu", "Çerkezköy", "Kapaklı", "Ergene", "Malkara", "Saray"],
    "Tokat": ["Merkez", "Erbaa", "Turhal", "Zile", "Niksar", "Reşadiye"],
    "Trabzon": ["Ortahisar", "Akçaabat", "Araklı", "Of", "Yomra", "Arsin", "Vakfıkebir", "Sürmene", "Maçka"],
    "Tunceli": ["Merkez", "Pertek", "Mazgirt", "Çemişgezek", "Hozat", "Ovacık"],
    "Şanlıurfa": ["Eyyübiye", "Haliliye", "Karaköprü", "Siverek", "Viranşehir", "Birecik", "Suruç", "Harran"],
    "Uşak": ["Merkez", "Banaz", "Eşme", "Sivaslı"],
    "Van": ["İpekyolu", "Tuşba", "Edremit", "Erciş", "Özalp", "Çaldıran", "Başkale"],
    "Yozgat": ["Merkez", "Sorgun", "Akdağmadeni", "Yerköy", "Boğazlıyan"],
    "Zonguldak": ["Merkez", "Ereğli", "Çaycuma", "Devrek", "Kozlu", "Kilimli", "Alaplı"],
    "Aksaray": ["Merkez", "Ortaköy", "Eskil", "Gülağaç", "Güzelyurt"],
    "Bayburt": ["Merkez", "Demirözü", "Aydıntepe"],
    "Karaman": ["Merkez", "Ermenek", "Sarıveliler", "Ayrancı"],
    "Kırıkkale": ["Merkez", "Yahşihan", "Keskin", "Delice", "Bahşılı"],
    "Batman": ["Merkez", "Kozluk", "Sason", "Beşiri", "Gercüş", "Hasankeyf"],
    "Şırnak": ["Cizre", "Silopi", "Merkez", "İdil", "Uludere", "Beytüşşebap"],
    "Bartın": ["Merkez", "Amasra", "Ulus", "Kurucaşile"],
    "Ardahan": ["Merkez", "Göle", "Çıldır", "Hanak", "Posof"],
    "Iğdır": ["Merkez", "Tuzluca", "Aralık", "Karakoyunlu"],
    "Yalova": ["Merkez", "Çiftlikköy", "Çınarcık", "Altınova", "Armutlu"],
    "Karabük": ["Merkez", "Safranbolu", "Yenice", "Eskipazar"],
    "Kilis": ["Merkez", "Musabeyli", "Elbeyli", "Polateli"],
    "Osmaniye": ["Merkez", "Kadirli", "Düziçi", "Bahçe", "Toprakkale"],
    "Düzce": ["Merkez", "Akçakoca", "Gölyaka", "Kaynaşlı", "Çilimli"],
}

# ---------------------------------------------------------------------------
# DISTRICT-SPECIFIC AUTHENTIC NEIGHBORHOODS (MAHALLELER)
# ---------------------------------------------------------------------------
DISTRICT_NEIGHBORHOODS: dict[str, list[str]] = {
    # İstanbul İlçeleri
    "Kadıköy": ["Caferağa", "Moda", "Caddebostan", "Fenerbahçe", "Feneryolu", "Suadiye", "Bostancı", "Göztepe", "Kozyatağı", "Acıbadem", "Rasimpaşa", "Hasanpaşa", "Erenköy", "Sahrayıcedit", "19 Mayıs", "Fikirtepe"],
    "Beşiktaş": ["Bebek", "Etiler", "Levent", "Ortaköy", "Abbasağa", "Akatlar", "Arnavutköy", "Balmumcu", "Gayrettepe", "Kuruçeşme", "Sinanpaşa", "Türkali", "Vişnezade", "Yıldız", "Nisbetiye"],
    "Şişli": ["Mecidiyeköy", "Fulya", "Nişantaşı", "Teşvikiye", "Halaskargazi", "Harbiye", "Cumhuriyet", "Gülbahar", "Merkez", "19 Mayıs", "Feriköy", "Pangaltı", "Esentepe"],
    "Üsküdar": ["Kuzguncuk", "Beylerbeyi", "Çengelköy", "Kandilli", "Altunizade", "Acıbadem", "Salacak", "Mimar Sinan", "Zeynep Kamil", "Bulgurlu", "Ünalan", "Kısıklı", "Valide-i Atik"],
    "Bakırköy": ["Ataköy", "Yeşilköy", "Yeşilyurt", "Florya", "Zuhuratbaba", "Kartaltepe", "Osmaniye", "Sakızağacı", "Cevizlik", "Yenimahalle"],
    "Beyoğlu": ["Cihangir", "Galata", "Karaköy", "Asmalımescit", "Gümüşsuyu", "Tomtom", "Pürtelaş", "Kuloğlu", "Halıcıoğlu", "Sütlüce"],
    "Fatih": ["Balat", "Fener", "Sultanahmet", "Aksaray", "Kocamustafapaşa", "Topkapı", "Cerrahpaşa", "Haseki", "Şehremini", "Karagümrük", "Zeyrek"],
    "Sarıyer": ["Tarabya", "Yeniköy", "İstinye", "Emirgan", "Maslak", "Rumelihisarı", "Baltalimanı", "Büyükdere", "Kilyos", "Bahçeköy"],
    "Maltepe": ["Bağlarbaşı", "İdealtepe", "Küçükyalı", "Altıntepe", "Yalı", "Zümrütevler", "Cevizli", "Feyzullah", "Girne", "Aydınevler"],
    "Kartal": ["Kordonboyu", "Atalar", "Petrol İş", "Cevizli", "Uğur Mumcu", "Yukarı", "Orhantepe", "Karlıktepe", "Yakacık"],
    "Ataşehir": ["Barbaros", "Batı Ataşehir", "Atatürk", "İçerenköy", "Kayışdağı", "Küçükbakkalköy", "Örnek", "Yenisahra", "Mevlana"],
    "Ümraniye": ["Atakent", "Çakmak", "İnkılap", "İstiklal", "Namık Kemal", "Site", "Tantavi", "Yamanevler", "Ihlamurkuyu"],
    "Pendik": ["Batı", "Doğu", "Kurtköy", "Yenişehir", "Güzelyalı", "Bahçelievler", "Kaynarca", "Çamlık", "Esenyalı"],
    
    # Ankara İlçeleri
    "Çankaya": ["Kızılay", "Ayrancı", "Bahçelievler", "Gaziosmanpaşa", "Kavaklıdere", "Çayyolu", "Ümitköy", "Bilkent", "Yıldızevler", "Mustafa Kemal", "Söğütözü", "Oran", "Maltepe", "Emek", "100. Yıl", "Tunalı"],
    "Keçiören": ["Etlik", "İncirli", "Kalaba", "Aşağı Eğlence", "Kuşcağız", "Bağlarbaşı", "Ayvalı", "Uyanış", "Esertepe", "Şenlik"],
    "Yenimahalle": ["Batıkent", "Demetevler", "Çayyolu", "Ostim", "İvedik", "Ergazi", "Kardelen", "Ragıp Tüzün", "Gazi", "Şentepe"],
    "Etimesgut": ["Eryaman", "Bağlıca", "Elvankent", "Alsancak", "Süvari", "Kazım Karabekir", "Ahi Mesut", "Topçu", "Şehit Osman Avcı"],
    
    # İzmir İlçeleri
    "Karşıyaka": ["Bostanlı", "Mavişehir", "Alaybey", "Bahriye Üçok", "Aksoy", "Tersane", "Donanmacı", "Nergiz", "Goncalar", "Şemikler", "Yalı"],
    "Konak": ["Alsancak", "Göztepe", "Güzelyalı", "Hatay", "Kahramanlar", "Basmane", "Pasaport", "Mithatpaşa", "Gültepe", "Kültür"],
    "Bornova": ["Küçükpark", "Büyükpark", "Erzene", "Kazımdirik", "Evka 3", "Evka 4", "Doğanlar", "Mevlana", "Işıklar", "Yeşilova"],
    "Buca": ["Şirinyer", "Adatepe", "Efeler", "Yaylacık", "Vali Rahmi Bey", "Yenigün", "Çamlıkule", "Kozağaç"],
    
    # Bursa İlçeleri
    "Nilüfer": ["Görükle", "Özlüce", "İhsaniye", "Beşevler", "Fethiye", "Ataevler", "Barış", "Ertuğrul", "Balat", "Altınşehir", "Yüzüncüyıl"],
    "Osmangazi": ["Heykel", "Çekirge", "Altıparmak", "Dikkaldırım", "Kükürtlü", "Gaziakdemir", "Santral Garaj", "Soğanlı", "Demirtaş"],
    
    # Antalya İlçeleri
    "Muratpaşa": ["Lara", "Şirinyalı", "Fener", "Meltem", "Kaleiçi", "Gençlik", "Kırcami", "Yeşilbahçe", "Varlık", "Bahçelievler", "Çağlayan"],
    "Konyaaltı": ["Gürsu", "Altınkum", "Arapsuyu", "Liman", "Hurma", "Sarısu", "Öğretmenevleri", "Uluç", "Toros"],
    
    # Trabzon, Samsun, Konya, Gaziantep, Eskişehir, vb.
    "Ortahisar": ["Meydan", "Boztepe", "Değirmendere", "Erdoğdu", "Çömlekçi", "Kalkınma", "Beşirli", "Yenicuma", "İskenderpaşa"],
    "İlkadım": ["Çiftlik", "Gazi", "Zafer", "Kale", "Kılıçdede", "Fevzi Çakmak", "Hürriyet", "Pazar", "Rasathane"],
    "Selçuklu": ["Bosna Hersek", "Yazır", "Binkonutlar", "Aydınlıkevler", "Hocacihan", "Parsana", "Nişantaş", "Işıklar"],
    "Şahinbey": ["Akkent", "Karataş", "Güneykent", "Yeditepe", "Binevler", "Kolejtepe", "Bey", "İnönü"],
    "Odunpazarı": ["Vişnelik", "Akarbaşı", "Sümer", "Kırmızıtoprak", "Büyükdere", "Yenikent", "Osmangazi", "Gökmeydan"],
}

# ---------------------------------------------------------------------------
# COMMON AUTHENTIC TURKISH NEIGHBORHOODS (Used across all other towns)
# ---------------------------------------------------------------------------
COMMON_NEIGHBORHOODS = [
    "Cumhuriyet", "Atatürk", "Fatih", "İnönü", "Zafer", "Hürriyet",
    "Gazi", "Barış", "Yeni", "Yıldız", "Bahçelievler", "Mimar Sinan",
    "Yavuz Selim", "Yeşilova", "Gültepe", "Esentepe", "Kurtuluş",
    "İstiklal", "Çamlık", "Kültür", "Doğan", "Bağlar", "Aydınlıkevler",
    "Pınar", "Emek", "Güneş", "Kavaklı", "Çınar", "Kale", "Merkez",
    "Şehitler", "Ulubatlı", "Akşemsettin", "Ertuğrulgazi", "Kayabaşı",
    "Yıldırım", "Yenidoğan", "Köroğlu", "Selçuklu", "Mevlana",
    "Yunus Emre", "Alparslan", "Fevzi Çakmak", "Kazım Karabekir",
    "19 Mayıs", "23 Nisan", "30 Ağustos", "Namık Kemal", "Ziya Gökalp",
]

# Alias for backwards compatibility
NEIGHBORHOODS = COMMON_NEIGHBORHOODS

# ---------------------------------------------------------------------------
# ADDRESS GENERATION HELPER
# ---------------------------------------------------------------------------
def generate_address(rng=None, city: str | None = None) -> dict[str, Any]:
    """Generate a geographically authentic and consistent Turkish address.

    Ensures that city, district (ilçe), neighborhood (mahalle), street, and
    postal code belong together logically following official UAVT/PTT standards.

    Returns:
        dict with keys: 'city', 'district', 'neighborhood', 'street',
                        'building_no', 'flat_no', 'postal_code', 'full_address'
    """
    if rng is None:
        import random
        rng = random.Random()

    try:
        from .geo_db import GeoDatabase
        geo_db = GeoDatabase.get_instance()
        return geo_db.get_random_address(rng=rng, city=city)
    except Exception:
        # High-reliability in-memory fallback
        if city is None or city not in CITY_DISTRICTS:
            city = rng.choices(CITIES, weights=CITY_WEIGHTS)[0]

        districts = CITY_DISTRICTS.get(city, ["Merkez"])
        district = rng.choice(districts)

        if district in DISTRICT_NEIGHBORHOODS:
            neighborhood = rng.choice(DISTRICT_NEIGHBORHOODS[district])
        else:
            neighborhood = rng.choice(COMMON_NEIGHBORHOODS)

        postal_code = f"{CITIES.index(city)+1:02d}{rng.randint(100, 990)}"
        full_address = f"{neighborhood} Mah. {postal_code} {district} / {city}"

        return {
            "city": city,
            "district": district,
            "neighborhood": neighborhood,
            "postal_code": postal_code,
            "full_address": full_address,
        }




# ---------------------------------------------------------------------------
# PRODUCT CATEGORIES & SUBCATEGORIES
# ---------------------------------------------------------------------------
PRODUCT_CATEGORIES = {
    "Elektronik": [
        "Akıllı Telefon", "Laptop", "Tablet", "Monitör", "Klavye",
        "Fare", "Kulaklık", "Hoparlör", "Kamera", "Drone",
        "Akıllı Saat", "TV", "Projeksiyon", "Yazıcı", "Tarayıcı",
    ],
    "Giyim": [
        "Erkek T-Shirt", "Kadın Bluz", "Pantolon", "Etek", "Elbise",
        "Mont", "Ceket", "Kazak", "Sweatshirt", "Şort",
        "İç Giyim", "Çorap", "Şapka", "Eşarp", "Eldiven",
    ],
    "Ev & Yaşam": [
        "Mobilya", "Aydınlatma", "Dekorasyon", "Mutfak Gereçleri",
        "Banyo Aksesuarları", "Yatak Odası", "Oturma Odası",
        "Bahçe & Dış Mekan", "Halı & Kilim", "Perde & Stor",
    ],
    "Spor & Outdoor": [
        "Fitness Ekipmanı", "Koşu Ayakkabısı", "Bisiklet", "Kamp",
        "Yüzme", "Futbol", "Basketbol", "Tenis", "Yoga", "Dağcılık",
    ],
    "Kozmetik": [
        "Makyaj", "Cilt Bakımı", "Saç Bakımı", "Parfüm",
        "Erkek Bakım", "Bebek & Çocuk", "Kişisel Bakım",
    ],
    "Kitap & Müzik": [
        "Roman", "Bilim Kurgu", "Tarih", "Biyografi", "Kişisel Gelişim",
        "Çocuk Kitapları", "Ders Kitabı", "Müzik CD", "Film DVD",
    ],
    "Gıda & İçecek": [
        "Atıştırmalık", "İçecek", "Kahvaltılık", "Bakliyat",
        "Baharat & Sos", "Tatlı & Çikolata", "Organik Ürünler",
    ],
    "Otomotiv": [
        "Lastik", "Akü", "Motor Yağı", "Araç Aksesuar",
        "Navigasyon", "Oto Ses Sistemi", "Araç Bakım",
    ],
}

ALL_SUBCATEGORIES = [
    sub for subs in PRODUCT_CATEGORIES.values() for sub in subs
]

# ---------------------------------------------------------------------------
# BRANDS
# ---------------------------------------------------------------------------
BRANDS = [
    "Arçelik", "Vestel", "Beko", "Bosch TR", "Karaca", "Arzum", "Fakir",
    "Sinbo", "Philips TR", "Lc Waikiki", "Defacto", "Koton", "Mavi",
    "Vakko", "Beymen", "Network", "Kiğılı", "Sarar", "Ramsey", "Tudors",
    "Çiçeksepeti", "Trendyol", "Hepsiburada", "Teknosa", "MediaMarkt TR",
    "Vatan Bilgisayar", "Migros", "Carrefour", "BİM", "A101", "ŞOK",
    "Gratis", "Watsons TR", "Rossmann TR", "Flormar", "Farmasi",
    "Bellona", "İstikbal", "Mondi", "Tepe Home", "Kelebek",
    "Doğtaş", "Yataş", "Lucas", "Goodyear TR", "Bridgestone TR",
    "Samsung TR", "Apple TR", "Huawei TR", "Xiaomi TR", "Lenovo TR",
]

# ---------------------------------------------------------------------------
# CORPORATE EMAIL DOMAINS (realistic fake Turkish companies)
# ---------------------------------------------------------------------------
COMPANY_DOMAINS = [
    "tefatech.com.tr", "deltasoft.com.tr", "novamed.com.tr",
    "atlasgroup.com.tr", "karateknik.com.tr", "zenginholding.com.tr",
    "promedya.com.tr", "innovasyonx.com", "digiturk24.com.tr",
    "ekomarket.com.tr", "smartlojistik.com.tr", "altinovaenerji.com.tr",
    "bosphorus.tech", "anatoliadigital.com", "istanbulfintech.com.tr",
    "turkdata.com.tr", "marmararetail.com.tr", "kapadokyasoft.com",
    "bogazicitech.com.tr", "anadoluglobal.com.tr", "akdenizbilisim.com.tr",
    "egegrubu.com.tr", "karadeniztech.com.tr", "trakya-dijital.com.tr",
    "silvertekno.com.tr", "goldenpazar.com.tr", "planinvest.com.tr",
    "netforce.com.tr", "pixelkod.com.tr", "veritaban.com.tr",
    "sigorta360.com.tr", "innolab.com.tr", "zirvetech.com.tr",
    "horizonmedia.com.tr", "startupistanbul.com", "turkcell-partner.com.tr",
    "yenimedya.com.tr", "megasoft.com.tr", "depomax.com.tr",
    "globalbridge.com.tr", "techizbilisim.com.tr", "bulutdepo.com.tr",
    "ultraveri.com.tr", "neocrm.com.tr", "iotplatform.com.tr",
    "datalab.istanbul", "mlops.com.tr",
]

# ---------------------------------------------------------------------------
# DEPARTMENTS & POSITIONS (name, min_salary, max_salary in TRY)
# ---------------------------------------------------------------------------
DEPARTMENTS = {
    "Yazılım Geliştirme": [
        ("Junior Yazılım Geliştirici", 25_000, 40_000),
        ("Yazılım Geliştirici", 40_000, 70_000),
        ("Kıdemli Yazılım Geliştirici", 70_000, 110_000),
        ("Teknik Lider", 100_000, 150_000),
        ("Yazılım Mimarı", 130_000, 180_000),
    ],
    "Veri Bilimi": [
        ("Veri Analisti", 30_000, 50_000),
        ("Veri Bilimcisi", 55_000, 90_000),
        ("Kıdemli Veri Bilimcisi", 85_000, 130_000),
        ("ML Mühendisi", 90_000, 140_000),
        ("Baş Veri Bilimcisi", 140_000, 200_000),
    ],
    "Ürün Yönetimi": [
        ("Ürün Analisti", 28_000, 45_000),
        ("Ürün Yöneticisi", 55_000, 90_000),
        ("Kıdemli Ürün Yöneticisi", 85_000, 130_000),
        ("Ürün Direktörü", 130_000, 190_000),
    ],
    "Pazarlama": [
        ("Pazarlama Uzmanı", 22_000, 38_000),
        ("Dijital Pazarlama Uzmanı", 28_000, 50_000),
        ("Pazarlama Müdürü", 50_000, 85_000),
        ("Pazarlama Direktörü", 85_000, 140_000),
    ],
    "Satış": [
        ("Satış Temsilcisi", 20_000, 35_000),
        ("Kıdemli Satış Temsilcisi", 32_000, 55_000),
        ("Satış Müdürü", 55_000, 95_000),
        ("Bölge Satış Direktörü", 90_000, 150_000),
    ],
    "İnsan Kaynakları": [
        ("İK Uzmanı", 22_000, 38_000),
        ("İK Müdürü", 45_000, 75_000),
        ("İK Direktörü", 75_000, 120_000),
        ("CHRO", 130_000, 200_000),
    ],
    "Finans": [
        ("Muhasebe Uzmanı", 25_000, 42_000),
        ("Mali Analist", 35_000, 60_000),
        ("CFO Yardımcısı", 70_000, 110_000),
        ("CFO", 130_000, 200_000),
    ],
    "Operasyon": [
        ("Operasyon Uzmanı", 22_000, 38_000),
        ("Lojistik Koordinatörü", 25_000, 42_000),
        ("Operasyon Müdürü", 50_000, 85_000),
        ("COO", 130_000, 200_000),
    ],
    "Müşteri Hizmetleri": [
        ("Müşteri Temsilcisi", 18_000, 28_000),
        ("Kıdemli Müşteri Temsilcisi", 25_000, 38_000),
        ("Müşteri Hizmetleri Müdürü", 45_000, 75_000),
    ],
    "Hukuk": [
        ("Hukuk Uzmanı", 45_000, 75_000),
        ("Avukat", 60_000, 100_000),
        ("Hukuk Müdürü", 90_000, 150_000),
        ("Genel Müdür Yardımcısı", 150_000, 220_000),
    ],
}

# ---------------------------------------------------------------------------
# SERVICES (for logs)
# ---------------------------------------------------------------------------
SERVICES = [
    "auth-service", "user-service", "order-service", "payment-service",
    "notification-service", "product-service", "cart-service",
    "search-service", "recommendation-service", "analytics-service",
    "gateway-api", "cdn-service", "cache-service", "scheduler-service",
    "email-service", "sms-service", "file-service", "report-service",
    "webhook-service", "audit-service",
]

# ---------------------------------------------------------------------------
# USER AGENTS
# ---------------------------------------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "python-requests/2.31.0",
    "okhttp/4.12.0",
    "axios/1.6.2",
    "curl/8.4.0",
    "PostmanRuntime/7.35.0",
]

# ---------------------------------------------------------------------------
# LOG MESSAGE TEMPLATES
# ---------------------------------------------------------------------------
LOG_MESSAGES = {
    "DEBUG": [
        "Cache miss for key '{key}' — fetching from DB",
        "Query executed in {ms}ms: SELECT * FROM {table}",
        "Connection pool size: {size}/{max}",
        "JWT token decoded successfully for user {user_id}",
        "Redis PING OK — latency {ms}ms",
        "Config reloaded from environment variables",
        "Incoming request: {method} {path}",
        "Rate limit counter incremented for IP {ip}: {count}/min",
        "Retry attempt {n}/3 for external API call",
        "Serializing response object ({bytes} bytes)",
    ],
    "INFO": [
        "User {user_id} logged in successfully",
        "Order {order_id} created for user {user_id}",
        "Payment of {amount} TRY processed for order {order_id}",
        "Email notification sent to {email}",
        "File uploaded: {filename} ({size} KB)",
        "Health check passed — all services operational",
        "Scheduled job '{job}' completed in {ms}ms",
        "User {user_id} updated profile settings",
        "Product {product_id} inventory updated: stock={stock}",
        "Session {session_id} started for user {user_id}",
        "API key {key} validated for client {client}",
        "Report generated: {report} ({rows} rows)",
        "Webhook delivered to {url} — status 200",
        "Cache warmed: {count} keys loaded",
        "Service started on port {port}",
    ],
    "WARNING": [
        "Slow query detected ({ms}ms): {query}",
        "Memory usage at {pct}% — approaching threshold",
        "Failed login attempt for user {email} from IP {ip}",
        "Deprecated API endpoint /v1/{path} called",
        "Rate limit approaching for user {user_id}: {count}/1000 req/hr",
        "External service {service} response time degraded: {ms}ms",
        "Disk usage at {pct}% on {mount}",
        "JWT token expiring soon for user {user_id} (in {min} minutes)",
        "Retry queue depth high: {count} pending jobs",
        "Certificate expires in {days} days for {domain}",
    ],
    "ERROR": [
        "Database connection failed: {error}",
        "Payment gateway timeout after {ms}ms for order {order_id}",
        "Failed to send email to {email}: {error}",
        "Unhandled exception in {service}: {error}",
        "File not found: {path}",
        "Invalid JSON payload in request body",
        "Authentication failed for API key {key}",
        "Order {order_id} processing failed — rolling back transaction",
        "Third-party API {api} returned 500 Internal Server Error",
        "Cache flush failed: {error}",
    ],
    "CRITICAL": [
        "Database cluster unreachable — all read replicas down",
        "Out of memory — killing worker process",
        "Security breach detected: {event} from IP {ip}",
        "Data corruption detected in table {table}",
        "Service {service} crash loop detected — 5 restarts in 2 minutes",
        "SSL certificate expired for {domain} — traffic blocked",
        "Disk full on {mount} — writes failing",
        "Master-slave replication lag critical: {lag}s",
    ],
}

# ---------------------------------------------------------------------------
# TRANSACTION CATEGORY DESCRIPTIONS
# ---------------------------------------------------------------------------
TRANSACTION_DESCRIPTIONS = {
    "market": [
        "Migros alışveriş", "CarrefourSA market alışverişi",
        "BİM market ödemesi", "A101 alışveriş", "ŞOK market",
        "Hakmar alışveriş", "Makromarket", "Macro Center",
        "Yiyecek alışverişi", "Gıda alışverişi", "Market ödemesi",
    ],
    "restaurant": [
        "Yemek Sepeti siparişi", "Getir yemek", "Trendyol Yemek",
        "McDonald's ödeme", "Burger King", "Pizza Hut Türkiye",
        "Sushi Bar ödemesi", "Kebap salonu", "Pide fırını ödemesi",
        "Restoran ödemesi", "Cafe & bistro", "Kahvaltı salonu",
    ],
    "transport": [
        "İETT biniş ücreti", "Metrobüs", "Marmaray", "Metro İstanbul",
        "Taxi ücreti", "BiTaksi ödemesi", "InDriver", "Uber TR",
        "Akbil yükleme", "İstanbulkart", "Benzin istasyonu",
        "Otoyol geçiş ücreti", "Park ücreti",
    ],
    "entertainment": [
        "Netflix abonelik", "Spotify Premium", "YouTube Premium",
        "BluTV abonelik", "Mubi abonelik", "Amazon Prime",
        "Sinema bileti", "Konser bileti", "Tiyatro bileti",
        "Steam oyun satın alma", "App Store", "Google Play",
    ],
    "health": [
        "Eczane ödemesi", "Doktor muayene ücreti", "Hastane ödeme",
        "Diş kliniği", "Optik muayene", "Fizik tedavi",
        "SGK katılım payı", "Özel sigorta ödemesi",
        "Vitamin & takviye gıda", "Medikal malzeme",
    ],
    "education": [
        "Udemy kurs satın alma", "Coursera abonelik",
        "Kitap satın alma", "Ders kitabı", "Online eğitim platformu",
        "Özel ders ücreti", "Dil okulu ödemesi", "ÖSYM başvuru ücreti",
        "Sertifika programı", "Okul kırtasiye",
    ],
    "giyim": [
        "Mavi alışveriş", "Zara giyim ödemesi", "LC Waikiki",
        "Koton mağaza", "Boyner alışveriş", "Defacto giyim",
        "Ayakkabı Dünyası", "Flo ayakkabı", "Giyim mağazası",
    ],
    "electronic": [
        "Teknosa alışveriş", "Vatan Bilgisayar", "MediaMarkt",
        "Hepsiburada Teknoloji", "Trendyol Elektronik", "Apple Store",
        "Telefon aksesuar", "Kulaklık satın alma",
    ],
    "other": [
        "Elektrik faturası", "Su faturası", "Doğalgaz faturası",
        "İnternet faturası", "Telefon faturası", "Kira ödemesi",
        "Sigorta ödemesi", "Kredi kartı borç ödemesi",
        "Banka havalesi", "Para transferi", "Çeşitli harcama",
    ],
}

ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]
ORDER_STATUS_WEIGHTS = [0.05, 0.10, 0.15, 0.55, 0.15]

PAYMENT_METHODS = [
    "Kredi Kartı", "Banka Kartı", "Havale/EFT",
    "Kapıda Ödeme", "Dijital Cüzdan", "BNPL",
]

CURRENCIES = ["TRY", "USD", "EUR"]
CURRENCY_WEIGHTS = [0.75, 0.15, 0.10]

TRANSACTION_TYPES = ["credit", "debit"]
TRANSACTION_TYPE_WEIGHTS = [0.30, 0.70]

GENDERS = ["Erkek", "Kadın"]
GENDER_WEIGHTS = [0.50, 0.50]
