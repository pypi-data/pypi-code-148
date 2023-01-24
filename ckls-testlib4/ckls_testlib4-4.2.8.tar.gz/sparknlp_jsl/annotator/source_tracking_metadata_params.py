from sparknlp_jsl.common import *


class SourceTrackingMetadataParams:

    includeOutputColumn = Param(
        Params._dummy(),
        "includeOutputColumn",
        "whether to include a metadata key/value to specify the output column name for the annotation",
        typeConverter=TypeConverters.toBoolean
    )

    def setIncludeOutputColumn(self, p):
        """Sets whether to include a metadata key/value to specify the output column name for the annotation

        Parameters
        ----------
        p : bool
            whether to include a metadata key/value to specify the output column name for the annotation
        """
        return self._set(includeOutputColumn=p)

    outputColumnKey = Param(Params._dummy(), "outputColumnKey",
                     "key name for the source column value",
                     TypeConverters.toString)

    def setOutputColumnKey(self, s):
        """Set key name for the source column value

        Parameters
        ----------
        s : str
           key name for the source column value
        """
        return self._set(outputColumnKey=s)

    includeStandardField = Param(
        Params._dummy(),
        "includeStandardField",
        "whether to include a metadata key/value to specify the output column name for the annotation",
        typeConverter=TypeConverters.toBoolean
    )

    def setIncludeStandardField(self, p):
        """Sets whether to include a metadata key/value to specify the output column name for the annotation

        Parameters
        ----------
        p : bool
            whether to include a metadata key/value to specify the output column name for the annotation
        """
        return self._set(includeStandardField=p)

    standardFieldKey = Param(Params._dummy(), "standardFieldKey",
                            "key name for the standard homogenized field",
                            TypeConverters.toString)

    def setStandardFieldKey(self, s):
        """Set key name for the source column value

        Parameters
        ----------
        s : str
           key name for the source column value
        """
        return self._set(standardFieldKey=s)

    allPossibleFieldsToStandardize = Param(
        Params._dummy(),
        "allPossibleFieldsToStandardize",
        "array with all possible fields containing the value to write in the standard field ordered by priority",
        typeConverter=TypeConverters.toListString
    )

    def setAllPossibleFieldsToStandardize(self, fields):
        """Sets array with all possible fields containing the value to write in the standard field ordered by priority

        Parameters
        ----------
        fields : list
            array with all possible fields containing the value to write in the standard field ordered by priority
        """
        return self._set(whiteList=fields)
