from sparknlp_jsl.common import *
from sparknlp_jsl.utils.licensed_annotator_type import InternalAnnotatorType


class AverageEmbeddings(AnnotatorModelInternal):
    """Averages two embdeddings into one.
    """
    name = "AverageEmbeddings"
    inputAnnotatorTypes = [AnnotatorType.SENTENCE_EMBEDDINGS, AnnotatorType.SENTENCE_EMBEDDINGS, AnnotatorType.CHUNK, ]
    outputAnnotatorType = AnnotatorType.SENTENCE_EMBEDDINGS

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.embeddings.AverageEmbeddings", java_model=None):
        super(AverageEmbeddings, self).__init__(
            classname=classname,
            java_model=java_model
        )
