from datetime import datetime
from pyspark.sql import SparkSession
from sigma_dq.sigma_dq_generate_dq_report import sigma_dq_generate_dq_report


spark = SparkSession.builder.master("local[*]") \
    .appName('sigma_dq') \
    .getOrCreate()

# sigma_dq_check_fieldCompare(target_column,api_response,target_table)
# '%<>%80'
def sigma_dq_check_field_compare_with_value(target_column,api_response,target_table,execution_type='',from_date=0,to_date=0,meta={}):
    column = target_column
    dq_rule = 'fieldCompare_zero'
    source_table_with_column = target_table+'.'+target_column
    source_table = target_table
    operator = ''.join(api_response.split('%')[1:-1])
    value = ''.join(api_response.split('%')[::-3])

    try:
        value = float(value)
    except:
        return("Insert valid number")
    else:
        value = float(value)

    if operator == '>':  # Greater than 0
        operator = '> ' + str(value)
        str_sql = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+\
            operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + source_table +"  "

    elif operator == '>':  # Greater than equal to 0
        operator = '> '+ str(value)
        str_sql = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+\
            operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + source_table +"  "

    elif operator == '<':  # Less than 0
        operator = '< '+ str(value)
        str_sql = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+\
            operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + source_table+"  "

    elif operator == '<=':  # Less than equal to 0
        operator = '<= '+ str(value)
        str_sql = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+\
            operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + source_table+"  "

    elif operator == '<>':  # Not equal to 0
        operator = '<> '+ str(value)
        str_sql = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+\
            operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + source_table+"  "

    elif operator == '=':  # Not equal to 0
        operator = '= '+ str(value)
        str_sql = "select "+source_table_with_column+", CASE WHEN " +source_table_with_column+" "+\
            operator+" THEN 'PASS' ELSE 'FAIL' END as DQ_Status from " + source_table+"  "

    else:
        return "Error please check the input dqRule:sigma_dq_check_fieldCompare_with_value"

    if execution_type == 'Incremental': 
        str_sql += " where UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "+target_table+ \
            ") OR dqAction = 'NA'"
    elif execution_type == "date_range":
        from_timestamp = datetime.fromtimestamp(from_date)
        from_date_str = from_timestamp.strftime( "%Y-%m-%d")
        to_timestamp = datetime.fromtimestamp(to_date)
        to_date_str = to_timestamp.strftime( "%Y-%m-%d")
        between_condition = \
            f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
        str_sql += between_condition

    dq_apply_column_data = spark.sql(str_sql)
    dq_report = sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule)

    return dq_report
