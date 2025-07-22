from usecases.wallet import WalletUsecase


def get_wallet_usecase() -> WalletUsecase:
    """Get the wallet usecase.

    Returns:
        The wallet usecase.

    """
    return WalletUsecase()
