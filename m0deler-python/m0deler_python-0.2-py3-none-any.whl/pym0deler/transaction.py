import datetime
class Transaction:
    def __init__(self, sender, receiver, amt):
        self.sender = sender
        self.receiver = receiver
        self.amt = amt
        self.date = datetime.datetime.now()