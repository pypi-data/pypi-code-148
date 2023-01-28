from datetime import datetime

from vja import login
from dateutil import tz


def format_date(timestamp):
    return timestamp.strftime("%a %d.%m") if timestamp else ""


def format_time(timestamp):
    return timestamp.strftime("%H:%M") if timestamp else ""


class PrintableTask(object):
    def __init__(self, task):
        self.id = task.id
        self.title = task.title
        self.is_favorite = task.is_favorite
        self.priority = task.priority

        self.due_date = None
        if task.due_date and task.due_date > "0001-01-01T00:00:00Z":
            self.due_date = datetime.fromisoformat(
                task.due_date.replace("Z", "")
            ).replace(tzinfo=None)

        lists = login.get_client().getLists()
        listDict = {x.id: x.title for x in lists}
        self.listname = str(listDict.get(int(task.list_id)))

        self.labelnames = []
        if task.labels:
            labels = login.get_client().getLabels()
            labelDict = {x.id: x.title for x in labels}
            self.labelnames = [str(labelDict.get(int(x.id))) for x in task.labels]

    def urgency(self):
        today = datetime.today()
        if (self.due_date):
            duedate = self.due_date
            datediff = (duedate - today).days
            if (datediff < 0):
                datepoints = 6
            elif (datediff == 0):
                datepoints = 5
            elif (datediff == 1):
                datepoints = 4
            elif (datediff > 1 and datediff <= 2):
                datepoints = 3
            elif (datediff > 2 and datediff <= 5):
                datepoints = 3
            elif (datediff > 5 and datediff <= 10):
                datepoints = 1
            elif (datediff > 10):
                datepoints = -1
            else:
                datepoints = 0
        else:
            datepoints = 0
        statuspoints = 0
        if ("next" in self.listname.lower() or "next" in " ".join(self.labelnames).lower()):
            statuspoints = 1
        return 2 + statuspoints + datepoints + int(self.priority) + (1 if self.is_favorite else 0)


    def due_date_format(self):
        return format_date(self.due_date)

    def due_time_format(self):
        return format_time(self.due_date)

    def label_names(self):
        return " ".join(self.labelnames)

    def representation(self):
        output = ["(%s)" % self.priority,
                  "%s" % "*" if self.is_favorite else " ",
                  f"{self.title:50.50}",
                  f"{self.due_date_format():9.9}",
                  f"{self.due_time_format():5.5}",
                  f"{self.listname:15.15}",
                  f"{self.label_names():15.15}",
                  f"{self.urgency():3}"]
        return " ".join(output)
