class BAD_DOMAIN(Exception):
    def __init__(self, text="We do not have such a domain/domain zone.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text