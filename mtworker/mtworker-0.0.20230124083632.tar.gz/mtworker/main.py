
#!/usr/bin/env python3
import sys, os, time
import typer
from datetime import datetime
from celery import Celery
from kombu import Queue
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
from celery.utils.log import get_task_logger
from celery import Celery
import httpx
from typing import Optional
import logging
from threading import Thread
import json
# from mtworker.tasks import app as celery_app
logger = get_task_logger(__name__)

# 启动命令：
# `celery -A mtxcms worker -l INFO`
# `celery -A mtxcms worker -l INFO -Q mtx_cloud`
# 这个命令的含义是：执行celery命令，从mtxcms模块中找到celery模块，并运行为工作进程。

# 参数在世写死
# api_url = "https://mtxtrpcv3.vercel.app/api/mtworker"

app = typer.Typer()


# def create_celery_app(broker:str):
#     app = Celery('tasks', broker=broker, result_backend=broker)
#     return app

def create_celery_app(api_url:str):
    response = httpx.get(api_url)
    print(f'params: {response.json()}')
    param = response.json()
    os.environ.setdefault("MTX_CELERY_BROKER",param["celery_broker"] )
    
    # celery_app = create_celery_app(param["celery_broker"])
    broker = param["celery_broker"]
    print(f"broker: {broker}")
    celery_app = Celery('tasks', broker=broker, result_backend=broker)
    celery_app.conf.beat_schedule = {
        'add-every-3-seconds': {
            'task': 'mtworker.tasks.test',
            'schedule': 3.0,
            'args': ('test task--- args',)
        },
    }
    return celery_app
    

@app.command()
def beat(api: Optional[str] = None):
    celery_app = create_celery_app(api)
    celery_app.conf.beat_schedule = {
        'add-every-3-seconds': {
            'task': 'mtworker.tasks.test',
            'schedule': 3.0,
            'args': ('test task--- args',)
        },
    }
    # 导入任务
    import mtworker.tasks.ad_tasks    
    celery_app.start(['beat','-l','DEBUG'])
        
@app.command()
def worker(api: Optional[str] = None):
    """作为worker 启动"""
    celery_app = create_celery_app(api)
    # 导入任务
    import mtworker.tasks.ad_tasks
    celery_app.start(['worker','-l','DEBUG'])
    
def cli():
    app()

if __name__ == "__main__":
    app()
