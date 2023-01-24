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

from sparknlp_jsl.common import AnnotatorProperties, AnnotatorType


class DocumentHashCoder(AnnotatorTransformer, AnnotatorProperties):
    """Shifts date information for deidentification purposes.

    This annotator can replace dates in a column of `DOCUMENT`
    type according with the hash code of any other column.
    It uses the hash of the specified column and creates a new
    document column containing the day shift information.
    In sequence, the `DeIdentification` annotator deidentifies
    the document with the shifted date information.

    If the specified column contains strings that can be parsed
    to integers, use those numbers to make the shift in the data accordingly.


    ============================= ======================
    Input Annotation types        Output Annotation type
    ============================= ======================
    ``DOCUMENT``                   ``DOCUMENT``
    ============================= ======================

    Parameters
    ----------
    patientIdColumn: str
        column that contains string. Must be part of DOCUMENT
    dateShiftColumn: str
        column containing the date shift information
    newDateShift: str
        column that has a reference of where chunk begins
    seed: int
        seed for the random number generator
    rangeDays: int
        range of days to be sampled by the random generator

    Examples
    --------

    >>> import pandas as pd

    >>> data = pd.DataFrame(
    ...     {
    ...         "patientID": ["A001", "A001", "A003", "A003"],
    ...         "text": [
    ...             "Chris Brown was discharged on 10/02/2022",
    ...             "Mark White was discharged on 10/04/2022",
    ...             "John was discharged on 15/03/2022",
    ...             "John Moore was discharged on 15/12/2022",
    ...         ],
    ...         "dateshift": ["10", "10", "30", "30"],
    ...     }
    ... )

    >>> my_input_df = spark.createDataFrame(data)

    >>> documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")

    >>> documentHasher = (
    ...     DocumentHashCoder()
    ...     .setInputCols("document")
    ...     .setOutputCol("document2")
    ...     .setDateShiftColumn("dateshift")
    ... )

    >>> tokenizer = Tokenizer().setInputCols(["document2"]).setOutputCol("token")

    >>> embeddings = (
    ...     WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models")
    ...     .setInputCols(["document2", "token"])
    ...     .setOutputCol("word_embeddings")
    ... )

    >>> clinical_ner = (
    ...     MedicalNerModel.pretrained("ner_deid_subentity_augmented", "en", "clinical/models")
    ...     .setInputCols(["document2", "token", "word_embeddings"])
    ...     .setOutputCol("ner")
    ... )

    >>> ner_converter = (
    ...     NerConverter().setInputCols(["document2", "token", "ner"]).setOutputCol("ner_chunk")
    ... )

    >>> de_identification = (
    ...     DeIdentification()
    ...     .setInputCols(["ner_chunk", "token", "document2"])
    ...     .setOutputCol("deid_text")
    ...     .setMode("obfuscate")
    ...     .setObfuscateDate(True)
    ...     .setDateTag("DATE")
    ...     .setLanguage("en")
    ...     .setObfuscateRefSource("faker")
    ...     .setUseShifDays(True)
    ... )

    >>> pipeline_col = Pipeline().setStages(
    ...     [
    ...         documentAssembler,
    ...         documentHasher,
    ...         tokenizer,
    ...         embeddings,
    ...         clinical_ner,
    ...         ner_converter,
    ...         de_identification,
    ...     ]
    ... )

    >>> empty_data = spark.createDataFrame([["", "", ""]]).toDF(
    ...     "patientID", "text", "dateshift"
    ... )
    >>> pipeline_col_model = pipeline_col.fit(empty_data)

    >>> output = pipeline_col_model.transform(my_input_df)
    >>> output.select("text", "dateshift", "deid_text.result").show(truncate=False)
    +----------------------------------------+---------+----------------------------------------------+
    text                                    |dateshift|result                                        |
    +----------------------------------------+---------+----------------------------------------------+
    Chris Brown was discharged on 10/02/2022|10       |[Ellender Manual was discharged on 20/02/2022]|
    Mark White was discharged on 10/04/2022 |10       |[Errol Bang was discharged on 20/04/2022]     |
    John was discharged on 15/03/2022       |30       |[Ariel Null was discharged on 14/04/2022]     |
    John Moore was discharged on 15/12/2022 |30       |[Jean Cotton was discharged on 14/01/2023]    |
    +----------------------------------------+---------+----------------------------------------------+
    """
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT]
    outputAnnotatorType = AnnotatorType.CHUNK

    patientIdColumn = Param(
        Params._dummy(),
        "patientIdColumn",
        "Column containing the patient ID",
        typeConverter=TypeConverters.toString,
    )
    dateShiftColumn = Param(
        Params._dummy(),
        "dateShiftColumn",
        "Column containing the date shift information",
        typeConverter=TypeConverters.toString,
    )
    newDateShift = Param(
        Params._dummy(),
        "newDateShift",
        "Column that has a reference of where chunk begins",
        typeConverter=TypeConverters.toString,
    )
    seed = Param(
        Params._dummy(),
        "seed",
        "Seed for the random number generator",
        typeConverter=TypeConverters.toInt,
    )
    rangeDays = Param(
        Params._dummy(),
        "rangeDays",
        "Range of days to be sampled by the random generator",
        typeConverter=TypeConverters.toInt,
    )
    name = "DocumentHashCoder"

    @keyword_only
    def __init__(self):
        super(DocumentHashCoder, self).__init__(classname="com.johnsnowlabs.nlp.annotators.deid.DocumentHashCoder")
        self._setDefault(
            rangeDays=365
        )

    @keyword_only
    def setParams(self):
        """Sets the given parameters.
        """
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setPatientIdColumn(self, value):
        """Sets column that contains the string.

        Parameters
        ----------
        value : str
            Name of the column containing patient ID
        """
        return self._set(patientIdColumn=value)

    def setDateShiftColumn(self, value):
        """Sets column to be used for hash or predefined shift.

        Parameters
        ----------
        value : str
            Name of the column to be used
        """
        return self._set(dateShiftColumn=value)


    def setNewDateShift(self, value):
        """Sets column that has a reference of where chunk begins.

        Parameters
        ----------
        value : str
            Name of the reference column
        """
        return self._set(newDateShift=value)

    def setRangeDays(self, value):
        """Sets the range of dates to be sampled from.

        Parameters
        ----------
        value : int
            range of days to be sampled by the random generator
        """
        return self._set(rangeDays=value)

    def setSeed(self, value):
        """Sets the seed for random number generator.

        Parameters
        ----------
        value : int
            seed for the random number generator
        """
        return self._set(seed=value)


