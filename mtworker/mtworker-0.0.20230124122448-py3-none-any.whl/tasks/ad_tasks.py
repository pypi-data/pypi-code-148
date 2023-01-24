
from playwright.sync_api import sync_playwright
import os,time
from datetime import datetime
from celery import Celery
from kombu import Queue
import time
import time
import random
from playwright.sync_api import sync_playwright
from playwright.sync_api import Route, Response
from celery import shared_task
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

targetUrl = "https://gamerushbin.blogspot.com/2022/12/the-top-10-best-meal-kit-delivery.html";
fakeHtml="""<html><body>
  <h1>fake html</h1>
  <iframe data-aa='2144138' src='//ad.a-ads.com/2144138?size=468x60' style='width:468px; height:60px; border:0px; padding:0; overflow:hidden; background-color: transparent;'></iframe>
</body></html>
"""

@shared_task(bind=True)
def adEmuAAD():
    # 随机延时 搭配 定时任务固定的触发间隔，能做到看起来时间点随机。
    time.sleep(random.randint(0, 15))
    def handle_route_target_url(route: Route):
        route.fulfill(status=200, content_type="text/html", body=fakeHtml)
    """使用住宅ip浏览a-ad广告"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            proxy={
                "server": "http://@geo.iproyal.com:12321",
                "username": "mattwin",
                "password": "feihuo321_country-us_skipispstatic-1"
            },
            timeout=60*1000
        )
        context = browser.new_context(
            http_credentials={"username": "bill", "password": "pa55w0rd"}
        )
        page = context.new_page()
        
        page.route(targetUrl, handle_route_target_url)
        page.goto(targetUrl)
        time.sleep(60)
        browser.close()
@shared_task
def mtxad_debug():
    print("mtxad debug1-------------", flush=True)
    return "some result for mtxad_debug"
