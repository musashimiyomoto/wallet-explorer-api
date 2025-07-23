import secrets
from decimal import Decimal

from factory.declarations import LazyAttribute, LazyFunction

from db.models.wallet import Wallet
from enums.network import NetworkEnum

from .base import AsyncSQLAlchemyModelFactory, fake


def generate_tron_address() -> str:
    return "T" + "".join(
        secrets.choice("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
        for _ in range(33)
    )


class WalletFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore[misc]
        model = Wallet

    network = NetworkEnum.TRON
    address = LazyFunction(generate_tron_address)

    balance = LazyAttribute(
        lambda obj: Decimal(fake.random_int(min=0, max=1000000)) / Decimal(1000)
    )
    bandwidth = LazyAttribute(lambda obj: fake.random_int(min=0, max=100000))
    energy = LazyAttribute(lambda obj: fake.random_int(min=0, max=100000))
