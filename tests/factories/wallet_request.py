import factory

from db.models.wallet_request import WalletRequest
from enums.network import NetworkEnum

from .base import AsyncSQLAlchemyModelFactory, fake


class WalletRequestFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = WalletRequest

    network = NetworkEnum.TRON
    address = factory.LazyAttribute(lambda obj: fake.address())

    balance = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=1000000))
    bandwidth = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=1000000))
    energy = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=1000000))
