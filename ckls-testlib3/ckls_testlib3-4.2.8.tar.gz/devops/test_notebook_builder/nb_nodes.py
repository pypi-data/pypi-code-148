from nbformat import NotebookNode


class Nodes:
    # Re-Usable Nodes to Inject
    auth = NotebookNode(
        cell_type='code',
        source="""import os
from pyspark.sql import SparkSession
os.environ['SPARK_NLP_LICENSE'] = "???"
os.environ['AWS_ACCESS_KEY_ID'] = "???"
os.environ['AWS_SECRET_ACCESS_KEY'] = "???"
os.environ['SPARK_OCR_LICENSE'] = '???'""",
        outputs=[],
        metadata={},

    )

    auth_with_jsl_lib = NotebookNode(
        cell_type='code',
        source="""! pip install jsl_tmp==4.2.3rc16
enterprise_nlp_secret = '<SECRET>'
MY_AWS_KEY = 'PUT YOUR CREDENTIALS HERE'
MY_AWS_KEY_ID = 'PUT YOUR CREDENTIALS HERE'
MY_MEDICAL_LICENSE = 'PUT YOUR CREDENTIALS HERE'
from johnsnowlabs import *
nlp.settings.enforce_versions = False
nlp.install(enterprise_nlp_secret=enterprise_nlp_secret,
            aws_access_key=MY_AWS_KEY,
            aws_key_id=MY_AWS_KEY_ID,
            med_license=MY_MEDICAL_LICENSE)
spark = nlp.start()
        """,
        outputs=[],
        metadata={},

    )

    get_sample_text_df = NotebookNode(
        cell_type='code',
        source="""smallCorpus = spark.createDataFrame(
[["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF("text")
smallCorpus.show()
documentAssembler = nlp.DocumentAssembler().setInputCol("text").setOutputCol("document")
result = documentAssembler.transform(smallCorpus)
result.select("document").show(truncate=False)        
""",
        metadata={},
        outputs=[],

    )
