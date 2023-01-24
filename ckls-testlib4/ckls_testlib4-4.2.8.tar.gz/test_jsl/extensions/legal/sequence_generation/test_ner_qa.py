import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
import sparknlp_jsl
from sparknlp_jsl.annotator import *
from sparknlp_jsl.finance.seq_generation.qa_ner_generator import FinanceNerQuestionGenerator
from sparknlp_jsl.legal.seq_generation.qa_ner_generator import LegalNerQuestionGenerator
from test_jsl.extensions.utils import get_spark_session


class LegalNerQACase(unittest.TestCase):
    spark = get_spark_session()
    smallCorpus: DataFrame = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.smallCorpus).select("test_result.result").show()

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        document_assembler = DocumentAssembler() \
            .setInputCol("text") \
            .setOutputCol("document")

        sentence_detector = SentenceDetectorDLModel.pretrained("sentence_detector_dl", "en") \
            .setInputCols(["document"]) \
            .setOutputCol("sentence")

        tokenizer = Tokenizer() \
            .setInputCols(["sentence"]) \
            .setOutputCol("token")

        word_embeddings = WordEmbeddingsModel.pretrained("glove_100d") \
            .setInputCols(["document", "token"]) \
            .setOutputCol("embeddings")
        ner_model = NerDLModel.pretrained("finnish_ner_6B_100", "fi") \
            .setInputCols(["document", "token", "embeddings"]) \
            .setOutputCol("ner")

        ner_converter = NerConverter() \
            .setInputCols(["sentence", "token", "ner"]) \
            .setOutputCol("ner_chunk")

        return Pipeline().setStages(
            [
                document_assembler,
                sentence_detector,
                tokenizer,
                word_embeddings,
                ner_model,
                ner_converter,
                annoToFit,
            ]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        self.buildAndFitAndTest(LegalNerQuestionGenerator()
                                .setInputCols("ner_chunk")
                                .setEntities1(["COMPANY"])
                                .setEntities2(["OBJECT"])
                                .setStrategyType("Combined")
                                .setOutputCol("test_result"))


if __name__ == '__main__':
    unittest.main()
