import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session

class LegalTokenBertCase(unittest.TestCase):
    folder = "/leg_zero_ner"
    # spark = get_spark_session()
    import sparknlp_jsl
    spark = get_spark_session()
    # spark = sparknlp_jsl()


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
        get_spark_session()
        anno_cls_to_test = legal.ZeroShotNerModel
        model = anno_cls_to_test.pretrained("legner_roberta_zeroshot", "en", "legal/models") \
            .setInputCols(["document", "token"]) \
            .setOutputCol("test_result") \
            .setEntityDefinitions(
            {
                "DATE": ['When was the company acquisition?', 'When was the company purchase agreement?'],
                "ORG": ["Which company was acquired?"],
                "PRODUCT": ["Which product?"],
                "PROFIT_INCREASE": ["How much has the gross profit increased?"],
                "REVENUES_DECLINED": ["How much has the revenues declined?"],
                "OPERATING_LOSS_2020": ["Which was the operating loss in 2020"],
                "OPERATING_LOSS_2019": ["Which was the operating loss in 2019"]
            })

        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
