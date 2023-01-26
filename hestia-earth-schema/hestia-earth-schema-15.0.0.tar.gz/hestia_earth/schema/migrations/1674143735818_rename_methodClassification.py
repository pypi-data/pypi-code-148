import pandas as pd


def migrate(df: pd.DataFrame):
    # make sure to return the DataFrame so it can be uploaded
    return df.replace({
      'consistent external source': 'consistent external sources',
      'inconsistent external source': 'inconsistent external sources'
    })
