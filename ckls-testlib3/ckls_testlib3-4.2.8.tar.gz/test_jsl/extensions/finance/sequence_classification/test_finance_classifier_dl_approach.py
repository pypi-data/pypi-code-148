from pyspark.ml import PipelineModel
import unittest
from pyspark.ml import PipelineModel

from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session

from sparknlp_jsl.annotator import finance


class FinanceClassifierDLApproachCase(unittest.TestCase):
    spark = get_spark_session()
    smallCorpus = spark.read.option("header", "true").csv("../src/test/resources/classifier/sentiment.csv")

    data = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def test_approach_model(self):
        model = finance.FinanceClassifierDLApproach() \
                 .setInputCols("sentence_embeddings") \
                 .setOutputCol("test_result").setLabelColumn('label')
        useEmbeddings = UniversalSentenceEncoder.pretrained() \
            .setInputCols("document") \
            .setOutputCol("sentence_embeddings")

        documentAssembler = DocumentAssembler() \
            .setInputCol("text") \
            .setOutputCol("document")

        from pyspark.ml import Pipeline
        pipeline = Pipeline(stages=[
            documentAssembler,
            useEmbeddings,
            model
        ])

        result = pipeline.fit(self.smallCorpus).transform(self.smallCorpus)
        result.select('test_result').show()


if __name__ == '__main__':
    unittest.main()
