class BAD_TOKEN(Exception):
    def __init__(self, text="Invalid token.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text