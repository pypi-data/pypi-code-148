import requests
from typing import Dict, List
import warnings

import pandas as pd
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    import pandasdmx as sdmx


def sdmx_request(api_url: str, params: str = {}) -> pd.Series:
    """
    API query for SDMX output
    Parameters:
        - api_url: url to query
        - params: additional query parameters

    Returns:
        - pd.Serie response
    """
    req = sdmx.Request()
    response = req.get(url=f"{api_url}?{params}")
    return sdmx.to_pandas(response)


def json_request(api_url: str, params: str = {}) -> dict:
    """
    API query for JSON output
    Parameters:
        - api_url: url to query
        - params: additional query parameters

    Returns:
        - dictionnary response
    """
    return requests.get(url=api_url, params=params).json()


def csv_request(api_url: str, params: str) -> pd.DataFrame:
    """
    API query for CSV output
    Parameters:
        - api_url: url to query
        - params: additional query parameters

    Returns:
        - pd.DataFrame response
    """
    # As dtype string to keep leading 0s and avoid decimals
    return pd.read_csv(f"{api_url}?{params}", dtype=str)


# Map the appropriate function based on the output type
REQUEST_FUNCTION_MAPPING = {
    "JSON": json_request,
    "SDMX-JSON": json_request,
    "SDMX-ML": sdmx_request,
    "CSV": csv_request,
}


def dict_to_string(filters: Dict[str, List[str]]) -> str:
    """
    Transform a dictionnary into a string of parameters
    Input {'a': ['1'], 'b': ['2', '3']} -> Output 'a=1&b=2&b=3'
    Parameters:
        - filters: dictionnary of parameters

    Returns:
        - formatted string of parameters
    """
    return "&".join(
        [
            f"{key}={val}"
            for key, val_list in filters.items()
            for val in val_list
        ]
    )
