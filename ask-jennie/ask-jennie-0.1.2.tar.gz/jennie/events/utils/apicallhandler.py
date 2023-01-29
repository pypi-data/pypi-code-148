import requests
from jennie.events.utils.helper import raise_error, get_user_access_token

GENERIC_HEADER = {"Content-type": "application/json"}

BASE_URL = "https://api.ask-jennie.com/"

LOGIN_URL = BASE_URL + "v1/login/"
LOGIN_VIA_GOOGLE_URL = BASE_URL + "v1/continue-with-google/"
LOGIN_VIA_KEY = BASE_URL + "v1/active-sdk/"
AUTOMATION_URL = BASE_URL + "v1/automation/TYPE/"
AUTOMATION_SYNC_URL = BASE_URL + "v1/automation/sync/"
AUTOMATION_VALIDATE_URL = BASE_URL + "v1/automation/TYPE/validate/"
CUSTOM_AUTOMATION_URL = BASE_URL + "v1/custom-automations/TYPE/validate/"
CUSTOM_AUTOMATION_VALIDATE_URL = BASE_URL + "v1/custom-automations/TYPE/validate/"
IMAGE_UPLOAD_URL = BASE_URL + "v1/image_upload/"
TEXT_UPLOAD_URL = BASE_URL + "v1/file_upload/"

class GenericAPICalls():
    """
    Simply library to simplify API Calls using python.
    """

    def __init__(self, logger):
        self.logger = logger
        self.logs = {}

    def log_request(self, type_req, url, headers=None, body=None):
        self.logger.debug(
            "Making {} API call with params".format(type_req), {
                "url": url,
                "headers": headers,
                "body": body
            }
        )

    def log_res(self, resp):
        self.logger.debug("Got response from api",resp)

    def return_response(self, resp):
        try:
            response = resp.json()
        except Exception as e:
            return raise_error("Backend Server not working")

        if response["payload"]:
            self.log_res(response)
            return response["payload"]
        else:
            return raise_error(response["message"])

    def recreate_url(self, url, params):
        split_keyword = "?"
        for key in params:
            url += split_keyword + key + "=" + params[key]
            split_keyword = "&"
        return url

    def get(self, url, headers=None, params=None):
        """
        Make a get api call, if params are present add params to url,
        if headers are present add headers to requests
        :param url: Request URL
        :param headers: Request Headers ( optional )
        :param params: Request Params ( optional )
        :return: API Call JSON Response.
        """

        if params != None:
            url = self.recreate_url(url, params)

        self.log_request(
            "GET", url, headers=headers
        )

        if headers == None:
            headers = {"Content-type": "application/json"}
        response = requests.get(url, headers=headers)
        return self.return_response(response)

    def get_text(self, url, params=None):
        """
        Make a get api call, if params are present add params to url,
        if headers are present add headers to requests
        :param url: Request URL
        :param headers: Request Headers ( optional )
        :param params: Request Params ( optional )
        :return: API Call JSON Response.
        """

        if params != None:
            url = self.recreate_url(url, params)

        response = requests.get(url)
        return response.text

    def post(self, url, headers=None, body=None):
        """
        Make a post api call, if headers are present add headers to requests, if body is present
        :param url: Request URL
        :param headers: Request Headers ( optional )
        :param body: Request Params ( optional )
        :return: API Call JSON Response.
        """
        if headers == None:
            headers = {"Content-type": "application/json"}

        if body == None:
            body = {}

        self.log_request(
            "POST", url, headers=headers, body=body
        )
        response = requests.post(url, headers=headers, json=body)
        return self.return_response(response)

    def put(self, url, headers=None, body=None):
        """
        Make a put api call, if headers are present add headers to requests, if body is present
        :param url: Request URL
        :param headers: Request Headers ( optional )
        :param body: Request Params ( optional )
        :return: API Call JSON Response.
        """
        if headers == None:
            headers = {"Content-type": "application/json"}

        if body == None:
            body = {}

        self.log_request(
            "POST", url, headers=headers, body=body
        )
        response = requests.put(url, headers=headers, json=body)
        return self.return_response(response)

    def delete(self, url, headers=None, body=None):
        """
        Make a delete api call, if headers are present add headers to requests, if body is present
        :param url: Request URL
        :param headers: Request Headers ( optional )
        :param body: Request Params ( optional )
        :return: API Call JSON Response.
        """
        if headers == None:
            headers = {"Content-type": "application/json"}

        if body == None:
            body = {}

        self.log_request(
            "POST", url, headers=headers, body=body
        )
        response = requests.delete(url, headers=headers, json=body)
        return self.return_response(response)

class APICalls():
    def __init__(self, logger):
        self.logger = logger
        self.api_generic_call = GenericAPICalls(self.logger)

    def get_auth_header(self):
        user_info = get_user_access_token()
        return {"token": user_info["token"], "Content-type": "application/json"}

    def login_api_call(self, email, password):
        response = self.api_generic_call.post(url=LOGIN_URL, headers=GENERIC_HEADER, body={
            "email": email, "password": password
        })
        return response

    def login_via_google(self, email, key):
        response = self.api_generic_call.post(url=LOGIN_VIA_GOOGLE_URL, headers=GENERIC_HEADER, body={
            "email": email, "key": key
        })
        return response

    def login_via_key(self, key):
        response = self.api_generic_call.post(url=LOGIN_VIA_KEY, headers=GENERIC_HEADER, body={
            "key": key
        })
        return response

    def download_file(self, filelink):
        return self.api_generic_call.get_text(filelink)

    def download_automation(self, app_name, app_type):
        """
        Download Automation from remote server based on application type.
        :param app_name: Application name
        :param app_type: Application type
        :return: response
        """
        url = AUTOMATION_URL.replace("TYPE", app_type)
        headers = self.get_auth_header()
        response = self.api_generic_call.get(
            url, headers=headers,
            params={"app_name": app_name}
        )
        return response

    def upload_image(self, image_file_path):
        """
        Upload Image File to Server
        :param image_file_path: Local path for image
        :return: Uploaded File path
        """
        files = {'media': open(image_file_path, 'rb')}
        image_res = requests.post(IMAGE_UPLOAD_URL, headers={"token": get_user_access_token()["token"]},
                                  files=files)
        return image_res.json()["payload"]["image_link"]

    def upload_automation(self, type, json_conf, is_update):
        """
        Add Type of automations to ASK SERVER
        :param type: Type of automations
        :param json_conf: automations configration.
        :return: API Call response JSON.
        """
        api_url = AUTOMATION_URL.replace("TYPE", type)
        headers = {"token": get_user_access_token()["token"] }
        if is_update:
            response = self.api_generic_call.put(api_url, headers, body=json_conf)
        else:
            response = self.api_generic_call.post(api_url, headers, body=json_conf)
        return response

    def validate_automation_api_call(self, type, app_name):
        """
        Validate if type of automations already exits on ASK SERVER
        :param type: Type of automations
        :param app_name: Automation name
        :return: True/False
        """
        api_url = AUTOMATION_VALIDATE_URL.replace("TYPE", type)
        headers = self.get_auth_header()
        response = requests.get(api_url + "?app_name={}".format(app_name), headers=headers).json()
        if not response["payload"]:
            return False
        return True


    def upload_text_file(self, text_file_path, app_name, type):
        """
        Upload text file to ASK SERVER
        :param text_file_path: Local path for text file.
        :param app_name: Application name
        :param type: Type of application
        :return: Uploaded File path
        """
        json_content = {
            "file_content": open(text_file_path, 'r').read(),
            "app_name": app_name,
            "filename": text_file_path.split("/")[-1],
            "type": type
        }

        text_res = requests.post(
            TEXT_UPLOAD_URL, headers={"token": get_user_access_token()["token"]},
                                 json=json_content
        )
        print (text_res.text)
        return text_res.json()["payload"]["file_link"]

    def upload_files(self, filepaths, app_name, type):
        """
        Upload text file to ASK SERVER
        :param text_file_path: Local path for text file.
        :param app_name: Application name
        :param type: Type of application
        :return: Uploaded File path
        """
        response = []
        for text_file_path in filepaths:
            json_content = {
                "file_content": open(text_file_path, 'r').read(),
                "app_name": app_name,
                "filename": text_file_path.split("/")[-1],
                "type": type
            }
            text_res = requests.post(TEXT_UPLOAD_URL, headers={"token": get_user_access_token()["token"]},
                                     json=json_content)
            response.append(text_res.json()["payload"]["file_link"])
        return response

    def delete_automation_api_call(self, type, app_name):
        """
        Update.md ASK Jennie automations that is already present on Server.
        :param type: Type of automations
        :param json_conf: automations configration.
        :return:
        """
        api_url = AUTOMATION_URL.replace("TYPE", type)
        headers = {"token": get_user_access_token()["token"] }
        response = self.api_generic_call.delete(api_url, headers, body={"app_name": app_name})
        return response

    def create_django_api(self, api_info):
        CREATE_DJANGO_API_URL = "https://api.ask-jennie.com/v1/automation/django/create_api/"
        headers = {"token": get_user_access_token()["token"]}
        text_res = requests.post(CREATE_DJANGO_API_URL, headers=headers, json=api_info)
        if text_res.status_code == 200:
            return text_res.json()["payload"]

        return None

    def validate_automation_exits(self, api_info):
        return None


