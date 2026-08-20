import random
from typing import Dict, Any, Optional

import dataforge.ml.reference_stats as stats

class CausalProfileExtender:
    def extend(self, profile: Dict[str, Any], rng: random.Random) -> Dict[str, Any]:
        p = profile.copy()
        
        age = p.get('age', 30)
        gender = p.get('gender', 'M')
        city = p.get('city', 'İstanbul')
        monthly_income = p.get('monthly_income', 30000)
        income_segment = p.get('income_segment', 'orta_gelir')
        education_level = p.get('education_level', 'lise')
        marital_status = p.get('marital_status', 'Bekar')
        
        # Age group
        if age >= 65:
            age_group = '65+'
        elif age >= 45:
            age_group = '45-64'
        elif age >= 25:
            age_group = '25-44'
        else:
            age_group = '18-24'

        # === KİŞİSEL ===
        p['birth_city'] = city if rng.random() > 0.3 else rng.choice(list(stats.CITY_PLATES.keys()))
        p['nationality'] = 'TC'
        
        if city in ['Diyarbakır', 'Van']:
            p['ethnicity'] = rng.choices(['Kürt', 'Türk', 'Arap'], weights=[0.55, 0.40, 0.05])[0]
        else:
            p['ethnicity'] = rng.choices(['Türk', 'Kürt', 'Göçmen'], weights=[0.85, 0.10, 0.05])[0]
            
        p['mother_tongue'] = 'Kürtçe' if p['ethnicity'] == 'Kürt' else 'Türkçe'
        
        # === EĞİTİM DERİNLİĞİ ===
        edu_probs = stats.EDUCATION_BY_AGE.get(age_group, stats.EDUCATION_BY_AGE['25-44'])
        p['education_level_detail'] = rng.choices(list(edu_probs.keys()), weights=list(edu_probs.values()))[0]
        
        if p['education_level_detail'] in ['lise', 'universite', 'lisansustu']:
            if income_segment == 'ust_gelir':
                p['high_school_type'] = rng.choices(['Özel Lise', 'Anadolu Lisesi', 'Fen Lisesi'], weights=[0.6, 0.3, 0.1])[0]
            else:
                p['high_school_type'] = rng.choices(['Devlet Lisesi', 'Meslek Lisesi', 'Anadolu Lisesi'], weights=[0.5, 0.3, 0.2])[0]
        else:
            p['high_school_type'] = None
            
        if p['education_level_detail'] in ['universite', 'lisansustu']:
            p['university_name'] = rng.choice(stats.UNIVERSITIES)
            p['foreign_language'] = rng.choices(['İngilizce', 'Almanca', 'Fransızca'], weights=[0.8, 0.15, 0.05])[0]
            p['foreign_language_level'] = rng.choices(['B1', 'B2', 'C1', 'C2'], weights=[0.4, 0.3, 0.2, 0.1])[0]
        else:
            p['university_name'] = None
            p['foreign_language'] = rng.choices(['İngilizce', 'Yok'], weights=[0.1, 0.9])[0]
            p['foreign_language_level'] = 'A1' if p['foreign_language'] != 'Yok' else 'Yok'
            
        p['has_master'] = p['education_level_detail'] == 'lisansustu'
        p['has_phd'] = p['has_master'] and rng.random() > 0.8
        
        # === ÇALIŞMA HAYATI ===
        if age < 24 and p['education_level_detail'] in ['universite', 'lisansustu'] and rng.random() > 0.5:
            p['employment_status_detail'] = 'Öğrenci'
        elif age > 60 and rng.random() > 0.7:
            p['employment_status_detail'] = 'Emekli'
        elif gender == 'F' and rng.random() > 0.6:
            p['employment_status_detail'] = 'Ev Hanımı'
        else:
            p['employment_status_detail'] = rng.choices(['Tam Zamanlı', 'Yarı Zamanlı', 'Serbest Meslek', 'İşsiz'], weights=[0.7, 0.1, 0.15, 0.05])[0]

        p['company_size'] = rng.choices(['Mikro', 'Küçük', 'Orta', 'Büyük', 'Kamu'], weights=[0.3, 0.2, 0.2, 0.15, 0.15])[0]
        p['work_location'] = rng.choices(['Ofis', 'Uzaktan', 'Hibrit', 'Saha', 'Fabrika'], weights=[0.4, 0.1, 0.2, 0.15, 0.15])[0]
        
        exp_years = max(0, age - 22) if p['education_level_detail'] in ['universite', 'lisansustu'] else max(0, age - 18)
        p['work_experience_years'] = exp_years
        p['job_change_count'] = exp_years // 4
        
        p['has_side_income'] = income_segment == 'ust_gelir' and rng.random() > 0.5
        p['side_income_tl'] = round(monthly_income * rng.uniform(0.1, 0.5), 2) if p['has_side_income'] else None
        p['annual_bonus_tl'] = round(monthly_income * rng.uniform(0, 2), 2) if p['employment_status_detail'] == 'Tam Zamanlı' else 0.0

        # === GELİR DERİNLİĞİ ===
        p['gross_salary_tl'] = round(monthly_income / 0.7, 2)
        p['net_salary_tl'] = monthly_income
        p['sgk_premium_base'] = min(p['gross_salary_tl'], stats.MINIMUM_WAGE_2025 * 7.5)
        
        tax_bracket = '15%'
        annual_gross = p['gross_salary_tl'] * 12
        for limit, rate in stats.TAX_BRACKETS_2025:
            if annual_gross < limit:
                tax_bracket = f"{int(rate*100)}%"
                break
        p['tax_bracket'] = tax_bracket
        
        p['monthly_fixed_expenses_tl'] = round(monthly_income * rng.uniform(0.4, 0.7), 2)
        p['monthly_discretionary_tl'] = round(monthly_income - p['monthly_fixed_expenses_tl'], 2)

        # === FİNANSAL DERİNLİK ===
        multiplier = rng.uniform(0, 5)
        p['savings_tl'] = round(monthly_income * multiplier, 2)
        p['gold_holdings_gram'] = round(rng.uniform(0, 100), 2) if income_segment != 'alt_gelir' else round(rng.uniform(0, 20), 2)
        p['stock_portfolio_tl'] = round(monthly_income * rng.uniform(0, 10), 2) if p['education_level_detail'] in ['universite', 'lisansustu'] else 0.0
        p['crypto_holdings_tl'] = round(monthly_income * rng.uniform(0, 5), 2) if age < 40 and p['education_level_detail'] in ['universite', 'lisansustu'] else 0.0
        p['forex_savings_usd'] = round(monthly_income * rng.uniform(0, 20), 2) if income_segment == 'ust_gelir' else 0.0
        
        p['investment_risk_tolerance'] = rng.choices(['Düşük', 'Orta', 'Yüksek'], weights=[0.5, 0.3, 0.2])[0] if age > 40 else rng.choices(['Düşük', 'Orta', 'Yüksek'], weights=[0.2, 0.4, 0.4])[0]
        
        p['bank_count'] = rng.randint(1, 2) if income_segment == 'alt_gelir' else rng.randint(2, 5)
        p['primary_bank'] = rng.choice(['Ziraat', 'Halkbank', 'VakıfBank']) if income_segment == 'alt_gelir' else rng.choice(['Garanti', 'İş Bankası', 'Yapı Kredi', 'Akbank'])
        p['has_investment_account'] = income_segment != 'alt_gelir'
        
        # === KONUT DERİNLİĞİ ===
        p['housing_type_detail'] = rng.choices(['Daire', 'Müstakil Ev', 'Gecekondu', 'Aile Yanı'], weights=[0.7, 0.1, 0.05, 0.15])[0]
        p['housing_sqm'] = rng.randint(60, 100) if income_segment == 'alt_gelir' else rng.randint(90, 250)
        p['room_count'] = '2+1' if p['housing_sqm'] < 100 else ('3+1' if p['housing_sqm'] < 150 else '4+1')
        p['building_age_years'] = rng.randint(0, 30)
        p['floor_number'] = rng.randint(1, 10) if p['housing_type_detail'] == 'Daire' else None
        p['has_balcony'] = rng.random() > 0.2
        p['has_garden'] = p['housing_type_detail'] == 'Müstakil Ev'
        p['has_parking'] = income_segment != 'alt_gelir'
        p['heating_type'] = 'Doğalgaz' if city in ['İstanbul', 'Ankara', 'İzmir', 'Bursa'] else rng.choice(['Kombi', 'Soba', 'Klima'])
        
        is_homeowner = rng.random() < (stats.HOMEOWNER_RATE_IST if city == 'İstanbul' else stats.HOMEOWNER_RATE_GENERAL)
        
        if not is_homeowner:
            p['monthly_rent_tl'] = round(rng.uniform(10000, 50000), 2)
            p['mortgage_debt_tl'] = None
        else:
            p['monthly_rent_tl'] = None
            p['mortgage_debt_tl'] = round(rng.uniform(500000, 3000000), 2) if age < 45 and rng.random() > 0.5 else None
            
        p['neighborhood_safety_score'] = rng.randint(4, 7) if income_segment == 'alt_gelir' else rng.randint(7, 10)

        # === MOBİLİTE DERİNLİĞİ ===
        p['vehicle_count'] = 0 if income_segment == 'alt_gelir' else rng.randint(1, 2)
        if p['vehicle_count'] > 0:
            p['vehicle_year'] = rng.randint(2005, 2015) if income_segment != 'ust_gelir' else rng.randint(2018, 2024)
            p['vehicle_fuel_type'] = rng.choice(['Benzin', 'Dizel', 'Elektrik', 'LPG', 'Hibrit'])
            p['vehicle_insurance_type'] = 'Trafik' if p['vehicle_year'] < 2010 else 'Kasko'
            p['plate_city_code'] = stats.CITY_PLATES.get(city, '34')
            p['daily_commute_method'] = 'Özel Araç'
        else:
            p['vehicle_year'] = None
            p['vehicle_fuel_type'] = None
            p['vehicle_insurance_type'] = None
            p['plate_city_code'] = None
            p['daily_commute_method'] = rng.choice(['Otobüs', 'Metro', 'Yürüme'])

        p['commute_time_minutes'] = rng.randint(15, 90)
        p['annual_km_driven'] = rng.randint(5000, 30000) if p['vehicle_count'] > 0 else None
        p['has_public_transport_card'] = True
        
        # === SAĞLIK DERİNLİĞİ ===
        p['bmi_value'] = round(rng.uniform(18.5, 35.0), 1)
        if p['bmi_value'] < 18.5: p['bmi_category'] = 'Zayıf'
        elif p['bmi_value'] < 25: p['bmi_category'] = 'Normal'
        elif p['bmi_value'] < 30: p['bmi_category'] = 'Kilolu'
        else: p['bmi_category'] = 'Obez'
        
        smoker_prob = stats.SMOKING_PREVALENCE.get(gender, 0.2)
        is_smoker = rng.random() < smoker_prob
        p['smoker_detail'] = 'İçiyor' if is_smoker else rng.choice(['Hiç içmedi', 'Eski içici'])
        p['cigarettes_per_day'] = rng.randint(5, 20) if is_smoker else None
        
        p['alcohol_user'] = rng.random() > 0.7 if city in ['Diyarbakır', 'Van', 'Erzurum'] else rng.random() > 0.4
        p['exercise_frequency'] = rng.choice(['Hiç', 'Ayda 1-3', 'Haftada 1-2', 'Haftada 3+', 'Her gün'])
        p['diet_type'] = 'Omnivore'
        
        has_chronic = rng.random() < stats.CHRONIC_DISEASE_PROBS.get(age_group, 0.1)
        p['chronic_disease_name'] = rng.choice(stats.CHRONIC_DISEASES) if has_chronic else None
        p['chronic_medications'] = ['İlaç A', 'İlaç B'] if has_chronic else []
        p['private_health_insurance'] = income_segment == 'ust_gelir' and p['employment_status_detail'] == 'Tam Zamanlı'
        p['last_doctor_visit_months'] = rng.randint(1, 12)
        p['disability_status'] = rng.choices(['Yok', 'Hafif', 'Orta', 'Ağır'], weights=[0.9, 0.05, 0.03, 0.02])[0]
        
        # === DİJİTAL YAŞAM DERİNLİĞİ ===
        p['phone_brand'] = rng.choices(['Apple', 'Samsung', 'Xiaomi', 'Oppo'], weights=[0.3, 0.4, 0.2, 0.1])[0]
        p['internet_speed_mbps'] = rng.choice([25, 50, 100, 200, 500, 1000])
        p['monthly_phone_bill_tl'] = round(rng.uniform(200, 1000), 2)
        p['streaming_platform_count'] = rng.randint(0, 4)
        p['social_media_platforms'] = stats.SOCIAL_MEDIA_BY_AGE.get(age_group, [])
        p['social_media_daily_hours'] = round(rng.uniform(1, 8), 1)
        p['gaming_habit'] = rng.choice(['Yok', 'Casual', 'Haftalık', 'Günlük'])
        p['e_commerce_platforms'] = ['Trendyol', 'Hepsiburada']
        p['food_delivery_apps'] = ['Yemeksepeti', 'Getir'] if age < 45 else []
        p['online_shopping_monthly_tl'] = round(rng.uniform(500, 5000), 2)
        p['has_crypto_wallet'] = age < 40 and p['education_level_detail'] in ['universite', 'lisansustu']
        p['uses_contactless_payment'] = True
        
        # === YAŞAM TARZI ===
        p['vacation_frequency_per_year'] = 0 if income_segment == 'alt_gelir' else rng.randint(1, 3)
        p['vacation_type'] = rng.choice(stats.VACATION_TYPES.get(income_segment, ['Tatil yok']))
        p['restaurant_frequency'] = rng.choice(stats.RESTAURANT_FREQ.get(income_segment, ['Hiç']))
        p['supermarket_preference'] = rng.choice(stats.SUPERMARKET_BY_INCOME.get(income_segment, ['BİM']))
        p['reading_habit'] = rng.choice(['Hiç', 'Gazete', 'Kitap', 'Blog'])
        p['gym_membership'] = p['exercise_frequency'] in ['Haftada 3+', 'Her gün']
        p['cultural_activity_freq'] = rng.choice(['Hiç', 'Yılda 1-2', 'Ayda 1', 'Haftada 1'])
        p['pet_ownership'] = rng.random() > 0.8
        
        # === SOSYOPOLİTİK ===
        p['religiosity_level'] = rng.choice(stats.RELIGIOSITY_LEVELS)

        return p
