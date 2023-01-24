import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session


class LegalZeroShotCase(unittest.TestCase):
    spark = get_spark_session()
    smallCorpus: DataFrame = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.smallCorpus).select("test_result.result").show()

    def _testSaveAndReloadPipe(self, pipe: PipelineModel) -> PipelineModel:
        pipe.save(self.pipeSavePath)
        reloadedPipe = PipelineModel.load(self.pipeSavePath)
        self._testPipe(reloadedPipe)
        return reloadedPipe

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")

        tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("tokens")

        sentencer = SentenceDetector().setInputCols(["document"]).setOutputCol("sentences")

        embeddings = WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models").setInputCols(
            ["sentences", "tokens"]).setOutputCol("embeddings")

        posTagger = PerceptronModel.pretrained("pos_clinical", "en", "clinical/models").setInputCols(
            ["sentences", "tokens"]).setOutputCol("posTags")

        nerTagger = MedicalNerModel.pretrained("ner_clinical", "en", "clinical/models").setInputCols(
            ["sentences", "tokens", "embeddings"]).setOutputCol("nerTags")

        nerConverter = NerConverter().setInputCols(["sentences", "tokens", "nerTags"]).setOutputCol("nerChunks")

        dependencyParser = DependencyParserModel.pretrained("dependency_conllu", "en").setInputCols(
            "document", "posTags", "tokens").setOutputCol("dependencies")

        reNerFilter = RENerChunksFilter().setRelationPairs(
            ["problem-test", "problem-treatment"]).setMaxSyntacticDistance(4).setDocLevelRelations(False).setInputCols(
            ["nerChunks", "dependencies"]).setOutputCol("RENerChunks")
        return Pipeline().setStages(
            [documentAssembler,
             sentencer,
             tokenizer,
             embeddings,
             posTagger,
             nerTagger,
             nerConverter,
             dependencyParser,
             reNerFilter,
             annoToFit, ]
        ).fit(self.smallCorpus)

    def test_pretrained_model(self):
        model = finance.ZeroShotRelationExtractionModel.pretrained("legre_zero_shot", "en",
                                                                   "legal/models").setInputCols(
            "document", "RENerChunks").setOutputCol("test_result").setRelationalCategories(
            {
                "GRANTS_TO": ["{OBLIGATION_SUBJECT} grants {OBLIGATION_INDIRECT_OBJECT}"],
                "GRANTS": ["{OBLIGATION_SUBJECT} grants {OBLIGATION_ACTION}"],
            })
        finance.ZeroShotRelationExtractionModel.set

        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
