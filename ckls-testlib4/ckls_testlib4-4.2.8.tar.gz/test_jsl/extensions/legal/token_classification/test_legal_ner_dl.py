import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session
import sparknlp_jsl.legal.token_classification

class LegalNerDlCase(unittest.TestCase):
    spark = get_spark_session()
    smallCorpus: DataFrame = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.smallCorpus).select("test_result.result").show()


    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
        tokenizer = Tokenizer().setInputCols("document").setOutputCol("tokens")
        embeddings = RoBertaEmbeddings.pretrained("roberta_embeddings_legal_roberta_base", "en").setInputCols(["document", "tokens"]).setOutputCol("embeddings")
        return Pipeline().setStages([
            documentAssembler,
            tokenizer,
            embeddings,
            annoToFit,
        ]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        model = legal.LegalNerModel.\
            pretrained("legner_whereas", "en", "legal/models")\
            .setInputCols("document", "tokens","embeddings").setOutputCol("test_result")
        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
