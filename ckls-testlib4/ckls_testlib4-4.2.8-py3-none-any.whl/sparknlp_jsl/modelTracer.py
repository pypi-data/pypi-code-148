from pyspark.ml import Pipeline
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, udf
from pyspark.sql.types import StringType, MapType
from datetime import datetime


class ModelTracer(object):
    def addUidCols(self, pipeline: Pipeline, df: DataFrame):
        """This functions adds models uids and timestamp to the output df as a new columns

        Parameters
        ----------
        pipelineModel : The pipeline to extract models from
        df : The dataframe to add the columns to
        """
        uid_columns = []
        for stage in pipeline.getStages():
            uid_columns.append((stage.uid[:stage.uid.rindex('_')].lower() + "_model_uid", stage.uid))
        timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M')

        @udf(returnType=MapType(StringType(), StringType()))
        def upperCase(str):
            return {"uid": str, "timestamp": timestamp}

        for column in uid_columns:
            df = df.withColumn(column[0], upperCase(lit(column[1])))
        return df
