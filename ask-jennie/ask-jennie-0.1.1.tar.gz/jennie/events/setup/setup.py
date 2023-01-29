import os, json
from jennie.events.colorprinting import ColorPrinting
from jennie.events.utils.apicallhandler import APICalls
from jennie.events.utils.helper import take_user_input, get_user_access_token, TOKEN_PATH

__version__ = "0.1.1"
__latest__ = "0.1.1"
__description__ = 'The package targets protocol for uploading and reusing task and libraries'
__author__ = 'ASK Jennie Developer <dextrop@ask-jennie.com>'

version_info = '''
__version__ = {0}
__latest__ = {1}
__description__ = {2}
__author__ = {3}
__supported_platforms__ = 'Angular, Django, Ubuntu Servers'
'''.format(__version__, __latest__, __description__, __author__)

USER_INPUT_FOR_SETUP = {
    "email": "Kindly enter email address registered with ASK jennie, \nDon't have account go to https://ask-jennie.com/register"
}

print_logs = ColorPrinting()

class Setup():
    def __init__(self, logger):
        self.state = 0
        self.logger = logger
        self.api_call = APICalls(self.logger)

    def show_version(self):
        print_logs.success (version_info)

        user_info = self.get_logged_in_user()
        if (user_info == None):
            print_logs.warning  ("Not logged in, To use the software try login using jennie setup")
            return

        print_logs.success ("User Name : " +  user_info["fullname"])
        print_logs.success ("User Email : " +  user_info["email"])

    def get_logged_in_user(self):
        user_saved_info = None
        try:
            user_saved_info = get_user_access_token()
        except Exception as e:
            return user_saved_info
        return user_saved_info

    def login_to_ask_jennie(self, key):
        response = self.api_call.login_via_key(key=key)
        with open(TOKEN_PATH, 'w') as f:
            json.dump(response, f)

        print_logs.success   ("User Logged In Successfully")
        return True

    def setup(self, key=None):
        token_info = self.get_logged_in_user()
        if (token_info):
            raise ValueError("User already logged in, try logout to re-setup < jennie logout > ")
        else:
            if not key:
                print ("Continue Login, Enter Information")
                key = input ("Input Application KEY \n>> ")
            return self.login_to_ask_jennie (key)

    def logout(self):
        if (self.get_logged_in_user() != None):
            command = "rm -rf {}".format(TOKEN_PATH)
            os.system(command)
            print_logs.success  ("Logged out successfully")
        else:
            print_logs.error  ("User not logged in")
        return True