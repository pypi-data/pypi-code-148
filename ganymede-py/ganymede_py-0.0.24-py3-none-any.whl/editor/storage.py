from google.cloud import storage
from typing import List


def get_project(project_name: str) -> str:
    """
    Gets project name

    Parameters
    ----------
    project_name : str
        current project name

    Returns
    -------
    str
        project name in bucket
    """
    if project_name == 'ganymede-core-dev':
        project_name = 'ganymede-dev'
    return project_name


def get_bucket_name(bucket_source: str, project: str) -> str:
    """
    Gets bucket name

    Parameters
    ----------
    bucket_source : str
        Either 'input' or 'output' bucket
    project : str
        Ganymede project name

    Returns
    -------
    str
        Bucket name to access

    Raises
    ------
    ValueError
        Invalid bucket source; has to be either 'input' or 'output'
    """
    bucket_source = bucket_source.strip().lower()

    if bucket_source == 'input':
        bucket_name = f"ganymede-{project}-lab-ingest"
    elif bucket_source == 'output':
        bucket_name = f"ganymede-{project}-output"
    else:
        raise ValueError("Data source must either be 'input' or 'output'")

    return bucket_name


def list_data(bucket_source='input') -> List[str]:
    """
    Retrieves listing of available files from cloud storage

    Parameters
    ----------
    filename : str
        File to retrieve
    bucket_source: str
        Bucket to retrieve file from; either 'input' or 'output'

    Returns
    -------
    List[str]
        list of files available for retrieval
    """
    client = storage.Client()

    project = get_project(client.project)
    bucket_name = get_bucket_name(bucket_source, project)

    try:
        file_list = []
        for blob in client.list_blobs(bucket_name):
            file_list.append(blob.name)
        return file_list
    except Exception as e:
        print('\033[91m' + 'File list from cloud storage cloud not be retrieved. '
              'See the following error.\n' + str(e))


def get_data(filename: str, bucket_source='input') -> bytes:
    """
    Retrieves data from cloud storage

    Parameters
    ----------
    filename : str
        File to retrieve
    bucket_source: str
        Bucket to retrieve file from; either 'input' or 'output'

    Returns
    -------
    bytes
        file contents
    """
    client = storage.Client()

    project = get_project(client.project)
    bucket_name = get_bucket_name(bucket_source, project)

    try:
        bucket = client.get_bucket(bucket_name)
        return bucket.blob(filename).download_as_string()
    except Exception as e:
        print('\033[91m' + 'Data retrieval was unsuccessful. '
              'See the following error.\n' + str(e))


def save_data_from_file(file_to_upload: str,
                        dest_blob_name: str,
                        dest_bucket='output',
                        timeout=60):
    """
    Store file in cloud storage

    Parameters
    ----------
    file_to_upload : str
        Filename of local file to upload to cloud storage
    dest_blob_name : str
        Path of destination blob
    dest_bucket: str
        Bucket to store file in; either 'input' or 'output'
    timeout: int
        Number of seconds before upload timeout
    """
    client = storage.Client()

    project = get_project(client.project)
    bucket_name = get_bucket_name(dest_bucket, project)

    try:
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(dest_blob_name)
        blob.upload_from_filename(file_to_upload, timeout=timeout)
    except Exception as e:
        print('\033[91m' + 'Data storage was unsuccessful. '
              'See the following error.\n' + str(e))

    print('File {file_to_upload} successfully uploaded to {dest_blob_name}/{dest_bucket_name}')
