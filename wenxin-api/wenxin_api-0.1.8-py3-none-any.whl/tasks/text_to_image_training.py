""" text generation task """
import time
import warnings
import json
import wenxin_api
from wenxin_api import requestor, error, log
from wenxin_api.api import Task, Train
from wenxin_api.api import CreatableAPIObject, ListableAPIObject
import wenxin_api.variable
from wenxin_api.const import SOURCE_WENXIN, SOURCE_CONSOLE
from wenxin_api.error import APIError, IllegalRequestArgumentError
from wenxin_api.const import (CMD_DO_DEPLOY, 
                              CMD_DO_INFERENCE, 
                              CMD_QUERY_MODEL, 
                              CMD_QUERY_TASK,
                              CMD_STOP_TASK,)
from wenxin_api.const import (MODEL_STATE_ERROR, 
                              MODEL_STATE_SUCCESS, 
                              MODEL_STATE_ON_SERVICE,)
from wenxin_api.const import (TASK_STATE_INFER_IN_QUEUE,
                              TASK_STATE_INFER_RUNNING,
                              TASK_STATE_INFER_END,)
from wenxin_api.const import (TASK_STATE_DEPLOY_SUBMIT, 
                              TASK_STATE_DEPLOY_IN_QUEUE, 
                              TASK_STATE_DEPLOY_RUNNING,
                              TASK_STATE_DEPLOY_SUCCESS,
                              TASK_STATE_DEPLOY_FAILED,)
logger = log.get_logger()

class TextToImageTuned(Task):
    """ text generation task """
    OBJECT_NAME = "text_to_image"
    training_api_type = 12

    def _http_init(self):
        """ http initialization """
        self.requestor = requestor.HTTPRequestor()

    @classmethod
    def _create(cls, *args, **params):
        """ create """
        cls._http_init(cls)            
        start = time.time()
        api_type = params.pop("api_type", None)
        timeout = params.pop("timeout", None)
        text = params.pop("text", "")
        style = params.pop("style", "")
        num = params.get("num", 6)
        resolution = params.get("resolution", "1024*1024")
        model = params.get("model", None)
        
        request_id = params.get("request_id", None)
        resp = cls.requestor.request(cls.get_url(api_type), 
                                      model_id=model.id,
                                      text=text, 
                                      style=style, 
                                      resolution=resolution,
                                      request_id=request_id,
                                      return_raw=True)

        try:
            task_id = resp.json()["data"]["taskId"]
        except Exception as e:
            raise APIError(json.dumps(resp.json(), 
                           ensure_ascii=False,
                           indent=2))
        not_ready = True
        while not_ready:
            resp = cls.requestor.request(wenxin_api.variable.VILG_TUNING_QUERY_URL, 
                                         request_id=request_id,
                                         model_id=model.id,
                                         taskId=task_id, 
                                         return_raw=True)
            print("resp:", resp.json())
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

    @classmethod
    def create(cls, text=None, model=None, **params):
        """ create """
        api_type = params.pop("api_type", cls.training_api_type)
        if text is None:
            raise IllegalRequestArgumentError("text shouldn't be none")
        if model is None:
            raise IllegalRequestArgumentError("model shouldn't be none")
        else:
            model.update()
        # deploy
        if model.status != MODEL_STATE_ON_SERVICE:
            request_id = CMD_DO_DEPLOY
            params["type"] = "task"
            deploy_task = CreatableAPIObject.create(model_id=model.id, 
                                                    request_id=request_id, 
                                                    api_type=api_type,
                                                    **params)

            not_ready = True
            while not_ready:
                deploy_task.update()
                print("deploy task:", deploy_task)
                not_ready = deploy_task.status != TASK_STATE_DEPLOY_SUCCESS
                if deploy_task.status == TASK_STATE_DEPLOY_FAILED:
                    raise APIError("deploy task:{} failed".format(deploy_task.id))
                logger.info("model is preparing now!, task_id:{}, status:{}".format(
                    deploy_task.id, 
                    deploy_task.status)
                )
                time.sleep(wenxin_api.variable.REQUEST_SLEEP_TIME)
        
        # inference
        api_type = params.pop("api_type", cls.training_api_type)
        logger.info("model {}: starts writing".format(model.id))
        request_id = CMD_DO_INFERENCE
        # todo:add base_model and is_prompt
        resp = cls._create(text=text, 
                           model=model, 
                           api_type=api_type,
                           request_id=request_id, 
                           **params)

        return resp
