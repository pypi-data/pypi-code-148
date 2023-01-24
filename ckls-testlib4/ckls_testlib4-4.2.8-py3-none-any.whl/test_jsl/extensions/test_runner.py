import os, sys, unittest

sys.path.append(os.getcwd())
from test_jsl.extensions.finance.deid.test_doc_hash_coder import FinanceDocHashCoderTestCase
from test_jsl.extensions.finance.sequence_generation.test_ner_qa import FinanceNerQACase
from test_jsl.extensions.finance.chunk_classification.test_assert import FinanceAssertCase
from test_jsl.extensions.finance.chunk_classification.test_assert_approach import FinanceAssertApproachCase
from test_jsl.extensions.finance.chunk_classification.test_chunk_mapper import FinanceChunkMapperCase
from test_jsl.extensions.finance.chunk_classification.test_chunk_mapper_approach import FinanceChunkMapperApproachCase
from test_jsl.extensions.finance.chunk_classification.test_sentence_resolver import FinanceSentenceResolveCase
from test_jsl.extensions.finance.chunk_classification.test_sentence_resolver_approach import \
    FinanceSentenceResolveApproachCase
from test_jsl.extensions.finance.graph.test_relation_dl import FinanceRelationCase
from test_jsl.extensions.finance.graph.test_relation_zero_shot import FinanceZeroShotCase
from test_jsl.extensions.finance.sequence_classification.finance_seq_bert import FinanceSeqBertCase
from test_jsl.extensions.finance.sequence_classification.test_finance_classifier_dl import FinanceClassifierDLCase
from test_jsl.extensions.finance.sequence_classification.test_finance_classifier_dl_approach import \
    FinanceClassifierDLApproachCase
from test_jsl.extensions.finance.token_classification.finance_token_bert import FinanceTokenBertCase
from test_jsl.extensions.finance.token_classification.test_finance_ner_dl import FinanceNerDlCase
from test_jsl.extensions.finance.token_classification.test_finance_ner_dl_approach import FinanceNerCase
from test_jsl.extensions.finance.token_classification.finance_zero_shot_ner import FinZeroShotNerCase
from test_jsl.extensions.legal.chunk_classification.test_assert import LegalAssertCase
from test_jsl.extensions.legal.chunk_classification.test_assert_approach import LegalAssertApproachCase
from test_jsl.extensions.legal.chunk_classification.test_chunk_mapper import LegalChunkMapperCase
from test_jsl.extensions.legal.chunk_classification.test_chunk_mapper_approach import LegalChunkMapperApproachCase
from test_jsl.extensions.legal.chunk_classification.test_sentence_resolver import LegalSentenceResolveCase
from test_jsl.extensions.legal.chunk_classification.test_sentence_resolver_approach import \
    LegalSentenceResolveApproachCase
from test_jsl.extensions.legal.graph.test_relation_dl import LegalRelationCase
from test_jsl.extensions.legal.graph.test_relation_zero_shot import LegalZeroShotCase
from test_jsl.extensions.legal.sequence_classification.legal_seq_bert import LegalTokenBertCase
from test_jsl.extensions.legal.sequence_classification.test_legal_classifier_dl import LegalClassifierDLCase
from test_jsl.extensions.legal.sequence_classification.test_legal_classifier_dl_approach import \
    LegalClassifierDLApproachCase
from test_jsl.extensions.legal.token_classification.legal_token_bert import LegalTokenBertCase
from test_jsl.extensions.legal.token_classification.test_legal_ner_dl import LegalNerDlCase
from test_jsl.extensions.legal.token_classification.test_legal_ner_dl_approach import LegalNerApproachCase
from test_jsl.extensions.legal.token_classification.legal_zero_shot_ner import LegalTokenBertCase
from test_jsl.extensions.legal.deid.test_doc_hash_coder import LegalDocHashCoderTestCase
from test_jsl.extensions.legal.sequence_generation.test_ner_qa import LegalNerQACase


def suite():
    # os.cwd() should be root of spark_internal git repo.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FinanceAssertCase))
    suite.addTest(unittest.makeSuite(FinanceAssertApproachCase))
    suite.addTest(unittest.makeSuite(FinanceChunkMapperCase))
    suite.addTest(unittest.makeSuite(FinanceChunkMapperApproachCase))
    suite.addTest(unittest.makeSuite(FinanceSentenceResolveCase))
    suite.addTest(unittest.makeSuite(FinanceSentenceResolveApproachCase))
    suite.addTest(unittest.makeSuite(FinanceRelationCase))
    suite.addTest(unittest.makeSuite(FinanceZeroShotCase))
    suite.addTest(unittest.makeSuite(FinanceSeqBertCase))
    suite.addTest(unittest.makeSuite(FinanceClassifierDLCase))
    suite.addTest(unittest.makeSuite(FinanceClassifierDLApproachCase))
    suite.addTest(unittest.makeSuite(FinanceTokenBertCase))
    suite.addTest(unittest.makeSuite(FinanceNerDlCase))
    suite.addTest(unittest.makeSuite(FinanceNerCase))
    suite.addTest(unittest.makeSuite(FinZeroShotNerCase))

    suite.addTest(unittest.makeSuite(FinanceNerQACase))
    suite.addTest(unittest.makeSuite(FinanceDocHashCoderTestCase))

    suite.addTest(unittest.makeSuite(LegalDocHashCoderTestCase))
    suite.addTest(unittest.makeSuite(LegalNerQACase))
    suite.addTest(unittest.makeSuite(LegalAssertCase))
    suite.addTest(unittest.makeSuite(LegalAssertApproachCase))
    suite.addTest(unittest.makeSuite(LegalChunkMapperCase))
    suite.addTest(unittest.makeSuite(LegalChunkMapperApproachCase))
    suite.addTest(unittest.makeSuite(LegalSentenceResolveCase))
    suite.addTest(unittest.makeSuite(LegalSentenceResolveApproachCase))
    suite.addTest(unittest.makeSuite(LegalRelationCase))
    suite.addTest(unittest.makeSuite(LegalZeroShotCase))
    suite.addTest(unittest.makeSuite(LegalTokenBertCase))
    suite.addTest(unittest.makeSuite(LegalClassifierDLCase))
    suite.addTest(unittest.makeSuite(LegalClassifierDLApproachCase))
    suite.addTest(unittest.makeSuite(LegalTokenBertCase))
    suite.addTest(unittest.makeSuite(LegalNerDlCase))
    suite.addTest(unittest.makeSuite(LegalNerApproachCase))
    suite.addTest(unittest.makeSuite(LegalTokenBertCase))

    return suite


if __name__ == '__main__':
    # Make sure working dir is root of the spark-internal repo!
    # NOT the root of Python project!
    runner = unittest.TextTestRunner()
    runner.run(suite())
