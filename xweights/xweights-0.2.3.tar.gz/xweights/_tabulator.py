import os

import pandas as pd
from pyhomogenize import get_var_name


def write_to_pandas(da, column_dict={}, name="name"):
    """Write xr.DataArray to pd.DataFrame

    Parameters
    ----------
    da: xr.DaraArray

    column_dict:  dict (optional)
        Dictionary containing new pd.DataFrame column names
        and corresponding values.

    name: str (optional)
        Name of the pd.DataFrame rows; e.g. name of the xr.DataArray

    Returns
    -------
    pd.DataFrame
    """
    df_output = da.to_dataframe()
    length = len(df_output)
    for key, value in column_dict.items():
        df_output[key] = [value] * length
    df_output["name"] = [name] * length
    return df_output


def concat_dataframe(dataframe, ds, variables=None, **kwargs):

    """Concatenate newly created pd.DataFrame to already existing pd.DataFrame

    Parameters
    ----------
    dataframe: pd.DataFrame
        Already existing pd.DataFrame, can also be empty.

    ds: xr.DataSet

    variables: str or list, default: `ds.vars`
        Names(s) of the xr.Dataset variables to be written to the pd.DataFrame

    kwargs:
        Opional parameters transferred to function `write_to_pandas`
        column_dict
        name
        var

    Returns
    -------
    pd.DataFrame
    """
    if variables is None:
        variables = get_var_name(ds)
    if isinstance(variables, str):
        variables = [variables]
    for var in variables:
        dataframe = pd.concat([dataframe, write_to_pandas(ds[var], **kwargs)])
    return dataframe


def write_to_csv(dataframe, output):
    """Write pd.DataFrame to csv table and save on disk

    Parameters
    ----------
    dataframe: pd.DataFrame

    output: str
        output name
        If directory path default name is 'spatial_average_table.csv'
    """

    if os.path.isdir(output):
        outfile = os.path.join(output, "spatial_average_table.csv")
    elif output[-3:] == "csv":
        outfile = output
    else:
        outfile = output + ".csv"
    dataframe.to_csv(outfile)
    print("File written: {}".format(outfile))
