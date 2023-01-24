from sparknlp_jsl.common import *


class ContextualParserApproach(AnnotatorApproachInternal):
    """Creates a model that extracts entity from a document based on user defined rules.

    Rule matching is based on a RegexMatcher defined in a JSON file that can be set through the method setJsonPath().
    In this JSON file, regex is defined that you want to match along with the information that will output on metadata
    field. 
    
    Additionally, a dictionary can be provided with the setDictionary() method to map extracted entities
    to a unified representation. The first column of the dictionary file should be the representation with following
    columns the possible matches.

    ========================================= ======================
    Input Annotation types                    Output Annotation type
    ========================================= ======================
    ``DOCUMENT, TOKEN``                       ``CHUNK``
    ========================================= ======================

    Parameters
    ----------
    jsonPath
        Path to json file with rules
    caseSensitive
        Whether to use case sensitive when matching values
    prefixAndSuffixMatch
        Whether to match both prefix and suffix to annotate the hit
    dictionary
        Path to dictionary file in tsv or csv format
    optionalContextRules
        When set to true, it will output regex match regardless of context matches
    shortestContextMatch
        When set to true, it will stop finding for matches when prefix/suffix data is found in the text.
    completeContextMatch
        Whether to do an exact match of prefix and suffix.

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


    >>> documentAssembler = DocumentAssembler() \
    ...   .setInputCol("text") \
    ...   .setOutputCol("document")
    ...
    >>> sentenceDetector = SentenceDetector() \
    ...   .setInputCols(["document"]) \
    ...   .setOutputCol("sentence")
    ...
    >>> tokenizer = Tokenizer() \
    ...   .setInputCols(["sentence"]) \
    ...   .setOutputCol("token")

    Define the parser (json file needs to be provided)

    >>> data = spark.createDataFrame([["A patient has liver metastases pT1bN0M0 and the T5 primary site may be colon or... "]]).toDF("text")
    >>> contextualParser = ContextualParserApproach() \
    ...   .setInputCols(["sentence", "token"]) \
    ...   .setOutputCol("entity") \
    ...   .setJsonPath("/path/to/regex_token.json") \
    ...   .setCaseSensitive(True)
    ...
    >>> pipeline = Pipeline(stages=[
    ...     documentAssembler,
    ...     sentenceDetector,
    ...     tokenizer,
    ...     contextualParser
    ...   ])

    >>> result = pipeline.fit(data).transform(data)
    >>> result.selectExpr("explode(entity)").show(5, truncate=False)

    +-------------------------------------------------------------------------------------------------------------------------+
    |col                                                                                                                      |
    +-------------------------------------------------------------------------------------------------------------------------+
    |{chunk, 32, 39, pT1bN0M0, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 0}, []}                  |
    |{chunk, 49, 50, T5, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 0}, []}                        |
    |{chunk, 148, 156, cT4bcN2M1, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 1}, []}               |
    |{chunk, 189, 194, T?N3M1, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 2}, []}                  |
    |{chunk, 316, 323, pT1bN0M0, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 3}, []}                |
    +-------------------------------------------------------------------------------------------------------------------------+

    """
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT, AnnotatorType.TOKEN]
    outputAnnotatorType = AnnotatorType.CHUNK

    jsonPath = Param(Params._dummy(),
                     "jsonPath",
                     "Path to json file with regex rules. This parameter can also detect JSON format",
                     typeConverter=TypeConverters.toString)

    caseSensitive = Param(Params._dummy(),
                          "caseSensitive",
                          "Whether to use case sensitive when matching values",
                          typeConverter=TypeConverters.toBoolean)

    prefixAndSuffixMatch = Param(Params._dummy(),
                                 "prefixAndSuffixMatch",
                                 "Whether to match both prefix and suffix to annotate the hit",
                                 typeConverter=TypeConverters.toBoolean)

    dictionary = Param(Params._dummy(),
                       "dictionary",
                       "Path to dictionary file in tsv or csv format",
                       typeConverter=TypeConverters.identity)

    optionalContextRules = Param(Params._dummy(),
                                 "optionalContextRules",
                                 "When set to true, it will output regex match regardless of context matches",
                                 typeConverter=TypeConverters.toBoolean)

    shortestContextMatch = Param(Params._dummy(),
                                 "shortestContextMatch",
                                 "When set to true, it will stop finding for matches when prefix/suffix data is found in the text.",
                                 typeConverter=TypeConverters.toBoolean)

    completeContextMatch = Param(Params._dummy(),
                                 "completeContextMatch",
                                 "Whether to do an exact match of prefix and suffix.",
                                 typeConverter=TypeConverters.toBoolean)

    @keyword_only
    def __init__(self):
        super(ContextualParserApproach, self).__init__(
            classname="com.johnsnowlabs.nlp.annotators.context.ContextualParserApproach")
        self._setDefault(caseSensitive=False, prefixAndSuffixMatch=False, optionalContextRules=False,
                         shortestContextMatch=False, completeContextMatch=False,
                         jsonPath="")

    def setJsonPath(self, value):
        """Sets path to json file with rules

        Parameters
        ----------
        value : str
            Path to json file with rules
        """
        return self._set(jsonPath=value)

    def setCaseSensitive(self, value):
        """Sets whether to use case sensitive when matching values

        Parameters
        ----------
        value : bool
            Whether to use case sensitive when matching values
        """
        return self._set(caseSensitive=value)

    def setPrefixAndSuffixMatch(self, value):
        """Sets whether to match both prefix and suffix to annotate the hit

        Parameters
        ----------
        value : bool
            Whether to match both prefix and suffix to annotate the hit
        """
        return self._set(prefixAndSuffixMatch=value)

    def setDictionary(self, path, read_as=ReadAs.TEXT, options=None):
        """Sets dictionary. If set, it replaces regex from JSON config file"

        Parameters
        ----------
        path : str
            Path for dictionary location
        read_as: ReadAs
            Format of the file
        options: dict
            Dictionary with the options to read the file.
        """
        if options is None:
            options = {"delimiter": "\t"}
        return self._set(dictionary=ExternalResource(path, read_as, options))

    def setOptionalContextRules(self, value):
        """Sets whether it will output regex match regardless of context matches.

        Parameters
        ----------
        value : bool
           When set to true, it will output regex match regardless of context matches.
        """
        return self._set(optionalContextRules=value)

    def setShortestContextMatch(self, value):
        """Sets whether to stop finding for matches when prefix/suffix data is found in the text.

        Parameters
        ----------
        value : bool
            When set to true, it will stop finding for matches when prefix/suffix data is found in the text.
        """
        return self._set(shortestContextMatch=value)

    def setCompleteContextMatch(self, value):
        """Sets whether to do an exact match of prefix and suffix.

        Parameters
        ----------
        value : bool
            When set to true, it will make an exact match, i.e. regex with boundaries
        """
        return self._set(completeContextMatch=value)

    def _create_model(self, java_model):
        return ContextualParserModel(java_model=java_model)


class ContextualParserModel(AnnotatorModelInternal):
    """Extracts entity from a document based on user defined rules based on a RegexMatcher.
    
    To train a custom model, check the documentation of ContextualParserApproach. 
    

    ========================================= ======================
    Input Annotation types                    Output Annotation type
    ========================================= ======================
    ``DOCUMENT, TOKEN``                       ``CHUNK``
    ========================================= ======================

    Parameters
    ----------
    caseSensitive
        Whether to use case sensitive when matching values
    prefixAndSuffixMatch
        Whether to match both prefix and suffix to annotate the hit
    optionalContextRules
        When set to true, it will output regex match regardless of context matches
    shortestContextMatch
        When set to true, it will stop finding for matches when prefix/suffix data is found in the text.

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

    Which means to extract the stage code on a sentence level.
    An example pipeline could then be defined like this
    Pipeline could then be defined like this

    >>> documentAssembler = DocumentAssembler() \
    ...   .setInputCol("text") \
    ...   .setOutputCol("document")
    ...
    >>> sentenceDetector = SentenceDetector() \
    ...   .setInputCols(["document"]) \
    ...   .setOutputCol("sentence")
    ...
    >>> tokenizer = Tokenizer() \
    ...   .setInputCols(["sentence"]) \
    ...   .setOutputCol("token")

    >>> data = spark.createDataFrame([["A patient has liver metastases pT1bN0M0 and the T5 primary site may be colon or... "]]).toDF("text")
    >>> contextualParser = ContextualParserModel.load("mycontextualParserModel") \
    ...   .setInputCols(["sentence", "token"]) \
    ...   .setOutputCol("entity") \
    ...
    >>> pipeline = Pipeline(stages=[
    ...     documentAssembler,
    ...     sentenceDetector,
    ...     tokenizer,
    ...     contextualParser
    ...   ])

    >>> result = pipeline.fit(data).transform(data)
    >>> result.selectExpr("explode(entity)").show(5, truncate=False)

    +-------------------------------------------------------------------------------------------------------------------------+
    |col                                                                                                                      |
    +-------------------------------------------------------------------------------------------------------------------------+
    |{chunk, 32, 39, pT1bN0M0, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 0}, []}                  |
    |{chunk, 49, 50, T5, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 0}, []}                        |
    |{chunk, 148, 156, cT4bcN2M1, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 1}, []}               |
    |{chunk, 189, 194, T?N3M1, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 2}, []}                  |
    |{chunk, 316, 323, pT1bN0M0, {field -> Stage, normalized -> , confidenceValue -> 1.00, sentence -> 3}, []}                |
    +-------------------------------------------------------------------------------------------------------------------------+

    """
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT, AnnotatorType.TOKEN]
    outputAnnotatorType = AnnotatorType.CHUNK

    caseSensitive = Param(Params._dummy(),
                          "caseSensitive",
                          "Whether to use case sensitive when matching values",
                          typeConverter=TypeConverters.toBoolean)

    prefixAndSuffixMatch = Param(Params._dummy(),
                                 "prefixAndSuffixMatch",
                                 "Whether to match both prefix and suffix to annotate the hit",
                                 typeConverter=TypeConverters.toBoolean)

    optionalContextRules = Param(Params._dummy(),
                                 "optionalContextRules",
                                 "When set to true, it will output regex match regardless of context matches",
                                 typeConverter=TypeConverters.toBoolean)

    shortestContextMatch = Param(Params._dummy(),
                                 "shortestContextMatch",
                                 "When set to true, it will stop finding for matches when prefix/suffix data is found in the text.",
                                 typeConverter=TypeConverters.toBoolean)

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.context.ContextualParserModel", java_model=None):
        super(ContextualParserModel, self).__init__(
            classname=classname,
            java_model=java_model
        )
        self._setDefault(caseSensitive=False, prefixAndSuffixMatch=False,
                         optionalContextRules=False, shortestContextMatch=False)

    def setCaseSensitive(self, value):
        """Sets whether to use case sensitive when matching values

        Parameters
        ----------
        value : bool
            Whether to use case sensitive when matching values
        """
        return self._set(caseSensitive=value)

    def setPrefixAndSuffixMatch(self, value):
        """Sets whether to match both prefix and suffix to annotate the hit

        Parameters
        ----------
        value : bool
            Whether to match both prefix and suffix to annotate the hit
        """

        return self._set(prefixAndSuffixMatch=value)

    def setOptionalContextRules(self, value):
        """Sets whether it will output regex match regardless of context matches.

        Parameters
        ----------
        value : bool
           When set to true, it will output regex match regardless of context matches.
        """
        return self._set(optionalContextRules=value)

    def setShortestContextMatch(self, value):
        """Sets whether to stop finding for matches when prefix/suffix data is found in the text.

        Parameters
        ----------
        value : bool
            When set to true, it will stop finding for matches when prefix/suffix data is found in the text.
        """
        return self._set(shortestContextMatch=value)
