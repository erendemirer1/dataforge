"""
Tests for all DataForge generators.
"""
import pytest
from dataforge.generators import (
    UsersGenerator,
    ProductsGenerator,
    OrdersGenerator,
    TransactionsGenerator,
    EmployeesGenerator,
    LogsGenerator,
    GENERATOR_MAP,
)
from dataforge.utils.tckn import is_valid_tckn


# ---------------------------------------------------------------------------
# UsersGenerator
# ---------------------------------------------------------------------------

class TestUsersGenerator:
    def setup_method(self):
        self.gen = UsersGenerator(seed=42)

    def test_generate_one(self):
        record = self.gen.generate_one(record_id=1)
        required = ['id', 'first_name', 'last_name', 'email', 'phone',
                    'birthdate', 'age', 'gender', 'tckn', 'city', 'address', 'created_at']
        for key in required:
            assert key in record, f"Missing key: {key}"

    def test_tckn_validity(self):
        for i in range(20):
            record = self.gen.generate_one(record_id=i + 1)
            assert is_valid_tckn(record['tckn']), f"Invalid TCKN: {record['tckn']}"

    def test_age_birthdate_consistency(self):
        from datetime import date
        for _ in range(20):
            record = self.gen.generate_one(record_id=1)
            age = record['age']
            birth_year = int(record['birthdate'][:4])
            current_year = date.today().year
            computed_age = current_year - birth_year
            # Allow 1 year tolerance for birthday not yet reached
            assert abs(computed_age - age) <= 1, (
                f"Age mismatch: age={age}, birthdate={record['birthdate']}"
            )

    def test_email_contains_at(self):
        for _ in range(20):
            record = self.gen.generate_one(record_id=1)
            assert '@' in record['email']

    def test_phone_format(self):
        for _ in range(20):
            record = self.gen.generate_one(record_id=1)
            phone = record['phone']
            assert phone.startswith('0'), f"Phone doesn't start with 0: {phone}"

    def test_gender_values(self):
        genders = set()
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            genders.add(record['gender'])
        assert 'Erkek' in genders or 'Kadın' in genders

    def test_generate_count(self):
        records = self.gen.generate(10)
        assert len(records) == 10

    def test_ids_sequential(self):
        records = [self.gen.generate_one(record_id=i + 1) for i in range(5)]
        ids = [r['id'] for r in records]
        assert ids == [1, 2, 3, 4, 5]

    def test_address_city_consistency(self):
        for i in range(25):
            record = self.gen.generate_one(record_id=i + 1)
            assert record['city'] in record['address'], (
                f"City {record['city']} not found in address: {record['address']}"
            )
            assert "Mah." in record['address']
            assert "/" in record['address']


# ---------------------------------------------------------------------------
# ProductsGenerator
# ---------------------------------------------------------------------------

class TestProductsGenerator:
    def setup_method(self):
        self.gen = ProductsGenerator(seed=42)

    def test_generate_one(self):
        record = self.gen.generate_one(record_id=1)
        required = ['id', 'name', 'category', 'subcategory', 'price',
                    'discount_price', 'stock', 'sku', 'brand',
                    'description', 'rating', 'review_count', 'created_at']
        for key in required:
            assert key in record

    def test_discount_less_than_price(self):
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            assert record['discount_price'] < record['price'], (
                f"discount_price {record['discount_price']} >= price {record['price']}"
            )

    def test_rating_range(self):
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            assert 1.0 <= record['rating'] <= 5.0

    def test_sku_format(self):
        for i in range(20):
            record = self.gen.generate_one(record_id=i + 1)
            assert '-' in record['sku']

    def test_subcategory_belongs_to_category(self):
        from dataforge.utils.turkish_data import PRODUCT_CATEGORIES
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            cat = record['category']
            subcat = record['subcategory']
            assert cat in PRODUCT_CATEGORIES
            assert subcat in PRODUCT_CATEGORIES[cat], (
                f"{subcat} not in {cat}: {PRODUCT_CATEGORIES[cat]}"
            )

    def test_generate_count(self):
        records = self.gen.generate(25)
        assert len(records) == 25


# ---------------------------------------------------------------------------
# OrdersGenerator
# ---------------------------------------------------------------------------

class TestOrdersGenerator:
    def setup_method(self):
        self.gen = OrdersGenerator(seed=42)

    def test_generate_one(self):
        record = self.gen.generate_one(record_id=1)
        required = ['id', 'order_number', 'user_id', 'product_id', 'quantity',
                    'unit_price', 'total_price', 'status', 'payment_method',
                    'shipping_address', 'created_at', 'updated_at']
        for key in required:
            assert key in record

    def test_total_price_consistency(self):
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            expected = round(record['quantity'] * record['unit_price'], 2)
            assert abs(record['total_price'] - expected) < 0.02, (
                f"total_price {record['total_price']} != {expected}"
            )

    def test_updated_at_after_created_at(self):
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            created = record['created_at']
            updated = record['updated_at']
            assert updated >= created, (
                f"updated_at {updated} < created_at {created}"
            )

    def test_status_valid(self):
        valid_statuses = {'pending', 'processing', 'shipped', 'delivered', 'cancelled'}
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            assert record['status'] in valid_statuses

    def test_referential_integrity(self):
        user_ids = [10, 20, 30, 40, 50]
        product_ids = [100, 200, 300]
        records = self.gen.generate(100, user_ids=user_ids, product_ids=product_ids)
        for r in records:
            assert r['user_id'] in user_ids
            assert r['product_id'] in product_ids


# ---------------------------------------------------------------------------
# TransactionsGenerator
# ---------------------------------------------------------------------------

class TestTransactionsGenerator:
    def setup_method(self):
        self.gen = TransactionsGenerator(seed=42)

    def test_generate_one(self):
        record = self.gen.generate_one(record_id=1)
        required = ['id', 'transaction_id', 'user_id', 'amount', 'currency',
                    'type', 'category', 'description', 'balance_after', 'created_at']
        for key in required:
            assert key in record

    def test_uuid_format(self):
        import uuid
        for i in range(20):
            record = self.gen.generate_one(record_id=i + 1)
            tid = record['transaction_id']
            # UUID-like format check
            assert len(tid) == 36 or '-' in tid

    def test_currency_valid(self):
        valid = {'TRY', 'USD', 'EUR'}
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            assert record['currency'] in valid

    def test_type_valid(self):
        valid = {'credit', 'debit'}
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            assert record['type'] in valid

    def test_referential_integrity(self):
        user_ids = [1, 2, 3, 4, 5]
        records = self.gen.generate(50, user_ids=user_ids)
        for r in records:
            assert r['user_id'] in user_ids

    def test_description_matches_category(self):
        from dataforge.utils.turkish_data import TRANSACTION_DESCRIPTIONS
        for i in range(50):
            record = self.gen.generate_one(record_id=i + 1)
            cat = record['category']
            desc = record['description']
            assert cat in TRANSACTION_DESCRIPTIONS
            assert desc in TRANSACTION_DESCRIPTIONS[cat]


# ---------------------------------------------------------------------------
# EmployeesGenerator
# ---------------------------------------------------------------------------

class TestEmployeesGenerator:
    def setup_method(self):
        self.gen = EmployeesGenerator(seed=42)

    def test_generate_one(self):
        record = self.gen.generate_one(record_id=1)
        required = ['id', 'first_name', 'last_name', 'email', 'department',
                    'position', 'salary', 'hire_date', 'manager_id', 'phone', 'city']
        for key in required:
            assert key in record

    def test_email_is_corporate(self):
        from dataforge.utils.turkish_data import COMPANY_DOMAINS
        for i in range(20):
            record = self.gen.generate_one(record_id=i + 1)
            domain = record['email'].split('@')[-1]
            assert domain in COMPANY_DOMAINS

    def test_salary_in_range(self):
        from dataforge.utils.turkish_data import DEPARTMENTS
        for i in range(30):
            record = self.gen.generate_one(record_id=i + 1)
            dept = record['department']
            position = record['position']
            salary = record['salary']
            positions = DEPARTMENTS[dept]
            for pos_name, sal_min, sal_max in positions:
                if pos_name == position:
                    assert sal_min <= salary <= sal_max, (
                        f"Salary {salary} out of range [{sal_min}, {sal_max}]"
                    )
                    break

    def test_manager_id_referential(self):
        records = self.gen.generate(20)
        all_ids = set(r['id'] for r in records)
        for r in records:
            if r['manager_id'] is not None:
                assert r['manager_id'] in all_ids or r['manager_id'] < r['id']


# ---------------------------------------------------------------------------
# LogsGenerator
# ---------------------------------------------------------------------------

class TestLogsGenerator:
    def setup_method(self):
        self.gen = LogsGenerator(seed=42)

    def test_generate_one(self):
        record = self.gen.generate_one(record_id=1)
        required = ['id', 'timestamp', 'level', 'service', 'message',
                    'ip_address', 'user_agent', 'request_id', 'duration_ms']
        for key in required:
            assert key in record

    def test_level_valid(self):
        valid = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        for i in range(100):
            record = self.gen.generate_one(record_id=i + 1)
            assert record['level'] in valid

    def test_level_distribution(self):
        records = self.gen.generate(1000)
        level_counts: dict[str, int] = {}
        for r in records:
            level_counts[r['level']] = level_counts.get(r['level'], 0) + 1
        # INFO should be most common
        assert level_counts.get('INFO', 0) > level_counts.get('ERROR', 0)
        assert level_counts.get('INFO', 0) > level_counts.get('CRITICAL', 0)

    def test_ip_format(self):
        for i in range(20):
            record = self.gen.generate_one(record_id=i + 1)
            parts = record['ip_address'].split('.')
            assert len(parts) == 4
            for part in parts:
                assert part.isdigit()

    def test_request_id_uuid_format(self):
        for i in range(20):
            record = self.gen.generate_one(record_id=i + 1)
            assert '-' in record['request_id']

    def test_generate_count(self):
        records = self.gen.generate(50)
        assert len(records) == 50


# ---------------------------------------------------------------------------
# GENERATOR_MAP
# ---------------------------------------------------------------------------

class TestGeneratorMap:
    def test_all_schemas_present(self):
        expected = {'users', 'products', 'orders', 'transactions', 'employees', 'logs'}
        assert expected == set(GENERATOR_MAP.keys())

    def test_all_generators_instantiable(self):
        for name, cls in GENERATOR_MAP.items():
            gen = cls(seed=0)
            record = gen.generate_one(record_id=1)
            assert isinstance(record, dict), f"{name} generator returned non-dict"
