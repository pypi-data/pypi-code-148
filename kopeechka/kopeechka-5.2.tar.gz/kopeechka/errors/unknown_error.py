class UNKNOWN_ERROR(Exception):
    def __init__(self, text="Unknown error", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text