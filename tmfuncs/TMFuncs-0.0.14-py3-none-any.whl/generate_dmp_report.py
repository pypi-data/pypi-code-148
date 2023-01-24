"""
DMP 8张表入库
"""

from TMFuncs import base

from pyspark.sql import Window
from pyspark.sql import functions as fn
from pyspark.sql.functions import col


# 校验数据是否已经入库
def valid_data(spark_ob, db, table, date_col, logger=None):
    dt_utc8 = base.get_date(days=1, str_format='%Y%m%d', time_zone='Asia/Shanghai')
    sql = f"select * from {db}.{table} where {date_col} =={dt_utc8}"
    data = spark_ob.sql(sql)
    records_num = data.count()
    if logger is not None:
        logger.info(f'valid_data for table [{table}], sql: {sql}, records_num: {records_num}')

    if records_num == 0:
        return True
    else:
        return False


# 读取昨日数据
def read_data(spark_ob, db, table, date_col, recent_days=1, limit_num=5000, limit_date='2022-12-14', test=False,
              logger=None):
    if test:
        sql = f"select * from {db}.{table} where {date_col} == to_date('{limit_date}') and event not in ('Pageview','PageView') limit {limit_num}"
    else:
        sql = f"select * from {db}.{table} where {date_col} == CURRENT_DATE() - INTERVAL '{recent_days}' DAY and event not in ('Pageview','PageView')"
    if logger is not None:
        logger.info(f'raw sql: {sql}')
    return spark_ob.sql(sql)


# 公用函数：写Delta表
def write_deltaLake(df, file_format, db, table, blob_path, max_file_size, mode='append'):
    df.write \
        .format(file_format) \
        .mode(mode) \
        .option("mergeSchema", 'true') \
        .option("delta.targetFileSize", max_file_size) \
        .option("path", f'{blob_path}/{db}/{table}') \
        .saveAsTable(f'{db}.{table}')  # 直接保存到delta表所在路径


# 公用函数：基础ETL
def basic_etl(df, hit_type):
    # 强制显示东八区时间
    df = df.withColumn("datetime", col('datetime') + fn.expr('INTERVAL 8 HOURS'))

    return df.select("*",
                     # 转换格式的字段
                     col('user_id').alias("FULL_VISITOR_ID"),
                     col('user_id').alias("CLIENTID"),
                     col('login_id').alias("AID"),
                     fn.date_format('date', "yyyyMMdd").alias("date_str"),
                     # 增加来源渠道信息
                     fn.concat_ws('_',
                                  fn.when(fn.get_json_object(df['properties'], '$.$latest_utm_source').isNull(),
                                          'null').otherwise(
                                      fn.get_json_object(df['properties'], '$.$latest_utm_source')),
                                  fn.when(fn.get_json_object(df['properties'], '$.$latest_utm_medium').isNull(),
                                          'null').otherwise(
                                      fn.get_json_object(df['properties'], '$.$latest_utm_medium')),
                                  fn.when(fn.get_json_object(df['properties'], '$.$latest_utm_content').isNull(),
                                          'null').otherwise(
                                      fn.get_json_object(df['properties'], '$.$latest_utm_content')),
                                  fn.when(fn.get_json_object(df['properties'], '$.$latest_utm_campaign').isNull(),
                                          'null').otherwise(
                                      fn.get_json_object(df['properties'], '$.$latest_utm_campaign')),
                                  fn.when(fn.get_json_object(df['properties'], '$.$latest_utm_term').isNull(),
                                          'null').otherwise(fn.get_json_object(df['properties'], '$.$latest_utm_term')),
                                  ).alias('reffer_id'),
                     fn.get_json_object(df['properties'], '$.$latest_utm_source').alias('source'),
                     fn.get_json_object(df['properties'], '$.$latest_utm_medium').alias('medium'),
                     fn.get_json_object(df['properties'], '$.$latest_utm_content').alias('ad_content'),
                     fn.get_json_object(df['properties'], '$.$latest_utm_campaign').alias('campaign'),
                     fn.get_json_object(df['properties'], '$.$latest_utm_term').alias('keyword'),
                     # 增加event互动字段
                     fn.regexp_extract(df['el'], r".+产品ID:(.+)_播放节点:15S|.+产品ID:(.+)_滑动", 1).alias('STDSKUCODE'),
                     fn.regexp_extract(df['el'], r".+菜谱ID:(.+)_产品:.+播放节点:15S|.+菜谱ID:(.+)_产品:.+滑动", 1).alias(
                         'CONTENT_ID'),
                     fn.when(df['event'].isin(hit_type['PAGE']), 'PAGE').when(df['event'].isin(hit_type['APPVIEW']),
                                                                              'APPVIEW').otherwise('EVENT').alias(
                         'HIT_TYPE'),
                     col('ec').alias('EVENT_CATEGORY'),
                     col('ea').alias('EVENT_ACTION'),
                     col('el').alias('EVENT_LABEL'),
                     fn.lit(None).astype('string').alias('EC_ACTION'),
                     col('datetime').alias('EVENT_TIME'),
                     # 增加页面信息
                     fn.get_json_object(df['properties'], '$.Pagegroup1').alias('PAGE_GROUP1'),
                     fn.get_json_object(df['properties'], '$.Pagegroup2').alias('PAGE_GROUP2'),
                     fn.get_json_object(df['properties'], '$.Pagegroup3').alias('PAGE_GROUP3'),
                     fn.get_json_object(df['properties'], '$.Template').alias('PAGE_TEMPLET'),
                     fn.get_json_object(df['properties'], '$.Area').alias('PAGE_AREA'),
                     fn.get_json_object(df['properties'], '$.Screenname').alias('SCREENNAME'),
                     fn.lit(None).astype('string').alias('SEARCHKEYWORD'),
                     # 其他
                     fn.get_json_object(df['properties'], '$.is_first_day').alias('is_newvisit'),
                     )


# 公用函数：定义session
def define_session(df, cookie_window):
    """
    计算session，核心主体字段是user_id（类似于GA Cookie的概念），逻辑包括三个（满足任意一个会话切分）：
     - 条件1：event30分钟静默
     - 条件2：每日0点会话强制切分（基于每日计算，自然就切分了）
     - 条件3：utm信息改变（所有5个参数的任意一个）
     - 条件4：events第一条记录，就是一个新session
    """
    # 第一步 基于user_id计算每个“用户”的2次event之间的时间间隔，计算会话 + 第一个event，就是一个新会话
    session_time = df.withColumn('pre_timestamp', fn.lag(col("timestamp"), 1).over(cookie_window))  # 上1条记录的时间
    session_time = session_time.withColumn('gap_time', col("timestamp") - col("pre_timestamp"))  # event时间间隔
    session_time = session_time.withColumn('is_time_new_session',
                                           fn.when((col('gap_time') > 30 * 60 * 1000) | (col('gap_time').isNull()),
                                                   1).otherwise(0))  # 超过30分钟，则产生新会话

    # 第二步 以user_id计算每个“用户”的2次event之间的来源媒介，计算会话
    session_channel = session_time.withColumn('pre_reffer_id',
                                              fn.lag(col("reffer_id"), 1).over(cookie_window))  # 上1条记录的来源
    session_channel = session_channel.withColumn('is_channel_new_session',
                                                 fn.when(col('reffer_id') != col('pre_reffer_id'), 1).otherwise(
                                                     0))  # 上1条记录的来源

    # 第三步 综合判断 is_time_new_session | is_channel_new_session，任意条件为1，则是新会话
    session_df = session_channel.withColumn('is_new_session', fn.when(
        (col('is_time_new_session') == 1) | (col('is_channel_new_session') == 1), 1).otherwise(0))
    return session_df


# 公用函数：计算session内各项指标
def process_session_metrics(df, cookie_window, session_window, session_window_raw):
    # 定义一个visit_id，方便后续的计算，基于user_id + 时间戳 组合而成
    session_df = df.withColumn('session_id', fn.sum("is_new_session").over(cookie_window))  # 跨visit会有重复
    session_df = session_df.withColumn("session_id", fn.dense_rank().over(Window.orderBy("user_id", "session_id"))
                                       # 跨visit不重复
                                       )

    # 访问起止时间
    session_df = session_df.withColumn('visit_start_time', fn.min(col("timestamp")).over(session_window))  # 访问开始时间
    session_df = session_df.withColumn('visit_end_time',
                                       fn.max(col("timestamp")).over(session_window_raw))  # 访问结束时间，使用无界窗口
    session_df = session_df.withColumn('is_pageview', fn.when(col("HIT_TYPE") == 'PAGE', 1).otherwise(
        0))  # 是否是pv事件，仅计算PAGE 类型的pv是否只有1个或更少
    session_df = session_df.withColumn('Newvisitstarttime',
                                       fn.from_unixtime(col('visit_start_time') / 1000, "yyyy-MM-dd HH:mm:ss").cast(
                                           'timestamp'))  # 新访问时间戳
    session_df = session_df.withColumn('Newvisitstarttime',
                                       col('Newvisitstarttime') + fn.expr('INTERVAL 8 HOURS'))  # 新访问时间戳，东八区时间显示

    # 计算session指标
    session_df = session_df.select(
        '*',
        col('visit_start_time').alias('visitID'),  # visitID，也就是访问开始时间戳
        fn.count(col("event_id")).over(session_window_raw).alias('totals_hits'),  # 访问内总互动次数
        ((col("visit_end_time") - col('visit_start_time')) / 1000).alias('timeOnSite'),  # 访问内总访问时间
        fn.sum(col("is_pageview")).over(session_window_raw).alias('pageviews'),  # 访问内总pv
        fn.lit(None).astype('int').alias('totals_transactions'),  # 订单量，原ec指标
    )
    # 计算是否为bounce session
    return session_df.withColumn('is_bounce', fn.when(session_df['pageviews'] <= 1, 1).otherwise(0))


# 公用函数：计算AID为主体内各项指标
def process_user_metrics(df):
    # 过滤出非空aid df
    unnull_df = df.filter(df['login_id'].isNull() == False). \
        filter(df['login_id'] != 'AID'). \
        where(fn.concat(df['source'], df['medium']).rlike('(?i)friend|wechat|moment|weixin|wx.qq|social'))

    # 基于session数据去重，每个session只保留1条记录
    unique_cols = ['user_id', 'login_id', 'date_str', 'session_id', 'pageviews', 'is_bounce', 'timeOnSite']
    unique_session_df = unnull_df[unique_cols].drop_duplicates(['session_id'])

    # 计算各个user指标
    agg_df = unique_session_df.groupBy('login_id', 'date_str').agg(
        fn.countDistinct('user_id').alias('Users'),  # UV量
        fn.countDistinct('session_id').alias('Sessions'),  # 会话数
        fn.sum('pageviews').alias('totalpageviews'),  # 总PV
        fn.sum('is_bounce').alias('bounce_sessions'),  # 跳出会话数
        fn.sum('timeOnSite').alias('totals_timeOnSite'),  # 总访问时长
    )
    agg_df = agg_df.withColumn('bounce_rate', col('bounce_sessions') / col('Sessions'))  # 跳出率

    return agg_df


# ETL模块，处理成8张表

def get_2022KR_LEADS_AIDLIST_Daily(df):
    df1 = df. \
        filter(df['AID'].isNull() == False). \
        filter(df['ec'] == "20220228_2022KR_900157"). \
        where(df['el'].rlike('%播放节点:15S%')). \
        select(
        col('AID'),
        col('date_str').alias('DATE'),
        col('STDSKUCODE'),
        col('CONTENT_ID'),
    )
    df2 = df. \
        filter(df['AID'].isNull() == False). \
        filter(df['ec'] == "20220228_2022KR_900157"). \
        filter(df['ea'] == "Slide"). \
        where(df['el'].rlike('菜谱详情页_菜谱%滑动%')). \
        select(
        col('AID'),
        col('date_str').alias('DATE'),
        col('STDSKUCODE'),
        col('CONTENT_ID'),
    )
    final_df = df1.join(df2, on=['AID', 'DATE', 'STDSKUCODE', 'CONTENT_ID'], how='inner'). \
        filter(col('CONTENT_ID').isNull() == False)
    return final_df.drop_duplicates()


def get_CHEFAPP_FACT_USER_INTERACTIONS(df):
    non_events = ['$AppRemoteConfigChanged',
                  '$WebStay',
                  '$AppInstall',
                  '$WebClick',
                  '$MPHide',
                  '$AppEnd',
                  '$AppClick',
                  '$WebPageLeave',
                  # '$MPViewScreen',
                  # '$SignUp',
                  '$MPShare',
                  '$WebPageLoad',
                  '$MPPageLeave',
                  '$ABTestTrigger',
                  '$AppStart',
                  '$AppPageLeave',
                  '$MPShow',
                  '$MPLaunch',
                  '$MPAddFavorites']
    return df.filter(df['AID'].isNull() == False). \
        where(~df['event'].isin(non_events)). \
        filter(col('app_name').isin(['群厨会APP', '厨师说APP', 'ChefApp'])). \
        select(
        col('FULL_VISITOR_ID'),
        col('CLIENTID'),
        col('AID'),
        col('visitID'),
        col('PAGE_GROUP1'),
        col('PAGE_GROUP2'),
        col('PAGE_GROUP3'),
        col('PAGE_TEMPLET'),
        col('PAGE_AREA'),
        col('app_name').alias('APPNAME'),
        col('SCREENNAME'),
        col('HIT_TYPE'),
        col('EVENT_CATEGORY'),
        col('EVENT_ACTION'),
        col('EVENT_LABEL'),
        col('EC_ACTION'),
        col('EVENT_TIME'),
    ).drop_duplicates()


def get_dto_session_fact(df):
    return df.select(
        col('FULL_VISITOR_ID').alias('fullVisitorId'),
        col('date_str').alias('DATE'),
        fn.lit(None).astype('int').alias('visitNumber'),
        col('Newvisitstarttime'),
        col('totals_hits').alias('totals.hits'),
        col('timeOnSite'),
        col('pageviews'),
        col('source'),
        col('medium'),
        col('campaign'),
        col('ad_content').alias('adContent'),
        col('keyword'),
        col('totals_transactions').alias('totals.transactions'),
    ).drop_duplicates()


def get_FACT_USER_INTERACTIONS(df):
    non_hosts = ['secure.unileverfoodsolutions.com.cn',
                 'stage.unileverfoodsolutions.com.cn',
                 'uat.unileverfoodsolutions.com.cn',
                 'stage-oauth.unileverfoodsolutions.com.cn',
                 'stagemember.unileverfoodsolutions.com.cn',
                 'stage-mirror.unileverfoodsolutions.com.cn',
                 'testonpack.unileverfoodsolutions.com.cn',
                 'community-stg.unileverfoodsolutions.com.cn',
                 'local.member.unileverfoodsolutions.com.cn',
                 'test-env1.jumbomart.cn',
                 'stage.publish.unileverfoodsolutions.com.cn',
                 'h5.wufae.com',
                 'localhost',
                 'www.ufs2.cn',
                 'p.gohalo.cn',
                 'ufs-test.beats-digital.com',
                 'www.ufs3.cn',
                 'api2.gerinn.com',
                 'p.gerinn.com',
                 'stage.author.unileverfoodsolutions.com.cn',
                 'app.gerinn.com',
                 'cdn.tcc.so',
                 '4swifi.com',
                 'dev-oauth.unileverfoodsolutions.com.cn',
                 'www.4swifi.com',
                 'tripobd.com',
                 'biotherm.nurunci.com',
                 'pt.pucanbt.com']
    non_events = ['$AppRemoteConfigChanged',
                  '$WebStay',
                  '$AppInstall',
                  '$WebClick',
                  '$MPHide',
                  '$AppEnd',
                  '$AppClick',
                  '$WebPageLeave',
                  # '$MPViewScreen',
                  # '$SignUp',
                  '$MPShare',
                  '$WebPageLoad',
                  '$MPPageLeave',
                  '$ABTestTrigger',
                  '$AppStart',
                  '$AppPageLeave',
                  '$MPShow',
                  '$MPLaunch',
                  '$MPAddFavorites']
    return df.filter(df['AID'].isNull() == False). \
        where(~df['host_name'].isin(non_hosts)). \
        where(~df['event'].isin(non_events)). \
        where(~df['app_name'].isin(['ChefApp'])). \
        filter(((df['ea'] != 'IniteDepth') & (df['ea'] != 'Scroll')) | (df['ea'].isNull() == True)). \
        select(
        col('FULL_VISITOR_ID'),
        col('CLIENTID'),
        col('AID'),
        col('visitID'),
        col('PAGE_GROUP1'),
        col('PAGE_GROUP2'),
        col('PAGE_GROUP3'),
        col('page_title').alias('PAGE_TITLE'),
        col('PAGE_TEMPLET'),
        col('PAGE_AREA'),
        col('host_name').alias('HOST_NAME'),
        col('page_path').alias('PAGE_PATH'),
        col('HIT_TYPE'),
        col('EVENT_CATEGORY'),
        col('EVENT_ACTION'),
        col('EVENT_LABEL'),
        col('EC_ACTION'),
        col('EVENT_TIME'),
        col('SEARCHKEYWORD'),
    ).drop_duplicates()


def get_ufs_cookieidAID(df):
    return df.filter(df['AID'].isNull() == False). \
        select(
        col('FULL_VISITOR_ID'),
        col('AID'),
    ).drop_duplicates()


def get_ufs_DailyWechat_AID(df):
    return df.filter(df['login_id'].isNull() == False). \
        select(
        col('login_id').alias('AID'),
        col('Users'),
        col('date_str').alias('date'),
        col('Sessions'),
        col('totalpageviews'),
        col('bounce_rate'),
        col('totals_timeOnSite'),
    ).drop_duplicates()


def get_ufs_new_session_fact(df):
    # 过滤出session的第一次互动
    first_events = df.filter(df['login_id'].isNull() == False). \
        filter(df['login_id'] != 'null').orderBy(['Newvisitstarttime']).drop_duplicates(
        ['session_id'])  # session_id全局唯一
    return first_events. \
        select(
        col('AID'),
        col('FULL_VISITOR_ID').alias('fullvisitorid'),
        col('date_str').alias('date'),
        col('visit_start_time').alias('visitStartTime'),
        col('Newvisitstarttime').alias('newvisitStartTime'),
        fn.lit(None).astype('int').alias('visitNumber'),
        col('reffer_id').alias('referID'),
        col('pageviews').alias('totalspageviews'),
        col('timeOnSite').alias('totalstimeOnSite'),
        col('is_newvisit').alias('totalsnewVisits'),
        col('is_bounce').alias('totalsbounces'),
        col('page_path').alias('hitspagepagePath'),
    ).drop_duplicates()


def get_ufs_referdim(df):
    return df.select(
        col('FULL_VISITOR_ID'),
        col('visitID'),
        col('reffer_id').alias('referID'),
        col('source').alias('SOURCE'),
        col('medium').alias('MEDIUM'),
        col('campaign').alias('CAMPAIGN'),
        col('ad_content').alias('ADCONTENT'),
        col('keyword').alias('KEYWORD'),
    ).drop_duplicates()
