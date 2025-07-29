from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from broker import broker
from enums.network import NetworkEnum
from explorers.utils import get_explorer
from schemas.wallet import WalletInfo
from tasks.dependencies import db
from usecases import WalletUsecase


@broker.task(task_name="save_wallet_info")
async def save_wallet_info(
    network: NetworkEnum,
    wallet_info: dict,
    session: AsyncSession = TaskiqDepends(db.get_session),  # noqa: B008
) -> None:
    """Save wallet info to database.

    Args:
        network: The network enum.
        wallet_info: The wallet info.
        session: Database session.

    """
    await WalletUsecase(explorer=get_explorer(network=network)).save_wallet_info(
        session=session, wallet_info=WalletInfo.model_validate(wallet_info)
    )
