class ClientException(ValueError):
    pass


class UnknownTypeError(ClientException):
    pass


class TooBigEntityError(ClientException):
    pass
