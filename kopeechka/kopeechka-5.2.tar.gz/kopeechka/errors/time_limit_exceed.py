class TIME_LIMIT_EXCEED(Exception):
    def __init__(self, text="The limit of mail orders per second has been reached (applies to special tariffs), it is necessary to expand the tariff.", data={}):
        self.text = text
        self.data = data

    def __str__(self):
        return self.text