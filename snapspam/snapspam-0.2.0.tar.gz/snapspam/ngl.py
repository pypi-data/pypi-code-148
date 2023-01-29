"""Functions to spam an NGL message."""
import requests
import uuid


class NGL:
    def __init__(self, link_or_id: str, proxies: dict = {}):
        """Initialize the NGL class

        Args:
            link_or_id (str): The NGL URL or the ID portion of the URL
            proxies (dict, optional): Proxies to use for requests
        """
        self._ngl_id = self._link_to_id(link_or_id)
        self._headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        self._proxies = proxies
        self._id = str(uuid.uuid4())

    def post(self, message: str) -> requests.Response:
        """Send a message to the API

        Args:
            message (str): The message to send

        Returns:
            requests.Response: The response from the POST
        """
        return requests.post(
            f"https://ngl.link/api/submit",
            data={
                "username": self._ngl_id,
                "question": message,
                "deviceId": self._id,
                "gameSlug": "",
                "referrer": "",
            },
            headers=self._headers,
            proxies=self._proxies,
        )

    def _link_to_id(self, link: str) -> str:
        """Convert an NGL link to just the username

        Args:
            link (str): The NGL link

        Returns:
            str: The username from the link
        """
        return link.strip("/").split("/")[-1]
