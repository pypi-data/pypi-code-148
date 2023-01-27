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

    missing_cols = []
    for col in new_cols:
        if col not in data.columns:
            data[col] = None
            missing_cols.append(col)

    data=data[new_cols]
    if len(missing_cols)>0:
        print('these columns are not present:',missing_cols)
    
    return data

def load_golden_records(wks_name:str):
    gfile = '1lhaPZdHH6K4ZdKiY8bvwCcRobhubKoFv4P7KhExUTkI'
    print('#####################')
    print('wks_name: ', wks_name)
    print('#####################')    
    df = g2d.download(gfile=gfile, col_names=True, row_names=True,wks_name=wks_name)
    df=df.reset_index().rename(columns={'index':'brand_name_1'})
    
    def convert_to_binary(x):
        if pd.isnull(x):
            return None
        if type(x)!=str:
            raise ValueError('found invalid value in golden recods:',x)
        
        if x.lower() not in ['true','false','yes','no']:
            raise ValueError('found invalid value in golden recods:',x)
            
        if x.lower() in ['true','yes']:
            return True
        elif x.lower() in ['false','no']:
            return False
        else:
            raise ValueError('found invalid value in golden recods:',x)
    
    df['is_same_brand_name']=df['is_same_brand_name'].apply(convert_to_binary)
    return df

def apply_mapping_mfn_names(data,golden_records):   
    data['brand_name'] = data['brand_name_orig'].copy(deep=True)
    aux=data.reset_index()[['index','brand_name_orig']]

    #Applying only brand mappings with "is_same_brand_name = True"
    aux_golden = golden_records[golden_records['is_same_brand_name']==True].copy(deep=True)
    aux_golden = aux_golden[['brand_name_1','brand_name_2']]
    merge = pd.merge(aux,aux_golden,left_on='brand_name_orig',right_on='brand_name_1')
    data.loc[merge['index'],'brand_name'] = merge['brand_name_2'].values   
    
    return data
