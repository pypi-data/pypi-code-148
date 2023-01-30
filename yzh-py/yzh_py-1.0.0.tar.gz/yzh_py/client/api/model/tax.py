from ...base import BaseRequest
 

class GetTaxFileRequest(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type ent_id: string
    :param ent_id: 平台企业签约主体
    
    :type year_month: string
    :param year_month: 所属期
    """
    def __init__(self, dealer_id=None, ent_id=None, year_month=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.ent_id = ent_id 
        self.year_month = year_month

    def get_dealer_id(self):
        """ Get 平台企业 ID

        :return: string, dealer_id
        """
        return self.dealer_id

    def set_dealer_id(self, dealer_id):
        """ Set 平台企业 ID

        :type dealer_id: string
        :param dealer_id: 平台企业 ID
        """
        self.dealer_id = dealer_id

    def get_ent_id(self):
        """ Get 平台企业签约主体

        :return: string, ent_id
        """
        return self.ent_id

    def set_ent_id(self, ent_id):
        """ Set 平台企业签约主体

        :type ent_id: string
        :param ent_id: 平台企业签约主体
        """
        self.ent_id = ent_id

    def get_year_month(self):
        """ Get 所属期

        :return: string, year_month
        """
        return self.year_month

    def set_year_month(self, year_month):
        """ Set 所属期

        :type year_month: string
        :param year_month: 所属期
        """
        self.year_month = year_month 

class GetTaxFileResponse(BaseRequest):
    """
    
    :type file_info: list
    :param file_info: 文件详情
    """
    def __init__(self, file_info=None):
        super().__init__() 
        self.file_info = file_info

    def get_file_info(self):
        """ Get 文件详情

        :return: list, file_info
        """
        return self.file_info

    def set_file_info(self, file_info):
        """ Set 文件详情

        :type file_info: list
        :param file_info: 文件详情
        """
        self.file_info = file_info 

class FileInfo(BaseRequest):
    """
    
    :type name: string
    :param name: 文件名称
    
    :type url: string
    :param url: 下载文件临时 URL
    
    :type pwd: string
    :param pwd: 文件解压缩密码
    """
    def __init__(self, name=None, url=None, pwd=None):
        super().__init__() 
        self.name = name 
        self.url = url 
        self.pwd = pwd

    def get_name(self):
        """ Get 文件名称

        :return: string, name
        """
        return self.name

    def set_name(self, name):
        """ Set 文件名称

        :type name: string
        :param name: 文件名称
        """
        self.name = name

    def get_url(self):
        """ Get 下载文件临时 URL

        :return: string, url
        """
        return self.url

    def set_url(self, url):
        """ Set 下载文件临时 URL

        :type url: string
        :param url: 下载文件临时 URL
        """
        self.url = url

    def get_pwd(self):
        """ Get 文件解压缩密码

        :return: string, pwd
        """
        return self.pwd

    def set_pwd(self, pwd):
        """ Set 文件解压缩密码

        :type pwd: string
        :param pwd: 文件解压缩密码
        """
        self.pwd = pwd 

class GetUserCrossRequest(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type year: string
    :param year: 年份
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type ent_id: string
    :param ent_id: 平台企业签约主体
    """
    def __init__(self, dealer_id=None, year=None, id_card=None, ent_id=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.year = year 
        self.id_card = id_card 
        self.ent_id = ent_id

    def get_dealer_id(self):
        """ Get 平台企业 ID

        :return: string, dealer_id
        """
        return self.dealer_id

    def set_dealer_id(self, dealer_id):
        """ Set 平台企业 ID

        :type dealer_id: string
        :param dealer_id: 平台企业 ID
        """
        self.dealer_id = dealer_id

    def get_year(self):
        """ Get 年份

        :return: string, year
        """
        return self.year

    def set_year(self, year):
        """ Set 年份

        :type year: string
        :param year: 年份
        """
        self.year = year

    def get_id_card(self):
        """ Get 身份证号码

        :return: string, id_card
        """
        return self.id_card

    def set_id_card(self, id_card):
        """ Set 身份证号码

        :type id_card: string
        :param id_card: 身份证号码
        """
        self.id_card = id_card

    def get_ent_id(self):
        """ Get 平台企业签约主体

        :return: string, ent_id
        """
        return self.ent_id

    def set_ent_id(self, ent_id):
        """ Set 平台企业签约主体

        :type ent_id: string
        :param ent_id: 平台企业签约主体
        """
        self.ent_id = ent_id 

class GetUserCrossResponse(BaseRequest):
    """
    
    :type is_cross: bool
    :param is_cross: 跨集团标识
    """
    def __init__(self, is_cross=None):
        super().__init__() 
        self.is_cross = is_cross

    def get_is_cross(self):
        """ Get 跨集团标识

        :return: bool, is_cross
        """
        return self.is_cross

    def set_is_cross(self, is_cross):
        """ Set 跨集团标识

        :type is_cross: bool
        :param is_cross: 跨集团标识
        """
        self.is_cross = is_cross