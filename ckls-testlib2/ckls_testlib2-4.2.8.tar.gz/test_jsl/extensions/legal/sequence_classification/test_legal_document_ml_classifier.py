from pyspark.ml import PipelineModel, Pipeline
import unittest
from pyspark.ml import PipelineModel

from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session

from sparknlp_jsl.annotator import finance


class FinanceClassifierDLApproachCase(unittest.TestCase):
    spark = get_spark_session()

    def test_svm(self):
        train = self.spark.read.option("header", "true").option("timestampFormat", "yyyy/MM/dd HH:mm:ss ZZ") \
            .csv("../src/test/resources/classification/logreg.csv").where("set='train'")
        test = self.spark.read.option("header", "true").option("timestampFormat", "yyyy/MM/dd HH:mm:ss ZZ") \
            .csv("../src/test/resources/classification/logreg.csv").where("set='test'")

        document = DocumentAssembler().setInputCol("text").setOutputCol("document")

        token = Tokenizer().setInputCols("document").setOutputCol("token")

        textMatcher = TextMatcher() \
            .setEntities("../src/test/resources/classification/textmatcher.csv", ReadAs.TEXT) \
            .setCaseSensitive(False) \
            .setMergeOverlapping(True) \
            .setInputCols("document", "token") \
            .setOutputCol("chunk")

        chunkTokenizer = ChunkTokenizer() \
            .setInputCols("chunk") \
            .setOutputCol("chunk_token")

        pipeline = Pipeline().setStages([document, token, textMatcher, chunkTokenizer]).fit(train)
        readyTrain = pipeline.transform(train)
        readyTest = pipeline.transform(test)

        classifier1 = legal.LegalDocumentMLClassifierApproach() \
            .setInputCols("token") \
            .setLabelCol("label") \
            .setOutputCol("partition") \
            .fit(readyTrain)

        t1 = classifier1.transform(readyTest)
        t1.show(100, False)

        classifier1.write().overwrite().save("classifier.model")
        classifier2 = DocumentMLClassifierModel.load("classifier.model")

        t2 = classifier2.transform(readyTest)
        t2.show(100, False)


if __name__ == '__main__':
    unittest.main()
