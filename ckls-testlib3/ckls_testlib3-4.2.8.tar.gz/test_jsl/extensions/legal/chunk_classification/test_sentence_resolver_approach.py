import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from sparknlp import Doc2Chunk

import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session

class LegalSentenceResolveApproachCase(unittest.TestCase):
    spark = get_spark_session()
    data = spark.read.load("../src/test/resources/resolution/snomed_100.parquet")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.data).select("test_result.result").show()

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        # create a basic pipeline for annoToFit and return the fitted pipeModel
        document = DocumentAssembler().setInputCol("description").setOutputCol("document")
        doc2chunk = Doc2Chunk().setInputCols("document").setOutputCol("chunk")
        token = Tokenizer().setInputCols("document").setOutputCol("token")
        bertEmbeddings = BertSentenceEmbeddings.pretrained().setInputCols("document").setOutputCol("bert_embeddings")
        return Pipeline().setStages(
            [document, doc2chunk, token, bertEmbeddings,  annoToFit]).fit(self.data)

    def test_pretrained_model(self):
        model = sparknlp_jsl.legal.SentenceEntityResolverApproach() \
            .setNeighbours(100) \
            .setThreshold(1000) \
            .setInputCols("bert_embeddings") \
            .setNormalizedCol("description_normalized") \
            .setLabelCol("code") \
            .setOutputCol("test_result") \
            .setDistanceFunction("EUCLIDEAN") \
            .setCaseSensitive(False)
        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
