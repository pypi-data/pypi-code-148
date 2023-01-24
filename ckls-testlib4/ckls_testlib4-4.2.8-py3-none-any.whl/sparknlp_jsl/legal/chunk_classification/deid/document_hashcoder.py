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
"""Contains classes for Doc2Chunk."""

from pyspark import keyword_only
from pyspark.ml.param import TypeConverters, Params, Param
from sparknlp.internal import AnnotatorTransformer

from sparknlp_jsl.common import AnnotatorProperties

from sparknlp_jsl.annotator import DocumentHashCoder as A


class LegalDocumentHashCoder(A):
    """Converts ``DOCUMENT`` type annotations into ``CHUNK`` type with the
    contents of a ``chunkCol``.

    Chunk text must be contained within input ``DOCUMENT``. May be either
    ``StringType`` or ``ArrayType[StringType]`` (using setIsArray). Useful for
    annotators that require a CHUNK type input.

    For more extended examples on document pre-processing see the
    `Spark NLP Workshop <https://github.com/JohnSnowLabs/spark-nlp-workshop/blob/master/tutorials/Certification_Trainings/Public/2.Text_Preprocessing_with_SparkNLP_Annotators_Transformers.ipynb>`__.

    ====================== ======================
    Input Annotation types Output Annotation type
    ====================== ======================
    ``DOCUMENT``           ``CHUNK``
    ====================== ======================

    Parameters
    ----------
    chunkCol
        Column that contains the string. Must be part of DOCUMENT
    startCol
        Column that has a reference of where the chunk begins
    startColByTokenIndex
        Whether start column is prepended by whitespace tokens
    isArray
        Whether the chunkCol is an array of strings, by default False
    failOnMissing
        Whether to fail the job if a chunk is not found within document.
        Return empty otherwise
    lowerCase
        Whether to lower case for matching case

    Examples
    --------
    >>> import sparknlp
    >>> from sparknlp.base import *
    >>> from sparknlp_jsl.common import *
    >>> from sparknlp.annotator import *
    >>> from sparknlp.training import *
    >>> from pyspark.ml import Pipeline
    >>> documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
    >>> chunkAssembler = Doc2Chunk() \\
    ...     .setInputCols("document") \\
    ...     .setChunkCol("target") \\
    ...     .setOutputCol("chunk") \\
    ...     .setIsArray(True)
    >>> data = spark.createDataFrame([[
    ...     "Spark NLP is an open-source text processing library for advanced natural language processing.",
    ...     ["Spark NLP", "text processing library", "natural language processing"]
    ... ]]).toDF("text", "target")
    >>> pipeline = Pipeline().setStages([documentAssembler, chunkAssembler]).fit(data)
    >>> result = pipeline.transform(data)
    >>> result.selectExpr("chunk.result", "chunk.annotatorType").show(truncate=False)
    +-----------------------------------------------------------------+---------------------+
    |result                                                           |annotatorType        |
    +-----------------------------------------------------------------+---------------------+
    |[Spark NLP, text processing library, natural language processing]|[chunk, chunk, chunk]|
    +-----------------------------------------------------------------+---------------------+

    See Also
    --------
    Chunk2Doc : for converting `CHUNK` annotations to `DOCUMENT`
    """

    @keyword_only
    def __init__(self):
        super(A, self).__init__(classname="com.johnsnowlabs.legal.deid.LegalDocumentHashCoder")
        self._setDefault(
            rangeDays=365
        )
