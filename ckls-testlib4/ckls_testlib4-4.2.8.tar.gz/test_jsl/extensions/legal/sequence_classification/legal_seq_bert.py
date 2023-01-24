import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

from sparknlp_jsl import legal as fin
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session


class LegalTokenBertCase(unittest.TestCase):
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
        return Pipeline().setStages([documentAssembler, tok, annoToFit]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        model = legal.LegalBertForSequenceClassification.pretrained("legclf_bert_judgements_argtype", "en", "legal/models").setInputCols("document", "token").setOutputCol(
            "test_result")
        self.buildAndFitAndTest(model)

    def test_quick(self):

        legal.LegalBertForTokenClassification.pretrained("finner_arabert_arabic", "ar", "legal/models") \
            .setInputCols("token", "document") \
            .setOutputCol("label")

if __name__ == '__main__':
    unittest.main()
