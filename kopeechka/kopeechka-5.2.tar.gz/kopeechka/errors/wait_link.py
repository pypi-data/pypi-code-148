class WAIT_LINK(Exception):
    def __init__(self, text="The letter hasn't arrived yet.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text