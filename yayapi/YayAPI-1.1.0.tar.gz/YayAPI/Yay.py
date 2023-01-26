from urllib.parse import quote
from fake_useragent import UserAgent
import requests
from typing import (
    Optional
)


class Yay:
    def __init__(self, Proxy: str = None, Token: str = None, Timeout: int = 10) -> None:
        self.Host = 'api.yay.space'
        self.UserAgent = str(UserAgent()["google chrome"])
        self.Timeout = Timeout
        if Proxy:
            self.Proxy = f"http://{Proxy}"
        else:
            self.Proxy = Proxy
        self.Headers = {
            'User-Agent': self.UserAgent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ja',
            'Referer': 'https://yay.space/',
            'Content-Type': 'application/json;charset=utf-8',
            'Agent': 'YayWeb 3.8.0',
            'X-Device-Info': f'Yay 3.8.0 Web ({self.UserAgent})',
            'Origin': 'https://yay.space',
        }
        if Token:
            self.Headers.setdefault("Authorization", f"Bearer {Token}")

    def Timeline(self) -> dict:
        """
        Yayのタイムラインを取得します。
        :rtype: dict
        """
        response = requests.get(f"https://{self.Host}/v1/web/posts/public_timeline?number=100",
                                headers=self.Headers,
                                timeout=self.Timeout, proxies={"http": self.Proxy, "https": self.Proxy})
        if response:
            return {"success": True, "data": response.json()["posts"]}
        else:
            return {"success": False}

    def UserSearch(self, Nickname: str = None, Biography: str = None,
                   Vip: bool = None,
                   RecentlyCreated: bool = None, NotRecentGomimushi: bool = None) -> dict:
        """
        ユーザーを検索します。
        :param Nickname: ニックネーム
        :type Nickname: str
        :param Biography: 自己紹介
        :type Biography: str
        :param Vip: VIPユーザーのみを出力します。
        :type Vip: bool
        :param RecentlyCreated: 最近アカウントを作成したユーザーを検索結果から除外します。
        :type RecentlyCreated: bool
        :param NotRecentGomimushi: 最近ゴミ虫になったユーザーを検索結果から除外します。
        :type NotRecentGomimushi: bool
        :rtype: dict
        """
        response = requests.get(f"https://{self.Host}/v1/web/users/search", params={
            'nickname': Nickname,
            'biography': Biography,
            'not_recent_gomimushi': NotRecentGomimushi,
            'recently_created': RecentlyCreated,
            'vip': Vip,
            'number': "100",
        }, headers=self.Headers, timeout=self.Timeout, proxies={"http": self.Proxy, "https": self.Proxy})
        if response:
            return {"success": True, "data": response.json()["users"]}
        else:
            return {"success": False}

    def TagSearch(self, Tag: str) -> dict:
        """
        ハッシュタグを検索します。
        :param Tag: 検索するハッシュタグ
        :type Tag: str
        :rtype: dict
        """
        response = requests.post(f"https://{self.Host}/v1/posts/recommended_tag", json={
            'tag': Tag,
        }, headers=self.Headers, timeout=self.Timeout, proxies={"http": self.Proxy, "https": self.Proxy})
        if response:
            return {"success": True, "data": response.json()["tags"]}
        else:
            return {"success": False}

    def KeywordSearch(self, Tag: str) -> dict:
        """
        指定のハッシュタグが含まれている投稿を検索します。
        :param Tag: 検索するハッシュタグ
        :type Tag: str
        :rtype: dict
        """
        response = requests.get(
            f"https://{self.Host}/v2/posts/tags/{quote(Tag)}?number=100", headers=self.Headers,
            timeout=self.Timeout, proxies={"http": self.Proxy, "https": self.Proxy}
        )
        if response:
            return {"success": True, "data": response.json()["posts"]}
        else:
            return {"success": False}

    def PostData(self, Postid: str) -> dict:
        """
        投稿データを取得します。
        :param Postid: 投稿id
        :type Postid: str
        :rtype: dict
        """
        response = requests.get(f"https://{self.Host}/v2/posts/{Postid}", headers=self.Headers, timeout=self.Timeout,
                                proxies={"http": self.Proxy, "https": self.Proxy})
        if response:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}

    def UserData(self, Userid: str) -> dict:
        """
        ユーザーデータを取得します。
        :param Userid: ユーザーid
        :type Userid: str
        :rtype: dict
        """
        response = requests.get(f"https://{self.Host}/v2/users/{Userid}", headers=self.Headers, timeout=self.Timeout,
                                proxies={"http": self.Proxy, "https": self.Proxy})
        if response:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}

    def UserActiveCall(self, Userid: str) -> dict:
        """
        ユーザーが通話をしているか確認します。
        :param Userid: ユーザーid
        :type Userid: str
        :rtype: dict
        """
        response = requests.get(f"https://{self.Host}/v1/posts/active_call?user_id={Userid}", headers=self.Headers,
                                timeout=self.Timeout, proxies={"http": self.Proxy, "https": self.Proxy})
        if response:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}

    def UserTimeline(self, Userid: str) -> dict:
        """
        ユーザー投稿データを取得します。
        :param Userid: ユーザーid
        :type Userid:str
        :rtype: dict
        """
        response = requests.get(f"https://{self.Host}/v2/posts/user_timeline?number=100&user_id={Userid}",
                                headers=self.Headers, timeout=self.Timeout,
                                proxies={"http": self.Proxy, "https": self.Proxy})
        if response:
            return {'success': True,
                    'data': response.json()}
        else:
            return {'success': False}

    def GetHimaUser(self) -> dict:
        """
        ひまなユーザーを取得します。
        :rtype: dict
        """
        response = requests.get(f"https://{self.Host}/v1/web/users/hima_users", params={
            'number': "100",
        }, headers=self.Headers, proxies={"http": self.Proxy, "https": self.Proxy}, timeout=self.Timeout)
        if response:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}

    def GetGroupMember(self, Groupid: str) -> dict:
        """
        サークルのユーザー情報を取得します。
        :param Groupid: サークルid
        :type Groupid: str
        :rtype:dict
        """
        response = requests.get(f"https://{self.Host}/v2/groups/{Groupid}/members?number=100",
                                headers=self.Headers,
                                proxies={"http": self.Proxy, "https": self.Proxy}, timeout=self.Timeout)
        if response:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}
