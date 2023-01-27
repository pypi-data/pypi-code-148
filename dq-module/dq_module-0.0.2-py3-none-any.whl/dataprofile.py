from datetime import date
import time
from .commonutilities import *
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
except:
    pass


class DataProfile():
    def __init__(self, tables_list, interaction_between_tables, data_read_ob , data_write_ob, data_right_structure , job_id, no_of_partition=4, output_db_name="data_quality_output"):
        self.spark = SparkSession(SparkContext.getOrCreate())
        self.tables_list = tables_list
        self.interaction_between_tables = interaction_between_tables
        self.data_write_ob = data_write_ob
        self.data_read_ob=data_read_ob
        self.data_right_structure = data_right_structure
        self.no_of_partition = no_of_partition
        self.dataframes = read_dataset(self.tables_list, self.data_read_ob, self.no_of_partition)
        self.data_profiling_schema = StructType([StructField("job_id", StringType(), True),
                                      StructField("source_type",
                                                  StringType(), True),
                                      StructField(
                                          "layer", StringType(), True),
                                          StructField(
                                          "source_name", StringType(), True),
                                     StructField(
                                          "filename", StringType(), True),          
                                      StructField("column_name",
                                                  StringType(), True),
                                      StructField("column_type",
                                                  StringType(), True),
                                      StructField(
                                          "total_column_count", StringType(), True),
                                      StructField("total_row_count",
                                                  StringType(), True),
                                      StructField("min", StringType(), True),
                                      StructField("max", StringType(), True),
                                      StructField("avg", StringType(), True),
                                      StructField("sum", StringType(), True),
                                      StructField(
                                          "stddev", StringType(), True),
                                      StructField(
            "25th_per", StringType(), True),
            StructField(
            "50th_per", StringType(), True),
            StructField(
            "75th_per", StringType(), True),
            StructField("missing_count",
                        StringType(), True),
            StructField("unique_count",
                        StringType(), True),
            StructField("mode", StringType(), True),
            StructField("list_of_uniques",
                        StringType(), True),
            StructField("run_date", StringType(), True)
        ])
        self.output_db_name = output_db_name
        self.job_id = job_id

    def apply_data_profiling_to_column(self, df, source_type, layer, source_name,filename, column_to_be_checked, rows, columns):
        column_type = column_type_identifier(df, column_to_be_checked)
        list_of_uniq = self.list_of_uniques(df, column_to_be_checked)
        rundate = date.today().strftime("%Y/%m/%d")
        if column_type == "numerical":
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("Column_type"),
                                 lit(columns),
                                 lit(rows),
                                 min(column_to_be_checked).alias("min"),
                                 max(column_to_be_checked).alias("max"),
                                 avg(column_to_be_checked).alias("avg"),
                                 sum(column_to_be_checked).alias("sum"),
                                 stddev(column_to_be_checked).alias("stddev"),
                                 percentile_approx(
                                     column_to_be_checked, 0.25).alias("25th_per"),
                                 percentile_approx(
                                     column_to_be_checked, 0.50).alias("50th_per"),
                                 percentile_approx(
                                     column_to_be_checked, 0.75).alias("75th_per"),
                                 sum(when(col(column_to_be_checked).isNull(), 1).otherwise(
                                     0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(None).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date"))

        elif column_type == "categorical":
            mode = self.find_mode(df, column_to_be_checked)
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 sum(when(col(column_to_be_checked).isNull(), 1).otherwise(
                                     0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(mode).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date")
                                 )

        else:
            mode = self.find_mode(df, column_to_be_checked)
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 min(column_to_be_checked).alias("min"),
                                 max(column_to_be_checked).alias("max"),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 percentile_approx(column_to_be_checked,
                                                   0.25).alias("25th_per"),
                                 percentile_approx(column_to_be_checked,
                                                   0.50).alias("50th_per"),
                                 percentile_approx(column_to_be_checked,
                                                   0.75).alias("75th_per"),
                                 sum(when(col(column_to_be_checked).isNull(),
                                          1).otherwise(0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(mode).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date")
                                 )

        return result_data

    def find_mode(self, df, column_to_be_checked):
        df = df.filter(col(column_to_be_checked).isNotNull()
                       ).groupBy(column_to_be_checked).count()
        mode_val_count = df.agg(max("count")).take(1)[0][0]
        result = df.filter(col("count") == mode_val_count).select(
            column_to_be_checked).rdd.flatMap(lambda x: x).collect()
        return str(result)

    def list_of_uniques(self, df, column_to_be_checked):
        df=df.filter(col(column_to_be_checked).isNotNull())
        result = df.agg(collect_set(column_to_be_checked)).take(1)[0][0]
        return str(result[:10])
        
       # ----- Function takes the filepath of source_csv as an input and apply data profiling.
    def apply_data_profiling(self, source_config_df, write_consolidated_report = True):
        source_config = source_config_df.collect()
        new_tables = get_missing_tables(self.tables_list, source_config)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(new_tables,self.data_read_ob,self.no_of_partition)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}
        data_profiling_df = self.apply_data_profiling_to_table_list(source_config,write_consolidated_report)
        return data_profiling_df

    def apply_data_profiling_to_table_list(self, source_config , write_consolidated_report):
        combined_data_profiling_schema=StructType(self.data_profiling_schema.fields+[StructField("data_profiling_report_write_location",StringType(), True)])
        combined_data_profiling_report_df=self.spark.createDataFrame(data=[], schema=combined_data_profiling_schema)
        for table in source_config:
            try:

                data_profiling_data = []
                data_profiling_df = self.spark.createDataFrame(data=data_profiling_data, schema=self.data_profiling_schema)
                source = f'''{table["source_type"]}_{table["layer"]}_{table["source_name"]}_{table["filename"]}'''

                self.dataframes[source].cache()
                rows = self.dataframes[source].count()
                columns = len(self.dataframes[source].columns)
                for column in self.dataframes[source].columns:
                    result_df = self.apply_data_profiling_to_column(
                        self.dataframes[source], table["source_type"], table["layer"], table["source_name"],table["filename"], column, rows, columns)
                    data_profiling_df = data_profiling_df.union(result_df)

                if self.data_right_structure == 'file':
                    try:
                        data_profiling_folder_path = get_folder_structure(table,"data_profiling")
                                       
                    except Exception as e:
                        raise Exception(f"Incorrect folder path or container name not specified, {e}")  
                    
                    data_profiling_file_name = f"data_profiling_report_{source}{date.today().strftime('_%Y_%m_%d_') + time.strftime('%H_%M_%S', time.localtime())}"
                    data_profiling_report_file_path = self.data_write_ob.write(data_profiling_df, data_profiling_folder_path, data_profiling_file_name, table)
                    print(f"Data profiling report for {source} is uploaded successfully at : {data_profiling_report_file_path}")
                
                else:
                    data_profiling_report_file_path=self.data_write_ob.write(data_profiling_df, self.output_db_name, source)
                    print(f"Data profiling report for {source} is added successfully at : {data_profiling_report_file_path}")

                data_profiling_report_df=data_profiling_df.withColumn("data_profiling_write_location",lit(data_profiling_report_file_path))
                combined_data_profiling_report_df=combined_data_profiling_report_df.union(data_profiling_report_df)
            except Exception as e:
                rundate = date.today().strftime("%Y/%m/%d")
                data_profiling_report_df  = self.spark.createDataFrame(data=[(self.job_id,
                table["source_type"], table["layer"], table["source_name"], table["filename"],
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, lit(rundate), f'Failed to perform profiling, {e}')], schema=combined_data_profiling_schema) 
                combined_data_profiling_report_df=combined_data_profiling_report_df.union(data_profiling_report_df)
                continue
        
        if write_consolidated_report==True: 
          if self.data_right_structure == 'file' :
              output_report_folder_path = f"{source_config[0]['output_folder_structure']}/data_profiling/consolidated_report/"
              combine_profiling_file_name = f"combined_data_profiling_report_{date.today().strftime('_%Y_%m_%d_')}{time.strftime('%H_%M_%S', time.localtime())}"
              combined_data_profiling_report_path=self.data_write_ob.write(combined_data_profiling_report_df,output_report_folder_path, combine_profiling_file_name, source_config[0])
              print(f"Combined report is uploaded successfully at : {combined_data_profiling_report_path}")
          else :
              combined_data_profiling_report_path=self.data_write_ob.write(combined_data_profiling_report_df, self.output_db_name, 'combined_data_profiling_report')
              print(f"Combined report is added successfully at : {combined_data_profiling_report_path}")
        else:
          pass