class ConversionError(Exception):
    def __init__(self, message="Conversion failed"):
        self.message = message
        super().__init__(self.message)
