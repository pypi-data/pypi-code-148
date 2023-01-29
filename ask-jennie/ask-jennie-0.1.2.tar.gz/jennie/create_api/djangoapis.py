from jennie.constants import *
from jennie.events.utils.apicallhandler import APICalls

def create_python_package(path):
    """
    Create Python package ( Folder with test.py file )
    :param path: python package path
    :return: True
    """
    os.system("mkdir {}".format(path))
    os.system("touch {}/test.py".format(path))
    return True

def path_does_not_exits(path):
    """
    Check if valid django-automations application
    :param path:
    :return:
    """
    print("'{}' is not a valid django-automations application folder, please specify application folder"
          "\n if you wish to proceed with the folder just press enter".format(path))
    new_path = input(">> ")
    if new_path == "":
        create_python_package(path)
        create_python_package(path + "/models")
        return check_django_app_folder(path)
    else:
        return check_django_app_folder(new_path)

def check_django_app_folder(path="src"):
    """
    @TODO merge this function with above function.
    :param path:
    :return:
    """
    if not os.path.exists(path):
        return path_does_not_exits(path)
    else:
        if os.path.exists(path + "/models"):
            return path
        else:
            return path_does_not_exits(path)

"""
Below class is used to create normal Django API's
To do so

# create object of class
django_controller = DjangoBackendAPIs()

# create normal api
django_controller.create_normal_api()
"""
class DjangoBackendAPIs():
    def __init__(self, logger, api_call_obj):
        self.logger = logger
        self.api_call = api_call_obj

    def write_api_files(self, file_link, outdir, app_name):
        if not os.path.exists(outdir):
            create_python_package(outdir)
        _file = outdir + "/" + file_link.split("/")[-1]
        _content = self.api_call.download_file(file_link).replace("src", app_name)
        open(_file, "w").write(_content)
        return True

    @property
    def create_api(self):
        name = input("Enter table name >> ")
        columns = input("Enter table columns separated with ( , )\n").replace(", ", ",").replace(" ,", "").split(",")
        api_info = {
            "table_name": name,
            "columns": columns
        }

        return False
    @property
    def create_normal_api(self):
        """
        Create API for normal use case
        :return: True
        """
        name = input("Enter table name >> ")
        columns = input("Enter table columns separated with ( , )\n").replace(", ", ",").replace(" ,", "").split(",")
        api_info = {
            "table_name": name,
            "columns": columns
        }
        response = self.api_call.create_django_api(api_info)

        application_folder = check_django_app_folder()

        controller_dir = application_folder + "/controllers"
        model_dir = application_folder + "/models"
        views_dir = application_folder + "/views"
        serializers_dir = application_folder + "/serializers"
        lib_dir = application_folder + "/libs"

        self.write_api_files(response["controller_file_link"], controller_dir, application_folder)
        self.write_api_files(response["model_file_link"], model_dir, application_folder)
        self.write_api_files(response["view_file_link"], views_dir, application_folder)
        self.write_api_files(response["serializer_file_link"], serializers_dir, application_folder)
        self.write_api_files(response["custom_resp"], lib_dir, application_folder)
        return True
