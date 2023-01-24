import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
import sparknlp_jsl
from sparknlp_jsl.annotator import *
from sparknlp_jsl.finance.chunk_classification.deid.document_hashcoder import FinanceDocumentHashCoder
from test_jsl.extensions.utils import get_spark_session


class FinanceDocHashCoderTestCase(unittest.TestCase):
    spark = get_spark_session()
    testDS = spark.sparkContext.parallelize(
        [("Has  gastroenteritis and stomach pain at 12/10/2008.", "A001")]).toDF(
        ["text", "patientID"])

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.testDS).select("test_result.result").show()

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        document_assembler = DocumentAssembler() \
            .setInputCol("text") \
            .setOutputCol("document")

        return Pipeline().setStages(
            [
                document_assembler,
                annoToFit,
            ]).fit(self.testDS)

    def test_pretrained_model(self):
        self.buildAndFitAndTest(FinanceDocumentHashCoder() \
                                .setInputCols("document") \
                                .setOutputCol("test_result") \
                                .setPatientIdColumn("patientID") \
                                .setRangeDays(10) \
                                .setNewDateShift("new_date")
                                )


if __name__ == '__main__':
    unittest.main()
