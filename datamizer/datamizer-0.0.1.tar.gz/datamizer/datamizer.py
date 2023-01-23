import pandas as pd

from helpers import generate_fake_value


class Datamize:
    def __init__(self, csv_path: str, sep=","):
        self.df = pd.read_csv(csv_path, sep=sep)

    def fake(self, column: str, provider: str, unique=False, consistent=False):
        df_copy = self.df.copy()
        consistent_values = {}
        try:
            for value in self.df[column]:
                fake_value = consistent_values.get(value) if consistent else generate_fake_value(provider, unique)

                if consistent:
                    if not fake_value:
                        fake_value = generate_fake_value(provider, unique)
                        consistent_values[value] = fake_value

                df_copy.loc[df_copy[column] == value, column] = fake_value
        except KeyError:
            raise KeyError(f'Column named {column} not found')

        self.df = df_copy

    def write_csv(self, path: str, index=False):
        """ Writes a CSV file with the new data """
        self.df.to_csv(path, index=index)
