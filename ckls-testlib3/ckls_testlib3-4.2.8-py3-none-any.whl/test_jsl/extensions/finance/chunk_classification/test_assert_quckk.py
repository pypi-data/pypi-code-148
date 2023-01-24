import unittest

from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
from sparknlp.base import LightPipeline

import sparknlp_jsl
from sparknlp_jsl.annotator import *
from test_jsl.extensions.utils import get_spark_session


class RouterTestcase(unittest.TestCase):
    spark = get_spark_session()

    def test_router(self):
        documentAssembler = DocumentAssembler() \
            .setInputCol("text") \
            .setOutputCol("document")

        sbiobert_embeddings = BertSentenceEmbeddings.pretrained("sbiobert_base_cased_mli","en","clinical/models") \
            .setInputCols(["document"]) \
            .setOutputCol("sbert_embeddings") \
            .setCaseSensitive(False)

        # filter PROBLEM entity embeddings
        router_sentence_icd10 = Router() \
            .setInputCols("sbert_embeddings") \
            .setFilterFieldsElements(['Psychological_Condition','Symptom','VS_Finding']) \
            .setOutputCol("icd_embeddings")

        pipeline = Pipeline(stages=[documentAssembler,sbiobert_embeddings,router_sentence_icd10,])

        empty_data = self.spark.createDataFrame([['']]).toDF("text")
        resolver_model = pipeline.fit(empty_data)
        LightPipeline(resolver_model).annotate("Hello world")
if __name__ == '__main__':
    unittest.main()
