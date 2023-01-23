class ValidationError(Exception):
    def __init__(self, error, value):
        self.error = error
        self.value = value


class SerializeError(Exception):
    def __init__(self, serializer):
        self.__serializer = serializer

    @property
    def serializer(self):
        return self.__serializer
