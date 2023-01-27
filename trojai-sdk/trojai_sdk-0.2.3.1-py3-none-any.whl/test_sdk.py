from trojsdk.core import data_utils
from trojsdk.core import client_utils
from trojsdk.core.client_utils import TrojJobHandler
import logging


def test_sdk_fail():
    # config = load_json_from_disk(Path("./trojsdk/examples/testing_config.json"))

    docker_metadata = {
        "docker_image_url": "trojai/trojai-engine-master:10ba6f109b9843e2be008db01465de9e40fc2dc0",
        "docker_secret_name": "trojaicreds",
    }

    troj_job_handler = client_utils.submit_evaluation("./trojsdk/configs/tabular_test/tabular_test_main.json", docker_metadata=docker_metadata)
    troj_job_handler = TrojJobHandler()
    try:
        troj_job_handler.check_job_status()
        assert False
    except:
        assert True


def test_sdk_pass_tabular():
    # config = load_json_from_disk(Path("./trojsdk/examples/testing_config.json"))

    # docker_metadata = {
    #     "docker_image_url": "trojai/trojai-engine-master:10ba6f109b9843e2be008db01465de9e40fc2dc0",
    #     "docker_secret_name": "trojaicreds",
    # }
    troj_job_handler = client_utils.submit_evaluation(
        # path_to_config="trojsdk/examples/nlp_test_main.json",
        path_to_config="trojsdk/examples/tabular_medical_insurance_config.json", nossl=True
    )

    import time

    time.sleep(2)
    try:
        troj_job_handler.check_job_status()
        troj_job_handler.status_response["data"][0]["job_name"]
        assert True
    except:
        assert False

# def test_sdk_pass_nlp():


#     troj_job_handler = client_utils.submit_evaluation(
#         path_to_config="./trojsdk/examples/nlp_test_main.json", nossl=True
#     )

#     import time

#     time.sleep(2)
#     try:
#         troj_job_handler.check_job_status()
#         troj_job_handler.status_response["data"][0]["job_name"]
#         assert True
#     except:
#         assert False

# def test_sdk_pass_cv():
#     # config = load_json_from_disk(Path("./trojsdk/examples/testing_config.json"))
#     # config = load_json_from_disk(Path("./trojsdk/examples/s3_test/s3_classification_config.json"))

#     troj_job_handler = client_utils.submit_evaluation(
#         path_to_config="./trojsdk/examples/s3_small_classification_pt_config.json"
#     )

#     import time

#     time.sleep(2)
#     try:
#         troj_job_handler.check_job_status()
#         troj_job_handler.status_response["data"][0]["job_name"]
#         assert True
#     except:
#         assert False


# if __name__ =="__main__":
#     test_sdk_pass_cv()