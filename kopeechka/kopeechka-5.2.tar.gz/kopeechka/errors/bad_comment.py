class BAD_COMMENT(Exception):
    def __init__(self, text="Activattion not found (It`s not your activation).", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text