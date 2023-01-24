from nbformat import NotebookNode


class Nodes:
    # Re-Usable Nodes to Inject
    sparksession = NotebookNode(
        cell_type='code',
        source='from johnsnowlabs import *;spark = nlp.start()',
        execution_count=0,
        metadata={'collapsed': True, 'pycharm': {'name': '#%%\n'}},
        outputs=[],
    )
    sparksession_with_cache_folder = NotebookNode(
        cell_type='code',
        source='from johnsnowlabs import *;spark = nlp.start(cache_folder="/home/ckl/dump/cache_pretrained")',
        execution_count=0,
        metadata={'collapsed': True, 'pycharm': {'name': '#%%\n'}},
        outputs=[],
    )

    imports = NotebookNode(
        cell_type='code',
        source='from sparknlp.base import LightPipeline\n'
               'from pyspark.ml import Pipeline',
        execution_count=0,
        metadata={'collapsed': True, 'pycharm': {'name': '#%%\n'}},
        outputs=[],
    )

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

    setup_notebook_pip_installs = NotebookNode(
        cell_type='code',
        source="""
def get_spark_session():
    open_source_jar = 'PATH_TO_OPEN_SOURCE_SPARK_NLP'
    enterprise_jar = 'PATH_TO_ENTERPRISE_SPARK_NLP'
    visual_jar = 'PATH_TO_VISUAL_JAR'
    spark = SparkSession.builder.config("spark.driver.memory", "16G").config("spark.jars", ','.join([open_source_jar, enterprise_jar,visual_jar])).getOrCreate()
    return spark

        
""",
        outputs=[],
        metadata={},

    )

    get_spark_session_custom_build = NotebookNode(
        cell_type='code',
        source="""
def get_spark_session():
    open_source_jar = 'PATH_TO_OPEN_SOURCE_SPARK_NLP'
    enterprise_jar = 'PATH_TO_ENTERPRISE_SPARK_NLP'
    visual_jar = 'PATH_TO_VISUAL_JAR'
    spark = SparkSession.builder.config("spark.driver.memory", "16G").config("spark.jars", ','.join([open_source_jar, enterprise_jar,visual_jar])).getOrCreate()
    return spark

        
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

    dummy = NotebookNode(
        cell_type='code',
        source='print("HELLO DUMMY WORLD")',
        execution_count=0,
        metadata={'collapsed': True, 'pycharm': {'name': '#%%\n'}},
        outputs=[],
    )



