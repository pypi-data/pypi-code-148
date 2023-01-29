import pandas as pd
import woodwork as ww

def parse_dataset(dataset):
    # parse dataset using woodwork and return a dictionary with column names as keys and logical column types as values
    ww_df = ww.init(dataset)
    logical_types = ww_df.logical_types
    logical_types_dict = {}
    for col in logical_types:
        logical_types_dict[col] = logical_types[col]
    return logical_types_dict

  # dict = {}
    # dict["rows"] = len(dataset)
    # dict["columns"] = []
    # for column in dataset.columns:
    #     if (
    #         column.lower() == "location"
    #         or column.lower() == "city"
    #         or column.lower() == "country"
    #         or column.lower() == "state"
    #     ):
    #         dict["columns"].append({"name": column, "type": "location"})
    #     if (
    #         column
    #         in dataset.select_dtypes(
    #             include=["int64", "float64", "int32", "float32"]
    #         ).columns.values
    #     ):
    #         dict["columns"].append({"name": column, "type": "numeric"})
    #     elif column in dataset.select_dtypes(include=["object"]).columns.values:
    #         if len(dataset[column].unique()) < len(dataset) * 0.1:
    #             dict["columns"].append({"name": column, "type": "categorical"})
    #             continue
    #         try:
    #             pd.to_datetime(dataset[column], dayfirst=True)
    #             dict["columns"].append({"name": column, "type": "datetime"})
    #             continue
    #         except:
    #             dict["columns"].append({"name": column, "type": "text"})
    # return dict
      


    
