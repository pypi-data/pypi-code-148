# !/usr/bin/env python3
""" free qa task """
import time
import json
import wenxin_api
from wenxin_api.api import Task
from wenxin_api.error import IllegalRequestArgumentError
from wenxin_api import requestor,log
from wenxin_api.error import APIError
logger = log.get_logger()

class QAExtract(Task):
    """ qa extract task """
    @staticmethod
    def _resolve_result(resp):
        rst = {}
        rst["result"] = resp["result"]
        return rst
    
    def _http_init(self):
        """ http initialization """
        self.requestor = requestor.HTTPRequestor()
        self.api_type = 9
        self.create_url = wenxin_api.variable.API_REQUEST_URLS[self.api_type]
        self.retrieve_url = wenxin_api.variable.API_GET_RESULT_URL

       


    @classmethod
    def create(cls, text=None, model=None, **params):
        """ create """
        cls._http_init(cls)

        if text is None:
            raise IllegalRequestArgumentError("text shouldn't be none")
        model_id = 1 if model is None else model.id
        task_prompt = params.pop("task_prompt", "qa_extract")
        modelId = params.pop("modelId", 2)
        logger.info("model {}: starts writing".format(modelId))

        is_async = params.pop("async", 1)
        params["async"] = is_async
        resp = cls.requestor.request(cls.create_url, "post", text=text,task_prompt=task_prompt,modelId=modelId, **params, return_raw=True)
        
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
                return cls._resolve_result(resp.json()["data"])
            rst = resp.json()
            logger.info("model is running now!, taskId: {}".format(rst["data"]["taskId"]))
            time.sleep(wenxin_api.variable.REQUEST_SLEEP_TIME)

