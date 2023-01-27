def sigma_dq_generate_dq_report(dq_apply_column_data,column,dq_rule,meta={}):
    dq_report = {}
    dq_report['column'] = column
    dq_report['rule'] = dq_rule
    print(f"column: {column}, RuleName: {dq_rule}")
    dq_report['total_rows_checked'] = dq_apply_column_data.count()
    total_dq_pass_count = \
        dq_apply_column_data.filter(dq_apply_column_data.DQ_Status == 'PASS').count()
    dq_report['total_rows_failed'] = dq_apply_column_data.filter(
        dq_apply_column_data.DQ_Status == 'FAIL').count()
    if dq_report['total_rows_failed'] > 0:
        print("inside failed")
        dq_report['success'] = False
        dq_report['failed_percent'] = \
            (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
        raw_fail_list = dq_apply_column_data.select(dq_apply_column_data[column]). \
            filter(dq_apply_column_data.DQ_Status == 'FAIL'). \
            rdd.flatMap(lambda x: x). \
            collect()
        dq_report['failed_values'] = raw_fail_list
    elif dq_report['total_rows_checked'] < 1:
        dq_report['success'] = False
        dq_report['successResult'] = 'Table is empty'
        dq_report['passed_percent'] = []
        dq_report['failed_values'] = []
        dq_report['failed_percent'] = []

    elif dq_report['total_rows_failed'] == dq_report['total_rows_checked']:
        dq_report['success'] = False
        dq_report['failed_values'] = []
        dq_report['failed_percent'] = []

    elif dq_report['total_rows_failed'] == dq_report['total_rows_checked']:
        dq_report['success'] = False
        dq_report['failed_percent'] = \
            (dq_report['total_rows_failed']/dq_report['total_rows_checked'])*100
        dq_report['failed_values'] = []
    else:
        dq_report['success'] = True
        dq_report['passed_percent'] = (total_dq_pass_count/dq_report['total_rows_checked'])*100

    dq_report['meta'] = meta
    return dq_report
