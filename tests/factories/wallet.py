import secrets
from decimal import Decimal

import factory

from db.models.wallet import Wallet
from enums.network import NetworkEnum

from .base import AsyncSQLAlchemyModelFactory, fake


def generate_tron_address() -> str:
    return "T" + "".join(
        secrets.choice("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
        for _ in range(33)
    )


class WalletFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Wallet

    network = NetworkEnum.TRON
    address = factory.LazyFunction(generate_tron_address)

    balance = factory.LazyAttribute(
        lambda obj: Decimal(fake.random_int(min=0, max=1000000)) / Decimal(1000)
    )
    bandwidth = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=100000))
    energy = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=100000))
