from fastapi import Query

from enums.network import NetworkEnum
from explorers import TronExplorer
from usecases.wallet import WalletUsecase


def get_wallet_usecase(
    network: NetworkEnum = Query(
        default=NetworkEnum.TRON, description="The network to use"
    )
) -> WalletUsecase:
    """Get the wallet usecase.

    Args:
        network: The network to use.

    Returns:
        The wallet usecase.

    """
    if network == NetworkEnum.TRON:
        explorer = TronExplorer()
    else:
        raise ValueError(f"Network {network} not supported")

    return WalletUsecase(explorer=explorer)
