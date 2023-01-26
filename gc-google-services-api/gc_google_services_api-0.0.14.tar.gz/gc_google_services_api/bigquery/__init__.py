from google.cloud import bigquery


def execute_query(query="", error_value=[]):
    client = bigquery.Client()
    query_job = client.query(query)

    try:
        return query_job.result()
    except Exception as e:
        print('[ERROR]: ', e)
        return error_value
