from IPython.display import display

import pandas as pd
import numpy as np
import plotly.express as px

from misc import percent

def infos(df, nb=5): 
    """Get shape and extract of a dataframe."""

    print('Shape: ', df.shape)
    display(df.sample(5))


def na_analyze(df, verbose=True):
    """Print out an analyze of NAN in the dataframe."""

    row_number = df.shape[0]
    col_number = df.shape[1]
    nan_number = df.isna().sum().sum()
    nan_columns = df.isna().sum()
    nan_columns_filtered = {key:value for (key, value) in nan_columns.items()}
    nan_columns_filtered = [{'col_name': key, 'na_nb': value, 'na_percent': value / row_number} for (key, value) in nan_columns_filtered.items()]

    if verbose: print('Total NaN number:', nan_number, '(' + percent(nan_number / (row_number * col_number)) + ')')
    if verbose: print('Columns number with nan:', len(nan_columns_filtered))

    if nan_number == 0: return

    nan_columns_filtered.sort(key=lambda x: x['na_nb'])

    for obj in nan_columns_filtered:
        if verbose: print('Column <' + str(obj['col_name']) + '> misses ' + str(obj['na_nb']) + ' (' + percent(obj['na_percent']) + ') values')


def column_analyze(df, column_name, nb=20):
    """Print out an analyse of values of a column."""

    uniques = df[column_name].unique()
    sumup = []

    for u in uniques:
        if pd.notna(u):
            sumup.append({
                "key": u,
                "count": (df[column_name] == u).sum()
            })
        else: 
            sumup.append({
                "key": "None",
                "count": (df[column_name].isna()).sum()
            })
    sumup.sort(key=lambda elt: elt['count'], reverse=True)

    print(f'{len(sumup)} unique values:')
    for i in range(min(nb, len(sumup))):
        print(percent(sumup[i]["count"] / len(df)) + f': "{sumup[i]["key"]}" ==> {sumup[i]["count"]}')
    

def histogram(df, column_name, title='', max_number=20):
    """Print out an horizontal histogram of a DataFrame column."""

    temp_df = df.copy()
    temp_df[column_name] = temp_df[column_name].astype(str)
    counts = temp_df.groupby(column_name).count()
    counts = counts.reset_index()[[column_name, counts.columns[0]]].sort_values(counts.columns[0], ascending=True)
    counts.rename(columns={counts.columns[1]:'Count'}, inplace=True)
    total_nb = counts['Count'].sum()
    counts['Percent'] = round((counts['Count'] / total_nb) * 1000) / 10
    counts['Percent'] = counts['Percent'].astype(str) + ' %'

    fig = px.bar(counts[-max_number:], x="Count", y=column_name, orientation='h', text="Percent", title=title)
    fig.show()