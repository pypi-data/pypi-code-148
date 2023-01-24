
#!/usr/bin/env python3
import typer
import os,time
from datetime import datetime
from celery import Celery
from kombu import Queue
from celery.schedules import crontab
import requests
from celery import shared_task,chord, group, signature, uuid
from celery.signals import (
    after_setup_task_logger,
    task_success,
    task_prerun,
    task_postrun,
    celeryd_after_setup,
    celeryd_init,
)
import time
import sys
from celery.utils.log import get_task_logger
from celery import Celery
import httpx
from threading import Thread
import logging
logger = get_task_logger(__name__)

# broker = os.environ.get("MTX_CELERY_BROKER")
# app = Celery('tasks', broker=broker, result_backend=broker)

# 导入其他模块定义的任务
from .ad_tasks import *

@shared_task
def mtworker_add(x, y):
    return x + y

@shared_task
def test(arg):
    print(f"test task called arg: {arg}", )
    return f"task result {arg}"

@shared_task
def add(x, y):
    print("add task called")
    z = x + y
    print(z)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # 这里可以添加定时任务，不过，目前的设计定时计划的数据来自api后端，所以这里暂时不配置
#     # print("setup_periodic_tasks")
#     # # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(1, test.s('hello'), name='add every 1')

#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     # # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
#     # print("setup_periodic_tasks")
#     pass
    
    

# app.conf.timezone = 'UTC'
