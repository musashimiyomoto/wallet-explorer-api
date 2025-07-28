from enums.network import NetworkEnum
from explorers import BaseExplorer, TronExplorer


def get_explorer(network: NetworkEnum) -> BaseExplorer:
    """Get explorer by network.

    Args:
        network: The network to use.

    """
    if network == NetworkEnum.TRON:
        return TronExplorer()

    msg = f"Network {network} not supported"
    raise ValueError(msg)
