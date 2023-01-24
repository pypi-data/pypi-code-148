import itertools
from typing import Union

import pandas as pd

from fso_metadata.api_class import Api
from fso_metadata.format_request import dict_to_string


def get_codelist(
    identifier: str,
    environment: str = "PRD",
    export_format: str = "SDMX-ML",
    version_format: float = 2.1,
    annotations: bool = False,
) -> Union[dict, pd.DataFrame]:
    """
    Get a codelist based on an identifier
    Parameters:
        - identifier (str): the codelist's identifier
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - export_format (str, default="SDMX-ML"): the export's format
           Available are CSV, XLSX, SDMX-ML or JSON.
        - version_format (float, default=2.1): the export format's version
          (2.0 or 2.1 when format is SDMX-ML).
        - annotations (bool, default=False): flag to include annotations

    Returns:
        - response (pd.DataFrame or dict) based on the export format
            - a pd.DataFrame if export_format was CSV or XLSX
            - a dictionnary if export_format was SDMX-ML or SDMX-JSON.
    """
    api = Api(
        api_type="codelist",
        environment=environment,
        _id=identifier,
        export_format=export_format,
        version_format=version_format,
        parameters=f"annotations={str(annotations).lower()}",
    )
    if export_format == "SDMX-ML":
        res =  api.get_response()[0][0]
    else:
        raise NotImplementedError("Only SDMX-ML implement for codelist yet.")
    return res


def get_data_structure(
    identifier: str, 
    environment: str = "PRD", 
    language: str = "fr"
) -> dict:
    """
    Get the data structure
    Parameters:
        - identifier (str): the dataset's identifier
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - language (str, default='fr'): the language of the response data
            Available are 'fr', 'de', 'it', 'en'.
    Returns:
        - response: datastructure dictionnary
    """
    api = Api(
        api_type="dcat_data_structure", 
        environment=environment, 
        _id=identifier, 
        language=language
    )
    return api.get_response()


def get_nomenclature_one_level(
    identifier: str,
    level_number: int,
    environment: str = "PRD",
    filters: dict = {},
    language: str = "fr",
    annotations: bool = False
) -> pd.DataFrame:
    """
    Get one level of a nomenclature
    Parameters:
        - identifier (str): nomenclature's identifier
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - level_number (int): level to export
        - filter (default={}): additionnal filters
        - language (str, default='fr'): response data's language
            Available are 'fr', 'de', 'it', 'en'.
        - annotations (bool, default=False): flag to include annotations
    Returns:
        - response (pd.DataFrame): dataframe with 3 columns
        (Code, Parent and Name in the selected language)
    """
    parameters = (
        f"language={language}"
        f"&level={level_number}"
        f"&annotations={str(annotations).lower()}"
        f"&{dict_to_string(filters)}"
    )
    api = Api(
        api_type="nomenclature_one_level",
        environment=environment,
        _id=identifier,
        parameters=parameters,
        export_format="CSV",
    )
    return api.get_response()


def get_nomenclature_multiple_levels(
    identifier: str,
    level_from: int,
    level_to: int,
    environment: str = "PRD",
    filters: dict = {},
    language: str = "fr",
    annotations: bool = False,
    post_processing: bool = False
) -> pd.DataFrame:
    """
    Get multiple levels of a nomenclature (from `level_from` to `level_to`)
    Parameters:
        - identifier (str): nomenclature's identifier
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - level_from (int): the 1st level to include
        - level_to (int): the last level to include
        - filter (default={}): additionnal filters
        - language (str, default='fr'): response data's language
            Available are 'fr', 'de', 'it', 'en'.
        - annotations (bool, default=False): flag to include annotations
        - post_processing (bool, default=False)
    Returns:
        - response (pd.DataFrame): dataframe columns
        from `level_from` to `level_to` codes
    """
    # Call api with appropriate url and parameters
    parameters = (
        f"language={language}"
        f"&levelFrom={level_from}"
        f"&levelTo={level_to}"
        f"&annotations={str(annotations).lower()}"
        f"&{dict_to_string(filters)}"
    )
    api = Api(
        api_type="nomenclature_multiple_levels",
        environment=environment,
        _id=identifier,
        parameters=parameters,
        export_format="CSV",
    )
    df = api.get_response()

    # Post-processing:
    if post_processing:
        # fill sub groups rows with parent group's values (instead of NaN)
        group_columns = [
            *itertools.takewhile(lambda col: col != "Code", df.columns)
        ]
        df[group_columns[0]] = df[group_columns[0]].fillna(method="ffill")
        df[group_columns[1:]] = (
            df.groupby([group_columns[0]])[group_columns[1:]]
        ).apply(lambda x: x.ffill())
    return df
