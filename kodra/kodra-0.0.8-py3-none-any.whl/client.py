import random
import time
import urllib.parse
from typing import Optional, Tuple

import pandas
import requests
from requests_toolbelt.multipart import encoder
from tqdm import tqdm

"""
This library can be used to interact with the Kodra web application for a
limited set of workflows. The primary workflow that is supported for now is 
uploading Pandas Dataframe objects to an existing Kodra project.

Usage:

import pandas
from kodra import Kodra

df = pandas.DataFrame({'name': ['John Smith', 'Alice', 'Bob'],
                       'department': ['engineering', 'finance', 'marketing'],
                       'tenure (years)': ['2', '5', '10']})
Kodra().share(
    data=df,
    name="<optional_name>"
)

The `name` field correspondonds to the dataset name. If the user
does not provide a name, a default one will be created and assigned by Kodra.

"""


def share(
    data: pandas.DataFrame, name: Optional[str] = "My Dataset"
) -> Tuple[int, str]:
    """Top level method to upload a DataFrame to Kodra with default Client.

    This instantiates a default Client() object and allows the user to upload
    a pandas DataFrame to Kodra with a valid upload token. The core functionality
    is handled by the Client's share() method (see below).

    Usage:
        import kodra
        kodra.share(data=my_dataframe, name="Awesome Dataset")

    Args:
        data: The Pandas DataFrame object
        name: The name of this dataset (optional)

    Returns:
        A Tuple containing the HTTP status code of the upload request along
        with an error string if any are returned. Examples:
            (200, "")
            (400, "Not Authorized")
    """
    client = Client(base_url="https://kodra.ai")
    return client.share(data=data, name=name)


class Client:
    """A simple client that interacts with the Kodra backend over HTTP."""

    def __init__(self, base_url: str = "http://localhost:3000"):
        # Url to upload a dataset to Kodra
        self.kodra_notebook_share_endpoint = base_url + "/api/share/"

        # Url to generate a new upload token
        self.kodra_notebook_new_token_endpoint = base_url + "/api/notebook-upload/"

        # Url to check if an upload token has been authorized
        self.kodra_notebook_token_check_endpoint = (
            base_url + "/api/notebook-upload/check/"
        )

        # Url to authorize a token via frontend UI
        self.kodra_notebook_token_auth_ui = base_url + "/authorize-notebook/{}"

        # Url to explore a dataset in the Kodra UI
        self.kodra_dataset_explore_url = base_url + "/studio/explore/{}"

    def wait_for_token_ready(self, token: str) -> bool:
        # Post a request to the Kodra server to check if the token has been authorized
        # Keep checking every 2 seconds for first minute, then every 10 seconds. Time out
        # after 5 minutes.
        # TODO: This should eventually be replaced with a websocket connection or SSE.
        # TODO: Should stop checking if user explicitly denies the upload.
        for i in range(30):  # 30 * 2 = 60 seconds = 1 minute
            try:
                resp = requests.post(
                    self.kodra_notebook_token_check_endpoint,
                    json={"upload-token": token},
                    timeout=2,
                )
                if resp.json()["ready"]:
                    return True
            except Exception as e:
                print(e)
            time.sleep(2)
        for i in range(24):  # 24 * 10 = 240 seconds = 4 minutes
            try:
                resp = requests.post(
                    self.kodra_notebook_token_check_endpoint,
                    json={"upload-token": token},
                    timeout=2,
                )
                if resp.json()["ready"]:
                    return True
            except Exception as e:
                print(e)
            time.sleep(10)
        return False

    def attempt_to_open_browser(self, url: str) -> None:
        """Attempts to open the provided URL in the user's browser, assuming a
        a notebook environment.
        """
        try:
            import IPython
            from IPython.display import Javascript, display

            display(Javascript("window.open('{}')".format(url)))
        except Exception as e:
            print("Unable to open browser automatically.")
        print(
            "If it doesn't open automatically, please visit the following URL to authorize this upload:"
        )
        print("\t" + url)

    def share(
        self, data: pandas.DataFrame, name: Optional[str] = "My Dataset"
    ) -> Tuple[int, str]:
        """Upload a Pandas Dataframe object to Kodra as a CSV file.

        Args:
            data: A Pandas DataFrame object containing the data to be uploaded.
            name: The name of the dataset. If not provided, a default name will
                  be generated: "My Dataset".

        Returns:
            A Tuple containing the HTTP status code along with an error string
            if any are returned. Examples:
            (200, "")
            (400, "Not Authorized")

        Raises:
            AssertionError: If the provided data is not a Pandas Dataframe
            ValueError: If the provided data is empty
        """
        assert isinstance(
            data, pandas.DataFrame
        ), "Provided data is not a Pandas DataFrame"
        if data.empty:
            raise ValueError("Provided DataFrame is empty")

        # Get a token by sending a post request to the Kodra server
        resp = requests.post(
            self.kodra_notebook_new_token_endpoint,
            timeout=2,
        )
        if resp.status_code != 201:
            raise ValueError("Could not get a token from Kodra")
        token = resp.json()["upload-token"]

        # Open the Kodra authorization page in the user's browser to authorize the token.
        # We are appending the dataset name to the URL so that the name passed into this
        # function is pre-populated in the UI.
        token_auth_ui_url = self.kodra_notebook_token_auth_ui.format(
            token
        ) + "?dataset_name={}".format(urllib.parse.quote(name, safe=""))
        self.attempt_to_open_browser(token_auth_ui_url)

        # Wait for the token to be authorized
        print("Waiting for upload to be authorized...")
        token_ready = self.wait_for_token_ready(token)
        if not token_ready:
            raise ValueError(
                "There was an error authorizing this upload, please try again."
            )
        print("Upload token authorized. Sharing data...")

        # Upload the data to Kodra

        # Convert the DataFrame to CSV for uploading. We are setting index = False
        # since we don't want the dataframe's index column to be included in the CSV.
        csv_data = data.to_csv(index=False)
        multipart_encoder = encoder.MultipartEncoder(
            fields={"file": ("dataset", csv_data)}
        )
        with tqdm(
            desc="Uploading data",
            total=multipart_encoder.len,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            # Used to display a progress bar for the streaming data upload
            encoder_monitor = encoder.MultipartEncoderMonitor(
                multipart_encoder,
                lambda monitor: progress_bar.update(
                    monitor.bytes_read - progress_bar.n
                ),
            )
            resp = requests.post(
                self.kodra_notebook_share_endpoint,
                data=encoder_monitor,
                headers={
                    "Upload-Token": token,
                    "Content-Type": multipart_encoder.content_type,
                },
            )
        # Get UUID from response and link to dataset explore page
        if resp.status_code == 201:
            dataset_uuid = resp.json()["uuid"]
            dataset_explore_url = self.kodra_dataset_explore_url.format(dataset_uuid)
            print(
                "Upload successful. Dataset available at:\n\t{}".format(
                    dataset_explore_url
                )
            )
        else:
            print("Upload failed.")

        return (resp.status_code, resp.reason)
