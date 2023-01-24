from sparknlp_jsl.common import *

class ChunkMapperFuzzyMatchingParams:
    enableTokenFingerprintMatching = Param(Params._dummy(),
                                           "enableTokenFingerprintMatching",
                                           "Whether to apply partial token Ngram fingerprint matching; this will create matching keys with partial Ngrams driven by three params: minTokenNgramFingerprint, maxTokenNgramFingerprint, maxTokenNgramDropping.",
                                           typeConverter=TypeConverters.toBoolean)

    def setEnableTokenFingerprintMatching(self, etfm):
        return self._set(enableTokenFingerprintMatching=etfm)

    enableCharFingerprintMatching = Param(Params._dummy(),
                                          "enableCharFingerprintMatching",
                                          "Whether to apply char Ngram fingerprint matching",
                                          typeConverter=TypeConverters.toBoolean)

    def setEnableCharFingerprintMatching(self, ecfm):
        return self._set(enableCharFingerprintMatching=ecfm)

    enableFuzzyMatching =  Param(Params._dummy(),
                                 "enableFuzzyMatching",
                                 "Whether to apply fuzzy matching",
                                 typeConverter=TypeConverters.toBoolean)

    def setEnableFuzzyMatching(self, efm):
        return self._set(enableFuzzyMatching=efm)

    maxTokenNgramFingerprint = Param(Params._dummy(),
                                       "maxTokenNgramFingerprint",
                                       "When enableTokenFingerprintMatching is true, the max number of tokens for partial Ngrams in Fingerprint",
                                       typeConverter=TypeConverters.toInt)

    def setMaxTokenNgramFingerprint(self, mxtnf):
        return self._set(maxTokenNgramFingerprint=mxtnf)

    minTokenNgramFingerprint = Param(Params._dummy(),
                                     "minTokenNgramFingerprint",
                                     "When enableTokenFingerprintMatching is true, the min number of tokens for partial Ngrams in Fingerprint",
                                     typeConverter=TypeConverters.toInt)

    def setMinTokenNgramFingerprint(self, mntnf):
        return self._set(minTokenNgramFingerprint=mntnf)

    maxTokenNgramDroppingTokens = Param(Params._dummy(),
                                  "maxTokenNgramDroppingTokens",
                                  "When enableTokenNgramMatching is true, this value drives the maximum number of tokens allowed to be dropped from the full chunk; " +
                                  "whenever it is desired for all Ngrams to be used as keys, no matter how short the final chunk is, this param should be set to a very high value: i.e sys.maxsize",
                                  typeConverter=TypeConverters.toInt)

    def setMaxTokenNgramDroppingTokens(self, etd):
        return self._set(maxTokenNgramDroppingTokens=etd)

    maxTokenNgramDroppingCharsRatio = Param(Params._dummy(),
                                            "maxTokenNgramDroppingCharsRatio",
                                            "When enableTokenNgramMatching is true, this value drives the max amount of tokens to allow dropping based on the maximum ratio of chars allowed to be dropped from the full chunk; " +
                                            "whenever it is desired for all Ngrams to be used as keys, no matter how short the final chunk is, this param should be set to 1.0",
                                            typeConverter=TypeConverters.toFloat)

    def setMaxTokenNgramDroppingCharsRatio(self, etd):
        return self._set(maxTokenNgramDroppingCharsRatio=etd)

    maxTokenNgramDroppingOperator = Param(Params._dummy(),
                                            "maxTokenNgramDroppingOperator",
                                            "When enableTokenNgramMatching is true, this value drives the max amount of tokens to allow dropping based on the maximum ratio of chars allowed to be dropped from the full chunk; " +
                                            "whenever it is desired for all Ngrams to be used as keys, no matter how short, this param should be set to 1.0",
                                            typeConverter=TypeConverters.toString)

    def setMaxTokenNgramDroppingOperator(self, etd):
        return self._set(maxTokenNgramDroppingOperator=etd)

    maxCharNgramFingerprint = Param(Params._dummy(),
                                    "maxCharNgramFingerprint",
                                    "When enableCharFingerprintMatching is true, the max number of chars for Ngrams in Fingerprint",
                                    typeConverter=TypeConverters.toInt)

    def setMaxCharNgramFingerprint(self, etfm):
        return self._set(maxCharNgramFingerprint=etfm)

    minCharNgramFingerprint = Param(Params._dummy(),
                                    "minCharNgramFingerprint",
                                    "When enableCharFingerprintMatching is true, the min number of chars for Ngrams in Fingerprint",
                                    typeConverter=TypeConverters.toInt)

    def setMinCharNgramFingerprint(self, etfm):
        return self._set(minCharNgramFingerprint=etfm)

    fuzzyMatchingDistances = Param(Params._dummy(),
                                   "fuzzyMatchingDistances",
                                   "When enableFuzzyMatching is true, this array contains the distances to calculate; " +
                                   "possible values are: levenshtein, longest-common-subsequence, cosine, jaccard",
                                   typeConverter=TypeConverters.toListString)

    def setFuzzyMatchingDistances(self, fmd):
        return self._set(fuzzyMatchingDistances=fmd)

    fuzzyMatchingDistanceThresholds = Param(Params._dummy(),
                                            "fuzzyMatchingDistanceThresholds",
                                            "When enableFuzzyMatching is true, the scaling mode for Integer Edit Distances; possible values are: left, right, long, short, none",
                                            typeConverter=TypeConverters.toListFloat)

    def setFuzzyMatchingDistanceThresholds(self, fmdth):
        if type(fmdth) != list:
            fmdth = [fmdth]
        return self._set(fuzzyMatchingDistanceThresholds=fmdth)

    fuzzyDistanceScalingMode = Param(Params._dummy(),
                                          "fuzzyDistanceScalingMode",
                                          "When enableFuzzyMatching is true, the scaling mode for Integer Edit Distances; possible values are: left, right, long, short, none",
                                          typeConverter=TypeConverters.toString)

    def setFuzzyDistanceScalingMode(self, fdsm):
        return self._set(fuzzyDistanceScalingMode=fdsm)


class CommonChunkMapperParams:
    allowMultiTokenChunk = Param(Params._dummy(),
                                 "allowMultiTokenChunk",
                                 "Whether   skyp relations with multitokens",
                                 typeConverter=TypeConverters.toBoolean)
    def setAllowMultiTokenChunk(self,mc):
        """Whether  if we skip relations with multitokens
        Parameters
        ----------
        mc : bool
            "Whether  to decide if we want to send multi-chunk tokens or only single token chunks
        """
        return self._set(allowMultiTokenChunk=mc)

    multivaluesRelations = Param(Params._dummy(),
                                 "multivaluesRelations",
                                 "Whether  to decide if we want to send multi-chunk tokens or only single token chunks",
                                 typeConverter=TypeConverters.toBoolean)
    def setMultivaluesRelations(self,mc):
        """Whether  to decide if we want to send multi-chunk tokens or only single token chunks
        Parameters
        ----------
         mc : bool
             "Whether  to decide if we want to send multi-chunk tokens or only single token chunks
        """
        return self._set(multivaluesRelations=mc)

    rel = Param(Params._dummy(),
                "rel",
                "Relation for the model",
                typeConverter=TypeConverters.toString)

    def setRel(self, r):
        return self._set(rel=r)

    rels = Param(Params._dummy(),
                 "rels",
                 "relations to be mapped in the dictionary",
                 typeConverter=TypeConverters.toListString)

    def setRels(self, rs):
        return self._set(rels=rs)

    lowerCase = Param(Params._dummy(),
                      "lowerCase",
                      "Set if we want to save the dictionary in lower case or not",
                      typeConverter=TypeConverters.toBoolean)

    def setLowerCase(self,lc):
        """Set if we want to save the keys of the dictionary in lower case or not
        Parameters
        ----------
        lc : bool
            Parameter that select if you want to use the keys in lower case or not
        """
        return self._set(lowerCase=lc)


class ChunkMapperApproach(AnnotatorApproachInternal, CommonChunkMapperParams, ChunkMapperFuzzyMatchingParams):
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
    inputAnnotatorTypes = [AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.LABELED_DEPENDENCY

    name = "ChunkMapperApproach"

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

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.chunker.ChunkMapperApproach"):
        super(ChunkMapperApproach, self).__init__(
            classname=classname
        )
    def _create_model(self, java_model):
        return ChunkMapperModel(java_model=java_model)


class ChunkMapperModel(AnnotatorModelInternal, CommonChunkMapperParams, ChunkMapperFuzzyMatchingParams):
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
    >>> chunkerMapperapproach = ChunkMapperModel()\
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
    inputAnnotatorTypes = [AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.LABELED_DEPENDENCY

    name = "ChunkMapperModel"

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.chunker.ChunkMapperModel", java_model=None):
        super(ChunkMapperModel, self).__init__(
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
        ChunkMapperModel
            The restored model
        """
        from sparknlp_jsl.pretrained import InternalResourceDownloader
        return InternalResourceDownloader.downloadModel(ChunkMapperModel, name, lang, remote_loc,
                                                        j_dwn='InternalsPythonResourceDownloader')