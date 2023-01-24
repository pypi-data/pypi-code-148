def __get_class(clazz: str):
    """
    Loads Python class from its name.
    If this fail, Pyspark will also fail to resolve the class path
    """
    print(f'Import for clzz= {clazz}')
    parts = clazz.split(".")
    module = ".".join(parts[:-1])
    print(f'importing {module} ')
    m = __import__(module)
    for comp in parts[1:]:
        print(f'Getting {comp} from {m.__name__}')
        m = getattr(m, comp)
    return m
clazz='sparknlp.annotator.Resolution2Chunk'
__get_class(clazz)


# com.johnsnowlabs.extensions
# print("_____________")
# clazz='com.johnsnowlabs.finance.chunk_classification.assertion'
# clazz='com.johnsnowlabs.nlp'
# __get_class(clazz)
#
# clazz='com.johnsnowlabs.finance.sequence_classification.FinanceBertForSequenceClassification'
# __get_class(clazz)



# AttributeError: module 'com.johnsnowlabs.finance' has no attribute 'FinanceClassifierDLModel'
"""
_____________
Import for clzz= com.johnsnowlabs.finance
importing com.johnsnowlabs 
Getting johnsnowlabs from <module 'com' from '/home/ckl/old_home/ckl/Documents/freelance/jsl/nlu/nlu4realgit3/nlu_venv/lib/python3.9/site-packages/com/__init__.py'>
Getting finance from <module 'com.johnsnowlabs' from '/home/ckl/old_home/ckl/Documents/freelance/jsl/nlu/nlu4realgit3/nlu_venv/lib/python3.9/site-packages/com/johnsnowlabs/__init__.py'>

Process finished with exit code 0




class	tail_class	file_name
com.johnsnowlabs.nlp.annotators.classifier.dl.ClassifierDLModel	ClassifierDLModel	legclf_recognition_clause_en_1.0.0_3.2_1660123901737
com.johnsnowlabs.legal.token_classification.ner.LegalNerModel	LegalNerModel	legner_br_large_pt_1.0.0_3.2_1660044366089
com.johnsnowlabs.legal.token_classification.ner.LegalBertForTokenClassification	LegalBertForTokenClassification	legner_obligations_en_1.0.0_3.2_1661182145726
com.johnsnowlabs.legal.graph.relation_extraction.RelationExtractionDLModel	RelationExtractionDLModel	legre_contract_doc_parties_en_1.0.0_3.2_1660293010932
com.johnsnowlabs.nlp.annotators.classifier.dl.BertForTokenClassification	BertForTokenClassification	legner_bert_large_courts_de_1.0.0_3.2_1660056373355
com.johnsnowlabs.legal.chunk_classification.resolution.ChunkMapperModel	ChunkMapperModel	legmapper_edgar_irs_en_1.0.0_3.2_1660817727715
com.johnsnowlabs.nlp.annotators.classifier.dl.RoBertaForSequenceClassification	RoBertaForSequenceClassification	legclf_human_rights_en_1.0.0_3.2_1660057114857
com.johnsnowlabs.nlp.annotators.classifier.dl.BertForQuestionAnswering	BertForQuestionAnswering	legqa_bert_en_1.0.0_3.2_1660054695560
org.apache.spark.ml.Pipeline	Pipeline	legpipe_whereas_en_1.0.0_3.2_1661340138139
com.johnsnowlabs.nlp.annotators.classifier.dl.RoBertaForTokenClassification	RoBertaForTokenClassification	legner_law_money_es_1.0.0_3.2_1660052484876
com.johnsnowlabs.legal.graph.relation_extraction.ZeroShotRelationExtractionModel	ZeroShotRelationExtractionModel	legre_zero_shot_en_1.0.0_3.2_1661181212397
com.johnsnowlabs.nlp.annotators.classification.MedicalBertForTokenClassifier	MedicalBertForTokenClassifier	legner_bert_base_courts_de_1.0.0_3.2_1660055531439
org.apache.spark.ml.PipelineModel	PipelineModel	legpipe_deid_en_1.0.0_3.2_1660839594078
com.johnsnowlabs.legal.chunk_classification.resolution.SentenceEntityResolverModel	SentenceEntityResolverModel	legel_crunchbase_companynames_en_1.0.0_3.2_1660041489236
com.johnsnowlabs.nlp.annotators.classifier.dl.RoBertaForQuestionAnswering	RoBertaForQuestionAnswering	legqa_roberta_en_1.0.0_3.2_1660054617548

















{
'SentenceEntityResolverModel':	'com.johnsnowlabs.legal.chunk_classification.resolution.SentenceEntityResolverModel',
'ChunkMapperModel':	'com.johnsnowlabs.legal.chunk_classification.resolution.ChunkMapperModel',
'AssertionDLModel':	'com.johnsnowlabs.legal.chunk_classification.assertion.AssertionDLModel',
'RelationExtractionDLModel':	'com.johnsnowlabs.legal.graph.relation_extraction.RelationExtractionDLModel',
'ZeroShotRelationExtractionModel':	'com.johnsnowlabs.legal.graph.relation_extraction.ZeroShotRelationExtractionModel',
'MedicalNerModel':	'com.johnsnowlabs.legal.token_classification.ner.LegalNerModel',
'MedicalBertForSequenceClassification':	'com.johnsnowlabs.legal.sequence_classification.LegalBertForSequenceClassification',
'MedicalBertForTokenClassifier':	'com.johnsnowlabs.legal.token_classification.ner.LegalBertForTokenClassification',
'ChunkMapperApproach':	'com.johnsnowlabs.legal.chunk_classification.resolution.ChunkMapperApproach',
'SentenceEntityResolverApproach':	'com.johnsnowlabs.legal.chunk_classification.resolution.SentenceEntityResolverApproach',
'AssertionDLApproach':	'com.johnsnowlabs.legal.chunk_classification.assertion.AssertionDLApproach',
'MedicalNerApproach':	'com.johnsnowlabs.legal.token_classification.ner.LegalNerApproach',
}

"""