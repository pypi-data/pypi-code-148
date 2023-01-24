from sparknlp_jsl.common import *

class ChunkMapperFilterer(AnnotatorModelInternal):
    """Filters chunks mapped or not by ChunkMapper.

    Filters chunks based on whether the ChunkMapper annotator
    successfully mapped the chunk or not.

    ==============================   =======================
        Input Annotation types        Output Annotation type
    ==============================   =======================
    ``CHUNK``,``LABEL_DEPENDENCY``          ``CHUNK``
    ==============================   =======================

    Parameters
    ----------
    returnCriteria (str)
        Has two possible values: "success" or "fail".
        If "fail" (default), returns the chunks that are not in the label dependencies;
        if "success", returns the labels that were successfully mapped by the ChunkMapper annotator.
    """
    inputAnnotatorTypes = [AnnotatorType.CHUNK, AnnotatorType.LABELED_DEPENDENCY]
    outputAnnotatorType = AnnotatorType.CHUNK

    name = "ChunkMapperFiltererModel"

    returnCriteria = Param(Params._dummy(),
                           "returnCriteria",
                           "Select what kind o chunk we will return. If is fail will return the chunk that are no in the label depencies if is success return the labels that are label dependencies",
                           typeConverter=TypeConverters.toString)

    def setReturnCriteria(self, return_criteria: str):
        """Sets the return criteria.

        Args:
            return_criteria (str): the new return criteria ("success" or "fail")

        Returns:
            self: the object itself
        """
        return self._set(returnCriteria=return_criteria)

    def __init__(self,
                 classname="com.johnsnowlabs.nlp.annotators.chunker.ChunkMapperFilterer",
                 java_model=None):
        super(ChunkMapperFilterer, self).__init__(
            classname=classname,
            java_model=java_model
        )