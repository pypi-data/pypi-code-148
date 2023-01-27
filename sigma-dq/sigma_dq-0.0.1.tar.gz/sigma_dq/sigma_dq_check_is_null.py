from datetime import datetime
from pyspark.sql import SparkSession
from sigma_dq.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


spark = SparkSession.builder.master("local[*]") \
    .appName('sigma_dq') \
    .getOrCreate()

"""sigma_dq_check_isNull('PRMSDDLVDT',target_table,'',meta = {})"""
def sigma_dq_check_is_null(target_column,target_table,execution_type='',from_date=0,to_date=0):
    column = target_column
    dq_rule = 'isNull'

    if execution_type == 'Incremental':
        str_sql = "select "+target_column+",case when "+target_column+" is not null AND TRIM("+\
            target_column+") <> ''  then 'PASS' else 'FAIL' end as DQ_Status from  "+target_table \
                + ' WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from '+target_table+') '

    elif execution_type == "date_range":
        from_timestamp = datetime.fromtimestamp(from_date)
        from_date_str = from_timestamp.strftime( "%Y-%m-%d")
        to_timestamp = datetime.fromtimestamp(to_date)
        to_date_str = to_timestamp.strftime( "%Y-%m-%d")
        between_condition = \
            f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
        str_sql = "select "+target_column+",case when "+target_column+" is not null AND TRIM("+\
            target_column+") <> ''  then 'PASS' else 'FAIL' end as DQ_Status from  "+target_table \
                + between_condition

    else:
        str_sql = "select "+target_column+",case when "+target_column+" is not null AND TRIM("+\
            target_column+") <> ''  then 'PASS' else 'FAIL' end as DQ_Status from  "+ \
                target_table + ' '

    dq_apply_column_data = spark.sql(str_sql)
    dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)

    return dq_report
