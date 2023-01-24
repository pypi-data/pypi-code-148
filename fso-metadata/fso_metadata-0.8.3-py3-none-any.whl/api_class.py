from typing import Union

import pandas as pd

#from fso_metadata.constants import BASE_URL
from fso_metadata.constants import ENVIRONMENTS
from fso_metadata.format_request import REQUEST_FUNCTION_MAPPING


class Api:
    """
    Api class to make appropriate request based on parameters
    """

    def __init__(
        self,
        api_type: str,
        *,
        export_format: str = "JSON",
        environment: str = "PRD",
        parameters: Union[str, dict] = None,
        _id: str = None,
        language: str = "en",
        version_format: float = 2.1,
    ) -> None:
        """
        Parameters:
        - api_type (str): the name of the api to call (see url_mapping)
        - export_format (str, default="JSON"): the export's format
           Available are CSV, XLSX, SDMX-ML and JSON.
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - parameters (Union[str, dict]): additional request parameters
        - _id: the identifier or id of the request's object
        - language (str, default='en'): the language of the response data
            Available are 'fr', 'de', 'it', 'en'.
        - version_format (float, default=2.1): the export format's version
          (2.0 or 2.1 when format is SDMX-ML) (for 'codelist')
        """
        self.environment = ENVIRONMENTS[environment]
        self.export_format = export_format
        self.parameters = parameters

        self.api_url = self.get_url(
            api_type, _id, version_format, language
        )
        

    def get_response(self) -> Union[dict, pd.DataFrame]:
        """
        Depending on the expected output, call the api appropriately
        Returns:
            - response (pd.DataFrame or dict) based on the export format
                - a pd.DataFrame if export_format was CSV or XLSX
                - a dictionnary if export_format was SDMX-ML or SDMX-JSON.
        """
        request_function = REQUEST_FUNCTION_MAPPING[self.export_format]
        return request_function(
            f"{self.environment}/api/{self.api_url}", self.parameters
        )

    def get_url(
        self,
        api_type: str,
        _id: str,
        version_format: float,
        language: str,
    ):
        """
        Get the url call based on the api type and parameters
        """
        url_mapping = {
            "codelist": f"CodeLists/{_id}/exports/{self.export_format}/{version_format}",
            "dcat_data_structure": f"DataStructures/{_id}/{language}",
            "nomenclature_one_level": f"Nomenclatures/{_id}/levelexport/CSV",
            "nomenclature_multiple_levels": f"Nomenclatures/{_id}/multiplelevels/CSV",
        }

        return url_mapping[api_type]
