# coding=utf-8
"""
    vja.service
    ~~~~~~~~~~~

    Business logic.

"""
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import tz
import parsedatetime as pdt
from time import mktime, time

from vja import login
from vja.model import PrintableTask

import logging

logger = logging.getLogger(__name__)


def list_tasks(list, list_size, urgency_sort):
    tasks = get_tasks(None, 'today', list)
    if list_size == 0:
        tasks += get_tasks('today', 'in 3 days', list)
        tasks += get_tasks(None, None, list, 'next action')
    if list_size > 0:
        tasks += get_tasks('today', 'tomorrow+364 days', list)
        tasks += get_tasks(None, None, list)
    if (urgency_sort):
        tasks.sort(key=lambda x: x.urgency(), reverse=True)
    print_tasks(tasks, urgency_sort)


def get_tasks(day_start=None, day_end='today', list=None, status=None):
    start = get_max_time(day_start) if day_start else None
    end = get_max_time(day_end) if day_end else None

    raw_tasks = login.get_client().getTasks(exclude_completed=True)

    filtered_tasks = [PrintableTask(x) for x in raw_tasks if is_in(x, start, end)]
    filtered_tasks.sort(key=lambda x: (x.due_date or datetime.max,
               -(x.priority),
               x.listname.upper(),
               x.title.upper()))
    return filtered_tasks

def get_max_time(day='today'):
    timest = pdt.Calendar().parse(day)[0]
    now = datetime.fromtimestamp(mktime(timest), tz.tzlocal())
    daystart = datetime(now.year, now.month, now.day, tzinfo=now.tzinfo)
    dayend = daystart + timedelta(days=1)
    utc_dayend = dayend.isoformat()
    return utc_dayend

def is_in(item, start_date, end_date):
    if ((not item.due_date and not start_date and not end_date)
        or (item.due_date and end_date and item.due_date < end_date)
        and (not start_date or (item.due_date and item.due_date > start_date))):
        return True
    else:
        return False

def print_tasks(tasks, priority_level_sort=False):
    if not tasks:
        print("No tasks found. Go home early!")
    if (priority_level_sort):
        tasks_by_prio = defaultdict(list)
        for task in tasks:
            tasks_by_prio[task.urgency()].append(task)
        for prio, items in tasks_by_prio.items():
            #print("--------------------------------------")
            print()
            print_task_list(tasks, items)
    else:
        print_task_list(tasks, tasks)

def print_task_list(tasks, items):
    for item in items:
        print(f"{str(tasks.index(item) + 1):2}" + " " + item.representation())
