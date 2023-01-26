import boto3
import logging
from botocore.exceptions import ClientError
import pandas as pd
import os
import re
import io
import datetime


def config_aws_env(profile_name):
    '''
    return
    A session stores configuration state and allows you to create service clients and resources.

    profile_name: The name of a profile to use. If not given, then the default profile is used.
    type: str

    '''
    
    try:
        response = boto3.Session(profile_name=profile_name)
        
        return response

    except Exception as err:
        error_message = f"{err}"
        raise Exception(error_message)
        

def get_file_from_s3(session, input_file_path, aws_filename, client_project_name='koya-canoa'):
    '''     
    This function reads data included within an S3 bucket.

    return
    file_dict: the dictionary with the specific file
    type: dict

    session: AWS temporary session token
    type: str

    input_file_path: Key of the object to get.
    type: str

    aws_filename: Name of the specific folder where the data is contained.
    type: str

    client_project_name: Project name within s3.
    type: str

    '''
    
    try:
        s3_client = session.client('s3')
        bucket = client_project_name

        return s3_client.get_object(Bucket=bucket, Key=input_file_path + aws_filename) 

    except Exception as err:
        error_message = f"{err}"
        raise Exception(error_message)
        
def put_file_in_s3(aws_session, df, input_file_path, aws_filename, client_project_name='koya-canoa'):

    '''
    This function sends data in csv format to a specific folder within s3.

    return
    response: Dictionary containing the status of sending data to s3.
    type: dict

    aws_session: AWS temporary session token.
    type: str

    df: dataframe that will be transformed into csv.
    type: str

    input_file_path: Key of the object to get.
    type: str

    aws_filename: Name of the specific folder where the data is contained.
    type: str

    client_project_name: Project name within s3.
    type: str

'''
    #TODO: fix it to work without self
    s3_resource = aws_session.resource()

    bucket = client_project_name

    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)        
        s3_resource.Object(bucket, input_file_path + '/' + aws_filename).put(Body=csv_buffer.getvalue())

    except Exception as e:
        print(e)
        raise Exception('Fail while uploading file to S3')
        

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False

    message = f"{bucket_name} created"

    return message

def load_data_aws(stage='development'
                  ,step='ingestion'
                  ,source='scottdental'
                  ,context='aws'
                  ,client_project_name='koya-faliam'
                  ,date=None
                  ,profile_name=None
                  ,get_latest_file=False):

    if profile_name is None:
        profile_name = os.getenv('AWS_PROFILE_NAME')
        
    aws_session = config_aws_env(profile_name=profile_name)

    if date is None and get_latest_file==True:
        available_files = get_available_files_aws(client_project_name,filter_by=step)
        latest_file = get_latest_file_aws(available_files,source)
        if latest_file is None:
            raise ValueError('not file match the criteria')
        else:
            aws_filename=latest_file[latest_file.find('data')+5:]

    else:
        aws_filename = f'{source}_{date}.csv'

    print(f'reading: {stage}/{step}/data/{aws_filename}')

    koya_s3_obj = get_file_from_s3(client_project_name=client_project_name
                                   ,session=aws_session
                                   ,input_file_path=f'{stage}/{step}/data/'
                                   ,aws_filename=aws_filename)
    s3_data = koya_s3_obj.get('Body')
    data = pd.read_csv(s3_data)
    return data

def get_available_files_aws(bucket,profile_name=None,filter_by=None):
    
    if profile_name is None:
        profile_name = os.getenv('AWS_PROFILE_NAME')
    
    aws_session = boto3.Session(profile_name=profile_name)
    s3 = aws_session.resource('s3')
    bucket_obj = s3.Bucket(bucket)
    
    l=[]
    for my_bucket_object in bucket_obj.objects.all():
        key = my_bucket_object.key
        if filter_by is not None:
            if filter_by in key:
                l.append(key)
        else:
            l.append(key)
    return l

def get_latest_file_aws(available_files,source):
    files = [k for k in available_files if source in k]
    if len(files)==0:
        raise ValueError(f'file not found for source: {source}')
        
    l=[]
    for k in files:
        d=re.search('(\d\d-\d\d-\d+).csv',k).group(1)
        l.append((k,pd.Timestamp(d)))
    l=(sorted(l, key = lambda x: x[1]))
    latest = l[-1][0]
    if source not in latest:
        return None
    return latest


def save_data_aws(data,stage,step,source,client_project_name,add_info,profile_name=None):
    
    if profile_name is None:
        profile_name = os.getenv('AWS_PROFILE_NAME')
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    
    today = datetime.datetime.now().strftime('%m-%d-%Y')
    
    aws_session = boto3.Session(profile_name=profile_name)
    s3_resource = aws_session.resource('s3')
    output_file_path=f'{stage}/{step}/data/'
    print('saving to:',output_file_path+f'{add_info}_{source}_{today}.csv')
    
    s3_resource.Object(client_project_name, output_file_path+f'{add_info}_{source}_{today}.csv').put(Body=csv_buffer.getvalue())
