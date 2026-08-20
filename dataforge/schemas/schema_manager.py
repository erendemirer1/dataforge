"""
Schema manager: built-in schemas, custom schema loading, YAML multi-schema.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any

import yaml

BUILTIN_SCHEMAS: dict[str, dict[str, Any]] = {
    'users': {
        'name': 'users',
        'description': '100+ Parametreli Kapsamlı Türk Vatandaşı Dijital İkizi (TÜİK, SGK, BDDK, KKB, BTK, Causal DAG)',
        'fields': [
            'id', 'first_name', 'last_name', 'email', 'phone', 'birthdate', 'age', 'gender', 'tckn', 'blood_type',
            'city', 'district', 'neighborhood', 'postal_code', 'address', 'district_archetype',
            'occupation', 'education_level', 'education_level_detail', 'high_school_type', 'university_name', 'foreign_language',
            'income_segment', 'income_segment_label', 'monthly_income', 'gross_salary_tl', 'net_salary_tl', 'tax_bracket',
            'marital_status', 'children_count', 'household_size', 'housing_status', 'housing_type_detail', 'housing_sqm', 'room_count', 'heating_type',
            'findeks_credit_score', 'credit_score_rating', 'credit_card_limit', 'savings_tl', 'gold_holdings_gram', 'stock_portfolio_tl', 'crypto_holdings_tl',
            'driving_license', 'vehicle_ownership', 'vehicle_count', 'vehicle_model', 'vehicle_fuel_type', 'daily_commute_method',
            'smartphone_model', 'phone_brand', 'operating_system', 'gsm_operator', 'monthly_data_gb', 'internet_speed_mbps', 'digital_subscriptions',
            'sgk_category', 'health_insurance', 'bmi_value', 'bmi_category', 'smoker_detail', 'supermarket_preference', 'vacation_type',
            'created_at',
        ],
    },
    'products': {
        'name': 'products',
        'description': 'Türk pazar yeri ürün katalogu',
        'fields': [
            'id', 'name', 'category', 'subcategory', 'price',
            'discount_price', 'stock', 'sku', 'brand',
            'description', 'rating', 'review_count', 'created_at',
        ],
    },
    'orders': {
        'name': 'orders',
        'description': 'E-ticaret siparişleri (user_id / product_id referanslı)',
        'fields': [
            'id', 'order_number', 'user_id', 'product_id', 'quantity',
            'unit_price', 'total_price', 'status', 'payment_method',
            'shipping_address', 'created_at', 'updated_at',
        ],
    },
    'transactions': {
        'name': 'transactions',
        'description': 'Finansal işlemler (TRY/USD/EUR, kategori bazlı)',
        'fields': [
            'id', 'transaction_id', 'user_id', 'amount', 'currency',
            'type', 'category', 'description', 'balance_after', 'created_at',
        ],
    },
    'employees': {
        'name': 'employees',
        'description': 'Kurumsal çalışan kayıtları (departman, pozisyon, maaş)',
        'fields': [
            'id', 'first_name', 'last_name', 'email', 'department',
            'position', 'salary', 'hire_date', 'manager_id', 'phone', 'city',
        ],
    },
    'logs': {
        'name': 'logs',
        'description': 'Uygulama log kayıtları (gerçekçi seviye dağılımı)',
        'fields': [
            'id', 'timestamp', 'level', 'service', 'message',
            'ip_address', 'user_agent', 'request_id', 'duration_ms',
        ],
    },
}


def list_schemas() -> list[dict[str, Any]]:
    """Return metadata for all built-in schemas."""
    return list(BUILTIN_SCHEMAS.values())


def get_schema(name: str) -> dict[str, Any] | None:
    """Return a built-in schema by name, or None if not found."""
    return BUILTIN_SCHEMAS.get(name)


def load_yaml_schema(path: Path) -> dict[str, Any]:
    """Load a YAML schema file.

    Supports two formats:
    1. Multi-schema with referential integrity:
       relations:
         - users: 1000
         - orders: 5000
    2. Custom single-schema definition.
    """
    with open(path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data


def is_multi_schema(data: dict[str, Any]) -> bool:
    """Check if a loaded YAML is a multi-schema relations file."""
    return 'relations' in data


def parse_relations(data: dict[str, Any]) -> list[tuple[str, int]]:
    """Parse the relations list from a multi-schema YAML.

    Returns a list of (schema_name, count) tuples in order.
    """
    relations = []
    for item in data.get('relations', []):
        if isinstance(item, dict):
            for schema_name, count in item.items():
                relations.append((str(schema_name), int(count)))
    return relations
