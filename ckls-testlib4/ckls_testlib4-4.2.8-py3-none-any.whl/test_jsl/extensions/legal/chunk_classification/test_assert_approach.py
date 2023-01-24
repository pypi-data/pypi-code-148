import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql.types import IntegerType
import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session


class LegalAssertApproachCase(unittest.TestCase):
    spark = get_spark_session()
    train_data = spark.read.option("header", "true").csv("../src/test/resources/rsAnnotations-1-120-random.csv")
    train_data = train_data.withColumn("start", train_data["start"].cast(IntegerType()))
    train_data = train_data.withColumn("end", train_data["end"].cast(IntegerType()))
    test_data = spark.createDataFrame([
        (1, "Has a past history of gastroenteritis and stomach pain, however patient shows no stomach pain now."),
        (2, "We don't care about gastroenteritis here, but we do care about heart failure. "),
        (3, "Test for asma, no asma.")
    ]).toDF("id", "text")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.test_data).select("test_result.result").show()

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        document_assembler = DocumentAssembler().setInputCol('text').setOutputCol('document')
        sentence_detector = SentenceDetectorDLModel.pretrained().setInputCols(["document"]).setOutputCol("sentence")
        tokenizer = Tokenizer().setInputCols("sentence").setOutputCol("token")
        POSTag = PerceptronModel.pretrained().setInputCols("sentence", "token").setOutputCol("pos")
        chunker = Chunker().setInputCols(["pos", "sentence"]).setOutputCol("chunk").setRegexParsers(["(<NN>)+"])
        pubmed = WordEmbeddingsModel.pretrained().setInputCols("sentence", "token").setOutputCol(
            "embeddings").setCaseSensitive(False)
        return Pipeline().setStages(
            [document_assembler, sentence_detector, tokenizer, POSTag, chunker, pubmed, annoToFit]).fit(self.train_data)

    def test_train_model(self):
        model = sparknlp_jsl.legal.AssertionDLApproach() \
            .setInputCols("sentence", "chunk", "embeddings") \
            .setOutputCol("test_result") \
            .setStartCol("start") \
            .setEndCol("end") \
            .setLabelCol("label") \
            .setLearningRate(0.01) \
            .setDropout(0.15) \
            .setBatchSize(16) \
            .setEpochs(3) \
            .setScopeWindow([9, 15]) \
            .setValidationSplit(0.2) \
            .setIncludeConfidence(True)
        self.buildAndFitAndTest(model)


if __name__ == '__main__':
    unittest.main()
