from db.models import WalletRequest
from repositories.base import BaseRepository


class WalletRequestRepository(BaseRepository[WalletRequest]):
    def __init__(self):
        super().__init__(WalletRequest)
