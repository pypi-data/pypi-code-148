from sparknlp_jsl.common import *
from sparknlp_jsl.annotator.source_tracking_metadata_params import SourceTrackingMetadataParams


class CommonNerConverterInternalParams:
    """Base class for NerConverterInternal classes
    
    Contains the common parameters and methods used in all internal classes.
    
    Parameters
    ----------
    whiteList
        If defined, list of entities to process.
        The rest will be ignored. Do not include IOB prefix on labels
    blackList
        If defined, list of entities to ignore.
        The rest will be proccessed. Do not include IOB prefix on labels
    preservePosition
        Whether to preserve the original position of the tokens in the
        original document or use the modified tokens
    greedyMode
        Whether to ignore B tags for contiguous tokens of same entity same
    threshold
        Confidence threshold to filter the chunk entities
    ignoreStopWords
        If defined, list of stop words to ignore if present between two entities.
        It should be a list of tokens/words or characters, and when two entities of the same 
        type are separated by those words, these entities can be combined to produce a single, larger chunk.
    
    """
    whiteList = Param(
        Params._dummy(),
        "whiteList",
        "If defined, list of entities to process. The rest will be ignored. Do not include IOB prefix on labels",
        typeConverter=TypeConverters.toListString,
    )
    blackList = Param(
        Params._dummy(),
        "blackList",
        "If defined, list of entities to ignore. The rest will be processed. Do not include IOB prefix on labels",
        TypeConverters.toListString,
    )
    preservePosition = Param(
        Params._dummy(),
        "preservePosition",
        "Whether to preserve the original position of the tokens in the original document or use the modified tokens",
        typeConverter=TypeConverters.toBoolean,
    )
    greedyMode = Param(
        Params._dummy(),
        "greedyMode",
        "Whether to ignore B tags for contiguous tokens of same entity same",
        typeConverter=TypeConverters.toBoolean,
    )
    threshold = Param(
        Params._dummy(),
        "threshold",
        "Confidence threshold",
        typeConverter=TypeConverters.toFloat,
    )
    ignoreStopWords = Param(
        Params._dummy(),
        "ignoreStopWords",
        "If defined, list of stop words to ignore.",
        typeConverter=TypeConverters.toListString,
    )
    
    def setWhiteList(self, entities):
        """Sets the `whiteList` parameter value.

        Parameters
        ----------
        entities : list
            The list of white-listed entities.
        """
        return self._set(whiteList=entities)

    def setBlackList(self, entities):
        """Sets the `blackList` parameter value.

        Parameters
        ----------
        entities : list
           The list of black-listed entities.
        """
        return self._set(blackList=entities)

    def setPreservePosition(self, preserve_position: bool):
        """Sets the `preservePosition` parameter value.

        Parameters
        ----------
        preserve_position : bool
            True or False to preserve the original position of the tokens in the original document or use the modified tokens.
        """
        return self._set(preservePosition=preserve_position)

    def setGreedyMode(self, greedy_mode: bool):
        """Sets the `greedyMode` parameter value.

        Parameters
        ----------
        greedy_mode : bool
            True or False to ignore B tags for contiguous tokens of same entity same.
        """
        return self._set(greedyMode=greedy_mode)

    def setThreshold(self, threshold: float):
        """Sets the `threshold` parameter value.

        Parameters
        ----------
        threshold : float
            Confidence threshold to filter the chunk entities.
        """
        return self._set(threshold=threshold)

    def setIgnoreStopWords(self, stopwords: list):
        """Sets the `ignoreStopWords` parameter value.

        Parameters
        ----------
        stopwords : list
           List of stop words to ignore.
        """
        return self._set(ignoreStopWords=stopwords)


class NerConverterInternal(AnnotatorApproachInternal, CommonNerConverterInternalParams, SourceTrackingMetadataParams):
    """Converts IOB or IOB2 representations of entities to a user-friendly one

    This is the AnnotatorApproachInternal version of the NerConverterInternal annotator.
    Converts a IOB or IOB2 representation of NER to a user-friendly one,
    by associating the tokens of recognized entities and their label.
    Chunks with no associated entity (tagged "O") are filtered.

    ==========================================  ======================
    Input Annotation types                      Output Annotation type
    ==========================================  ======================
    ``DOCUMENT, TOKEN, NAMED_ENTITY``           ``CHUNK``
    ==========================================  ======================

    Parameters
    ----------
    replaceDictResource
        If defined, path to a dictionary file to replace the tokens with
    replaceLabels
        If defined, a dictionary that maps old to new labels
        
    
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
    >>> data = spark.createDataFrame([["A 63-year-old man presents to the hospital ..."]]).toDF("text")
    >>> documentAssembler = DocumentAssembler() \\
    ...    .setInputCol("text") \\
    ...    .setOutputCol("document")
    >>> sentenceDetector = SentenceDetector() \\
    ...    .setInputCols(["document"]) \\
    ...    .setOutputCol("sentence")
    >>> tokenizer = Tokenizer() \\
    ...    .setInputCols(["sentence"]) \\
    ...    .setOutputCol("token")
    >>> embeddings = WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models") \\
    ...    .setInputCols(["sentence", "token"])\
    ...    .setOutputCol("embeddings")
    >>> nerModel = MedicalNerModel.pretrained("ner_jsl", "en", "clinical/models") \\
    ...    .setInputCols(["sentence", "token", "embeddings"]) \\
    ...    .setOutputCol("ner")
    >>> nerConverter = NerConverterInternal() \\
    ...    .setInputCols(["sentence", "token", "ner"]) \\
    ...    .setOutputCol("ner_chunk")
    ...
    >>> pipeline = Pipeline(stages=[
    ...     documentAssembler,
    ...     sentenceDetector,
    ...     tokenizer,
    ...     embeddings,
    ...     nerModel,
    ...     nerConverter])
    """
    name = 'NerConverterInternal'

    inputAnnotatorTypes = [AnnotatorType.DOCUMENT, AnnotatorType.TOKEN, AnnotatorType.NAMED_ENTITY]
    outputAnnotatorType = AnnotatorType.CHUNK

    replaceDictResource = Param(
        Params._dummy(),
        "replaceDictResource",
        "If defined, path to the file containing a dictionary for entity replacement",
        typeConverter=TypeConverters.identity,
    )

    replaceLabels = Param(
        Params._dummy(),
        "replaceLabels",
        "If defined, contains a dictionary for entity replacement",
        TypeConverters.identity,
    )

    def setReplaceDictResource(self, path, read_as=ReadAs.TEXT, options=None):
        """Sets the `replaceDictResource` parameter

        The method sets the `replaceDictResource` parameter to the path of the external resource.
        Usual usage is to set the path to a CSV file containing the dictionary pairs, one
        substitution per line, with the original label and the new label separated by a comma.

        Parameters
        ----------
        path : str
            Path to the external resource
        read_as : str, optional
            How to read the resource, by default "TEXT".
            Possible values:  "TEXT" (ReadAs.TEXT),  "SPARK" (ReadAs.SPARK) or "BINARY" (ReadAs.BINARY)
        options : dict, optional
            Options for reading the resource, by default None


        Examples
        --------

        Reading a CSV file

        >>> ner_converter = NerConverterInternal()\
        ...    .setInputCols(["sentence", "token", "ner"])\
        ...    .setOutputCol("replaced_ner_chunk")\
        ...    .setReplaceDictResource("path/to/dictionary.csv", "TEXT", {"delimiter": ","})

        Reading a TSV file

        >>> ner_converter = NerConverterInternal()\
        ...    .setInputCols(["sentence","token", "jsl_ner"])\
        ...    .setOutputCol("replaced_ner_chunk")\
        ...    .setReplaceDictResource("path/to/dictionary.tsv", "TEXT", {"delimiter": "\t"})

        """
        if options is None:
            options = {"delimiter": ","}
        return self._set(replaceDictResource=ExternalResource(path, read_as, options))

    def setReplaceLabels(self, labels):
        """Sets dictionary that maps old to new labels

        Parameters
        ----------
        labels : dict[str, str]
            Dictionary which maps old to new labels

        Examples
        --------
        
        Change the labels PER to PERSON and LOC to LOCATION 

        >>> ner_converter = NerConverterInternal()\
        ...    .setInputCols(["sentence", "token", "ner"])\
        ...    .setOutputCol("ner_chunk")\
        ...    .setReplaceLabels({"PER": "PERSON", "LOC": "LOCATION"})

        Change `ner_jsl` entities for drugs.

        >>> ner_converter = NerConverterInternal()\
        ...    .setInputCols(["sentence", "token", "jsl_ner"])\
        ...    .setOutputCol("replaced_ner_chunk")\
        ...    .setReplaceLabels(
        ...        {
        ...            "Drug_BrandName": "Drug",
        ...            "Frequency": "Drug_Frequency",
        ...            "Dosage": "Drug_Dosage",
        ...            "Strength": "Drug_Strength",
        ...        })

        """
        labels = labels.copy()
        from sparknlp_jsl.internal import CustomLabels

        return self._set(replaceLabels=CustomLabels(labels))

    @keyword_only
    def __init__(self):
        super(NerConverterInternal, self).__init__(
            classname="com.johnsnowlabs.nlp.annotators.ner.NerConverterInternal"
        )

    def _create_model(self, java_model):
        return NerConverterInternalModel(java_model=java_model)


class NerConverterInternalModel(AnnotatorModelInternal, CommonNerConverterInternalParams, SourceTrackingMetadataParams):
    """
    Converts a IOB or IOB2 representation of NER to a user-friendly one,
    by associating the tokens of recognized entities and their label.
    Chunks with no associated entity (tagged "O") are filtered.

    ==========================================  ======================
    Input Annotation types                      Output Annotation type
    ==========================================  ======================
    ``DOCUMENT, TOKEN, NAMED_ENTITY``           ``CHUNK``
    ==========================================  ======================

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
    >>> data = spark.createDataFrame([["A 63-year-old man presents to the hospital ..."]]).toDF("text")
    >>> documentAssembler = DocumentAssembler() \\
    ...    .setInputCol("text") \\
    ...    .setOutputCol("document")
    >>> sentenceDetector = SentenceDetector() \\
    ...    .setInputCols(["document"]) \\
    ...    .setOutputCol("sentence")
    >>> tokenizer = Tokenizer() \\
    ...    .setInputCols(["sentence"]) \\
    ...    .setOutputCol("token")
    >>> embeddings = WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models") \\
    ...    .setInputCols(["sentence", "token"])\
    ...    .setOutputCol("embeddings")
    >>> nerModel = MedicalNerModel.pretrained("ner_jsl", "en", "clinical/models") \\
    ...    .setInputCols(["sentence", "token", "embeddings"]) \\
    ...    .setOutputCol("ner")
    >>> nerConverter = NerConverterInternal() \\
    ...    .setInputCols(["sentence", "token", "ner"]) \\
    ...    .setOutputCol("ner_chunk")
    ...
    >>> pipeline = Pipeline(stages=[
    ...     documentAssembler,
    ...     sentenceDetector,
    ...     tokenizer,
    ...     embeddings,
    ...     nerModel,
    ...     nerConverter])
    """
    
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT, AnnotatorType.TOKEN, AnnotatorType.NAMED_ENTITY]
    outputAnnotatorType = AnnotatorType.CHUNK

    name = 'NerConverterInternalModel'
    
    def __init__(
        self,
        classname="com.johnsnowlabs.nlp.annotators.ner.NerConverterInternalModel",
        java_model=None,
    ):
        super(NerConverterInternalModel, self).__init__(
            classname=classname, java_model=java_model
        )

    def __init__(
        self,
        classname="com.johnsnowlabs.nlp.annotators.ner.NerConverterInternalModel",
        java_model=None,
    ):
        super(NerConverterInternalModel, self).__init__(
            classname=classname, java_model=java_model
        )
