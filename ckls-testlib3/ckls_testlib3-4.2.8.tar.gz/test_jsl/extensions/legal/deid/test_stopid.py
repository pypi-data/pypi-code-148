import unittest
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame
import sparknlp_jsl
from sparknlp_jsl.annotator import *

from sparknlp_jsl.legal.chunk_classification.deid.document_hashcoder import LegalDocumentHashCoder
from test_jsl.extensions.utils import get_spark_session

import json
import os

import sparknlp
import sparknlp_jsl

from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp_jsl.annotator import *

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml import Pipeline, PipelineModel
from sparknlp.pretrained import PretrainedPipeline

import numpy as np
import pandas as pd

pd.set_option('display.max_colwidth', 200)

import warnings

warnings.filterwarnings('ignore')

spark = get_spark_session()
names = """Mitchell#NAME
Clifford#NAME
Jeremiah#NAME
Lawrence#NAME
Brittany#NAME
Patricia#NAME
Samantha#NAME
Jennifer#NAME
Jo#NAME
Wu#NAME
Yu#NAME
Jackson#NAME
Leonard#NAME
Randall#NAME
Camacho#NAME
Ferrell#NAME
Mueller#NAME
Bowman#NAME
Hansen#NAME
Acosta#NAME
Gillespie#NAME
Zimmerman#NAME
Gillespie#NAME
Chandler#NAME
Bradshaw#NAME
Ferguson#NAME
Jacobson#NAME
Figueroa#NAME
Chandler#NAME
Schaefer#NAME
Matthews#NAME
Ferguson#NAME
Bradshaw#NAME
Figueroa#NAME
Delacruz#NAME
Gallegos#NAME
Cox#NAME
Ray#NAME
Ray#NAME
Liu#NAME
Villarreal#NAME
Williamson#NAME
Montgomery#NAME
Mclaughlin#NAME
Blankenship#NAME
Fitzpatrick#NAME
Dana#NAME
Mike#NAME
Jill#NAME
Darlene#NAME
Pedro#NAME
Alice#NAME
Debra#NAME
Kim#NAME
Jill#NAME
Dana#NAME
Max#NAME
Zoe#NAME
Brandi#NAME
Travis#NAME
Melody#NAME"""

with open('names_test.txt', 'w') as file:
    file.write(names)

documentAssembler = DocumentAssembler() \
    .setInputCol("text") \
    .setOutputCol("document")


tokenizer = Tokenizer() \
    .setInputCols("sentence") \
    .setOutputCol("token")

tokenClassifier = MedicalBertForTokenClassifier.pretrained("bert_token_classifier_ner_deid", "en", "clinical/models") \
    .setInputCols(["sentence", "token"]) \
    .setOutputCol("ner") \
    .setCaseSensitive(True)

ner_converter_name = NerConverterInternal() \
    .setInputCols(["sentence", "token", "ner"]) \
    .setOutputCol("ner_chunk") \
    .setReplaceLabels({"PATIENT": "NAME"})
# .setWhiteList(['PATIENT'])
#

# p = "names_test.txt"
p = '/media/ckl/dump/Documents/freelance/MOST_RECENT/jsl/jsl_internal_latest69696/src/test/resources/obfuscator_names_test.txt'
nameChunkObfuscator = NameChunkObfuscatorApproach() \
    .setInputCols("ner_chunk") \
    .setOutputCol("replacement") \
    .setRefFileFormat("csv") \
    .setObfuscateRefFile(p) \
    .setRefSep("#")

replacer_name = Replacer() \
    .setInputCols("replacement", "document") \
    .setOutputCol("obfuscated_document_name") \
    .setUseReplacement(True)

sentenceDetector = SentenceDetector() \
    .setInputCols(["document"]) \
    .setOutputCol("sentence")

replacer_name._java_obj.setUseReplacement(True)

nlpPipeline = Pipeline(stages=[
    documentAssembler,
    sentenceDetector,
    tokenizer,
    tokenClassifier,
    ner_converter_name,
    nameChunkObfuscator,
    replacer_name,
    # replacer_date
])

empty_data = spark.createDataFrame([[""]]).toDF("text")
model = nlpPipeline.fit(empty_data)

# Looks messy but thats because of the ner model i think
# sample_text = '''Tom is friend of Ismae and he was born in 19/10/2000'''
sample_text = '''Tom is friend of Ismae'''

df = spark.createDataFrame([[sample_text]]).toDF("text")


lmodel = LightPipeline(model)

res = lmodel.fullAnnotate(sample_text)

print("Original text.  : ", res[0]['document'][0].result)
print("Obfuscated text : ", res[0]['obfuscated_document_name'][0].result)
# print("Obfuscated text : ", res[0]['obfuscated_document_date'][0].result)

"""

Original text.  :  Tom is friend of Ismae and he was born in 19/10/2000
Obfuscated text :  Ray is friend of <COUNTRY> and he was born in <AGE>
"""


print('LMAO?')