import os
import datetime
import sys
import boto3
import pandas as pd

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from koya_aws import get_file_from_s3, config_aws_env, create_bucket

import socket
import platform
import psutil
import subprocess
import sqlalchemy
import json


def get_engine(host='koya-internal.cr4gqvnvc2y8.us-east-1.rds.amazonaws.com', port='3306', db_user=None, db_password=None):
    
    if db_user is None or db_password is None:
        db_user = os.getenv('KOYA_DB_SCRAPER_LOGS_USER')
        db_password = os.getenv('KOYA_DB_SCRAPER_LOGS_PASSWORD')
    return sqlalchemy.create_engine(f'mysql+pymysql://{db_user}:{db_password}@{host}')

def get_executor_info():
    hostname = socket.gethostname()
    system = platform.platform()
    processor = platform.processor()
    cpu_count = psutil.cpu_count()
    memory_total = round(psutil.virtual_memory().total/(1024*1024*1024))
    if os.name == 'nt':
        cpu_info = subprocess.check_output('wmic cpu list /format:list', shell=True).decode()
        cpu_dict = {i.split('=')[0]:i.split('=')[1] for i in cpu_info.split('\r\r\n') if i!=''}
    elif os.name=='posix':
        cpu_dict = {'Name':'skip'}
    else:
        cpu_info = subprocess.check_output('lscpu', shell=True).decode()
        cpu_dict = [i.replace('  ','').strip() for i in cpu_info.split('\n')]
        cpu_dict = {i.split(':')[0]:i.split(':')[1] for i in cpu_dict if ':' in i}
        cpu_dict['Name'] = cpu_dict['Model Name'] # "Changing" key name
    
    exec_dict = cpu_dict.copy()
    exec_dict.update({
        'hostname': hostname
        ,'system': system
        ,'processor': processor
        ,'cpu_count': cpu_count
        ,'memory_total': memory_total
    })

    return exec_dict

def run_spider(stage = 'development'
               ,client_project_name = 'koya-boom-and-bucket'
               ,scrape_project_name = 'Cat'
               ,context='aws'
               ,return_data=True
               ,profile_name=None
               ,save_execution_logs=True):
    
    if profile_name is None:
        profile_name = os.getenv('AWS_PROFILE_NAME')
    
    
    
    
    package = scrape_project_name.lower()
    today = datetime.datetime.now().strftime('%m-%d-%Y')
    filename = f'{package}_{today}.csv'
    
    cwd = os.getcwd()
    root = cwd[:cwd.find('/Koya/')]
    root_path = root+'/Koya/'+client_project_name+'/scrape/'
    module_path = os.path.join(root_path, scrape_project_name, scrape_project_name, 'spiders')
    sys.path.append(module_path)

    name = f"{scrape_project_name}spider"
    spider = getattr(__import__(package, fromlist=[name]), name)
    
    #get local path
    data_save_path = os.path.join(root, client_project_name, 'pipeline','1-ingestion','data')
    
    if context == 'aws':
        scrapy_profile = os.getenv('AWS_PROFILE_NAME')
        session = boto3.Session(profile_name=scrapy_profile)
        credentials = session.get_credentials()
        current_credentials = credentials.get_frozen_credentials()
        scrapy_access_key = current_credentials.access_key
        scrapy_secret_key = current_credentials.secret_key
        
        print('context: aws')
        
        bucket = client_project_name
        key = f'{stage}/ingestion/data/{filename}'
    
    elif context == 'local':
        key = None
        bucket= None
        profile_name  = None
        print('context: local')
        
        session = None
        credentials = None
        current_credentials = None
        scrapy_access_key = None
        scrapy_secret_key = None
        
    # Local storage file
    f = os.path.join(data_save_path, filename)
    s = get_project_settings()
    s['LOG_LEVEL'] = 'INFO'
    
    if context == 'aws':
        
        if key is None or bucket is None:
            raise ValueError('key or bucket are missing')
            
        s3_uri = f'S3://{bucket}/{key}'
        
        # https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-storage-fs
        # https://stackoverflow.com/questions/38788096/how-to-upload-crawled-data-from-scrapy-to-amazon-s3-as-csv-or-json
        s['AWS_ACCESS_KEY_ID'] = scrapy_access_key
        s['AWS_SECRET_ACCESS_KEY'] = scrapy_secret_key
        s['FEEDS'] =  {
            f'{s3_uri}': {
                'format': 'csv'
            }
        }

    elif context == 'local':
        
        local_storage_disk = f.split(':')[0].lower()
        
        # https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES
        s['FEED_STORAGES'] = {f'{local_storage_disk}': 'scrapy.extensions.feedexport.FileFeedStorage'}
        s['FEEDS']  = {
            f:
            {
                "format": "csv",
                "overwrite": True
            }
        }
    
    process = CrawlerProcess(s)
    crawler = process.create_crawler(spider)
    d=process.crawl(crawler)

    # TODO: Even when the spider fails, the function returns "finished" status. We would have to capture/parser the exception from the crawler_stats in order to define errors. 
    # Is there are better way?
    # What are the possible/most common spider exceptions? So we can parse (search for the key in the key:value)
    
    try:

        process.start()

        if save_execution_logs:

            crawler_stats = crawler.stats.get_stats()
            exec_info = get_executor_info()

            start_time = crawler_stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')
            finish_time = crawler_stats['finish_time'].strftime('%Y-%m-%d %H:%M:%S')
            time_lapsed = crawler_stats['elapsed_time_seconds']
            author = os.getenv('KOYA_DB_SCRAPER_LOGS_USER')
            system_details = {k:v for k,v in exec_info.items() if k=='hostname' or k=='system' or k=='processor' or k=='cpu_count' or k=='memory_total' or k=='Name'}
            website = spider.start_urls[0]
            crawler_name = spider.name
            execution_details = {k:v for k,v in crawler_stats.items() if k!='start_time' and k!='finish_time' and k!='elapsed_time_seconds' and k!='item_scraped_count'}
            num_items = crawler_stats['item_scraped_count']
            #crawler_version = None #TODO: how to implement? git tag versioning?
            if context == 'aws':
                storage_path = s3_uri
            else:
                storage_path = local_storage_disk
            status = 'OK' #TODO: TBD. Define status names. Idea: if is captured by an exception in this function, should throw 'NOK'?
            #error_message = None #TODO: TBD, maybe a try/except capturing the traceback error
            #browser_configs = {} #TODO: implement selenium

            engine = get_engine()

            # raise Exception('Exception test')

            query = f"""
                INSERT INTO koya_internal.scraper_executions (start_time, finish_time, time_lapsed, author, system_details, website, crawler_name, execution_details, num_items, storage_path, context, status)
                VALUES ('{start_time}', '{finish_time}', {time_lapsed}, '{author}', '{json.dumps(system_details)}', '{website}', '{crawler_name}', '{json.dumps(execution_details, indent=4, sort_keys=True, default=str)}', {num_items}, '{storage_path}', '{context}', '{status}')
            """
            with engine.connect() as conn:
                conn.execute(query)

            print('Execution logs written to DB')
    
    except Exception as e:

        error_message = str(e)

        if save_execution_logs:
            status = 'NOK'            
            query = f"""
                INSERT INTO koya_internal.scraper_executions (start_time, finish_time, time_lapsed, author, system_details, website, crawler_name, execution_details, num_items, storage_path, context, status, error_message)
                VALUES ('{start_time}', '{finish_time}', {time_lapsed}, '{author}', '{json.dumps(system_details)}', '{website}', '{crawler_name}', '{json.dumps(execution_details, indent=4, sort_keys=True, default=str)}', {num_items}, '{storage_path}', '{context}', '{status}', '{error_message}')
            """
            with engine.connect() as conn:
                    conn.execute(query)

            print('Error - Execution logs written to DB')

        raise e

    if return_data:
        if context == 'aws':
            aws_session = config_aws_env(profile_name=profile_name)
            koya_s3_obj = get_file_from_s3(client_project_name=bucket
                                       ,session=aws_session
                                       ,input_file_path=stage+'/ingestion/data/'
                                       ,aws_filename=filename)
        
            data = pd.read_csv(koya_s3_obj['Body'])
            
        elif context == 'local':
            
            # Checking if file was saved in local storage
            if not os.path.exists(f):
                raise Exception('File not found')
            
            print('reading from local:',f'{f}')
            data = pd.read_csv(f)
        
        return data

    return None
