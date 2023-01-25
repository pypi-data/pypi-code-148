class SYSTEM_ERROR(Exception):
    def __init__(self, text="Unknown, system error. Contact support - we will help!", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text