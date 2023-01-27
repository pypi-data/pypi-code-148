import os


class CustomObjectBase(object):
    def __init__(self):
        # 储存所有属性的字典
        self.__custom_properties = {}
        # 储存所有信息的字典
        self.__custom_data = {}

    def add_property_to_custom_properties(self, d1):
        self.__custom_properties = {**self.__custom_properties, **d1}

    def get_custom_properties(self):
        return self.__custom_properties


class CustomObject(CustomObjectBase):
    def __init__(self):
        super().__init__()


class CustomScene(CustomObject):
    def __init__(self, full_path):
        super().__init__()
        if not full_path:
            raise Exception('不能输入空地址')

        self.__scene_name = ''
        self.__full_path = os.path.normpath(full_path)
        self.__scene_type = ''
        self.__size = ''
        self.__scene_details = ''

        self.add_property_to_custom_properties(
            {
                'SceneName': self.__scene_name,
                'FullPath': self.__full_path,
                'SceneType': self.__scene_type,
                'Size': self.__size,
            }
        )

    def is_file_exists(self):
        return os.path.exists(self.__full_path)

    def is_dir(self):
        """
        此路径是否为文件夹
        :return:
        """
        return os.path.isdir(self.__full_path)

    def is_file(self):
        """
        此路径是否是一个文件
        :return:
        """
        return os.path.isfile(self.__full_path)

    def is_maya_file(self):
        """
        如果是Maya类型的文件，则返回后缀名。如果不是，则返回False或这None
        :return:
        """
        if self.is_file():
            _, suffix = os.path.splitext(os.path.basename(self.__full_path))
            if suffix in ['.ma', '.mb']:
                return suffix
        return False

    def get_scene_name(self):
        return os.path.normpath(self.__full_path)


class SceneDetails(CustomObject):
    def __init__(self):
        super().__init__()

        self.__scene_details = {}

    def get_scene_details(self):
        return self.__scene_details
