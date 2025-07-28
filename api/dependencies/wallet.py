from typing import Annotated

from fastapi import Depends, Query

from enums.network import NetworkEnum
from explorers.utils import get_explorer
from usecases.wallet import WalletUsecase


def get_network(
    network: Annotated[
        NetworkEnum, Query(description="The network to use")
    ] = NetworkEnum.TRON,
) -> NetworkEnum:
    """Get the network parameter.

    Args:
        network: The network to use.

    Returns:
        The network.

    """
    return network


def get_wallet_usecase(
    network: Annotated[NetworkEnum, Depends(get_network)],
) -> WalletUsecase:
    """Get the wallet usecase.

    Args:
        network: The network to use.

    Returns:
        The wallet usecase.

    """
    return WalletUsecase(explorer=get_explorer(network=network))
