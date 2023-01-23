import unittest

import pandas as pd

from datamizer.datamizer import Datamize


class TestCsvDatamize(unittest.TestCase):
    def test_fake_username_consistent(self):
        datamize_csv = Datamize('users.csv', sep=";")
        datamize_csv.fake('Username', 'user_name', consistent=True)
        df = pd.read_csv('users.csv', sep=";")
        self.assertNotEqual(df, datamize_csv.df)
        # self.assertEqual(True, False)

    # def test_fake_first_name_consistent(self):
    #     datamize_csv = Datamize('users.csv')
    #     datamize_csv.fake('First name', 'first_name', consistent=True)
    #
    #     self.assertEqual(True, False)
    #
    # def test_fake_last_name_consistent(self):
    #     datamize_csv = Datamize('users.csv')
    #     datamize_csv.fake('Last name', 'last_name', consistent=True)
    #
    #     self.assertEqual(True, False)
    #
    # def test_fake_points_consistent(self):
    #     datamize_csv = Datamize('users.csv')
    #     datamize_csv.fake('Points', 'random_int', consistent=True)
    #
    #     self.assertEqual(True, False)
    #
    # def test_fake_money_consistent(self):
    #     datamize_csv = Datamize('users.csv')
    #     datamize_csv.fake('Money', 'pricetag', consistent=True)
    #
    #     self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
