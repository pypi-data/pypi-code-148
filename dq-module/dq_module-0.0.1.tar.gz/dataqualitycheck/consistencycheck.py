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


class ConsistencyCheck():
    def __init__(self, tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure, job_id, output_db_name="data_quality_output", no_of_partition=4):
        self.spark = SparkSession(SparkContext.getOrCreate())
        self.data_read_ob = data_read_ob
        self.tables_list = tables_list
        self.interaction_between_tables = interaction_between_tables
        self.data_write_ob = data_write_ob
        self.data_right_structure = data_right_structure
        self.no_of_partition = no_of_partition
        self.dataframes = read_dataset(
            self.tables_list, self.data_read_ob, self.no_of_partition)
        self.output_db_name = output_db_name
        self.job_id = job_id
        self.consistency_schema = StructType([StructField("job_id", StringType(), True),
                                              StructField(
                                                  "container_name", StringType(), True),
                                              StructField(
                                                  "base_table_source_type", StringType(), True),
                                              StructField(
                                                  "base_table_layer", StringType(), True),
                                              StructField(
                                                  "base_table_source_name", StringType(), True),
                                              StructField(
                                                  "base_table_filename", StringType(), True),
                                              StructField(
                                                  "base_table_sum", StringType(), True),
                                              StructField(
                                                  "mapped_table_source_type", StringType(), True),
                                              StructField(
                                                  "mapped_table_layer", StringType(), True),
                                              StructField(
                                                  "mapped_table_source_name", StringType(), True),
                                              StructField(
                                                  "mapped_table_filename", StringType(), True),
                                              StructField(
                                                  "mapped_table_sum", StringType(), True),
                                              StructField(
                                                  "description", StringType(), True),
                                              StructField(
                                                  "difference", StringType(), True),
                                              StructField(
                                                  "percentage_difference", StringType(), True),
                                              StructField(
                                                  "run_date", StringType(), True),
                                              ])
        self.consistency_check_summary = []

    def consistency_check(self, rule):
        base_table_source = f'''{rule["base_table_source_type"]}_{rule["base_table_layer"]}_{rule["base_table_source_name"]}_{rule["base_table_filename"]}'''
        base_table = self.dataframes[base_table_source]
        mapped_table_source = f'''{rule["mapped_table_source_type"]}_{rule["mapped_table_layer"]}_{rule["mapped_table_source_name"]}_{rule["mapped_table_filename"]}'''
        mapped_table = self.dataframes[mapped_table_source]
        base_table_col_name = rule["base_table_col_name"]
        mapped_table_col_name = rule["mapped_table_col_name"]
        rundate = date.today().strftime("%Y/%m/%d")
        base_table_source = f'''{rule["base_table_source_type"]}_{rule["base_table_layer"]}_{rule["base_table_source_name"]}_{rule["base_table_filename"]}'''
        mapped_table_source = f'''{rule["mapped_table_source_type"]}_{rule["mapped_table_layer"]}_{rule["mapped_table_source_name"]}_{rule["mapped_table_filename"]}'''
        base_table_sum = ''
        mapped_table_sum = ''
        difference_col = ''
        per_difference_col = ''
        desc = ''
        try:
            base_table_col_type = column_type_identifier(
                base_table, base_table_col_name)
            mapped_table_col_type = column_type_identifier(
                mapped_table, mapped_table_col_name)
            if base_table_col_type == mapped_table_col_type:
                if base_table_col_type == 'numerical':
                    base_table_sum = base_table.select(
                        sum(base_table_col_name)).take(1)[0][0]
                    mapped_table_sum = mapped_table.select(
                        sum(mapped_table_col_name)).take(1)[0][0]
                else:
                    base_table_sum = base_table.select(
                        countDistinct(base_table_col_name)).take(1)[0][0]
                    mapped_table_sum = mapped_table.select(
                        countDistinct(mapped_table_col_name)).take(1)[0][0]

                difference_col = base_table_sum - mapped_table_sum
                if difference_col == 0:
                    per_difference_col = 0.0
                else:
                    per_difference_col = (difference_col / base_table_sum)*100

                 # QUALITY DISCRIPTION COLUMN
                desc = str("Difference check between " + base_table_col_name + " and " +
                           mapped_table_col_name + " in tables " + base_table_source + " and " + mapped_table_source)

            else:
                desc = f"consistency check cannot be applicable for {base_table_col_name} and {mapped_table_col_name} columns"
        except Exception as e:
            desc = str(e)

        res = (self.job_id,
               rule["container_name"],
               rule["base_table_source_type"],
               rule["base_table_layer"],
               rule["base_table_source_name"],
               rule["base_table_filename"],
               str(base_table_sum),
               rule["mapped_table_source_type"],
               rule["mapped_table_layer"],
               rule["mapped_table_source_name"],
               rule["mapped_table_filename"],
               str(mapped_table_sum),
               str(desc),
               str(difference_col),
               str(per_difference_col),
               rundate)
        self.consistency_check_summary.append(res)
        return res

    def table_info(self, tables_list, rule_set):
        new_tables = {}
        for rule in rule_set:
            base_table_source = f'''{rule["base_table_source_type"]}_{rule["base_table_layer"]}_{rule["base_table_source_name"]}_{rule["base_table_filename"]}'''
            mapped_table_source = f'''{rule["mapped_table_source_type"]}_{rule["mapped_table_layer"]}_{rule["mapped_table_source_name"]}_{rule["mapped_table_filename"]}'''
            if base_table_source not in tables_list.keys():
                new_tables[base_table_source] = {"read_connector_method": rule["read_connector_method"],
                                                 "container_name": rule["container_name"],
                                                 "latest_file_path": rule["base_table_file_path"],
                                                 "source_name": rule["base_table_source_name"],
                                                 "source_type": rule["base_table_source_type"],
                                                 "layer": rule["base_table_layer"],
                                                 "filename": rule["base_table_filename"]
                                                 }

            if mapped_table_source not in tables_list.keys():
                new_tables[mapped_table_source] = {"read_connector_method": rule["read_connector_method"],
                                                   "container_name": rule["container_name"],
                                                   "latest_file_path": rule["mapped_table_file_path"],
                                                   "source_name": rule["mapped_table_source_name"],
                                                   "source_type": rule["mapped_table_source_type"],
                                                   "layer": rule["mapped_table_layer"],
                                                   "filename": rule["mapped_table_filename"]
                                                   }
        return new_tables

    def apply_consistency_check(self, rule_config_df):
        rule_set = rule_config_df.collect()
        new_tables = self.table_info(self.tables_list, rule_set)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(
            new_tables, self.data_read_ob, self.no_of_partition)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}

        test_summary = []
        try:
            for rule in rule_set:
                result_df = self.consistency_check(rule)
                test_summary.append(result_df)

            summary_df = self.spark.createDataFrame(
                data=test_summary, schema=self.consistency_schema)
            summary_df.display()
            if self.data_right_structure == 'file':
                report_folder_path = f'''{rule["output_folder_structure"]}{rule["base_table_source_type"]}_{rule["base_table_layer"]}_{rule["base_table_source_name"]}_{rule["base_table_filename"]}_{rule["base_table_col_name"]}_{rule["mapped_table_source_type"]}_{rule["mapped_table_layer"]}_{rule["mapped_table_source_name"]}_{rule["mapped_table_filename"]}_{rule["mapped_table_col_name"]}/'''
                file_name = f"consistency_check_report{date.today().strftime('_%Y_%m_%d_') + time.strftime('%H_%M_%S', time.localtime())}"
                report_file_path = self.data_write_ob.write(
                    summary_df, report_folder_path, file_name, rule)
                print(
                    f"Data consistency report is uploaded successfully at : {report_file_path}")
            else:
                report_file_path = self.data_write_ob.write(
                    summary_df, self.output_db_name, 'consistency_check')
                print(
                    f"Data consistency report is added successfully at : {report_file_path}")
        except Exception as e:
            raise Exception(e)
