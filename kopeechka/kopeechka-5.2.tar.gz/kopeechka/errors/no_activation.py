class NO_ACTIVATION(Exception):
    def __init__(self, text="Invalid $TASK_ID activation.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text