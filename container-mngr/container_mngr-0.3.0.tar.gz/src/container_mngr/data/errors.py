class ContainerRuntimeAPIError(Exception):
    def __init__(self, message: str, inner_error: Exception) -> None:
        super().__init__(message)

        self.inner_error = inner_error


class ModelMappingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
