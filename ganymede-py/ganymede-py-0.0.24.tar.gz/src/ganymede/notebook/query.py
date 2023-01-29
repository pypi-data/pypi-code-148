from google.cloud import bigquery
import pandas as pd
import pandas_gbq


def dry_run(query_sql: str):
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    try:
        query_job = client.query(query_sql, job_config=job_config)
        print('\033[92m' + 'Query ran successfully. '
              'It will process {} bytes.'.format(query_job.total_bytes_processed))
    except Exception as e:
        print('\033[91m' + 'Query did not run successfully. '
              'See the following error.\n' + e.errors[0].get('message'))


def results(query_sql: str):
    client = bigquery.Client()
    pandas_gbq.context.credentials = client._credentials
    pandas_gbq.context.project = client.project
    try:
        df = pd.read_gbq(query_sql, progress_bar_type='tqdm')
        return df
    except Exception as e:
        print('\033[91m' + 'Query did not run successfully. '
              'See the following error.\n' + str(e))
