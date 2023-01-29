import os,time
from pathlib import Path
from datetime import datetime
import traceback
from celery import Celery
from kombu import Queue
# from stem.control import Controller
# import stem
import time
import random
from scrapy.crawler import CrawlerProcess
# import stem.process
# from stem.util import term

from .scrapy_tutorial.spiders.common_spider import CommonSpider
from .scrapy_tutorial.spiders.quotes_spider import QuotesSpider
# from .quotes_spider import QuotesSpider
from celery import shared_task,chord, group, signature, uuid
from celery.signals import (
    after_setup_task_logger,
    task_success,
    task_prerun,
    task_postrun,
    celeryd_after_setup,
    celeryd_init,
)
from celery import shared_task

@shared_task
def scrapy_demo(item_cb_url:str):
    """通过celery worker 来执行爬网"""
    print("scrapy 启动",flush=True)
    logfile = "logs/mtscrapy_log.log"
    try:
        Path(logfile).parents[0].mkdir(parents=True, exist_ok=True)
        process=CrawlerProcess(settings={
                    # "FEEDS": {
                    #     "items.json": {"format": "json"},
                    # },
                    "LOG_FILE": logfile,
                    "ROBOTSTXT_OBEY":True,
                    "CONCURRENT_REQUESTS":10,
                    "ITEM_PIPELINES" : {
                        'mtworker.tasks.scrapy_tutorial.pipelines.ScrapyTutorialPipeline': 300,
                        'mtworker.tasks.scrapy_tutorial.pipelines.ScrapyPipeLine2': 400,
                    },
                    "REQUEST_FINGERPRINTER_IMPLEMENTATION" : '2.7',
                    # 自定义settings
                    "MTX_ITEM_CALLBACK_URL":item_cb_url
                })
        process.crawl(CommonSpider)
        print("scrapy start...")
        process.start() # the script will block here until the crawling is finished
        print("domain_crawl finished")
    except Exception as e:
        print("启动爬网失败。。")
        traceback.print_exception(e)

    
        
