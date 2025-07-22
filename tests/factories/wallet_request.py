from decimal import Decimal

import factory

from db.models.wallet import WalletRequest
from enums.network import NetworkEnum

from .base import AsyncSQLAlchemyModelFactory, fake


def generate_tron_address():
    """Генерирует валидный TRON адрес для тестов"""
    # Генерируем случайный TRON адрес (34 символа, начинается с 'T')
    import secrets
    import string

    base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    # Генерируем 33 случайных символа из base58 и добавляем 'T' в начало
    random_part = "".join(secrets.choice(base58_chars) for _ in range(33))
    return f"T{random_part}"


class WalletRequestFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = WalletRequest

    network = NetworkEnum.TRON
    address = factory.LazyFunction(generate_tron_address)

    balance = factory.LazyAttribute(
        lambda obj: Decimal(fake.random_int(min=0, max=1000000)) / Decimal(1000)
    )
    bandwidth = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=100000))
    energy = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=100000))
