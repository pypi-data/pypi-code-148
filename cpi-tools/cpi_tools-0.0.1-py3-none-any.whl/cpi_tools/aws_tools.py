import pandas as pd
import boto3
import s3fs

from dotenv import load_dotenv, find_dotenv

def read_from_s3(s3_bucket: str, s3_file_path:str, file_name: str, file_type = 'csv', sheet_name=None, skip_rows=0) -> pd.DataFrame:
    # Read data from s3 storage

    if load_dotenv(find_dotenv()):

        if file_type == 'csv':
            df = pd.read_csv(f's3://{s3_bucket}/{s3_file_path}/{file_name}',skiprows=skip_rows, encoding='utf-8')

        elif file_type == 'xlsx':
            if sheet_name:
                df = pd.read_excel(f's3://{s3_bucket}/{s3_file_path}/{file_name}', sheet_name=sheet_name, skiprows=skip_rows)
            else:
                df = pd.read_excel(f's3://{s3_bucket}/{s3_file_path}/{file_name}', skiprows=skip_rows)
    else:
        print('No AWS account variables found. Please add account variables to the .env file in your local directory')

    return df