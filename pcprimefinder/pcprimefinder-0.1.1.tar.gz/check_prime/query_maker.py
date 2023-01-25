def apply_rule(target_column:str, api_resp:str, target_table: str) -> str:
    query = f"select {target_column} , case when {target_column} = '{api_resp}' then pass " + \
            f"else 'FAIL' end as dq_status from {target_table}"
    return query
