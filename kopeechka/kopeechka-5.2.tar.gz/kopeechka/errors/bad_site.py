class BAD_SITE(Exception):
    def __init__(self, text="You specified the site incorrectly.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text