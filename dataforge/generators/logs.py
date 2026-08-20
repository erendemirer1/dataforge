"""
Logs schema generator.
Produces realistic application log records with proper level distribution.

Level distribution:
  INFO     60%
  DEBUG    20%
  WARNING  15%
  ERROR     4%
  CRITICAL  1%
"""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from typing import Any

from .base import BaseGenerator
from ..utils import turkish_data as td

LOG_LEVELS = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
LOG_LEVEL_WEIGHTS = [0.60, 0.20, 0.15, 0.04, 0.01]

_HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
_PATHS = [
    '/api/v1/users', '/api/v1/orders', '/api/v1/products',
    '/api/v2/auth/login', '/api/v2/auth/logout', '/api/v1/payments',
    '/api/v1/cart', '/api/v1/search', '/api/v1/notifications',
    '/health', '/metrics', '/api/v1/reports',
]
_ERRORS = [
    'Connection refused', 'Timeout after 30000ms',
    'NullPointerException', 'OutOfMemoryError',
    'SocketException: broken pipe', 'DataIntegrityViolation',
]
_TABLES = ['users', 'orders', 'products', 'transactions', 'sessions', 'logs']
_JOBS = [
    'nightly-report', 'cleanup-expired-sessions',
    'sync-inventory', 'send-digest-emails', 'reindex-search',
]
_DOMAINS = [
    'example.com', 'api.myapp.com', 'cdn.myapp.com', 'auth.myapp.com'
]


def _render(template: str, rng: Any) -> str:
    """Fill in placeholder variables in a log message template."""
    ip = (f"{rng.randint(1, 254)}.{rng.randint(0, 255)}"
          f".{rng.randint(0, 255)}.{rng.randint(1, 254)}")
    replacements = {
        '{key}': f"cache:user:{rng.randint(1000, 9999)}",
        '{ms}': str(rng.randint(1, 5000)),
        '{table}': rng.choice(_TABLES),
        '{size}': str(rng.randint(5, 50)),
        '{max}': str(rng.randint(50, 200)),
        '{user_id}': str(rng.randint(1, 100_000)),
        '{order_id}': f"ORD-{rng.randint(1, 999_999):08d}",
        '{amount}': str(round(rng.uniform(10, 5000), 2)),
        '{email}': f"user{rng.randint(1, 9999)}@example.com",
        '{filename}': f"file_{rng.randint(1, 9999)}.pdf",
        '{job}': rng.choice(_JOBS),
        '{product_id}': str(rng.randint(1, 10_000)),
        '{stock}': str(rng.randint(0, 1000)),
        '{session_id}': str(uuid.UUID(int=rng.getrandbits(128))),
        '{key2}': ''.join([rng.choice('ABCDEF0123456789') for _ in range(16)]),
        '{key}': f"cache:user:{rng.randint(1000, 9999)}",
        '{client}': f"client-{rng.randint(1, 999)}",
        '{report}': rng.choice(['monthly-sales', 'user-activity', 'inventory']),
        '{rows}': str(rng.randint(100, 1_000_000)),
        '{url}': f"https://hooks.example.com/{rng.randint(1, 9999)}",
        '{count}': str(rng.randint(100, 100_000)),
        '{port}': str(rng.randint(3000, 9999)),
        '{query}': 'SELECT * FROM orders WHERE status=pending',
        '{pct}': str(rng.randint(70, 99)),
        '{ip}': ip,
        '{path}': rng.choice(_PATHS),
        '{service}': rng.choice(td.SERVICES),
        '{mount}': rng.choice(['/data', '/var', '/tmp', '/home']),
        '{min}': str(rng.randint(1, 59)),
        '{days}': str(rng.randint(1, 30)),
        '{domain}': rng.choice(_DOMAINS),
        '{error}': rng.choice(_ERRORS),
        '{method}': rng.choice(_HTTP_METHODS),
        '{n}': str(rng.randint(1, 3)),
        '{bytes}': str(rng.randint(100, 100_000)),
        '{event}': 'brute-force-login',
        '{api}': rng.choice(['stripe', 'sendgrid', 'twilio', 's3']),
        '{lag}': str(rng.randint(10, 600)),
    }
    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)
    return result


class LogsGenerator(BaseGenerator):
    """Generator for the 'logs' schema."""

    def generate_one(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[override]
        record_id: int = kwargs.get('record_id', self.randint(1, 999_999))

        level = self.choices(LOG_LEVELS, weights=LOG_LEVEL_WEIGHTS)[0]
        templates = td.LOG_MESSAGES[level]
        template = self.choice(templates)
        message = _render(template, self.rng)

        service = self.choice(td.SERVICES)
        ip = (
            f"{self.randint(1, 254)}.{self.randint(0, 255)}"
            f".{self.randint(0, 255)}.{self.randint(1, 254)}"
        )
        user_agent = self.choice(td.USER_AGENTS)
        request_id = str(uuid.uuid4())
        duration_ms = self.randint(1, 10_000)

        ts_days_ago = self.randint(0, 90)
        ts_secs_ago = self.randint(0, 86_400)
        timestamp = datetime.now() - timedelta(days=ts_days_ago, seconds=ts_secs_ago)

        return {
            'id': record_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'level': level,
            'service': service,
            'message': message,
            'ip_address': ip,
            'user_agent': user_agent,
            'request_id': request_id,
            'duration_ms': duration_ms,
        }

    def generate(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        return [self.generate_one(record_id=i) for i in range(1, count + 1)]
