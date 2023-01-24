import os
import datetime
import sys
import boto3
import pandas as pd

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from koya_aws import get_file_from_s3, config_aws_env, create_bucket


def run_spider(stage = 'development'
               ,client_project_name = 'koya-boom-and-bucket'
               ,scrape_project_name = 'Cat'
               ,context='aws'
               ,return_data=True
               ,profile_name=None):
    
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
    d=process.crawl(spider)
    process.start()

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
    