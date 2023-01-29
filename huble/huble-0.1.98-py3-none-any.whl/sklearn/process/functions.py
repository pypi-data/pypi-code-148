import re
from re import sub
import sklearn
from sklearn.impute import SimpleImputer
import pandas as pd
from scipy import stats
import numpy as np
from AutoClean import AutoClean

def remove_nan_values(**params):
    data = params['data']
    data = data.dropna(**params["parameters"])
    return data


def replace_nan_values(**params):
    imputer = SimpleImputer(**params["parameters"])
    data = params['data']
    data[(params['column'])] = imputer.fit_transform(data[(params['column'])].values.reshape(-1,1))[:,0]
    return data


def drop_rows_columns(**params):
    data = params['data']
    data = data.drop(**params["parameters"])
    return data


def remove_outliers(**params):
    data = params['data']
    for column in params["columns"]:
        data = data[
            (np.abs(stats.zscore(data[(params['column'])])) < 3)
        ]
    return data


def drop_duplicates(**params):
    data = params['data']
    data = data.drop_duplicates(**params["parameters"])
    return data


def change_data_type(**params):
    data = params['data']
    data[(params['column'])] = data[(params['column'])].astype(**params["parameters"])
    return data


def round_data(**params):
    data = params['data']
    data = data.round(**params["parameters"])
    return data


def filter_dataframe(**params):
    data = params['data']
    data = data.filter(**params["parameters"])
    return data


def truncate_dataframe(**params):
    data = params['data']
    data = data.truncate(**params["parameters"])
    return data


def sort_values(**params):
    data = params['data']
    data = data.sort_values(**params["parameters"])
    return data


def transpose(**params):
    data = params['data']
    data = data.transpose()
    return data


def min_max_scale(**params):
    data = params['data']
    scaler = sklearn.preprocessing.MinMaxScaler(**params["parameters"])
    data[(params['column'])] = scaler.fit_transform(data[(params['column'])].values.reshape(-1,1))[:,0]
    return data


def max_abs_scale(**params):
    data = params['data']
    scaler = sklearn.preprocessing.MaxAbsScaler(**params["parameters"])
    data[(params['column'])] = scaler.fit_transform(data[(params['column'])].values.reshape(-1,1))[:,0]
    return data


def robust_scale(**params):
    data = params['data']
    scaler = sklearn.preprocessing.RobustScaler(**params["parameters"])
    data[(params['column'])] = scaler.fit_transform(data[(params['column'])].values.reshape(-1,1))[:,0]
    return data


def standard_scale(**params):
    data = params['data']
    scaler = sklearn.preprocessing.StandardScaler(**params["parameters"])
    data[(params['column'])] = scaler.fit_transform(data[(params['column'])].values.reshape(-1,1))[:,0]
    return data


def normalize(**params):
    data = params['data']
    for column in params['columns']:
        params["X"]=column
        data = sklearn.preprocessing.normalize(**params["parameters"])
    return data


def ordinal_encode(**params):
    data = params['data']
    data_columns = params["columns"]
    enc = sklearn.preprocessing.OrdinalEncoder(**params["parameters"])
    data[data_columns] = enc.fit_transform(data[data_columns])
    return data


def one_hot_encode(**params):
    data = params['data']
    data_columns = params["columns"]
    le = sklearn.preprocessing.LabelEncoder()
    data[data_columns] = data[data_columns].apply(lambda col: le.fit_transform(col))
    enc = sklearn.preprocessing.OneHotEncoder(**params["parameters"])
    array_hot_encoded = enc.fit_transform(data[data_columns])
    data_hot_encoded = pd.DataFrame(array_hot_encoded, index=data.index)
    data_other_cols = data.drop(columns=data_columns)
    data_out = pd.concat([data_hot_encoded, data_other_cols], axis=1)
    print(data_out)
    return data_out
   

def remove_mismatch_data(**params):
    data = params['data']
    exceptions = params['parameters']['exceptions']
    for col in data : 
        if col in exceptions : continue
        data.reset_index(drop=True, inplace=True)
        s = [False]*len(data[col])
        for i,cell in enumerate(data[col]) : 
            try : n = int(cell)
            except : s[i] = True
        t = s.count(True)
        f = s.count(False)
        st = False
        if(t>f) : st = True
        remove = [i for i in range(len(data[col])) if s[i]!=st]
        data.drop(remove,axis=0,inplace=True)
    return data

def merge(**params):
    data = params['data']
    df = data.merge(**params['parameters'])
    return df

# def split_data(**params):
#     df_shuffled = df.sample(frac=1)
# df_splits = np.array_split(df_shuffled, 2)
# for df in df_splits:
#     display(df)
#     return 0

def rename_columns(**params):
    data = params['data']
    dict = params['dict']
    axis = params['axis']
    data = data.rename(dict, axis)
    return data

def select_column(**params):
    data = params['data']
    df = data.select_dtypes(**params['parameters'])
    return df

def clean_column_names(**params):
    data = params['data']
    match=r"[\]\[\,\{\}\"\:]+"
    data.rename(columns=lambda x: re.sub(match, "", str(x)))
    return data

def clean_data(**params):
    data = params['data']
    df = AutoClean(data)
    return df.output

def clip(**params):
    data = params['data']
    data = data.clip(**params['paramters'])
    return data

def split_data(**params):
    data = params['data']
    df_shuffled = data.sample(frac=1)
    df_splits = np.array_split(df_shuffled, 2)
    return df_splits

