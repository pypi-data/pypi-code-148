#  Copyright 2017-2022 John Snow Labs
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from sparknlp_jsl.annotator import DocumentMLClassifierApproach as A
from sparknlp_jsl.annotator import DocumentMLClassifierModel as M
from sparknlp_jsl.common import *


class LegalDocumentMLClassifierApproach(A):
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
    ...    .setLabelColumn("category") \\
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

    def _create_model(self, java_model):
        return LegalDocumentMLClassifierModel(java_model=java_model)

    @keyword_only
    def __init__(self):
        super(A, self).__init__(
            classname="com.johnsnowlabs.legal.sequence_classification.LegalDocumentMLClassifierApproach")
        self._setDefault(
            labelCol="selector",
            maxIter=10,
            tol=1e-6,
            fitIntercept=True,
            vectorizationModelPath="",
            classificationModelPath="")

class LegalDocumentMLClassifierModel(M):
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

    name = "FinanceDocumentMLClassifierModel"

    def __init__(self, classname="com.johnsnowlabs.legal.sequence_classification.LegalClassifierDLModel",
                 java_model=None):
        super(LegalDocumentMLClassifierModel, self).__init__(
            classname=classname,
            java_model=java_model
        )

    @staticmethod
    def pretrained(name, lang="en", remote_loc=None):
        from sparknlp_jsl.pretrained import InternalResourceDownloader
        return InternalResourceDownloader.downloadModel(LegalDocumentMLClassifierModel, name, lang, remote_loc,
                                                        j_dwn='InternalsPythonResourceDownloader')
