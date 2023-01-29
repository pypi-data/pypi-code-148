###########################################################################
###############      protPy - Composition Module Tests      ###############
###########################################################################

import pandas as pd
import numpy as np
import os
import unittest
import re
import random
from Bio import SeqIO
unittest.TestLoader.sortTestMethodsUsing = None
from json import JSONDecodeError

import protpy as protpy

class ProtPyCompositionTests(unittest.TestCase):
    """
    Test suite for testing composition module and functionality 
    in protpy package. 

    Test Cases
    ----------
    test_amino_acid_composition:
        testing correct protpy amino acid composition functionality.
    test_dipeptide_composition:
        testing correct protpy dipeptide amino acid composition functionality.
    test_tripeptide_composition:
        testing correct protpy tripeptide amino acid composition functionality.
    test_pseudo_amino_acid_composition:
        testing correct protpy pseudo amino acid composition functionality.
    test_amphiphilic_pseudo_amino_acid_composition:
        testing correct protpy amphophilic amino acid composition functionality.
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

        #list of canonical amino acids
        self.amino_acids = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", 
            "Q", "R", "S", "T", "V", "W", "Y"]

    def test_amino_acid_composition(self):
        """ Testing Amino Acid Composition protein descriptor attributes and methods. """
#1.)
        aa_composition_seq1 = protpy.aa_composition(self.protein_seq1)
        aa_composition_seq1_expected_values = pd.DataFrame(columns=["A", "C", "D", "E", "F", "G", "H", 
            "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"])
        aa_composition_seq1_expected_values.loc[0] = [6.693, 3.108, 5.817, 3.347, 6.614, 6.295, 1.195, 
            6.215, 4.781, 7.888, 1.594, 6.454, 4.542, 4.382, 3.108, 7.649, 7.888, 7.251, 0.876, 4.303]

        self.assertIsInstance(aa_composition_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(aa_composition_seq1.shape, (1, 20), 'Descriptor not of correct shape.') 
        self.assertEqual(self.amino_acids, list(aa_composition_seq1.columns), 'Incorrect column values found.')
        self.assertTrue(aa_composition_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(aa_composition_seq1.equals(aa_composition_seq1_expected_values))
#2.)
        aa_composition_seq2 = protpy.aa_composition(self.protein_seq2)
        aa_composition_seq2_expected_values = pd.DataFrame(columns=["A", "C", "D", "E", "F", "G", "H", 
            "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"])
        aa_composition_seq2_expected_values.loc[0] = [8.057, 0.0, 5.213, 3.318, 3.081, 10.664, 1.185, 
            2.607, 6.872, 6.161, 1.659, 5.924, 7.346, 8.057, 7.346, 8.294, 7.82, 2.607, 1.185, 2.607]

        self.assertIsInstance(aa_composition_seq2, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(aa_composition_seq2.shape, (1, 20), 'Descriptor not of correct shape.') 
        self.assertEqual(self.amino_acids, list(aa_composition_seq2.columns), 'Incorrect column values found.')
        self.assertTrue(aa_composition_seq2.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(aa_composition_seq2.equals(aa_composition_seq2_expected_values))
#3.)
        aa_composition_seq3 = protpy.aa_composition(self.protein_seq3)
        aa_composition_seq3_expected_values = pd.DataFrame(columns=["A", "C", "D", "E", "F", "G", "H", 
            "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"])
        aa_composition_seq3_expected_values.loc[0] = [5.263, 3.947, 1.316, 3.947, 5.263, 2.632, 0.0, 
            3.947, 2.632, 18.421, 1.316, 6.579, 2.632, 0.0, 2.632, 9.211, 6.579, 18.421, 0.0, 5.263]

        self.assertIsInstance(aa_composition_seq3, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(aa_composition_seq3.shape, (1, 20), 'Descriptor not of correct shape.') 
        self.assertEqual(self.amino_acids, list(aa_composition_seq3.columns), 'Incorrect column values found.')
        self.assertTrue(aa_composition_seq3.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(aa_composition_seq3.equals(aa_composition_seq3_expected_values))
#4.)
        aa_composition_seq4 = protpy.aa_composition(self.protein_seq4)
        aa_composition_seq4_expected_values = pd.DataFrame(columns=["A", "C", "D", "E", "F", "G", "H", 
            "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"])
        aa_composition_seq4_expected_values.loc[0] = [8.831, 0.0, 5.728, 2.864, 3.103, 10.263, 0.955, 
            3.341, 7.399, 6.444, 1.671, 5.251, 6.683, 8.353, 6.921, 8.831, 7.637, 1.909, 1.193, 2.625]

        self.assertIsInstance(aa_composition_seq4, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(aa_composition_seq4.shape, (1, 20), 'Descriptor not of correct shape.') 
        self.assertEqual(self.amino_acids, list(aa_composition_seq4.columns), 'Incorrect column values found.')
        self.assertTrue(aa_composition_seq4.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(aa_composition_seq4.equals(aa_composition_seq4_expected_values))
#5.)
        invalid_seq5 = "ABCDEF"
        with (self.assertRaises(ValueError)):
            aa_composition_seq5 = protpy.aa_composition(invalid_seq5)
#6.)
        invalid_seq6 = "OOOOO"
        with (self.assertRaises(ValueError)):
            aa_composition_seq5 = protpy.aa_composition(invalid_seq6)
#7.)
        invalid_seq7 = 12345
        with (self.assertRaises(TypeError)):
            aa_composition_seq5 = protpy.aa_composition(invalid_seq7)

    def test_dipeptide_composition(self):
        """ Testing Dipeptide Composition protein descriptor attributes and functionality. """
#1.)
        dipeptide_comp_seq1 = protpy.dipeptide_composition(self.protein_seq1)

        self.assertIsInstance(dipeptide_comp_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(dipeptide_comp_seq1.shape, (1, 400), 'Descriptor not of correct shape.') 
        for col in list(dipeptide_comp_seq1.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{2}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(dipeptide_comp_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.float64 for col in list(dipeptide_comp_seq1.dtypes)), "")
#2.)
        dipeptide_comp_seq2 = protpy.dipeptide_composition(self.protein_seq2)

        self.assertIsInstance(dipeptide_comp_seq2, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(dipeptide_comp_seq2.shape, (1, 400), 'Descriptor not of correct shape.') 
        for col in list(dipeptide_comp_seq2.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{2}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(dipeptide_comp_seq2.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.float64 for col in list(dipeptide_comp_seq2.dtypes)), "")
#3.)
        dipeptide_comp_seq3 = protpy.dipeptide_composition(self.protein_seq3)

        self.assertIsInstance(dipeptide_comp_seq3, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(dipeptide_comp_seq3.shape, (1, 400), 'Descriptor not of correct shape.') 
        for col in list(dipeptide_comp_seq3.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{2}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(dipeptide_comp_seq3.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.float64 for col in list(dipeptide_comp_seq3.dtypes)), "")
#4.)
        dipeptide_comp_seq4 = protpy.dipeptide_composition(self.protein_seq4)

        self.assertIsInstance(dipeptide_comp_seq4, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(dipeptide_comp_seq4.shape, (1, 400), 'Descriptor not of correct shape.') 
        for col in list(dipeptide_comp_seq4.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{2}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(dipeptide_comp_seq4.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.float64 for col in list(dipeptide_comp_seq4.dtypes)), "")
#5.)
        invalid_seq5 = "ABCDEF"
        with (self.assertRaises(ValueError)):
            dipeptide_composition_seq5 = protpy.dipeptide_composition(invalid_seq5)
#6.)
        invalid_seq6 = "OOOOO"
        with (self.assertRaises(ValueError)):
            dipeptide_composition_seq5 = protpy.dipeptide_composition(invalid_seq6)
#7.)
        invalid_seq7 = 12345
        with (self.assertRaises(TypeError)):
            dipeptide_composition_seq5 = protpy.dipeptide_composition(invalid_seq7)

    @unittest.skip("Descriptor can take quite a bit of time to calculate therefore skipping.")
    def test_tripeptide_composition(self):
        """ Testing Tripeptide Composition protein descriptor attributes and functionality. """
#1.)
        tripeptide_comp_seq1 = protpy.tripeptide_composition(self.protein_seq1)

        print("tripeptide_comp_seq1")
        print(tripeptide_comp_seq1.dtypes)
        self.assertIsInstance(tripeptide_comp_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(tripeptide_comp_seq1.shape, (1, 8000), 'Descriptor not of correct shape.') 
        for col in list(tripeptide_comp_seq1.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{3}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(tripeptide_comp_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.int64 for col in list(tripeptide_comp_seq1.dtypes)), "")
#2.)
        tripeptide_comp_seq2 = protpy.tripeptide_composition(self.protein_seq2)

        self.assertIsInstance(tripeptide_comp_seq2, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(tripeptide_comp_seq2.shape, (1, 8000), 'Descriptor not of correct shape.') 
        for col in list(tripeptide_comp_seq2.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{3}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(tripeptide_comp_seq2.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.int64 for col in list(tripeptide_comp_seq2.dtypes)), "")
#3.)
        tripeptide_comp_seq3 = protpy.tripeptide_composition(self.protein_seq3)

        self.assertIsInstance(tripeptide_comp_seq3, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(tripeptide_comp_seq3.shape, (1, 8000), 'Descriptor not of correct shape.') 
        for col in list(tripeptide_comp_seq3.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{3}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(tripeptide_comp_seq3.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.int64 for col in list(tripeptide_comp_seq3.dtypes)), "")
#4.)
        tripeptide_comp_seq4 = protpy.tripeptide_composition(self.protein_seq4)

        self.assertIsInstance(tripeptide_comp_seq4, pd.DataFrame, 'Descriptor not of type DataFrame.')
        self.assertEqual(tripeptide_comp_seq4.shape, (1, 8000), 'Descriptor not of correct shape.') 
        for col in list(tripeptide_comp_seq4.columns):
            #check all columns follow pattern of XY where x & y are amino acids 
            self.assertTrue(bool(re.match(r'^[A-Z]{3}$', col)), "")      
            self.assertIn(col[0], self.amino_acids, "")
            self.assertIn(col[1], self.amino_acids, "")
        self.assertTrue(tripeptide_comp_seq4.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
        self.assertTrue(all(col == np.int64 for col in list(tripeptide_comp_seq4.dtypes)), "")
#5.)
        invalid_seq5 = "ABCDEF"
        with (self.assertRaises(ValueError)):
            tripeptide_composition_seq5 = protpy.tripeptide_composition(invalid_seq5)
#6.)
        invalid_seq6 = "OOOOO"
        with (self.assertRaises(ValueError)):
            tripeptide_composition_seq5 = protpy.tripeptide_composition(invalid_seq6)
#7.)
        invalid_seq7 = 12345
        with (self.assertRaises(TypeError)):
            tripeptide_composition_seq5 = protpy.tripeptide_composition(invalid_seq7)

    @unittest.skip("Descriptor can take quite a bit of time to calculate therefore skipping.")
    def test_pseudo_amino_acid_composition(self):
        """ Testing pseudo aa composition protein descriptor attributes and functionality. """
        lambda_range = range(30, 60, 10) 
        weight_range = []
        for i in range(10): weight_range.append(random.random())
#1.)
        for lam in lambda_range:
            for weight in weight_range:
                pseudo_amino_acid_composition_seq1 = protpy.pseudo_amino_acid_composition(self.protein_seq1,
                    weight=weight, lamda=lam)
            
                self.assertIsInstance(pseudo_amino_acid_composition_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
                self.assertEqual(pseudo_amino_acid_composition_seq1.shape, (1, 50), 'Descriptor not of correct shape.') 
                # for col in list(pseudo_amino_acid_composition_seq1.columns):
                #     #check all columns follow pattern of XY where x & y are amino acids 
                #     self.assertTrue(bool(re.match(r'^[A-Z]{3}$', col)), "")      
                self.assertTrue(pseudo_amino_acid_composition_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')
                self.assertTrue(all(col == np.float64 for col in list(pseudo_amino_acid_composition_seq1.dtypes)), "")

# def pseudo_amino_acid_composition(sequence, lamda=30, weight=0.05, properties=["ARGP820101", "KUHL950101"]):

    def amp_pseudo_amino_acid_composition(self):
        """ """
        #random list of floats for weight from 0 - 1
        #random lambda values from 30 - 100
        pass
# def amphiphilic_pseudo_aac(sequence, lamda=30, weight=0.5, properties=["ARGP820101", "KUHL950101"]):

