from sparknlp_jsl.common import *


class CommonChunkMergeParams:
    mergeOverlapping = Param(Params._dummy(),
                             "mergeOverlapping",
                             "whether to merge overlapping matched chunks. Defaults false",
                             typeConverter=TypeConverters.toBoolean)

    def setMergeOverlapping(self, b):
        """Sets whether to merge overlapping matched chunks. Defaults false

        Parameters
        ----------
        b : bool
            whether to merge overlapping matched chunks. Defaults false

        """
        return self._set(mergeOverlapping=b)

    blackList = Param(Params._dummy(), "blackList",
                      "If defined, list of entities to ignore. The rest will be processed. Do not include IOB prefix on labels",
                      TypeConverters.toListString)

    def setBlackList(self, entities):
        """If defined, list of entities to ignore. The rest will be processed.

        Parameters
        ----------
        entities : list
           If defined, list of entities to ignore. The rest will be processed.
        """
        return self._set(blackList=entities)


class MergePriorizationParams:
    orderingFeatures = Param(Params._dummy(), "orderingFeatures",
                             "Array of strings specifying the ordering features to use for overlapping entities. Possible values are ChunkBegin, ChunkLength, ChunkPrecedence, ChunkConfidence.",
                             TypeConverters.toListString)

    def setOrderingFeatures(self, _orderingFeatures):
        """Sets Array of strings specifying the ordering features to use for overlapping entities. Possible values are ChunkBegin, ChunkLength, ChunkPrecedence, ChunkConfidence.

        Parameters
        ----------
        _orderingFeatures : list
           Array of strings specifying the ordering features to use for overlapping entities. Possible values are ChunkBegin, ChunkLength, ChunkPrecedence, ChunkConfidence.
        """
        return self._set(orderingFeatures=_orderingFeatures)

    selectionStrategy = Param(Params._dummy(),
                              "selectionStrategy",
                              "Whether to select annotations sequentially based on annotation order (Sequential) or using any other available strategy, currently only DiverseLonger is available.",
                              typeConverter=TypeConverters.toString)

    def setSelectionStrategy(self, _selectionStrategy):
        """Sets Whether to select annotations sequentially based on annotation order (Sequential) or using any other available strategy, currently only DiverseLonger is available.

        Parameters
        ----------
        _selectionStrategy : str
            Whether to select annotations sequentially based on annotation order (Sequential) or using any other available strategy, currently only DiverseLonger is available.

        """
        return self._set(selectionStrategy=_selectionStrategy)

    defaultConfidence = Param(Params._dummy(),
                              "chunkPrecedence",
                              "When ChunkConfidence Strategy is included and a given annotation does not have any confidence the value of this param will be used.",
                              typeConverter=TypeConverters.toFloat)

    def setDefaultConfidence(self, _defaultConfidence):
        """Sets when ChunkConfidence Strategy is included and a given annotation does not have any confidence the value of this param will be used.

        Parameters
        ----------
        _defaultConfidence : str
            When ChunkConfidence Strategy is included and a given annotation does not have any confidence the value of this param will be used.

        """
        return self._set(defaultConfidence=_defaultConfidence)

    chunkPrecedence = Param(Params._dummy(),
                            "chunkPrecedence",
                            "When ChunkPrecedence Strategy is used this param contains the comma separated metadata fields that drive prioritization of overlapping annotations. When used by itself (empty chunkPrecedenceValuePrioritization) annotations will be prioritized based on number of metadata fields present. When used together with chunkPrecedenceValuePrioritization param it will prioritize based on the order of its values.",
                            typeConverter=TypeConverters.toString)

    def setChunkPrecedence(self, _chunkPrecedence):
        """Sets ChunkPrecedence param

        Parameters
        ----------
        _chunkPrecedence : str
            Single or comma separated metadata fields that drive prioritization of overlapping annotations. When used by itself (empty chunkPrecedenceValuePrioritization) annotations will be prioritized based on number of metadata fields present. When used together with chunkPrecedenceValuePrioritization param it will prioritize based on the order of its values.

        """
        return self._set(chunkPrecedence=_chunkPrecedence)

    chunkPrecedenceValuePrioritization = Param(Params._dummy(), "chunkPrecedenceValuePrioritization",
                                               "When ChunkPrecedence Strategy is used this param contains an Array of comma separated strings representing the desired order of prioritization for the values in the metadata fields included in chunkPrecedence.",
                                               TypeConverters.toListString)

    def setChunkPrecedenceValuePrioritization(self, _chunkPrecedenceValuePrioritization):
        """When ChunkPrecedence Strategy is used this param contains an Array of comma separated strings representing the desired order of prioritization for the values in the metadata fields included in chunkPrecedence.

        Parameters
        ----------
        _chunkPrecedenceValuePrioritization : list
           Array of strings specifying the ordering features to use for overlapping entities. Possible values are ChunkBegin, ChunkLength, ChunkPrecedence, ChunkConfidence.
        """
        return self._set(chunkPrecedenceValuePrioritization=_chunkPrecedenceValuePrioritization)


class ChunkMergeApproach(AnnotatorApproachInternal, CommonChunkMergeParams, MergePriorizationParams):
    """
    Merges two chunk columns coming from two annotators(NER, ContextualParser or any other annotator producing
    chunks). The merger of the two chunk columns is made by selecting one chunk from one of the columns according
    to certain criteria.
    The decision on which chunk to select is made according to the chunk indices in the source document.
    (chunks with longer lengths and highest information will be kept from each source)
    Labels can be changed by setReplaceDictResource.

    =========================== ======================
    Input Annotation types      Output Annotation type
    =========================== ======================
    ``CHUNK,CHUNK``               ``CHUNK``
    =========================== ======================

    Parameters
    ----------
    mergeOverlapping
        whether to merge overlapping matched chunks. Defaults false
    falsePositivesResource
        file with false positive pairs
    replaceDictResource
        replace dictionary pairs
    chunkPrecedence
        Select what is the precedence when two chunks have the same start and end indices. Possible values are [entity|identifier|field]
    blackList
        If defined, list of entities to ignore. The rest will be proccessed.

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
    Define a pipeline with 2 different NER models with a ChunkMergeApproach at the end
    >>> data = spark.createDataFrame([["A 63-year-old man presents to the hospital ..."]]).toDF("text")
    >>> pipeline = Pipeline(stages=[
    ...  DocumentAssembler().setInputCol("text").setOutputCol("document"),
    ...  SentenceDetector().setInputCols(["document"]).setOutputCol("sentence"),
    ...  Tokenizer().setInputCols(["sentence"]).setOutputCol("token"),
    ...   WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models").setOutputCol("embs"),
    ...   MedicalNerModel.pretrained("ner_jsl", "en", "clinical/models") \\
    ...     .setInputCols(["sentence", "token", "embs"]).setOutputCol("jsl_ner"),
    ...  NerConverter().setInputCols(["sentence", "token", "jsl_ner"]).setOutputCol("jsl_ner_chunk"),
    ...   MedicalNerModel.pretrained("ner_bionlp", "en", "clinical/models") \\
    ...     .setInputCols(["sentence", "token", "embs"]).setOutputCol("bionlp_ner"),
    ...  NerConverter().setInputCols(["sentence", "token", "bionlp_ner"]) \\
    ...     .setOutputCol("bionlp_ner_chunk"),
    ...  ChunkMergeApproach().setInputCols(["jsl_ner_chunk", "bionlp_ner_chunk"]).setOutputCol("merged_chunk")
    >>> ])
    >>> result = pipeline.fit(data).transform(data).cache()
    >>> result.selectExpr("explode(merged_chunk) as a") \\
    ...   .selectExpr("a.begin","a.end","a.result as chunk","a.metadata.entity as entity") \\
    ...   .show(5, False)
    +-----+---+-----------+---------+
    |begin|end|chunk      |entity   |
    +-----+---+-----------+---------+
    |5    |15 |63-year-old|Age      |
    |17   |19 |man        |Gender   |
    |64   |72 |recurrent  |Modifier |
    |98   |107|cellulitis |Diagnosis|
    |110  |119|pneumonias |Diagnosis|
    +-----+---+-----------+---------+
    """
    inputAnnotatorTypes = [AnnotatorType.CHUNK, AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.CHUNK

    name = "ChunkMergeApproach"

    falsePositivesResource = Param(Params._dummy(),
                                   "falsePositivesResource",
                                   "file with false positive pairs",
                                   typeConverter=TypeConverters.identity)

    replaceDictResource = Param(Params._dummy(),
                                "replaceDictResource",
                                "replace dictionary pairs",
                                typeConverter=TypeConverters.identity)

    def setFalsePositivesResource(self, path, read_as=ReadAs.TEXT, options=None):
        """Sets file with false positive pairs

        Parameters
        ----------
        path : str
            Path to the external resource
        read_as : str, optional
            How to read the resource, by default ReadAs.TEXT
        options : dict, optional
            Options for reading the resource, by default {"format": "text"}

        """
        if options is None:
            options = {"delimiter": "\t"}
        return self._set(falsePositivesResource=ExternalResource(path, read_as, options))

    def setReplaceDictResource(self, path, read_as=ReadAs.TEXT, options={"delimiter": ","}):
        """Sets replace dictionary pairs

        Parameters
        ----------
        path : str
            Path to the external resource

        read_as : str, optional
            How to read the resource, by default ReadAs.TEXT
        options : dict, optional
            Options for reading the resource, by default {"format": "text"}
        """

        return self._set(replaceDictResource=ExternalResource(path, read_as, options))

    @keyword_only
    def __init__(self):
        super(ChunkMergeApproach, self).__init__(classname="com.johnsnowlabs.nlp.annotators.merge.ChunkMergeApproach")

    def _create_model(self, java_model):
        return ChunkMergeModel(java_model=java_model)

    def setInputCols(self, *value):
        """Sets column names of input annotations.
        Parameters
        ----------
        *value : str
            Input columns for the annotator
        """
        # Overloaded setInputCols to evade validation until updated on Spark-NLP side
        if type(value[0]) == str or type(value[0]) == list:
            # self.inputColsValidation(value)
            if len(value) == 1 and type(value[0]) == list:
                return self._set(inputCols=value[0])
            else:
                return self._set(inputCols=list(value))
        else:
            raise TypeError("InputCols datatype not supported. It must be either str or list")


class ChunkMergeModel(AnnotatorModelInternal, CommonChunkMergeParams, MergePriorizationParams):
    """
    The model produced by ChunkMergerAproach.

    =========================== ======================
    Input Annotation types      Output Annotation type
    =========================== ======================
    ``CHUNK,CHUNK``             ``CHUNK``
    =========================== ======================

    Parameters
    ----------

    mergeOverlapping
        whether to merge overlapping matched chunks. Defaults false
    chunkPrecedence
        Select what is the precedence when two chunks have the same start and end indices. Possible values are [entity|identifier|field]
    blackList
        If defined, list of entities to ignore. The rest will be proccessed.
    """
    name = "ChunkMergeModel"

    inputAnnotatorTypes = [AnnotatorType.CHUNK, AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.CHUNK

    falsePositives = Param(Params._dummy(), "falsePositives", "list of false positive tuples (text, entity)",
                           typeConverter=TypeConverters.identity)
    replaceDict = Param(Params._dummy(), "replaceDict", "dictionary of entities to replace",
                        typeConverter=TypeConverters.identity)

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.merge.ChunkMergeModel",
                 java_model=None):
        super(ChunkMergeModel, self).__init__(
            classname=classname,
            java_model=java_model
        )

    @staticmethod
    def pretrained(name, lang="en", remote_loc=None):
        from sparknlp_jsl.pretrained import InternalResourceDownloader
        return InternalResourceDownloader.downloadModel(ChunkMergeModel, name, lang, remote_loc,
                                                        j_dwn='InternalsPythonResourceDownloader')

    def setInputCols(self, *value):
        """Sets column names of input annotations.
        Parameters
        ----------
        *value : str
            Input columns for the annotator
        """
        # Overloaded setInputCols to evade validation until updated on Spark-NLP side
        if type(value[0]) == str or type(value[0]) == list:
            # self.inputColsValidation(value)
            if len(value) == 1 and type(value[0]) == list:
                return self._set(inputCols=value[0])
            else:
                return self._set(inputCols=list(value))
        else:
            raise TypeError("InputCols datatype not supported. It must be either str or list")
