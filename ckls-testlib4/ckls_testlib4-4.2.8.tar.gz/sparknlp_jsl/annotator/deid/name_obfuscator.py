from pyspark import keyword_only
from pyspark.ml.param import TypeConverters, Params, Param
from sparknlp.internal import AnnotatorTransformer

from sparknlp_jsl.common import *

class NameChunkObfuscatorApproach(AnnotatorApproachInternal):
    inputAnnotatorTypes = [AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.CHUNK
    obfuscateRefFile = Param(Params._dummy(), "obfuscateRefFile", "File with the terms to be used for Obfuscation",
                             TypeConverters.toString)
    refFileFormat = Param(Params._dummy(), "refFileFormat", "Format of the reference file", TypeConverters.toString)
    refSep = Param(Params._dummy(), "refSep", "Sep character in refFile", TypeConverters.toString)
    seed = Param(Params._dummy(), "seed", "It is the seed to select the entities on obfuscate mode",
                 TypeConverters.toInt)


    @keyword_only
    def __init__(self):
        super(NameChunkObfuscatorApproach, self).__init__(classname="com.johnsnowlabs.nlp.annotators.deid.NameChunkObfuscatorApproach")


    def setObfuscateRefFile(self, f):
        """Set file with the terms to be used for Obfuscation

        Parameters
        ----------
        f : str
            File with the terms to be used for Obfuscation
        """
        return self._set(obfuscateRefFile=f)

    def setRefFileFormat(self, f):
        """Sets format of the reference file

        Parameters
        ----------
        f : str
            Format of the reference file
        """
        return self._set(refFileFormat=f)

    def setRefSep(self, c):
        """Sets separator character in refFile

        Parameters
        ----------
        f : str
            Separator character in refFile
        """
        return self._set(refSep=c)

    def setSeed(self, s):
        """Sets the seed to select the entities on obfuscate mode

        Parameters
        ----------
        s : int
            The seed to select the entities on obfuscate mode
        """
        return self._set(seed=s)
    def _create_model(self, java_model):
            return NameChunkObfuscator(java_model=java_model)


class NameChunkObfuscator(AnnotatorModelInternal):
    inputAnnotatorTypes = [AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.CHUNK

    seed = Param(Params._dummy(), "seed", "It is the seed to select the entities on obfuscate mode",
                 TypeConverters.toInt)
    def setSeed(self, s):
        """Sets the seed to select the entities on obfuscate mode

        Parameters
        ----------
        s : int
            The seed to select the entities on obfuscate mode
        """
        return self._set(seed=s)

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.deid.NameChunkObfuscator", java_model=None):
        super(NameChunkObfuscator, self).__init__(
            classname=classname,
            java_model=java_model
        )

    @staticmethod
    def pretrained(name, lang="en", remote_loc=None):
        from sparknlp.pretrained import ResourceDownloader
        return ResourceDownloader.downloadModel(NameChunkObfuscator, name, lang, remote_loc,
                                                j_dwn='InternalsPythonResourceDownloader')
