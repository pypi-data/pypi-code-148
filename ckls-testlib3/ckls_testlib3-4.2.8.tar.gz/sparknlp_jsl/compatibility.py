"""Verifies which models are compatible with the current distribution.
"""
from pyspark.sql import SparkSession


class Compatibility:
    """Verifies which models are compatible with the current distribution.
    """

    def __init__(self, spark: SparkSession):
        self.spark = spark

        self.instance = self.spark._jvm.com.johnsnowlabs.util.Compatibility()

    def findVersion(self, model: str = "all"):
        """Returns the private models that are compatible with the current library version.

        Parameters
        ----------
        model : str
            Name of the model that you try to find.
            If 'all' (default), returns all private models.
        """
        result = self.instance.findVersion(model)
        return result

    def showVersion(self, model: str = "all"):
        """Prints the private models that are compatibles with the current library version.

        Parameters
        ----------
        model : str
            Name of the model that you try to find.
            If 'all' (default), prints all private models.
        """
        print(self.instance.showStringVersion(model))
