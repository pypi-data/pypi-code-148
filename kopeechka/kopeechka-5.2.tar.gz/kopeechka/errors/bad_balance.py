class BAD_BALANCE(Exception):
    def __init__(self, text="There are not enough funds to perform the operation.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text