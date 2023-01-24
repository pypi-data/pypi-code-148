class TodaysActivity:
    def __init__(self):
        self.todays_completed_tasks = []

    def add_task(self,target, task):
        self.todays_completed_tasks.append({"lead":target,"notes":task})

    def get_tasks(self):
        print(self.todays_completed_tasks)
