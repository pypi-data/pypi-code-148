import pandas as pd
import boto3
import s3fs

from dotenv import load_dotenv, find_dotenv

def read_from_s3(s3_bucket: str, s3_file_path:str, file_name: str, file_type = 'csv', sheet_name=None, skip_rows=0) -> pd.DataFrame:
    """
    This function reads data from an S3 bucket and returns it as a pandas DataFrame.

    Inputs:

    s3_bucket (str): The name of the S3 bucket where the file is located.
    s3_file_path (str): The file path within the S3 bucket.
    file_name (str): The name of the file to be read.
    file_type (str, optional): The file type of the file to be read. Defaults to 'csv'.
    sheet_name (str, optional): The sheet name to be read from the excel file. Only used if file_type is 'xlsx'.
    skip_rows (int, optional): The number of rows to skip when reading the file. Defaults to 0.
    Returns:

    df (pd.DataFrame): The data read from the file.
    """

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