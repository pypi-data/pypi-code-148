from sparknlp_jsl.common import *


class ResolverMerger(AnnotatorModelInternal):
    """
        Merge Label dependencies entities and the Sentence enitity resolver returning the sentence entity resolver.

        ===============================  =======================
        Input Annotation types            Output Annotation type
        ===============================  =======================
        ``ENTITY``,``LABEL_DEPENDENCY``  ``ENTITY``
        ===============================  =======================

    """

    inputAnnotatorTypes = [AnnotatorType.ENTITY, AnnotatorType.LABELED_DEPENDENCY]
    outputAnnotatorType = AnnotatorType.ENTITY

    name = "ResolverMerger"

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.resolution.ResolverMerger", java_model=None):
        super(ResolverMerger, self).__init__(
            classname=classname,
            java_model=java_model
        )
