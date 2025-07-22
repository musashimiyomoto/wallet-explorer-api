from db.models import Wallet
from repositories.base import BaseRepository


class WalletRepository(BaseRepository[Wallet]):
    def __init__(self):
        super().__init__(Wallet)
