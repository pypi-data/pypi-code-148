from sparknlp_jsl.common import *

from sparknlp_jsl.annotator import NerQuestionGenerator as A


class LegalNerQuestionGenerator(A):
    """
    The chunk mapper Approach load a JsonDictionary that have the relations to be mapped in the ChunkMapperModel

    ====================== =======================
    Input Annotation types Output Annotation type
    ====================== =======================
    ``CHUNK``              ``LABEL_DEPENDENCY``
    ====================== =======================

    Parameters
    ----------
    dictionary
        Dictionary path where is the json that contains the mappinmgs columns
    rel
        Relation that we going to use to map the chunk
    lowerCase
        Parameter to decide if we going to use the chunk mapper or not

    Examples
    --------
    >>> import sparknlp
    >>> from sparknlp.base import *
    >>> from sparknlp_jsl.common import *
    >>> from sparknlp.annotator import *
    >>> from sparknlp.training import *
    >>> import sparknlp_jsl
    >>> from sparknlp_jsl.base import *
    >>> from sparknlp_jsl.annotator import *
    >>> from pyspark.ml import Pipeline
    >>> documenter = DocumentAssembler()\
    ...     .setInputCol("text")\
    ...     .setOutputCol("documents")
    >>> sentence_detector = SentenceDetector() \
    ...     .setInputCols("documents") \
    ...     .setOutputCol("sentences")
    >>> tokenizer = Tokenizer() \
    ...     .setInputCols("sentences") \
    ...     .setOutputCol("tokens")
    >>> embeddings = WordEmbeddingsModel() \
    ...     .pretrained("embeddings_clinical", "en", "clinical/models")\
    ...     .setInputCols(["sentences", "tokens"])\
    ...     .setOutputCol("embeddings")
    >>> ner_model = MedicalNerModel()\
    ...     .pretrained("ner_posology_large", "en", "clinical/models")\
    ...     .setInputCols(["sentences", "tokens", "embeddings"])\
    ...     .setOutputCol("ner")
    >>> ner_converter = NerConverterInternal()\
    ...     .setInputCols("sentences", "tokens", "ner")\
    ...     .setOutputCol("ner_chunks")
    >>> chunkerMapperapproach = ChunkMapperApproach()\
    ...    .setInputCols(["ner_chunk"])\
    ...    .setOutputCol("mappings")\
    ...    .setDictionary("/home/jsl/mappings2.json") \
    ...    .setRels(["action"]) \
    >>> sampleData = "The patient was given Warfarina Lusa and amlodipine 10 MG."
    >>> pipeline = Pipeline().setStages([
    ...     documenter,
    ...     sentence_detector,
    ...     tokenizer,
    ...     embeddings,
    ...     ner_model,
    ...     ner_converter])
    >>> results = pipeline.fit(data).transform(data)
    >>> results.select("mappings").show(truncate=False)
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |mappings                                                                                                                                                                                                                                                                                                                                                                                               |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |[{labeled_dependency, 22, 35, Analgesic, {chunk -> 0, relation -> action, confidence -> 0.56995, all_relations -> Antipyretic, entity -> Warfarina Lusa, sentence -> 0}, []}, {labeled_dependency, 41, 50, NONE, {entity -> amlodipine, sentence -> 0, chunk -> 1, confidence -> 0.9989}, []}, {labeled_dependency, 55, 56, NONE, {entity -> MG, sentence -> 0, chunk -> 2, confidence -> 0.9123}, []}]|
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

    """

    def __init__(self, classname="com.johnsnowlabs.legal.sequence_generation.LegalNerQuestionGenerator",
                 java_model=None):
        super(LegalNerQuestionGenerator, self).__init__(
            classname=classname,
            java_model=java_model
        )
