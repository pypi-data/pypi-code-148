from sparknlp_jsl.common import *


class DocumentMLClassifierParams:
    labels = Param(Params._dummy(), "labels", "array to output the label in the original form.",
                   typeConverter=TypeConverters.toListString)

    def setLabels(self, value):
        """Sets array to output the label in the original form.

        Parameters
        ----------
        label : list
           array to output the label in the original form.

        """
        return self._set(labels=value)

    mergeChunks = Param(Params._dummy(), "mergeChunks", "whether or not to combine all chunks and make a single query",
                        typeConverter=TypeConverters.toBoolean)

    def setMergeChunks(self, merge):
        """Sets whether to merge all chunks in a document or not (Default: false)

        Parameters
        ----------
        merge : list
           whether to merge all chunks in a document or not (Default: false)
        """
        return self._set(mergeChunks=merge)

    minTokenNgram = Param(Params._dummy(), "minTokenNgram", "the min number of tokens for Ngrams.",
                          TypeConverters.toInt)

    maxTokenNgram = Param(Params._dummy(), "maxTokenNgram", "the max number of tokens for Ngrams.",
                          TypeConverters.toInt)


class DocumentMLClassifierApproach(AnnotatorApproachInternal, DocumentMLClassifierParams):
    """Trains a model to classify documents with a Logarithmic Regression algorithm. Training data requires columns for
    text and their label. The result is a trained GenericClassifierModel.

    ========================================= ======================
    Input Annotation types                    Output Annotation type
    ========================================= ======================
    ``TOKEN``                       `         ``CATEGORY``
    ========================================= ======================

    Parameters
    ----------
    labelCol
        Column with the value result we are trying to predict.
    maxIter
        maximum number of iterations.
    tol
        convergence tolerance after each iteration.
    fitIntercept
        whether to fit an intercept term, default is true.
    labels
        array to output the label in the original form.
    vectorizationModelPath
        specify the vectorization model if it has been already trained.
    classificationModelPath
        specify the classification model if it has been already trained.
    classificationModelClass
        specify the SparkML classification class; possible values are: logreg, svm.
    maxTokenNgram
        the max number of tokens for Ngrams
    minTokenNgram
        the min number of tokens for Ngrams
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

    An example pipeline could then be defined like this

    >>> tokenizer = Tokenizer() \\
    ...    .setInputCols("document") \\
    ...    .setOutputCol("token")
    ...
    >>> normalizer = Normalizer() \\
    ...    .setInputCols("token") \\
    ...    .setOutputCol("normalized")
    ...
    >>> stopwords_cleaner = StopWordsCleaner()\\
    ...    .setInputCols("normalized")\\
    ...    .setOutputCol("cleanTokens")\\
    ...    .setCaseSensitive(False)
    ...
    ...stemmer = Stemmer() \
    ...    .setInputCols("cleanTokens") \
    ...    .setOutputCol("stem")
    ...
    >>> gen_clf = DocumentMLClassifierApproach() \\
    ...    .setlabelCol("category") \\
    ...    .setInputCols("stem") \\
    ...    .setOutputCol("prediction")
    ...
    >>> pipeline = Pipeline().setStages([
    ...    document_assembler,
    ...    tokenizer,
    ...    normalizer,
    ...    stopwords_cleaner,
    ...    stemmer,
    ...    gen_clf
    ...])
    ...
    >>> clf_model = pipeline.fit(data)
    """

    inputAnnotatorTypes = [AnnotatorType.TOKEN]
    outputAnnotatorType = AnnotatorType.CATEGORY

    labelCol = Param(Params._dummy(), "labelCol", "column with the value result we are trying to predict.",
                     typeConverter=TypeConverters.toString)
    maxIter = Param(Params._dummy(), "maxIter", "maximum number of iterations.", TypeConverters.toInt)
    tol = Param(Params._dummy(), "tol", "convergence tolerance after each iteration.", TypeConverters.toFloat)
    fitIntercept = Param(Params._dummy(), "fitIntercept", "whether to fit an intercept term, default is true.",
                         typeConverter=TypeConverters.toBoolean)
    vectorizationModelPath = Param(Params._dummy(), "vectorizationModelPath",
                                   "specify the vectorization model if it has been already trained.",
                                   typeConverter=TypeConverters.toString)
    classificationModelPath = Param(Params._dummy(), "classificationModelPath",
                                    "specify the classification model if it has been already trained.",
                                    typeConverter=TypeConverters.toString)
    classificationModelClass = Param(Params._dummy(), "classificationModelClass",
                                     "specify the SparkML classification class; possible values are: logreg, svm.",
                                     typeConverter=TypeConverters.toString)

    def setLabelCol(self, label):
        """Sets column with the value result we are trying to predict.

        Parameters
        ----------
        label : str
            Column with the value result we are trying to predict.

        """
        return self._set(labelCol=label)

    def setMaxIter(self, k):
        """Sets maximum number of iterations.

        Parameters
        ----------
        k : int
             Maximum number of iterations.

        """
        return self._set(maxIter=k)

    def setTol(self, dist):
        """Sets  convergence tolerance after each iteration.

        Parameters
        ----------
        dist : float
            Convergence tolerance after each iteration.

        """
        return self._set(tol=dist)

    def setFitIntercept(self, merge):
        """Sets whether to fit an intercept term, default is true.

        Parameters
        ----------
        label : str
            Whether to fit an intercept term, default is true.

        """
        return self._set(fitIntercept=merge)

    def setVectorizationModelPath(self, value):
        """Sets a path to the classification model if it has been already trained.

        Parameters
        ----------
        label : str
          Path to the classification model if it has been already trained.

        """
        return self._set(vectorizationModelPath=value)

    def setClassificationModelPath(self, value):
        """Sets a path to the classification model if it has been already trained.

        Parameters
        ----------
        label : str
            Path to the classification model if it has been already trained.

        """
        return self._set(classificationModelPath=value)

    def setClassificationModelClass(self, value):
        """Sets a the classification model class from SparkML to use; possible values are: logreg, svm.

        Parameters
        ----------
        label : str
            specify the SparkML classification class; possible values are: logreg, svm.

        """
        return self._set(classificationModelClass=value)

    def setMinTokenNgram(self, k):
        """Sets minimum number of tokens for Ngrams.

        Parameters
        ----------
        k : int
             Minimum number of tokens for Ngrams.

        """
        return self._set(minTokenNgram=k)

    def setMaxTokenNgram(self, k):
        """Sets maximum number of tokens for Ngrams.

        Parameters
        ----------
        k : int
             Maximum number of tokens for Ngrams.

        """
        return self._set(maxTokenNgram=k)

    def _create_model(self, java_model):
        return DocumentMLClassifierModel(java_model=java_model)

    @keyword_only
    def __init__(self):
        super(DocumentMLClassifierApproach, self).__init__(
            classname="com.johnsnowlabs.nlp.annotators.classification.DocumentMLClassifierApproach")
        self._setDefault(
            labelCol="selector",
            maxIter=10,
            tol=1e-6,
            fitIntercept=True,
            vectorizationModelPath="",
            classificationModelPath="")


class DocumentMLClassifierModel(AnnotatorModelInternal, DocumentMLClassifierParams):
    """ Classifies documents with a Logarithmic Regression algorithm.


    ========================================= ======================
    Input Annotation types                    Output Annotation type
    ========================================= ======================
    ``TOKEN``                                 ``CATEGORY``
    ========================================= ======================

    Parameters
    ----------
    mergeChunks
        Whether to merge all chunks in a document or not (Default: false)
    labels
        Array to output the label in the original form.
    vectorizationModel
       Vectorization model if it has been already trained.
    classificationModel
        Classification model if it has been already trained.
    """
    name = "DocumentMLClassifierModel"

    inputAnnotatorTypes = [AnnotatorType.TOKEN]
    outputAnnotatorType = AnnotatorType.CATEGORY

    vectorizationModel = Param(Params._dummy(), "vectorizationModel", "wrapped vectorization model.",
                               typeConverter=TypeConverters.identity)
    classificationModel = Param(Params._dummy(), "classificationModel", "wrapped classification model.",
                                typeConverter=TypeConverters.identity)
    labels = Param(Params._dummy(), "labels", "array to output the label in the original form.",
                   typeConverter=TypeConverters.toListString)

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.classification.DocumentMLClassifierModel",
                 java_model=None):
        super(DocumentMLClassifierModel, self).__init__(
            classname=classname,
            java_model=java_model
        )

    def setLabels(self, value):
        """Sets array to output the label in the original form.

        Parameters
        ----------
        label : list
           array to output the label in the original form.

        """
        return self._set(labels=value)

    def setVectorizationModel(self, model):
        """Sets a path to the classification model if it has been already trained.

        Parameters
        ----------
        model: :class:`pyspark.ml.PipelineModel`
            Classification model if it has been already trained.

        """
        return self._set(vectorizationModel=model)

    def setClassificationModel(self, model):
        """Sets a path to the classification model if it has been already trained.

        Parameters
        ----------
        model: :class:`pyspark.ml.PipelineModel`
            Classification model if it has been already trained.

        """
        return self._set(classificationModel=model)

    @staticmethod
    def pretrained(name, lang="en", remote_loc=None):
        from sparknlp_jsl.pretrained import InternalResourceDownloader
        return InternalResourceDownloader.downloadModel(DocumentMLClassifierModel, name, lang, remote_loc,
                                                        j_dwn='InternalsPythonResourceDownloader')
