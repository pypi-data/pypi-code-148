class ACTIVATION_CANCELED(Exception):
    def __init__(self, text="The mail was canceled.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text