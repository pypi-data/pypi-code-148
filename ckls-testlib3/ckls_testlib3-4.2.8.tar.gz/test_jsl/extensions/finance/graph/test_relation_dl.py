import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session

class FinanceRelationCase(unittest.TestCase):
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

        embeddings = BertEmbeddings.pretrained("bert_embeddings_sec_bert_base", "en") \
            .setInputCols(["sentence", "token"]) \
            .setOutputCol("embeddings")

        ner_model = finance.FinanceNerModel().pretrained('finner_org_per_role_date', 'en', 'finance/models') \
            .setInputCols(["sentence", "token", "embeddings"]) \
            .setOutputCol("ner")

        ner_converter = NerConverter() \
            .setInputCols(["sentence", "token", "ner"]) \
            .setOutputCol("ner_chunk")

        pos = PerceptronModel.pretrained() \
            .setInputCols(["sentence", "token"]) \
            .setOutputCol("pos")

        dependency_parser = DependencyParserModel().pretrained("dependency_conllu", "en") \
            .setInputCols(["sentence", "pos", "token"]) \
            .setOutputCol("dependencies")

        re_ner_chunk_filter = RENerChunksFilter() \
            .setInputCols(["ner_chunk", "dependencies"]) \
            .setOutputCol("re_ner_chunk") \
            .setRelationPairs(["PERSON-ROLE, ORG-ROLE, DATE-ROLE, PERSON-ORG"]) \
            .setMaxSyntacticDistance(5)

        return Pipeline().setStages(
            [
                document_assembler,
                sentence_detector,
                tokenizer,
                embeddings,
                ner_model,
                ner_converter,
                pos,
                dependency_parser,
                re_ner_chunk_filter,
                annoToFit,
            ]).fit(self.smallCorpus)

    def test_pretrained_model2(self):
        anno_cls_to_test = sparknlp_jsl.finance.RelationExtractionDLModel
        model = anno_cls_to_test.pretrained("finre_acquisitions_subsidiaries_md", "en", "finance/models") \
            .setInputCols(["re_ner_chunk", "sentence"]) \
            .setOutputCol("test_result") \
            .setPredictionThreshold(0.5)
        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
