import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession, DataFrame

import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session

class LegalRelationCase(unittest.TestCase):

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
        embeddings = WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models").setInputCols(
            "document", "tokens").setOutputCol("embeddings")

        posTagger = PerceptronModel.pretrained("pos_clinical", "en", "clinical/models").setInputCols("document",
                                                                                                     "tokens").setOutputCol(
            "posTags")

        nerTagger = MedicalNerModel.pretrained("ner_clinical", "en", "clinical/models").setInputCols("document",
                                                                                                     "tokens",
                                                                                                     "embeddings").setOutputCol(
            "nerTags")

        nerConverter = NerConverter().setInputCols("document", "tokens", "nerTags").setOutputCol("nerChunks")

        dependencyParser = DependencyParserModel.pretrained("dependency_conllu", "en").setInputCols("document",
                                                                                                    "posTags",
                                                                                                    "tokens").setOutputCol(
            "dependencies")

        reNerFilter = RENerChunksFilter().setRelationPairs(
            ["problem-test", "problem-treatment"]).setMaxSyntacticDistance(
            4).setDocLevelRelations(True).setInputCols("nerChunks", "dependencies").setOutputCol("RENerChunks")
        return Pipeline().setStages([
            documentAssembler,
            tokenizer,
            embeddings,
            posTagger,
            nerTagger,
            nerConverter,
            dependencyParser,
            reNerFilter,
            annoToFit,
        ]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        model = sparknlp_jsl.legal.RelationExtractionDLModel.pretrained("legre_whereas", "en",
                                                                        "legal/models")
        model.setOutputCol(
            "test_result").setPredictionThreshold(0.5).setInputCols("document", "RENerChunks").setCustomLabels(
            {"1": "CustomLabel"})
        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
