from pyspark import keyword_only
from pyspark.ml.param import TypeConverters, Params, Param
from sparknlp.internal import AnnotatorTransformer

from sparknlp_jsl.common import AnnotatorModelInternal, AnnotatorType


class Replacer(AnnotatorModelInternal):
    name = "Replacer"
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT, AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.DOCUMENT
    useReplacement = Param(Params._dummy(), "useReplacement", "I",
                           TypeConverters.toBoolean)


    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.deid.Replacer", java_model=None):
        super(Replacer, self).__init__(
            classname=classname,
            java_model=java_model
        )

    def setUseReplacement(self, value):
        """Enable or disable Replacement of entities

        Parameters
        ----------
        value : bool
            True for Replacing, False otherwise.
        """
        return self._set(useReplacement=value)

    def getUseReplacement(self):
        """Enable or disable Replacement of entities

        Parameters
        ----------
        value : bool
            True for Replacing, False otherwise.
        """
        return self.getOrDefault(self.useReplacement)
