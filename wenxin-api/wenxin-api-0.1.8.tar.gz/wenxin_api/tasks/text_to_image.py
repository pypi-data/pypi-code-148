""" text generation task """
import time
import warnings
import json
import os
import wenxin_api
from wenxin_api import requestor, error, log
from wenxin_api.api import Task
from wenxin_api.api import ListableAPIObject
import wenxin_api.variable
from wenxin_api.const import SOURCE_WENXIN, SOURCE_CONSOLE
from wenxin_api.error import APIError
logger = log.get_logger()

class TextToImage(Task):
    """ text generation task """
    OBJECT_NAME = "text_to_image"

    def _http_init(self):
        """ http initialization """
        self.requestor = requestor.HTTPRequestor()
        self.create_url = wenxin_api.variable.VILG_CREATE_URL
        self.retrieve_url = wenxin_api.variable.VILG_RETRIEVE_URL

    @classmethod
    def create(cls, *args, **params):
        """ create """
        cls._http_init(cls)            
        start = time.time()
        timeout = params.pop("timeout", None)
        text = params.pop("text", "")
        style = params.pop("style", "")
        watermark = params.get("watermark", 1)
        num = params.get("num", 6)
        resolution = params.get("resolution", "1024*1024")
        resp = cls.requestor.request(cls.create_url, 
                                      text=text, 
                                      style=style, 
                                      watermark=watermark,
                                      num=num,
                                      resolution=resolution,
                                      return_raw=True)

        try:
            task_id = resp.json()["data"]["taskId"]
        except Exception as e:
            raise APIError(json.dumps(resp.json(), 
                           ensure_ascii=False,
                           indent=2))
        not_ready = True
        while not_ready:
            resp = cls.requestor.request(cls.retrieve_url, taskId=task_id, return_raw=True)
            not_ready = resp.json()["data"]["status"] == 0
            if not not_ready:
                return cls._resolve_result(resp.json())
            rst = resp.json()
            logger.info("model is painting now!, taskId: {}, waiting: {}".format(
                rst["data"]["taskId"],
                rst["data"]["waiting"]))
            time.sleep(wenxin_api.variable.REQUEST_SLEEP_TIME)

    @staticmethod
    def _resolve_result(resp):
        if resp["code"] == 0:
            ret_dict = {"imgUrls": []}
            for d in resp["data"]["imgUrls"]:
                ret_dict["imgUrls"].append(d["image"])
            return ret_dict
        else:
            return resp


class TextToImageRef(TextToImage):
    """ text generation task """
    OBJECT_NAME = "text_to_image"

    @classmethod
    def create(cls, *args, **params):
        """ create """
        cls._http_init(cls)   
        print("create url", cls.create_url)         
        start = time.time()
        timeout = params.pop("timeout", None)
        text = params.pop("text", "")
        style = params.pop("style", "")
        num = params.get("num", 6)
        resolution = params.get("resolution", "1024*1024")
        local_file_path = params.get("ref_img", None)

        with open(local_file_path, 'rb') as f:
            file_ext = os.path.splitext(local_file_path)[-1]
            if file_ext == ".jpg":
                files = {"image": ("image", f, "image/jpeg")}
            elif file_ext == ".png":
                files = {"image": ("image", f, "image/png")}
            else:
                files = {"image": ("image", f)}

            headers = {}
            resp = cls.requestor.request(cls.create_url, 
                                        headers=headers,
                                        files=files,
                                        text=text, 
                                        style=style, 
                                        resolution=resolution,
                                        num=num,
                                        return_raw=True)

        try:
            task_id = resp.json()["data"]["taskId"]
        except Exception as e:
            raise APIError(json.dumps(resp.json(), 
                           ensure_ascii=False,
                           indent=2))
        not_ready = True
        while not_ready:
            resp = cls.requestor.request(cls.retrieve_url, taskId=task_id, return_raw=True)
            not_ready = resp.json()["data"]["status"] == 0
            if not not_ready:
                return cls._resolve_result(resp.json())
            rst = resp.json()
            logger.info("model is painting now!, taskId: {}, waiting: {}".format(
                rst["data"]["taskId"],
                rst["data"]["waiting"]))
            time.sleep(wenxin_api.variable.REQUEST_SLEEP_TIME)

    @staticmethod
    def _resolve_result(resp):
        if resp["code"] == 0:
            ret_dict = {"imgUrls": []}
            for d in resp["data"]["imgUrls"]:
                ret_dict["imgUrls"].append(d["image"])
            return ret_dict
        else:
            return resp


class TextToImageConsole(TextToImage):
    """ text generation task """
    OBJECT_NAME = "text_to_image_console"

    def _http_init(self):
        """ http initialization """
        self.requestor = requestor.ConsoleHTTPRequestor()
        access_token = self.requestor._get_access_token()
        self.create_url = wenxin_api.variable.VILG_CREATE_URL_CONSOLE + "?access_token={}".format(access_token)
        self.retrieve_url = wenxin_api.variable.VILG_RETRIEVE_URL_CONSOLE + "?access_token={}".format(access_token)

    @staticmethod
    def _resolve_result(resp):
        ret_dict = {"imgUrls": []}
        for d in resp["data"]["imgUrls"]:
            ret_dict["imgUrls"].append(d["image"])
        return ret_dict