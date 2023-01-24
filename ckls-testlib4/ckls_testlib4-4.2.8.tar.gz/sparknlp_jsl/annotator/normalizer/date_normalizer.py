from sparknlp_jsl.common import *

class DateNormalizer(AnnotatorModelInternal):
    """
    Try to normalize dates in chunks annotations.
    The expected format for the date will be YYYY/MM/DD.
    If the date is normalized then field normalized in metadata will be true else will be false.


    ====================== ======================
    Input Annotation types Output Annotation type
    ====================== ======================
    ``CHUNK``              ``CHUNK``
    ====================== ======================

    Parameters
    ----------
    anchorDateYear
        Add an anchor year for the relative dates such as a day after tomorrow.
        If not set it will use the current year. Example: 2021
    anchorDateMonth
        Add an anchor month for the relative dates such as a day after tomorrow.
        If not set it will use the current month. Example: 1 which means January
    anchorDateDay
        Add an anchor day of the day for the relative dates such as a day after
        tomorrow. If not set it will use the current day. Example: 11

    Examples
    --------
    >>> import sparknlp
    >>> from sparknlp.base import *
    >>> from sparknlp_jsl.common import *
    >>> from sparknlp.annotator import *
    >>> from sparknlp.training import *
    >>> import sparknlp_jsl
    >>> from sparknlp_jsl.base import *
    >>> from sparknlp_jsl.annotator import *
    >>> from pyspark.ml import Pipeline
    >>> dates = [
    ...     "08/02/2018",
    ...     "11/2018",
    ...     "11/01/2018",
    ...     "12Mar2021",
    ...     "Jan 30, 2018",
    ...     "13.04.1999",
    ...     "3April 2020",
    ...     "next monday",
    ...     "today",
    ...     "next week",
    ... ]
    >>> df = spark.createDataFrame(dates, StringType()).toDF("original_date")

    >>> document_assembler = (
    ...     DocumentAssembler().setInputCol("original_date").setOutputCol("document")
    ... )

    >>> doc2chunk = Doc2Chunk().setInputCols("document").setOutputCol("date_chunk")

    >>> date_normalizer = (
    ...     DateNormalizer()
    ...     .setInputCols("date_chunk")
    ...     .setOutputCol("date")
    ...     .setAnchorDateYear(2000)
    ...     .setAnchorDateMonth(3)
    ...     .setAnchorDateDay(15)
    ... )

    >>> pipeline = Pipeline(stages=[document_assembler, doc2chunk, date_normalizer])

    >>> result = pipeline.fit(df).transform(df)
    >>> result.selectExpr(
    ...     "date.result as normalized_date",
    ...     "original_date",
    ...     "date.metadata[0].normalized as metadata",
    ... ).show()

    +---------------+-------------+--------+
    |normalized_date|original_date|metadata|
    +---------------+-------------+--------+
    |   [2018/08/02]|   08/02/2018|    true|
    |   [2018/11/DD]|      11/2018|    true|
    |   [2018/11/01]|   11/01/2018|    true|
    |   [2021/03/12]|    12Mar2021|    true|
    |   [2018/01/30]| Jan 30, 2018|    true|
    |   [1999/04/13]|   13.04.1999|    true|
    |   [2020/04/03]|  3April 2020|    true|
    |   [2000/03/20]|  next monday|    true|
    |   [2000/03/15]|        today|    true|
    |   [2000/03/22]|    next week|    true|
    +---------------+-------------+--------+
    """
    inputAnnotatorTypes = [AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.CHUNK

    name = "DateNormalizer"

    anchorDateYear = Param(Params._dummy(),
                           "anchorDateYear",
                           "Add an anchor year for the relative dates such as a day after tomorrow. If not set it "
                           "will use the current year. Example: 2021",
                           typeConverter=TypeConverters.toInt
                           )

    anchorDateMonth = Param(Params._dummy(),
                            "anchorDateMonth",
                            "Add an anchor month for the relative dates such as a day after tomorrow. If not set it "
                            "will use the current month. Example: 1 which means January",
                            typeConverter=TypeConverters.toInt
                            )

    anchorDateDay = Param(Params._dummy(),
                          "anchorDateDay",
                          "Add an anchor day of the day for the relative dates such as a day after tomorrow. If not "
                          "set it will use the current day. Example: 11",
                          typeConverter=TypeConverters.toInt
                          )
    outputDateFormat = Param(Params._dummy(),
                          "outputDateFormat",
                          "If is eu should be YYYY/MM/DD if is usa should be  MM/DD/YYYY",
                          typeConverter=TypeConverters.toString
                          )


    defaultReplacementDay = Param(Params._dummy(),
                             "defaultReplacementDay",
                             "Defines which value to use for creating the Day Value when original Date-Entity has no Day Information. Defaults to 15.",
                             typeConverter=TypeConverters.toInt
                             )

    defaultReplacementMonth = Param(Params._dummy(),
                             "defaultReplacementMonth",
                             "Defines which value to use for creating the Month Value when original Date-Entity has no Day Information. Defaults to 6.",
                             typeConverter=TypeConverters.toInt
                             )


    defaultReplacementYear = Param(Params._dummy(),
                             "defaultReplacementYear",
                             "Defines which value to use for creating the Year Value when original Date-Entity has no Day Information. Defaults to 2020.",
                             typeConverter=TypeConverters.toInt
                             )


    def setAnchorDateYear(self, value):
        """Sets an anchor year for the relative dates such as a day after
        tomorrow. If not set it will use the current year.

        Example: 2021

        Parameters
        ----------
        value : int
            The anchor year for relative dates
        """
        return self._set(anchorDateYear=value)

    def setAnchorDateMonth(self, value):
        """Sets an anchor month for the relative dates such as a day after
        tomorrow. If not set it will use the current month.

        Example: 1 which means January

        Parameters
        ----------
        value : int
            The anchor month for relative dates
        """
        normalized_value = value - 1
        return self._set(anchorDateMonth=normalized_value)

    def setAnchorDateDay(self, value):
        """Sets an anchor day of the day for the relative dates such as a day
        after tomorrow. If not set it will use the current day.

        Example: 11

        Parameters
        ----------
        value : int
            The anchor day for relative dates
        """
        return self._set(anchorDateDay=value)
    def setOutputDateformat(self, value):
        """Sets an anchor day of the day for the relative dates such as a day
        after tomorrow. If not set it will use the current day.

        Example: 11

        Parameters
        ----------
        value : int
            The anchor day for relative dates
        """
        return self._set(outputDateFormat=value)



    def setDefaultReplacementDay(self, value):
        """Defines which value to use for creating the Day Value
        when original Date-Entity has no Day Information. Defaults to 15.

        Example: "11"

        Parameters
        ----------
        value : int
             The default value to use when creating a value for Day
             while normalizing and the original date has no day data
        """
        return self._set(defaultReplacementDay=value)

    def setDefaultReplacementMonth(self, value):
        """Defines which value to use for creating the Month Value when original Date-Entity has no Month Information.
        Defaults to 06.

        Example: "11"

        Parameters
        ----------
        value : int
             The default value to use when creating a value for
              Month while normalizing and the original date has no Month data
        """
        return self._set(defaultReplacementMonth=value)


    def setDefaultReplacementYear(self, value):
        """Defines which value to use for creating the Year Value when original Date-Entity has no Year Information.
        Defaults to 2020.

        Example: "2023"

        Parameters
        ----------
        value : int
             The default value to use when creating a value for
              Year while normalizing and the original date has no Year data
        """
        return self._set(defaultReplacementYear=value)


    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.normalizer.DateNormalizer", java_model=None):
        super(DateNormalizer, self).__init__(
            classname=classname,
            java_model=java_model
        )
