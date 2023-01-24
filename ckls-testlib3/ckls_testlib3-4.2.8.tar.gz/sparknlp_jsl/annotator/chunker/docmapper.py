from sparknlp_jsl.annotator.chunker.chunkmapper import CommonChunkMapperParams, ChunkMapperFuzzyMatchingParams
from sparknlp_jsl.common import *


class DocMapperApproach(AnnotatorApproachInternal, CommonChunkMapperParams, ChunkMapperFuzzyMatchingParams):
    """
    The chunk mapper Approach load a JsonDictionary that have the relations to be mapped in the DocMapperModel

    ====================== =======================
    Input Annotation types Output Annotation type
    ====================== =======================
    ``DOCUMENT``              ``LABEL_DEPENDENCY``
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
    >>> chunkerMapperapproach = DocMapperApproach()\
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
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT]
    outputAnnotatorType = AnnotatorType.LABELED_DEPENDENCY

    name = "DocMapperApproach"

    dictionary = Param(Params._dummy(),
                       "dictionary",
                       "Path to dictionary file in tsv or csv format",
                       typeConverter=TypeConverters.toString)

    def setDictionary(self, p):
        """Sets if we want to use 'bow' for word embeddings or 'sentence' for sentences"
        Parameters
        ----------
        path : str
            Path where is the dictionary
        """
        return self._set(dictionary=p)

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.chunker.DocMapperApproach"):
        super(DocMapperApproach, self).__init__(
            classname=classname
        )

    def _create_model(self, java_model):
        return DocMapperModel(java_model=java_model)


class DocMapperModel(AnnotatorModelInternal, CommonChunkMapperParams, ChunkMapperFuzzyMatchingParams):
    """
    The chunk mapper Approach load a JsonDictionary that have the relations to be mapped in the DocMapperModel

    ====================== =======================
    Input Annotation types Output Annotation type
    ====================== =======================
    ``DOCUMENT``              ``LABEL_DEPENDENCY``
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
    >>> chunkerMapperapproach = DocMapperModel()\
    ...    .pretrained()\
    ...    .setInputCols(["ner_chunk"])\
    ...    .setOutputCol("mappings")\
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
    >>> results = results \
    ...     .selectExpr("explode(drug_chunk_embeddings) AS drug_chunk") \
    ...     .selectExpr("drug_chunk.result", "slice(drug_chunk.embeddings, 1, 5) AS drug_embedding") \
    ...     .cache()
    >>> results.show(truncate=False)
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |mappings                                                                                                                                                                                                                                                                                                                                                                                               |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |[{labeled_dependency, 22, 35, Analgesic, {chunk -> 0, relation -> action, confidence -> 0.56995, all_relations -> Antipyretic, entity -> Warfarina Lusa, sentence -> 0}, []}, {labeled_dependency, 41, 50, NONE, {entity -> amlodipine, sentence -> 0, chunk -> 1, confidence -> 0.9989}, []}, {labeled_dependency, 55, 56, NONE, {entity -> MG, sentence -> 0, chunk -> 2, confidence -> 0.9123}, []}]|
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    """
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT]
    outputAnnotatorType = AnnotatorType.LABELED_DEPENDENCY

    name = "DocMapperModel"

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.chunker.DocMapperModel", java_model=None):
        super(DocMapperModel, self).__init__(
            classname=classname,
            java_model=java_model
        )

    @staticmethod
    def pretrained(name="", lang="en", remote_loc="clinical/models"):
        """Downloads and loads a pretrained model.

        Parameters
        ----------
        name : str, optional
            Name of the pretrained model.
        lang : str, optional
            Language of the pretrained model, by default "en"
        remote_loc : str, optional
            Optional remote address of the resource, by default None. Will use
            Spark NLPs repositories otherwise.

        Returns
        -------
        DocMapperModel
            The restored model
        """
        from sparknlp_jsl.pretrained import InternalResourceDownloader
        return InternalResourceDownloader.downloadModel(DocMapperModel, name, lang, remote_loc,
                                                        j_dwn='InternalsPythonResourceDownloader')
