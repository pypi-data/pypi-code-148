class BAD_EMAIL(Exception):
    def __init__(self, text="Mail was banned.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text