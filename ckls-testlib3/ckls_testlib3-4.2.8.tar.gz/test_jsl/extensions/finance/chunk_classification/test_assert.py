import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session


class FinanceAssertCase(unittest.TestCase):
    spark = get_spark_session()
    smallCorpus: DataFrame = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.smallCorpus).select("test_result.result").show()

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
        tok = Tokenizer().setInputCols("document").setOutputCol("token")
        POSTag = PerceptronModel.pretrained().setInputCols("document", "token").setOutputCol("pos")
        chunker = Chunker().setInputCols("pos", "document").setOutputCol("chunk").setRegexParsers(["(<NN>)+"])
        emb = BertEmbeddings.pretrained("bert_embeddings_sec_bert_base", "en") \
            .setInputCols("token", "document").setOutputCol("emb")
        return Pipeline().setStages([documentAssembler, tok, POSTag, chunker, emb, annoToFit]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        model = sparknlp_jsl.finance.AssertionDLModel\
            .pretrained("finassertion_time", "en", "finance/models")\
            .setInputCols("document", "chunk", "emb")\
            .setOutputCol("test_result")
        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
