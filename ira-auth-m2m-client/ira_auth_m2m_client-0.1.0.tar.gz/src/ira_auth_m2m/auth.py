import asyncio
from functools import partial
from typing import Union
import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client


class MaxRetriesReached(Exception):
    pass


class IraAuth:
    token_endpoint = ""

    def __init__(self, client_id: str, client_secret: str, cookie_name: str = "token", token_endpoint: Union[str, None] = None):
        if token_endpoint != None:
            self.token_endpoint = token_endpoint
        self.oauth2_client = AsyncOAuth2Client(client_id, client_secret, scope="api", token_endpoint_auth_method="client_secret_post")
        self.http_client = httpx.AsyncClient(headers={"Accept": "application/json"})
        self.cookies = httpx.Cookies()
        self.cookie_name = cookie_name

    async def get_token(self) -> str:
        token = await self.oauth2_client.fetch_token(self.token_endpoint, grant_type="client_credentials")
        return token["access_token"]

    async def http(self, base_path: str, method: str, url:str, data: any = None, retry_after=5, max_retries=-1, _acc=0):
        try:
            response = await self.http_client.request(method, base_path + url, data=data, cookies=self.cookies)
            if response.status_code == httpx.codes.UNAUTHORIZED:
                if _acc > 0:
                    await asyncio.sleep(retry_after)
                
                if max_retries != -1 and _acc == max_retries:
                    raise MaxRetriesReached
                    
                token =  await self.get_token()
                self.cookies.set(self.cookie_name, token)
                _acc += 1
                response = await self.http(base_path, method, url, data, retry_after, max_retries, _acc)
                return response
            else:
                return response
        except Exception as e:
            print(e)
        return None

    def get_http_client(self, base_path: str=""):
        return partial(self.http, base_path)

    async def cleanup(self):
        await self.oauth2_client.aclose()
        await self.http_client.aclose()