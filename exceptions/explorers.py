from http import HTTPStatus


class ExplorerException(Exception):
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class InvalidAddressException(ExplorerException):
    def __init__(
        self,
        message: str = "Invalid address",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(message=message, status_code=status_code)
