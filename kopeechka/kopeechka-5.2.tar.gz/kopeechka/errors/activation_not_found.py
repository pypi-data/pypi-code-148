class ACTIVATION_NOT_FOUND(Exception):
    def __init__(self, text="First letter has not been received, reorder isn`t possible.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text