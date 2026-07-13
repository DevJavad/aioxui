class XUIError(Exception):
    pass


class XUIAuthError(XUIError):
    pass


class XUINotFoundError(XUIError):
    pass


class XUIRequestError(XUIError):
    pass