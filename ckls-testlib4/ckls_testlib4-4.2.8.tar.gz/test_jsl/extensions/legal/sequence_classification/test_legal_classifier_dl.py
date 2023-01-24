from pyspark.ml import PipelineModel
import unittest
from pyspark.ml import PipelineModel

from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session



class LegalClassifierDLCase(unittest.TestCase):
    spark = get_spark_session()
    data = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def test_pretrained_model(self):
        # TODO
        pass

if __name__ == '__main__':
    unittest.main()
