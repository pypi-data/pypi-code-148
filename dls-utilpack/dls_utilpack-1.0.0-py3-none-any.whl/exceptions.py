class NotFound(RuntimeError):
    pass


# When something has no value set yet.
class NotSet(RuntimeError):
    pass


class CapacityReached(RuntimeError):
    pass


class DuplicateLabelException(RuntimeError):
    pass


class DuplicateUuidException(RuntimeError):
    pass


class Factory:
    def build(qualname):
        if qualname == "dls_bxflow_api.exceptions.DuplicateLabelException":
            return DuplicateLabelException
        return None
