"""
streaming Kafka的处理、解析相关功能
"""

from pyspark.sql import functions as fn
from pyspark.sql.functions import col, get_json_object, from_unixtime, concat_ws, lit


# 根据需求，新请求从最新数据开始订阅。由于指定的group id，每次订阅将基于上次继续订阅。
def read_kafka(spark_ob, kafka_servers, kafka_topics, max_offset, unique_label):
    return spark_ob \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_servers) \
        .option("kafka.group.id", unique_label) \
        .option("kafka.session.timeout.ms", 30000) \
        .option("subscribe", kafka_topics) \
        .option("maxOffsetsPerTrigger", f"{max_offset}") \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .option("includeHeaders", "false") \
        .load()


# 处理消息
def process_streaming(events, filter_project, filter_events, start_date, end_date):
    # 获取基础数据
    # 提取公用字段值并转换为string类型
    events = events.withColumn('partition', col('partition').cast('string'))  # 分区，转字符串
    events = events.withColumn('offset', col('offset').cast('string'))  # 分区内消息的偏移量，转字符串
    events = events.withColumn('data', col('value').cast('string'))  # 将二进制value转换为字符串
    events = events.withColumn('properties', get_json_object(events['data'].cast('string'), '$.properties'))  # 提取属性
    events = events.withColumn('project', get_json_object(events['data'], '$.project'))  # 提取project
    # 过滤项目（仅包含正式环境数据）
    events = events.filter(events['project'] == filter_project)  # 只保留正式项目数据
    events = events.withColumn('t', get_json_object(events['data'], '$.time'))  # 提取时间戳，字符串格式，临时公用

    # 加工以及提取特定字段，并输出原始streaming消息
    events = events.select(
        # 公用字段
        # 生成事件标识
        concat_ws('_', col('project'), col('topic'), col('partition'), col('offset')).alias('event_id'),
        # 项目_topic_分区_偏移量，保证唯一消息值
        get_json_object(events['data'], '$.event').alias('event'),  # 事件名
        # 获取不同格式的时间戳字段
        from_unixtime(events['t'] / 1000, "yyyy-MM-dd HH:mm:ss").cast('timestamp').cast('date').alias('date'),
        # 日期，date格式。注意使用datetime的时区
        from_unixtime(events['t'] / 1000, "yyyy-MM-dd HH:mm:ss").cast('timestamp').alias('datetime'),  # 时间戳，datetime格式
        events['t'].cast('bigint').alias('timestamp'),  # 时间戳，bigint格式

        # 提取用户各种ID，从(data)中获取
        get_json_object(events['data'], '$.user_id').alias('user_id'),  # cookieID
        get_json_object(events['data'], '$.login_id').alias('login_id'),  # AID
        get_json_object(events['data'], '$.device_id').alias('device_id'),  # 设备ID

        # 提取事件参数，从(properties)中获取
        get_json_object(events['properties'], '$.Eventcategory').alias('ec'),  # 事件类型，同GA的EC
        get_json_object(events['properties'], '$.Eventlabel').alias('el'),  # 事件标志，同GA的EL
        get_json_object(events['properties'], '$.Eventaction').alias('ea'),  # 事件动作，同GA的EA
        get_json_object(events['properties'], '$.$event_duration').alias('event_duration'),  # 事件时长

        # 提取页面和域信息，从properties)中获取
        get_json_object(events['properties'], '$.Appname').alias('app_name'),  # 应用名称，区分不同的平台
        get_json_object(events['properties'], '$.Hostname').alias('host_name'),  # 域名
        get_json_object(events['properties'], '$.Pagepath').alias('page_path'),  # 页面路径
        get_json_object(events['properties'], '$.Pagetitle').alias('page_title'),  # 页面名称

        # 提取可变json属性，方便后续扩展
        col('properties'),

        # 增加各种时间标记
        from_unixtime(events['t'] / 1000, "yyyy-MM-dd HH:mm:ss").cast('timestamp').alias('process_datetime'),
        # kafka消息时间，该时间不等于消息中的行为时间 timestamp
        fn.current_timestamp().alias('insert_datetime')  # 系统处理时间，约等于入库时间

    )

    # 过滤event 以及 日期内的数据
    return events.where(~col('event').isin(filter_events)).filter(col('date') >= (lit(start_date)).cast('date')).filter(
        col('date') <= (lit(end_date)).cast('date'))


# 写库
def write_deltaLake(events, file_format, db_name, table_name, blob_path, partition_cols, max_file_size, unique_label,
                    mode='append'):
    events.coalesce(1).writeStream \
        .format(file_format) \
        .outputMode(mode) \
        .option("checkpointLocation", f"{blob_path}/{db_name}/{table_name}/{unique_label}/_checkpoints/") \
        .option("mergeSchema", 'true') \
        .option("delta.targetFileSize", max_file_size) \
        .option("path", f'{blob_path}/{db_name}/{table_name}') \
        .partitionBy(*partition_cols) \
        .toTable(f'{db_name}.{table_name}')
