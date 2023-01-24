
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
logger = get_task_logger(__name__)

# 启动命令：
# `celery -A mtxcms worker -l INFO`
# `celery -A mtxcms worker -l INFO -Q mtx_cloud`
# 这个命令的含义是：执行celery命令，从mtxcms模块中找到celery模块，并运行为工作进程。

# 参数在世写死
# api_url = "https://mtxtrpcv3.vercel.app/api/mtworker"

app = typer.Typer()

def loadParam(api_url:str):
    response = httpx.get(api_url)
    print(f'params: {response.json()}')
    param = response.json()
    os.environ.setdefault("MTX_CELERY_BROKER",param["celery_broker"] )

@app.command()
def beat(api: Optional[str] = None):
    loadParam(api)
    from tasks import app
    
    app.conf.beat_schedule = {
        'add-every-10-seconds': {
            'task': 'tasks.test',
            'schedule': 10.0,
            'args': ('dddddddddddd args',)
        },
    }    
    app.start(['beat','-l','DEBUG'])
        
@app.command()
def worker(api: Optional[str] = None):
    """作为worker 启动"""
    loadParam(api)
    from tasks import app
    app.start(['worker','-l','DEBUG'])

if __name__ == "__main__":
    app()
