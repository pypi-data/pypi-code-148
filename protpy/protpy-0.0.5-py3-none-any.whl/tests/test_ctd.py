# ###########################################################################
# ##################      protPy - CTD Module Tests      ####################
# ###########################################################################

# import pandas as pd
# import numpy as np
# import os
# import unittest
# import re
# from Bio import SeqIO
# unittest.TestLoader.sortTestMethodsUsing = None
# from json import JSONDecodeError

# import protpy as protpy

# class ProtPyCTDTests(unittest.TestCase):
#     """
#     Test suite for testing CTD (Composition, Transition, Distribution) 
#     module and functionality in protpy package. 

#     Test Cases
#     ----------
#     test_ctd:
#         testing correct protpy CTD functionality.
#     test_ctd_composition:
#         testing correct protpy composition functionality.
#     test_ctd_transition:
#         testing correct protpy transition functionality.
#     test_ctd_distribution:
#         testing correct protpy distribution functionality.
#     """
#     def setUp(self):
#         """ Import protein sequences from test fasta files using Biopython package. """
#         #using next() to get first item (protein seq) from SeqIO Generator
#         with open(os.path.join("tests", "test_fasta1.fasta")) as pro:
#             self.protein_seq1 = str(next(SeqIO.parse(pro,'fasta')).seq)

#         with open(os.path.join("tests", "test_fasta2.fasta")) as pro:
#             self.protein_seq2 = str(next(SeqIO.parse(pro,'fasta')).seq)
        
#         with open(os.path.join("tests", "test_fasta3.fasta")) as pro:
#             self.protein_seq3 = str(next(SeqIO.parse(pro,'fasta')).seq)

#         with open(os.path.join("tests", "test_fasta4.fasta")) as pro:
#             self.protein_seq4 = str(next(SeqIO.parse(pro,'fasta')).seq)

#     def test_ctd(self):
#         """ Testing CTD descriptor attributes and functionality. """   
#         properties = ["hydrophobicity", "normalized_VDWV", "polarity", "charge",
#             "sec_struct", "solvent_accessibility", "polarizability"]
 
#         for prop in properties:
# #1.)
#             ctd_seq1 = protpy.ctd_(self.protein_seq1, property=prop)
            
#             # print("ctd_seq1")
#             # print(ctd_seq1)
            
#         # hydrophobicity_CTD_C_1
#         #                 self.assertTrue(bool(re.match(r"MoreauBrotoAuto_[A-Z0-9]{10}_[0-9]", col)), 

#             self.assertFalse(ctd_seq1.empty, 'Descriptor dataframe should not be empty')
#             self.assertEqual(ctd_seq1.shape, (1, 147), 'Descriptor not of correct shape.') 
#             self.assertIsInstance(ctd_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
#             self.assertTrue(ctd_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  

# # 'hydrophobicity_CTD_D_2_001', 

#             print(ctd_seq1.columns)
#             print(prop)
#             for col in list(ctd_seq1.columns):
                
#                 # print("col", col)
#                 # print(bool(re.search(prop + "_CTD_[A-Z]{1}_[0-9]", col)))

#                 # print("prop", prop)
#                 self.assertTrue((bool(re.search(prop + "_CTD_[A-Z]{1}_[0-9]", col)) or bool(re.search(prop + "_CTD_[A-Z]{1}_[0-9]_[0-9]{3}", col))), 
#                     "Column name doesn't match expected regex pattern: {}, {}.".format(col, prop))  

# #                 # r'\b(?<=\w){0}\b(?!\w)' re.search('(.+)'+var_name+'(.+)'
# #                 # self.assertTrue(bool(re.match(rf"{re.escape(prop)}_CTD_[A-Z]{1}_[0-9]", col)), 
# #                 #     "Column name doesn't match expected regex pattern: {}.".format(col))  

# # #2.)
# #             ctd_composition_seq1 = protpy.ctd_composition(self.protein_seq1, property=prop)


# #             self.assertFalse(ctd_composition_seq1.empty, 'Descriptor dataframe should not be empty')
# #             self.assertEqual(ctd_composition_seq1.shape, (1, 3), 'Descriptor not of correct shape.') 
# #             self.assertIsInstance(ctd_composition_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
# #             self.assertTrue(ctd_composition_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  

# # #3.)
# #             ctd_transition_seq1 = protpy.ctd_transition(self.protein_seq1, property=prop)


# #             self.assertFalse(ctd_transition_seq1.empty, 'Descriptor dataframe should not be empty')
# #             self.assertEqual(ctd_transition_seq1.shape, (1, 3), 'Descriptor not of correct shape.') 
# #             self.assertIsInstance(ctd_transition_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
# #             self.assertTrue(ctd_transition_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  

# # #4.)
# #             ctd_distribution_seq1 = protpy.ctd_distribution(self.protein_seq1, property=prop)


#             # self.assertFalse(ctd_distribution_seq1.empty, 'Descriptor dataframe should not be empty')
#             # self.assertEqual(ctd_distribution_seq1.shape, (1, 3), 'Descriptor not of correct shape.') 
#             # self.assertIsInstance(ctd_distribution_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
#             # self.assertTrue(ctd_distribution_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  








# # #2.)        
# #         for prop in properties:
# #             ctd_seq1 = protpy.ctd_(self.protein_seq1, property=prop)

# #             self.assertFalse(ctd_seq1.empty, 'Descriptor dataframe should not be empty')
# #             self.assertEqual(ctd_seq1.shape, (1, 3), 'Descriptor not of correct shape.') 
# #             self.assertIsInstance(ctd_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
# #             self.assertTrue(ctd_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  


# #             ctd_composition_seq1 = protpy.ctd_composition(self.protein_seq1, property=prop)


# #             self.assertFalse(ctd_composition_seq1.empty, 'Descriptor dataframe should not be empty')
# #             self.assertEqual(ctd_composition_seq1.shape, (1, 3), 'Descriptor not of correct shape.') 
# #             self.assertIsInstance(ctd_composition_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
# #             self.assertTrue(ctd_composition_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  


# #             ctd_transition_seq1 = protpy.ctd_transition(self.protein_seq1, property=prop)


# #             self.assertFalse(ctd_transition_seq1.empty, 'Descriptor dataframe should not be empty')
# #             self.assertEqual(ctd_transition_seq1.shape, (1, 3), 'Descriptor not of correct shape.') 
# #             self.assertIsInstance(ctd_transition_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
# #             self.assertTrue(ctd_transition_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  


# #             ctd_distribution_seq1 = protpy.ctd_distribution(self.protein_seq1, property=prop)


# #             self.assertFalse(ctd_distribution_seq1.empty, 'Descriptor dataframe should not be empty')
# #             self.assertEqual(ctd_distribution_seq1.shape, (1, 3), 'Descriptor not of correct shape.') 
# #             self.assertIsInstance(ctd_distribution_seq1, pd.DataFrame, 'Descriptor not of type DataFrame.')
# #             self.assertTrue(ctd_distribution_seq1.any().isnull().sum()==0, 'Descriptor should not contain any null values.')  


# # def seq_order_coupling_number(sequence, lag=30,
# #     distance_matrix="schneider-wrede-physiochemical-distance-matrix.json"):

# # hydrophobicity = {"name": "hydrophobicity", "1": "RKEDQN", "2": "GASTPHY", "3": "CLVIMFW"}
# # # '1' -> Polar; '2' -> Neutral, '3' -> Hydrophobicity

# # normalized_VDWV = {"name": "normalized_VDWV", "1": "GASTPD", "2": "NVEQIL", "3": "MHKFRYW"}
# # # '1' -> (0-2.78); '2' -> (2.95-4.0), '3' -> (4.03-8.08)

# # polarity = {"name": "polarity", "1": "LIFWCMVY", "2": "CPNVEQIL", "3": "KMHFRYW"}
# # # '1' -> (4.9-6.2); '2' -> (8.0-9.2), '3' -> (10.4-13.0)

# # charge = {"name": "charge", "1": "KR", "2": "ANCQGHILMFPSTWYV", "3": "DE"}
# # # '1' -> Positive; '2' -> Neutral, '3' -> Negative

# # sec_struct = {"name": "secondary_struct", "1": "EALMQKRH", "2": "VIYCWFT", "3": "GNPSD"}
# # # '1' -> Helix; '2' -> Strand, '3' -> coil

# # solvent_accessibility = {"name": "solvent_accessibility", "1": "ALFCGIVW", "2": "RKQEND", "3": "MPSTHY"}
# # # '1' -> Buried; '2' -> Exposed, '3' -> Intermediate

# # polarizability = {"name": "polarizability", "1": "GASDT", "2": "CPNVEQIL", "3": "KMHFRYW"}
# # # '1' -> (0-0.108); '2' -> (0.128-0.186), '3' -> (0.219-0.409)



# # #1.)
# #         self.assertFalse(ctd.empty, 'Descriptor dataframe should not be empty')
# #         self.assertEqual(ctd.shape, (self.num_seqs[dataset], 147), 'Descriptor not of correct ({},147)'.format(self.num_seqs[dataset]))
# #         self.assertIsInstance(ctd, pd.DataFrame)
# #         self.assertTrue(ctd.any().isnull().sum()==0, 'Descriptor should not contain any null values.')

# # #2.)
# #         #get descriptor values
# #         comp = desc.get_composition()
# # #2.)
# #         self.assertFalse(comp.empty, 'Descriptor dataframe should not be empty')
# #         self.assertEqual(comp.shape, (self.num_seqs[dataset], 3), 'Descriptor not of correct ({},3)'.format(self.num_seqs[dataset]))
# #         self.assertIsInstance(comp, pd.DataFrame)
# #         self.assertTrue(comp.any().isnull().sum()==0, 'Descriptor should not contain any null values.')

# #         #get descriptor values
# #         trans = desc.get_transition()
# # #3.)
# #         self.assertFalse(trans.empty, 'Descriptor dataframe should not be empty')
# #         self.assertEqual(trans.shape, (self.num_seqs[dataset], 3), 'Descriptor not of correct ({},3)'.format(self.num_seqs[dataset]))
# #         self.assertIsInstance(trans, pd.DataFrame)
# #         self.assertTrue(trans.any().isnull().sum()==0, 'Descriptor should not contain any null values.')

# #         #get descriptor values
# #         distr = desc.get_distribution()
# # #4.)
# #         self.assertFalse(distr.empty, 'Descriptor dataframe should not be empty')
# #         self.assertEqual(distr.shape, (self.num_seqs[dataset],15), 'Descriptor not of correct ({},15)'.format(self.num_seqs[dataset]))
# #         self.assertIsInstance(distr, pd.DataFrame)
# #         self.assertTrue(distr.any().isnull().sum()==0, 'Descriptor should not contain any null values.')

