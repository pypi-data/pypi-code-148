import pyspark.sql.types as T
import pyspark.sql.functions as F
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

import sparknlp
from sparknlp.internal import ExtendedJavaWrapper

from ._tf_graph_builders.graph_builders import TFGraphBuilderFactory
from ._tf_graph_builders_1x.graph_builders import TFGraphBuilderFactory as TFGraphBuilderFactory1x


class AnnotationToolJsonReader(ExtendedJavaWrapper):
    """
    The annotation tool json reader is a reader to parse Named Entity Recognition, Assertion and Relation Extraction Annotations
    from a JSON exported from the Annotation Tool.

    Examples
    --------
    >>> from sparknlp_jsl.training import AnnotationToolJsonReader
    >>> assertion_labels = ["AsPresent","Absent"]
    >>> excluded_labels = ["Treatment"]
    >>> split_chars = [" ", "\\-"]
    >>> context_chars = [".", ",", ";"]
    >>> SDDLPath = ""
    >>> rdr = AnnotationToolJsonReader(assertion_labels = assertion_labels, excluded_labels = excluded_labels, split_chars = split_chars, context_chars = context_chars,SDDLPath=SDDLPath)
    >>> path = "src/test/resources/anc-pos-corpus-small/test-training.txt"
    >>> df = rdr.readDataset(spark, json_path)
    >>> assertion_df = rdr.generateAssertionTrainSet(df)
    >>> assertion_df.show()

    """

    def __init__(self, pipeline_model=None, assertion_labels=None, excluded_labels=None, cleanup_mode="disabled",
                 split_chars=None, context_chars=None, scheme="IOB", min_chars_tol=2, align_chars_tol=1,
                 merge_overlapping=True, SDDLPath=""):
        """
        Attributes
        ----------
        pipeline_model: str
             The pipeline model that is used to create the documents the sentences and the tokens.That pipeline model
             needs to have a DocumentAssembler, SentenceDetector and Tokenizer.The input column of the document assembler
             needs to be named a 'text'.The output of the sentence detector needs to be named a 'sentence'.
             The output of the tokenizer needs to be named 'token'.
        assertion_labels: list
            The assertions labels are used for the training dataset creation.
        excluded_labels: list
            The assertions labels that are excluded for the training dataset creation.
        cleanup_mode: str
            The clean mode that is used in the DocumentAssembler transformer.
        split_chars: list
            The split chars that are used in the default tokenizer.
        context_chars: list
            The context chars that are used in the default tokenizer.
        scheme: str
             The schema that will use to create the IOB_tagger (IOB or BIOES).
        minCharsTol
             The min length of the token to apply the alignment tolerance feature.
        alignCharsTol
             The maximum number of char difference to consider the start / end tokens alignment with the assertion annotations.
        merge_overlapping: bool
             Whether merge the chunks when they are in the same position.

        """
        if assertion_labels is None:
            assertion_labels = []
        if excluded_labels is None:
            excluded_labels = []
        if type(pipeline_model) == PipelineModel:
            if scheme is None:
                scheme = "IOB"
            if min_chars_tol is None:
                min_chars_tol = 2
            super(AnnotationToolJsonReader, self).__init__("com.johnsnowlabs.nlp.training.AnnotationToolJsonReader",
                                                           pipeline_model._to_java(), assertion_labels, excluded_labels,
                                                           scheme, min_chars_tol, align_chars_tol, merge_overlapping)
        else:
            if split_chars is None:
                split_chars = [" "]
            if context_chars is None:
                context_chars = [".", ",", ";", ":", "!", "?", "*", "-", "(", ")", "\"", "'"]

            super(AnnotationToolJsonReader, self).__init__("com.johnsnowlabs.nlp.training.AnnotationToolJsonReader",
                                                           assertion_labels, excluded_labels, cleanup_mode,
                                                           split_chars, context_chars, scheme,
                                                           min_chars_tol, align_chars_tol, merge_overlapping, SDDLPath)

    def readDataset(self, spark, path):

        # ToDo Replace with std pyspark
        jSession = spark._jsparkSession

        jdf = self._java_obj.readDataset(jSession, path)
        return self.getDataFrame(spark, jdf)

    def generateAssertionTrainSet(self, df, sentenceCol="sentence", assertionCol="assertion_label"):

        jdf = self._java_obj.generateAssertionTrainSet(df._jdf, sentenceCol, assertionCol)
        session = df.sparkSession if hasattr(df, "sparkSession") else df.sql_ctx
        return DataFrame(jdf, session)

    def generateConll(self, df, path: str, taskColumn: str = "task_id", tokenCol: str = "token",
                      nerLabel: str = "ner_label"):
        """
        Deprecated
        """
        jdf = self._java_obj.generateConll(df._jdf, path, taskColumn, tokenCol, nerLabel)


    def generatePlainAssertionTrainSet(self, df, taskColumn: str = "task_id", tokenCol: str = "token",
                                       nerLabel: str = "ner_label", assertion_label: str = "assertion_label"):
        """
        Deprecated
        """
        jdf = self._java_obj.generatePlainAssertionTrainSet(df._jdf, taskColumn, tokenCol, nerLabel, assertion_label)
        session = df.sparkSession if hasattr(df, "sparkSession") else df.sql_ctx
        return DataFrame(jdf, session)


class CodiEspReader(ExtendedJavaWrapper):
    def __init__(self, scheme="IOB"):
        super(CodiEspReader, self).__init__("com.johnsnowlabs.nlp.training.CodiEspReader", scheme)

    def readDatasetTaskX(self, spark, path, textFolder, sep="\t"):
        # ToDo Replace with std pyspark
        jSession = spark._jsparkSession

        jdf = self._java_obj.readDatasetTaskX(jSession, path, textFolder, sep)
        dataframe = self.getDataFrame(spark, jdf)
        return dataframe


class CantemistReader(ExtendedJavaWrapper):
    def __init__(self, scheme="IOB"):
        super(CantemistReader, self).__init__("com.johnsnowlabs.nlp.training.CantemistReader", scheme)

    def readDatasetTaskNer(self, spark, textFolder):
        # ToDo Replace with std pyspark
        jSession = spark._jsparkSession

        jdf = self._java_obj.readDatasetTaskNer(jSession, textFolder)
        dataframe = self.getDataFrame(spark, jdf)
        return dataframe


tf_graph = TFGraphBuilderFactory()
tf_graph_1x = TFGraphBuilderFactory1x()


class SynonymAugmentationUMLS(ExtendedJavaWrapper):
    def __init__(self, spark, umls_path="", code_col="code", description_col="description", case_sensitive=False):
        self._spark = spark
        super(SynonymAugmentationUMLS, self).__init__("com.johnsnowlabs.nlp.training.SynonymAugmentationUMLS",
                                                      spark._jsparkSession, umls_path, code_col, description_col, case_sensitive)

    def augmentCsv(self, corpus_csv_path, ner_pipeline, language="ENG", do_product=False,
                   augmentation_mode="plain_text", synonym_source="umls", regex_parsers=None,
                   euclidean_distance_threshold=10.0, cosine_distance_threshold=0.25, synonym_limit=5, casing_functions=None):
        regex_parsers, casing_functions = regex_parsers or [], casing_functions or ['infer']
        jdf = self._java_obj.augmentCsv(corpus_csv_path, ner_pipeline._to_java(), language, do_product,
                                        augmentation_mode, synonym_source, regex_parsers,
                                        euclidean_distance_threshold, cosine_distance_threshold, synonym_limit, casing_functions)
        return self.getDataFrame(self._spark, jdf)

    def augmentDataFrame(self, corpus_df, ner_pipeline, language="ENG", do_product=False,
                         augmentation_mode="plain_text", synonym_source="umls", regex_parsers=None,
                         euclidean_distance_threshold=10.0, cosine_distance_threshold=0.25, synonym_limit=5, casing_functions=None):
        regex_parsers, casing_functions = regex_parsers or [], casing_functions or ['infer']
        jdf = self._java_obj.augmentDataFrame(corpus_df._jdf, ner_pipeline._to_java(), language, do_product,
                                              augmentation_mode, synonym_source, regex_parsers,
                                              euclidean_distance_threshold, cosine_distance_threshold, synonym_limit, casing_functions)
        return self.getDataFrame(self._spark, jdf)


class REDatasetHelper:
    """
    Class to preprocess RE dataset loaded into Spark Dataframe.

    Examples
    --------
    >>> from sparknlp_jsl.training import REDatasetHelper
    >>> PATH = "/content/i2b2_clinical_rel_dataset.csv"
    >>> data = spark.read.option("header","true").format("csv").load(PATH)
    >>>
    >>> column_map = {
            "begin1": "firstCharEnt1",
            "end1": "lastCharEnt1",
            "begin2": "firstCharEnt2",
            "end2": "lastCharEnt2",
            "chunk1": "chunk1",
            "chunk2": "chunk2",
            "label1": "label1",
            "label2": "label2"
        }
    >>>
    >>> # apply preprocess function to dataframe
    >>> data = REDatasetHelper(data).create_annotation_column(column_map)
    >>> data.show(5)
    +-------+-------------+--------------------+--------------------+-------+--------------------+------+----+-----+--------------------+------+----+---------+---------+------------+-------------+------------+-------------+-------------+-------------+-------------+
    |dataset|       source|            txt_file|            sentence|sent_id|              chunk1|begin1|end1|  rel|              chunk2|begin2|end2|   label1|   label2|lastCharEnt1|firstCharEnt1|lastCharEnt2|firstCharEnt2|words_in_ent1|words_in_ent2|words_between|
    +-------+-------------+--------------------+--------------------+-------+--------------------+------+----+-----+--------------------+------+----+---------+---------+------------+-------------+------------+-------------+-------------+-------------+-------------+
    |   test|beth+partners|i2b2 2010 VA/test...|VITAL SIGNS - Tem...|     44|    respiratory rate|    12|  13|    O|          saturation|    17|  17|     test|     test|          64|           49|          84|           75|            2|            1|            3|
    |   test|beth+partners|i2b2 2010 VA/test...|No lotions , crea...|    146|             lotions|     1|   1|TrNAP|           incisions|     7|   7|treatment|  problem|           9|            3|          42|           34|            1|            1|            5|
    |  train|     partners|i2b2 2010 VA/conc...|Because of expect...|     43|expected long ter...|     2|   6|    O|         a picc line|     8|  10|treatment|treatment|          54|           11|          68|           58|            5|            3|            1|
    |  train|     partners|i2b2 2010 VA/conc...|She states this l...|     21|    light-headedness|     3|   3|  PIP|         diaphoresis|    12|  12|  problem|  problem|          31|           16|          92|           82|            1|            1|            8|
    |   test|beth+partners|i2b2 2010 VA/test...|Initial electroca...|     61|an inferior and r...|    38|  43|  PIP|1-mm st depressio...|    28|  34|  problem|  problem|         239|          196|         176|          145|            6|            7|            3|
    +-------+-------------+--------------------+--------------------+-------+--------------------+------+----+-----+--------------------+------+----+---------+---------+------------+-------------+------------+-------------+-------------+-------------+-------------+
    only showing top 5 rows
    >>> #   if data contains different splits, you can first preprocess then filter by dataset column.
    >>> train_data = data.where("dataset='train'")
    >>> test_data = data.where("dataset='test'")
    """

    def __init__(self, spark_df: DataFrame):
        self.annotation_schema = T.ArrayType(T.StructType([
            T.StructField('annotatorType', T.StringType(), False),
            T.StructField('begin', T.IntegerType(), False),
            T.StructField('end', T.IntegerType(), False),
            T.StructField('result', T.StringType(), False),
            T.StructField('metadata', T.MapType(T.StringType(), T.StringType()), False),
            T.StructField('embeddings', T.ArrayType(T.FloatType()), False)
        ]))

        self.data = spark_df

    def create_annotation_column(self, column_map,  ner_column_name="train_ner_chunks"):
        """
        A method to create label column for RelationExtractionApproach
        :param column_map: Required mapping between entity columns and dataset columns.
        Required columns are: begin1, end1, chunk1, label1, begin2, end2, chunk2, label2

        Examples
        --------
        # for dataset with following schema:
        >>> data.printSchema()
        root
         |-- sentence: string (nullable = true)
         |-- chunk1: string (nullable = true)
         |-- begin1: string (nullable = true)
         |-- end1: string (nullable = true)
         |-- rel: string (nullable = true)
         |-- chunk2: string (nullable = true)
         |-- begin2: string (nullable = true)
         |-- end2: string (nullable = true)
         |-- label1: string (nullable = true)
         |-- label2: string (nullable = true)
         |-- lastCharEnt1: string (nullable = true)
         |-- firstCharEnt1: string (nullable = true)
         |-- lastCharEnt2: string (nullable = true)
         |-- firstCharEnt2: string (nullable = true)

         #  map should be as follows:
         >>> column_map = {
                "begin1": "firstCharEnt1",
                "end1": "lastCharEnt1",
                "begin2": "firstCharEnt2",
                "end2": "lastCharEnt2",
                "chunk1": "chunk1",
                "chunk2": "chunk2",
                "label1": "label1",
                "label2": "label2"
            }
        :param ner_column_name: a label column name for RelationExtractionApproach
        :return: A new dataframe extended with ner chunk column.
        """

        required_maps = ["begin1", "end1", "chunk1", "label1", "begin2", "end2", "chunk2", "label2"]
        for col in required_maps:
            if column_map.get(col) is None:
                raise ValueError(f'{col} value is None. Following columns should be mapped: {required_maps}')

        num_rows = self.data.count()
        cast_columns = ["begin1", "end1", "begin2", "end2"]
        for col in cast_columns:

            #  cast integer columns before creating ner chunks
            data_casted = self.data.withColumn(column_map[col], self.data[column_map[col]].cast(T.IntegerType()))
            if num_rows == data_casted.where(F.col(column_map[col]).isNull()).count():
                raise ValueError(f'{column_map[col]} could not be casted as integer!')
            else:
                self.data = data_casted

        @F.udf(returnType=self.annotation_schema)
        def create_train_annotations(begin1, end1, chunk1, label1, begin2, end2, chunk2, label2):

            entity1 = sparknlp.annotation.Annotation(
                "chunk", begin1, end1, chunk1, {'entity': label1.upper(), 'sentence': '0'}, [])
            entity2 = sparknlp.annotation.Annotation(
                "chunk", begin2, end2, chunk2, {'entity': label2.upper(), 'sentence': '0'}, [])

            entity1.annotatorType = "chunk"
            entity2.annotatorType = "chunk"

            return [entity1, entity2]

        self.data = self.data.withColumn(
            ner_column_name,
            create_train_annotations(
                column_map["begin1"], column_map["end1"], column_map["chunk1"], column_map["label1"],
                column_map["begin2"], column_map["end2"], column_map["chunk2"], column_map["label2"]
            ).alias(ner_column_name, metadata={'annotatorType': "chunk"})
        )

        drop_columns = []
        for col in required_maps:
            if column_map[col] != col:
                drop_columns.append(col)

        return_columns = set(self.data.columns) - set(drop_columns)
        self.data = self.data.select(list(return_columns))
        return self.data
