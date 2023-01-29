class KPTV:
    def __init__(self, name, job):
        self.name = name
        self.job = job

    def do(self):
        return f'{self.name}正在打麻将'
