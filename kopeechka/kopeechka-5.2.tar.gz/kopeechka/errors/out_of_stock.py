class OUT_OF_STOCK(Exception):
    def __init__(self, text="There is no mail with such settings. Try changing $MAIL_TYPE or write to support - we'll try to add mailboxes.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text