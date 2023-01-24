import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
from sparknlp import Doc2Chunk
import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session



class FinanceChunkMapperApproachCase(unittest.TestCase):
    spark = get_spark_session()

    smallCorpus: DataFrame = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.smallCorpus).select("test_result.result").show()


    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        # create a basic pipeline for annoToFit and return the fitted pipeModel
        documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
        chunk = Doc2Chunk().setInputCols("document").setOutputCol("chunk")
        return Pipeline().setStages([documentAssembler, chunk, annoToFit]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        model = sparknlp_jsl.finance.chunk_classification.ChunkMapperApproach() \
            .setInputCols("chunk") \
            .setOutputCol("test_result") \
            .setDictionary("../src/test/resources/chunkmapper/mapper.json") \
            .setRel("action")

        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
