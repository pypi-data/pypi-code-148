import pandas as pd
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
import gspread


def load_standard_columns(gfile: str,wks_name: str):
    df = g2d.download(gfile=gfile, col_names=True, row_names=True,wks_name=wks_name)
    df=df.reset_index().rename(columns={'index':'source'})
    return df

def map_to_standard_columns(std_cols_df,source,data):
    mapping = std_cols_df[std_cols_df['source']==source].T.reset_index()
    mapping.columns = ['std_cols','scraper_cols']
    mapping = mapping.set_index('scraper_cols').to_dict()['std_cols']
    mapped_cols = [mapping[col] if col in mapping else col for col in data.columns]
    
    data.columns=mapped_cols
    std_cols = list(std_cols_df.columns[1:])
    other_cols = list(set(data.columns)-set(std_cols))
    new_cols = std_cols+other_cols
    data=data[new_cols]
    
    return data
