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

import sys

from sparknlp import annotator
from sparknlp.base import DocumentAssembler
from sparknlp_jsl.common import *
from sparknlp.annotator.classifier_dl.classifier_dl import ClassifierDLModel as M
from sparknlp.annotator.classifier_dl.classifier_dl import ClassifierDLApproach as A


class FinanceClassifierDLApproach(A):
    """Trains a ClassifierDL for generic Multi-class Text Classification.

    ClassifierDL uses the state-of-the-art Universal Sentence Encoder as an
    input for text classifications.
    The ClassifierDL annotator uses a deep learning model (DNNs) we have built
    inside TensorFlow and supports up to 100 classes.

    For instantiated/pretrained models, see :class:`.ClassifierDLModel`.

    For extended examples of usage, see the Spark NLP Workshop
    `Spark NLP Workshop  <https://github.com/JohnSnowLabs/spark-nlp-workshop/blob/master/tutorials/Certification_Trainings/Public/5.Text_Classification_with_ClassifierDL.ipynb>`__.

    ======================= ======================
    Input Annotation types  Output Annotation type
    ======================= ======================
    ``SENTENCE_EMBEDDINGS`` ``CATEGORY``
    ======================= ======================

    Parameters
    ----------
    lr
        Learning Rate, by default 0.005
    batchSize
        Batch size, by default 64
    dropout
        Dropout coefficient, by default 0.5
    maxEpochs
        Maximum number of epochs to train, by default 30
    configProtoBytes
        ConfigProto from tensorflow, serialized into byte array.
    validationSplit
        Choose the proportion of training dataset to be validated against the
        model on each Epoch. The value should be between 0.0 and 1.0 and by
        default it is 0.0 and off.
    enableOutputLogs
        Whether to use stdout in addition to Spark logs, by default False
    outputLogsPath
        Folder path to save training logs
    labelColumn
        Column with label per each token
    verbose
        Level of verbosity during training
    randomSeed
        Random seed for shuffling

    Notes
    -----
    - This annotator accepts a label column of a single item in either type of
      String, Int, Float, or Double.
    - UniversalSentenceEncoder, Transformer based embeddings, or
      SentenceEmbeddings can be used for the ``inputCol``.

    Examples
    --------
    >>> import sparknlp
    >>> from sparknlp.base import *
    >>> from sparknlp.annotator import *
    >>> from pyspark.ml import Pipeline

    In this example, the training data ``"sentiment.csv"`` has the form of::

        text,label
        This movie is the best movie I have wached ever! In my opinion this movie can win an award.,0
        This was a terrible movie! The acting was bad really bad!,1
        ...

    Then traning can be done like so:

    >>> smallCorpus = spark.read.option("header","True").csv("src/test/resources/classifier/sentiment.csv")
    >>> documentAssembler = DocumentAssembler() \\
    ...     .setInputCol("text") \\
    ...     .setOutputCol("document")
    >>> useEmbeddings = UniversalSentenceEncoder.pretrained() \\
    ...     .setInputCols("document") \\
    ...     .setOutputCol("sentence_embeddings")
    >>> docClassifier = ClassifierDLApproach() \\
    ...     .setInputCols("sentence_embeddings") \\
    ...     .setOutputCol("category") \\
    ...     .setLabelColumn("label") \\
    ...     .setBatchSize(64) \\
    ...     .setMaxEpochs(20) \\
    ...     .setLr(5e-3) \\
    ...     .setDropout(0.5)
    >>> pipeline = Pipeline().setStages([
    ...     documentAssembler,
    ...     useEmbeddings,
    ...     docClassifier
    ... ])
    >>> pipelineModel = pipeline.fit(smallCorpus)

    See Also
    --------
    MultiClassifierDLApproach : for multi-class classification
    SentimentDLApproach : for sentiment analysis
    """

    def _create_model(self, java_model):
        return FinanceClassifierDLModel(java_model=java_model)

    @keyword_only
    def __init__(self):
        super(A, self).__init__(
            classname="com.johnsnowlabs.finance.sequence_classification.FinanceClassifierDLApproach")
        self._setDefault(
            maxEpochs=30,
            lr=float(0.005),
            batchSize=64,
            dropout=float(0.5),
            enableOutputLogs=False
        )


class FinanceClassifierDLModel(M):
    """FinanceClassifierDL for generic Multi-class Text Classification.

    ClassifierDL uses the state-of-the-art Universal Sentence Encoder as an
    input for text classifications. The ClassifierDL annotator uses a deep
    learning model (DNNs) we have built inside TensorFlow and supports up to
    100 classes.

    This is the instantiated model of the :class:`.ClassifierDLApproach`.
    For training your own model, please see the documentation of that class.

    Pretrained models can be loaded with :meth:`.pretrained` of the companion
    object:

    >>> classifierDL = ClassifierDLModel.pretrained() \\
    ...     .setInputCols(["sentence_embeddings"]) \\
    ...     .setOutputCol("classification")

    The default model is ``"classifierdl_use_trec6"``, if no name is provided.
    It uses embeddings from the UniversalSentenceEncoder and is trained on the
    `TREC-6 <https://deepai.org/dataset/trec-6#:~:text=The%20TREC%20dataset%20is%20dataset,50%20has%20finer%2Dgrained%20labels>`__
    dataset.

    For available pretrained models please see the
    `Models Hub <https://nlp.johnsnowlabs.com/models?task=Text+Classification>`__.

    For extended examples of usage, see the
    `Spark NLP Workshop <https://github.com/JohnSnowLabs/spark-nlp-workshop/blob/master/tutorials/Certification_Trainings/Public/5.Text_Classification_with_ClassifierDL.ipynb>`__.

    ======================= ======================
    Input Annotation types  Output Annotation type
    ======================= ======================
    ``SENTENCE_EMBEDDINGS`` ``CATEGORY``
    ======================= ======================

    Parameters
    ----------
    configProtoBytes
        ConfigProto from tensorflow, serialized into byte array.
    classes
        Get the tags used to trained this ClassifierDLModel

    Examples
    --------
    >>> import sparknlp
    >>> from sparknlp.base import *
    >>> from sparknlp.annotator import *
    >>> from pyspark.ml import Pipeline
    >>> documentAssembler = DocumentAssembler() \\
    ...     .setInputCol("text") \\
    ...     .setOutputCol("document")
    >>> sentence = SentenceDetector() \\
    ...     .setInputCols("document") \\
    ...     .setOutputCol("sentence")
    >>> useEmbeddings = UniversalSentenceEncoder.pretrained() \\
    ...     .setInputCols("document") \\
    ...     .setOutputCol("sentence_embeddings")
    >>> sarcasmDL = ClassifierDLModel.pretrained("classifierdl_use_sarcasm") \\
    ...     .setInputCols("sentence_embeddings") \\
    ...     .setOutputCol("sarcasm")
    >>> pipeline = Pipeline() \\
    ...     .setStages([
    ...       documentAssembler,
    ...       sentence,
    ...       useEmbeddings,
    ...       sarcasmDL
    ...     ])
    >>> data = spark.createDataFrame([
    ...     ["I'm ready!"],
    ...     ["If I could put into words how much I love waking up at 6 am on Mondays I would."]
    ... ]).toDF("text")
    >>> result = pipeline.fit(data).transform(data)
    >>> result.selectExpr("explode(arrays_zip(sentence, sarcasm)) as out") \\
    ...     .selectExpr("out.sentence.result as sentence", "out.sarcasm.result as sarcasm") \\
    ...     .show(truncate=False)
    +-------------------------------------------------------------------------------+-------+
    |sentence                                                                       |sarcasm|
    +-------------------------------------------------------------------------------+-------+
    |I'm ready!                                                                     |normal |
    |If I could put into words how much I love waking up at 6 am on Mondays I would.|sarcasm|
    +-------------------------------------------------------------------------------+-------+

    See Also
    --------
    MultiClassifierDLModel : for multi-class classification
    SentimentDLModel : for sentiment analysis
    """

    name = "FinanceClassifierDLModel"

    def __init__(self, classname="com.johnsnowlabs.finance.sequence_classification.FinanceClassifierDLModel",
                 java_model=None):
        super(FinanceClassifierDLModel, self).__init__(
            classname=classname,
            java_model=java_model
        )

    @staticmethod
    def pretrained(name, lang="en", remote_loc=None):
        from sparknlp_jsl.pretrained import InternalResourceDownloader
        return InternalResourceDownloader.downloadModel(FinanceClassifierDLModel, name, lang, remote_loc,
                                                        j_dwn='InternalsPythonResourceDownloader')
