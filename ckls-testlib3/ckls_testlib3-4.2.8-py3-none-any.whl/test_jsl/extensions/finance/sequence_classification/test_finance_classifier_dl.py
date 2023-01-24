from pyspark.ml import PipelineModel, Pipeline
import unittest
from pyspark.ml import PipelineModel

from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session



class FinanceClassifierDLCase(unittest.TestCase):
    spark = get_spark_session()
    data = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def test_pretrained_model(self):
        model = finance.FinanceClassifierDLModel \
            .pretrained("finclf_exhibits_item", "en", "finance/models").setInputCols(
            ["sentence_embeddings"]).setOutputCol("category")
        useEmbeddings = UniversalSentenceEncoder.pretrained() \
            .setInputCols("document") \
            .setOutputCol("sentence_embeddings")

        documentAssembler = DocumentAssembler() \
            .setInputCol("text") \
            .setOutputCol("document")

        pipeline = Pipeline() \
            .setStages([
            documentAssembler,
            useEmbeddings,
            model
        ])

        result = pipeline.fit(self.data).transform(self.data)
        result.show()
        print(model)



if __name__ == '__main__':
    unittest.main()
