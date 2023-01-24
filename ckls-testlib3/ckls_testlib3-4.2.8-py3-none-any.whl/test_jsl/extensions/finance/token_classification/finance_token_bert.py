import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session
import sparknlp_jsl.finance.token_classification


class FinanceTokenBertCase(unittest.TestCase):
    spark = get_spark_session()
    smallCorpus: DataFrame = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def _testSaveAndReloadPipe(self, pipe: PipelineModel) -> PipelineModel:
        pipe.save(self.pipeSavePath)
        reloadedPipe = PipelineModel.load(self.pipeSavePath)
        self._testPipe(reloadedPipe)
        return reloadedPipe

    def buildAndFitAndTest(self, annoToFitAndTest):
        self.buildAndFit(self.buildAndFit(annoToFitAndTest)).transform(self.smallCorpus).select('test_result').show()

    def buildAndFit(self, annoToFit) -> PipelineModel:
        documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
        tok = Tokenizer().setInputCols("document").setOutputCol("token")
        return Pipeline().setStages([documentAssembler, tok, annoToFit]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        model = sparknlp_jsl.finance.FinanceBertForTokenClassification \
            .pretrained("finner_bert_roles", "en", "finance/models").setInputCols("document","token").setOutputCol('test_result')
        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
