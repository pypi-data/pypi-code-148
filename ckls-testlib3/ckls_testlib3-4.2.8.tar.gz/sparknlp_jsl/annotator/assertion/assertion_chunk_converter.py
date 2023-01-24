
from sparknlp_jsl.common import *
from sparknlp.internal import AnnotatorTransformer

from sparknlp import DocumentAssembler
class AssertionChunkConverter(AnnotatorTransformer):
    """Creates an extended chunk column with metadata that can be used for assertion status detection model training.

    In some cases, there may be issues while creating the chunk column by using
    token indices and losing some data while training and testing the assertion
    status model if there are issues in these token indices.

    > Chunk begin and end indices in the assertion status model training dataframe
    > can be populated using the new version of ALAB module.

    Args:
        chunkTextCol (str): Name of the column containing the text of the chunk
        chunkBeginCol (str): Name of the column containing the start index of the chunk
        chunkEndCol (str): Name of the column containing the end index of the chunk
        outputTokenBeginCol (str): Name of the column containing selected token start index
        outputTokenEndCol (str): Name of the column containing selected token end index

    Examples

    >>> data = spark.createDataFrame([
    ...     ["An angiography showed bleeding in two vessels off of the Minnie supplying the sigmoid that were succesfully embolized.", 
    ...     "Minnie", 57, 64],
    ...     ["After discussing this with his PCP, Leon was clear that the patient had had recurrent DVTs and ultimately a PE and his PCP felt strongly that he required long-term anticoagulation ", 
    ...     "PCP", 31, 34]]).toDF("text", "target", "char_begin", "char_end")
    >>> document_assembler = DocumentAssembler() \
    ...     .setInputCol("text") \
    ...     .setOutputCol("document")
    >>> sentenceDetector = SentenceDetector()\
    ...     .setInputCols(["document"])\
    ...     .setOutputCol("sentence")
    >>> tokenizer = Tokenizer() \
    ...     .setInputCols(["sentence"]) \
    ...     .setOutputCol("tokens")
    >>> converter = AssertionChunkConverter() \
    ...     .setInputCols("tokens")\
    ...     .setChunkTextCol("target")\
    ...     .setChunkBeginCol("char_begin")\
    ...     .setChunkEndCol("char_end")\
    ...     .setOutputTokenBeginCol("token_begin")\
    ...     .setOutputTokenEndCol("token_end")\
    ...     .setOutputCol("chunk")
    >>> pipeline = Pipeline().setStages([document_assembler,sentenceDetector, tokenizer, converter])
    >>> results = pipeline.fit(data).transform(data)
    >>> results\
    ... .selectExpr(
    ...     "target",
    ...     "char_begin",
    ...     "char_end",
    ...     "token_begin",
    ...     "token_end",
    ...     "tokens[token_begin].result",
    ...     "tokens[token_end].result",
    ...     "target",
    ...     "chunk")\
    ... .show(truncate=False)
    +------+----------+--------+-----------+---------+--------------------------+------------------------+------+----------------------------------------------+
    |target|char_begin|char_end|token_begin|token_end|tokens[token_begin].result|tokens[token_end].result|target|chunk                                         |
    +------+----------+--------+-----------+---------+--------------------------+------------------------+------+----------------------------------------------+
    |Minnie|57        |64      |10         |10       |Minnie                    |Minnie                  |Minnie|[{chunk, 57, 62, Minnie, {sentence -> 0}, []}]|
    |PCP   |31        |34      |5          |5        |PCP                       |PCP                     |PCP   |[{chunk, 31, 33, PCP, {sentence -> 0}, []}]   |
    +------+----------+--------+-----------+---------+--------------------------+------------------------+------+----------------------------------------------+
    """

    name = 'AssertionChunkConverter'

    inputAnnotatorTypes = [AnnotatorType.TOKEN]
    outputAnnotatorType = AnnotatorType.CHUNK

    inputCols = Param(Params._dummy(), "inputCols",
                      "input annotations",
                      typeConverter=TypeConverters.toListString)

    outputCol = Param(Params._dummy(), "outputCol",
                       "output finished annotation col",
                       typeConverter=TypeConverters.toString)

    chunkTextCol = Param(Params._dummy(), "chunkTextCol",
                         "Name of the column containing the text of the chunk",
                          TypeConverters.toString)
    chunkBeginCol = Param(Params._dummy(), "chunkBeginCol",
                         "Name of the column containing the start index of the chunk",
                         TypeConverters.toString)
    chunkEndCol = Param(Params._dummy(), "chunkEndCol",
                          "Name of the column containing the end index of the chunk",
                          TypeConverters.toString)
    outputTokenBeginCol = Param(Params._dummy(), "outputTokenBeginCol",
                        "Name of the column containing selected token start index",
                        TypeConverters.toString)
    outputTokenEndCol = Param(Params._dummy(), "outputTokenEndCol",
                                "Name of the column containing selected token end index",
                                TypeConverters.toString)


    def setInputCols(self, *value):
        """Sets column names of input annotations.

        Parameters
        ----------
        *value : str
            Input columns for the annotator
        """
        if len(value) == 1 and type(value[0]) == list:
            return self._set(inputCols=value[0])
        else:
            return self._set(inputCols=list(value))

    def setOutputCol(self, value):
        """Sets column name of output annotations.

        Parameters
        ----------
        *value : str
            Name of output columns
        """
        return self._set(outputCol=value)

    def setChunkTextCol(self, col):
        """Sets the name of the column containing the text of the chunk.

        Parameters
        ----------
        col : string
            Name of the column containing the text of the chunk
        """
        return self._set(chunkTextCol=col)


    def setChunkBeginCol(self, col):
        """Sets the name of the column containing the start index of the chunk.

        Parameters
        ----------
        col : string
            Name of the column containing the start index of the chunk
        """
        return self._set(chunkBeginCol=col)

    def setChunkEndCol(self, col):
        """Sets the name of the column containing the end index of the chunk.

        Parameters
        ----------
        col : string
            Name of the column containing the end index of the chunk
        """
        return self._set(chunkEndCol=col)

    def setOutputTokenBeginCol(self, col):
        """Sets the name of the column containing selected token start index.

        Parameters
        ----------
        col : string
            Name of the column containing selected token start index
        """
        return self._set(outputTokenBeginCol=col)

    def setOutputTokenEndCol(self, col):
        """Sets the name of the column containing selected token end index.

        Parameters
        ----------
        col : string
            Name of the column containing selected token end index
        """
        return self._set(outputTokenEndCol=col)

    @keyword_only
    def __init__(self):
        super(AssertionChunkConverter, self)\
            .__init__(classname="com.johnsnowlabs.nlp.annotators.assertion.AssertionChunkConverter")

    @keyword_only
    def setParams(self):
        kwargs = self._input_kwargs
        return self._set(**kwargs)
