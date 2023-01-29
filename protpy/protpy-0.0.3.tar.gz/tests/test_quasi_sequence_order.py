###########################################################################
#############      protPy - Quasi Sequence Module Tests      ##############
###########################################################################

import pandas as pd
import numpy as np
import os
import unittest
import re
from decimal import *
from Bio import SeqIO
unittest.TestLoader.sortTestMethodsUsing = None
from json import JSONDecodeError

import protpy as protpy

class ProtPyQuasiSequenceOrderTests(unittest.TestCase):
    """
    Test suite for testing CTD (Composition, Transition, Distribution) 
    module and functionality in protpy package. 

    Test Cases
    ----------
    test_sequence_order_coupling_number:
        testing correct protpy sequence order coupling number functionality.
    test_quasi_sequence_order:
        testing correct protpy quasi sequence order functionality.
    """
    def setUp(self):
        """ Import protein sequences from test fasta files using Biopython package. """
        #using next() to get first item (protein seq) from SeqIO Generator
        with open(os.path.join("tests", "test_fasta1.fasta")) as pro:
            self.protein_seq1 = str(next(SeqIO.parse(pro,'fasta')).seq)

        with open(os.path.join("tests", "test_fasta2.fasta")) as pro:
            self.protein_seq2 = str(next(SeqIO.parse(pro,'fasta')).seq)
        
        with open(os.path.join("tests", "test_fasta3.fasta")) as pro:
            self.protein_seq3 = str(next(SeqIO.parse(pro,'fasta')).seq)

        with open(os.path.join("tests", "test_fasta4.fasta")) as pro:
            self.protein_seq4 = str(next(SeqIO.parse(pro,'fasta')).seq)

    def test_sequence_order_coupling_number(self):
        """ Testing sequence order coupling number descriptor attributes and functionality. """
        socn_lag = list(range(5, 35, 5))
        distance_matrix_schneider_wrede = "schneider-wrede-physiochemical-distance-matrix"
        distance_matrix_grantham = "grantham-physiochemical-distance-matrix"
#1.)
        for lag in socn_lag:
            socn_seq1 = protpy.seq_order_coupling_number(self.protein_seq1, lag=lag, 
                distance_matrix=distance_matrix_schneider_wrede)

            self.assertFalse(socn_seq1.empty, 'Descriptor dataframe should not be empty')
            self.assertEqual(socn_seq1.shape, (1, lag), 'Descriptor not of correct shape.') 
            self.assertIsInstance(socn_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
            for col in list(socn_seq1.columns):
                #check all columns follow pattern of SOCNX or SOCNXY where x & y integers between 0 and 9
                self.assertTrue((bool(re.match(r'SOCN[0-9]{1}$', col)) or bool(re.match(r'SOCN[0-9]{2}$', col))), 
                    "Column name doesn't match expected regex pattern: {}.".format(col))     
            self.assertTrue(socn_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
            self.assertTrue(all(col == np.float64 for col in list(socn_seq1.dtypes)), "")
#1.2)
            socn_seq1 = protpy.seq_order_coupling_number(self.protein_seq1, lag=lag, 
                distance_matrix=distance_matrix_grantham)

            self.assertFalse(socn_seq1.empty, 'Descriptor dataframe should not be empty')
            self.assertEqual(socn_seq1.shape, (1, lag), 'Descriptor not of correct shape.') 
            self.assertIsInstance(socn_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
            for col in list(socn_seq1.columns):
                #check all columns follow pattern of SOCNX or SOCNXY where x & y integers between 0 and 9
                self.assertTrue((bool(re.match(r'SOCN[0-9]{1}$', col)) or bool(re.match(r'SOCN[0-9]{2}$', col))), 
                    "Column name doesn't match expected regex pattern: {}.".format(col))     
            self.assertTrue(socn_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
            self.assertTrue(all(col == np.float64 for col in list(socn_seq1.dtypes)), "")

#2.)
            socn_seq2 = protpy.seq_order_coupling_number(self.protein_seq2, lag=lag, 
                distance_matrix=distance_matrix_schneider_wrede)

            self.assertFalse(socn_seq2.empty, 'Descriptor dataframe should not be empty')
            self.assertEqual(socn_seq2.shape, (1, lag), 'Descriptor not of correct shape.') 
            self.assertIsInstance(socn_seq2, pd.DataFrame, 'Descriptor not of type DataFrame.')
            for col in list(socn_seq2.columns):
                #check all columns follow pattern of SOCNX or SOCNXY where x & y integers between 0 and 9
                self.assertTrue((bool(re.match(r'SOCN[0-9]{1}$', col)) or bool(re.match(r'SOCN[0-9]{2}$', col))), 
                    "Column name doesn't match expected regex pattern: {}.".format(col))     
            self.assertTrue(socn_seq2.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
            self.assertTrue(all(col == np.float64 for col in list(socn_seq2.dtypes)), "")
#3.)

#4.)

#5.)
    def test_quasi_sequence_order(self):
        """ Testing quasi sequence order descriptor attributes and functionality. """
#1.)

#2.)

#3.)

#4.)

#5.)
        pass


# def seq_order_coupling_number(sequence, lag=30,
#     distance_matrix="schneider-wrede-physiochemical-distance-matrix.json"):

# def quasi_sequence_order(sequence, max_lag=30, weight=0.1,
#     distance_matrix="schneider-wrede-physicochemical-distance-matrix.json"):