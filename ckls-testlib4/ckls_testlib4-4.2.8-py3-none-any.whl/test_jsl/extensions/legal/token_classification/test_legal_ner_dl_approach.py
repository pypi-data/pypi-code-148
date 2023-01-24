import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from sparknlp.training import CoNLL

import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session
class LegalNerApproachCase(unittest.TestCase):
    spark = get_spark_session()
    conll = CoNLL()
    train_data = conll.readDataset(spark=spark, path="../src/test/resources/conll2003/eng.testa").limit(10)
    test_data = conll.readDataset(spark=spark, path="../src/test/resources/conll2003/eng.testa").limit(100)
    test_data_parquet_path = "./test_data_parquet"

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.train_data).select("test_result.result").show()

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        # create a basic pipeline for annoToFit and return the fitted pipeModel
        emb = BertEmbeddings.pretrained("bert_embeddings_sec_bert_base", "en") \
            .setInputCols(["sentence", "token"]) \
            .setOutputCol("embeddings")
        return Pipeline().setStages([emb, annoToFit]).fit(self.train_data)

    def test_pretrained_model(self):
        model = sparknlp_jsl.legal.LegalNerApproach() \
            .setInputCols(["sentence", "token", "embeddings"]) \
            .setLabelColumn("label") \
            .setOutputCol("test_result") \
            .setMaxEpochs(2) \
            .setLr(0.003) \
            .setBatchSize(8) \
            .setRandomSeed(0) \
            .setEvaluationLogExtended(False) \
            .setEnableOutputLogs(False) \
            .setIncludeConfidence(True)

        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
