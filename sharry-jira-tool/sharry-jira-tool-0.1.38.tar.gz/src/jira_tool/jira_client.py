# -*- coding: utf-8 -*-
"""
This module is used to store excel column definition information.
"""
import json

from requests import Response, get, post
from requests.exceptions import RequestException
from requests.status_codes import codes


class JiraClient:
    def __init__(self, access_token: str) -> None:
        self.base_url: str = "https://pd.nextestate.com"
        self.timeout: int = 3
        self.access_token: str = access_token
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

    def health_check(self) -> bool:
        url = f"{self.base_url}/rest/api/2/dashboard"

        try:
            response: Response = get(
                url,
                headers=self.headers,
                verify=False,
                timeout=self.timeout,
            )

            if response.status_code == codes["OK"]:
                return True
        except RequestException as e:
            print(e)
        return False

    def get_stories_status(self, story_ids: list[str]) -> "dict":
        url = f"{self.base_url}/rest/api/2/search"
        id_query = ",".join([f"'{str(story_id)}'" for story_id in story_ids])
        request_body = json.dumps(
            {
                "expand": [],
                "jql": f"id in ({id_query})",
                "maxResults": len(story_ids),
                "fields": ["status"],
                "startAt": 0,
            }
        )

        try:
            response: Response = post(
                url,
                data=request_body,
                headers=self.headers,
                verify=False,
                timeout=self.timeout,
            )

            if response.status_code == codes["OK"]:
                search_result = response.json()

                return {
                    issue["key"]: issue["fields"]["status"]["name"]
                    for issue in search_result["issues"]
                }
            else:
                return {}
        except RequestException as e:
            print(e)

            return {}
