

class TodayTarget:
    def __init__(self, targets):
        self.targets = targets
        self.index = 0

    def get_next_target(self):
        if self.index >= len(self.targets):
            return None
        target = self.targets[self.index]
        self.index += 1
        return target