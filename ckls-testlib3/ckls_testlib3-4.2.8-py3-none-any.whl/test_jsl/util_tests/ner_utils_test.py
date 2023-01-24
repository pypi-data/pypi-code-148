import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
import sparknlp_jsl
from sparknlp_jsl.annotator import *

from sparknlp_jsl.legal.chunk_classification.deid.document_hashcoder import LegalDocumentHashCoder
from sparknlp_jsl.utils.ner_utils import get_charts, loss_plot, evaluate
from test_jsl.extensions.utils import get_spark_session
from test_jsl.util import SparkContextForTest


class NerUtilCase(unittest.TestCase):
    spark = SparkContextForTest.spark
    testDS = spark.sparkContext.parallelize(
        [("Has  gastroenteritis and stomach pain at 12/10/2008.", "A001")]).toDF(
        ["text", "patientID"])

    # TODO TESTS
    def test_conll_evaluate(self):
        get_charts()

    def test_loss_plot(self):
        loss_plot()

    def test_evaluate(self):
        evaluate()


if __name__ == '__main__':
    unittest.main()
