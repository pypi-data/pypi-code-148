import pandas as pd

from datamizer.helpers import generate_fake_value


class Datamizer:
    """ Datamizer Object used for anonymization of a CSV file

    Args:
        csv_path(str): Path to the CSV file that will be anonymized
        sep(str): Delimiter used in the CSV file, default is ","

    Attributes:
        df(pd.DataFrame): Were we save the dataframe used for data anonymization
    """
    def __init__(self, csv_path: str, sep=","):
        self.df: pd.DataFrame = pd.read_csv(csv_path, sep=sep)

    def fake(self, column: str, provider: str, consistent=False, unique=False):
        """ Create fake data for the column indicated

        Args:
            column(str): Name of the column to be anonymized
            provider(str): Provider from Faker package used to generate the fake data
            consistent(bool): Indicates if the changes should be consistent when the data repeats itself through the
            column, default is False
            unique(bool): Indicates whether values should be repeated or not, default is False
        """
        consistent_values = {}
        try:
            for value in self.df[column]:
                fake_value = consistent_values.get(value) if consistent else generate_fake_value(provider, unique)

                if consistent:
                    if not fake_value:
                        fake_value = generate_fake_value(provider, unique)
                        consistent_values[value] = fake_value

                self.df.loc[self.df[column] == value, column] = fake_value
        except KeyError:
            raise KeyError(f'Column named {column} not found')

    def write_csv(self, path: str, index=False):
        """ Writes a CSV file with the new data

        Args:
            path(str): Path where the CSV file will be created
            index(bool): Indicates if the index will be added to the CSV file, default is False
        """
        self.df.to_csv(path, index=index)
