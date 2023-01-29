import pandas as pd
import duckdb
from datetime import datetime
import pytz



def create_time_parts(tz):
    if tz:
        tz = pytz.timezone(tz)
    now = datetime.now(tz)
    now_parts = [str(i) for i in[now.year, now.month, now.day, now.hour, now.minute, now.second]]
    return ",".join(now_parts)


def scd2(src: pd.DataFrame, tgt: pd.DataFrame, cols_to_track: list=None, tz: str=None) -> pd.DataFrame:
    """"
    src: pandas dataframe with the source of the SCD
    tgt: pandas dataframe with the target of the SCD (target can be empty)
    cols_to_track: list of columns to track changes (default is all columns from the source table)
    tz: pytz time zone to use on start_ts and end_ts, default is None (will use local time)
    the return dataframe contain the entire target table with the new changes, ready for insert overwrite of the current target table
    """

    if not cols_to_track:
        cols_to_track = list(src.columns)

    if not isinstance(cols_to_track, list):
        raise TypeError('cols_to_track must be of type list')


    duck = duckdb.connect()
    time_parts = create_time_parts(tz)
    duck.execute(f"CREATE TABLE source_scd AS SELECT *, md5(concat_ws('_', {','.join(cols_to_track)})) as hash FROM src")
    duck.execute(f"CREATE TABLE target_scd as select *, md5(concat_ws('_', {','.join(cols_to_track)})) as hash from tgt")

    results = {}
    # rows that are in both target and source, and active
    ### unchanged_active_keys (active - old) ###
    duck.execute("""
        CREATE TABLE unchanged_active_keys as 
        select * 
        from target_scd
        where is_active = True
        and exists(
            select * 
            from source_scd
            where target_scd.hash = source_scd.hash
        )
        """)

    unchanged_active_keys = duck.execute("select count(*) from unchanged_active_keys").fetchone()[0]
    results['unchanged active keys (active - old)'] = unchanged_active_keys
    
    # rows that are in the target but no longer in the source, and are inactive
    ### unchanged_inactive_keys (inactive - old) ###
    duck.execute("""
        CREATE TABLE unchanged_inactive_keys as 
        select * 
        from target_scd
        where is_active = False
        and not exists(
            select * 
            from source_scd
            where target_scd.hash = source_scd.hash
        )
        """)

    unchanged_inactive_keys = duck.execute("select count(*) from unchanged_inactive_keys").fetchone()[0]
    results['unchanged inactive keys (inactive - old)'] = unchanged_inactive_keys

    # rows that are in the target but no longer in the source, and are active
    ### ended_keys (inactive - new) ###
    duck.execute(f"""
    create table ended_keys as 
    select * EXCLUDE (end_ts, is_active, hash),
    make_timestamp({time_parts}) as end_ts,
    FALSE as is_active,
    from target_scd
    where is_active = True
    and not exists (
        select * 
        from source_scd
        where target_scd.hash = source_scd.hash
    )
    """)

    ended_keys = duck.execute("select count(*) from ended_keys").fetchone()[0]
    results['ended keys (inactive - new)'] = ended_keys

    # rows that are in the source but not in the target
    ### new_keys (active - new) ###
    duck.execute(f"""
    create table new_keys as 
    select * EXCLUDE (hash),
    make_timestamp({time_parts}) as start_ts,
    null as end_ts,
    TRUE as is_active,
    from source_scd
    where not exists (
        select * 
        from target_scd
        where target_scd.hash = source_scd.hash
    )
    """)

    new_keys = duck.execute("select count(*) from new_keys").fetchone()[0]
    results['new keys (active - new)'] = new_keys

    duck.execute("""
    create table final as 
    select * EXCLUDE(hash) from unchanged_active_keys
    union all by name 
    select * EXCLUDE(hash) from unchanged_inactive_keys
    union all by name 
    select * from ended_keys
    union all by name 
    select * from new_keys
    """)


    result_df = pd.DataFrame.from_dict(results, orient='index')
    result_df.loc['total'] = result_df.sum(numeric_only=True)
    print(result_df.to_markdown(headers=['category', 'row count'], tablefmt='psql'))
    
    df = duck.execute("select * from final").fetch_df()    
    return df