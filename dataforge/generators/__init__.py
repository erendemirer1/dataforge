from .users import UsersGenerator
from .products import ProductsGenerator
from .orders import OrdersGenerator
from .transactions import TransactionsGenerator
from .employees import EmployeesGenerator
from .logs import LogsGenerator

GENERATOR_MAP: dict[str, type] = {
    'users': UsersGenerator,
    'products': ProductsGenerator,
    'orders': OrdersGenerator,
    'transactions': TransactionsGenerator,
    'employees': EmployeesGenerator,
    'logs': LogsGenerator,
}

__all__ = [
    'UsersGenerator', 'ProductsGenerator', 'OrdersGenerator',
    'TransactionsGenerator', 'EmployeesGenerator', 'LogsGenerator',
    'GENERATOR_MAP',
]
