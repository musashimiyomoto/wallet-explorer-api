from broker import broker
from db.sessions import async_session
from enums.network import NetworkEnum
from explorers.utils import get_explorer
from schemas.wallet import WalletInfo
from usecases import WalletUsecase


@broker.task(task_name="save_wallet_info")
async def save_wallet_info(network: NetworkEnum, wallet_info: dict) -> None:
    """Save wallet info to database.

    Args:
        wallet_info: The wallet info.

    """
    async with async_session() as session:
        await WalletUsecase(explorer=get_explorer(network=network)).save_wallet_info(
            session=session, wallet_info=WalletInfo.model_validate(wallet_info)
        )
