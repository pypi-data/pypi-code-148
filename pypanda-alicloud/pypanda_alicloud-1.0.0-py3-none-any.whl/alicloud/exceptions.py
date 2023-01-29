class IException(Exception):
    def __init__(self, msg):
        self.message = msg


class ServiceNotEnabledError(IException):
    """Raised when a service is not enabled in the region"""
    pass


class PleaseRetryError(IException):
    """Raised when retry needed"""
    pass


class EntityNotExists(IException):
    """Raised when a entity not exists"""
    pass

class EntityAlreadyExists(IException):
    """Raised when a entity not exists"""
    pass
