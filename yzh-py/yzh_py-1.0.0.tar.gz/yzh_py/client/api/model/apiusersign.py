from ...base import BaseRequest
 

class ApiUseSignContractRequest(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    """
    def __init__(self, dealer_id=None, broker_id=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id

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

    def get_broker_id(self):
        """ Get 综合服务主体 ID

        :return: string, broker_id
        """
        return self.broker_id

    def set_broker_id(self, broker_id):
        """ Set 综合服务主体 ID

        :type broker_id: string
        :param broker_id: 综合服务主体 ID
        """
        self.broker_id = broker_id 

class ApiUseSignContractResponse(BaseRequest):
    """
    
    :type url: string
    :param url: 预览跳转 URL
    
    :type title: string
    :param title: 协议名称
    """
    def __init__(self, url=None, title=None):
        super().__init__() 
        self.url = url 
        self.title = title

    def get_url(self):
        """ Get 预览跳转 URL

        :return: string, url
        """
        return self.url

    def set_url(self, url):
        """ Set 预览跳转 URL

        :type url: string
        :param url: 预览跳转 URL
        """
        self.url = url

    def get_title(self):
        """ Get 协议名称

        :return: string, title
        """
        return self.title

    def set_title(self, title):
        """ Set 协议名称

        :type title: string
        :param title: 协议名称
        """
        self.title = title 

class ApiUserSignRequest(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type id_card: string
    :param id_card: 证件号码
    
    :type card_type: string
    :param card_type: 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证
    """
    def __init__(self, broker_id=None, dealer_id=None, real_name=None, id_card=None, card_type=None):
        super().__init__() 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.real_name = real_name 
        self.id_card = id_card 
        self.card_type = card_type

    def get_broker_id(self):
        """ Get 综合服务主体 ID

        :return: string, broker_id
        """
        return self.broker_id

    def set_broker_id(self, broker_id):
        """ Set 综合服务主体 ID

        :type broker_id: string
        :param broker_id: 综合服务主体 ID
        """
        self.broker_id = broker_id

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

    def get_real_name(self):
        """ Get 姓名

        :return: string, real_name
        """
        return self.real_name

    def set_real_name(self, real_name):
        """ Set 姓名

        :type real_name: string
        :param real_name: 姓名
        """
        self.real_name = real_name

    def get_id_card(self):
        """ Get 证件号码

        :return: string, id_card
        """
        return self.id_card

    def set_id_card(self, id_card):
        """ Set 证件号码

        :type id_card: string
        :param id_card: 证件号码
        """
        self.id_card = id_card

    def get_card_type(self):
        """ Get 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证

        :return: string, card_type
        """
        return self.card_type

    def set_card_type(self, card_type):
        """ Set 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证

        :type card_type: string
        :param card_type: 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证
        """
        self.card_type = card_type 

class ApiUserSignResponse(BaseRequest):
    """
    
    :type status: string
    :param status: 是否签约成功
    """
    def __init__(self, status=None):
        super().__init__() 
        self.status = status

    def get_status(self):
        """ Get 是否签约成功

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 是否签约成功

        :type status: string
        :param status: 是否签约成功
        """
        self.status = status 

class GetApiUserSignStatusRequest(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type id_card: string
    :param id_card: 证件号码
    """
    def __init__(self, dealer_id=None, broker_id=None, real_name=None, id_card=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.real_name = real_name 
        self.id_card = id_card

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

    def get_broker_id(self):
        """ Get 综合服务主体 ID

        :return: string, broker_id
        """
        return self.broker_id

    def set_broker_id(self, broker_id):
        """ Set 综合服务主体 ID

        :type broker_id: string
        :param broker_id: 综合服务主体 ID
        """
        self.broker_id = broker_id

    def get_real_name(self):
        """ Get 姓名

        :return: string, real_name
        """
        return self.real_name

    def set_real_name(self, real_name):
        """ Set 姓名

        :type real_name: string
        :param real_name: 姓名
        """
        self.real_name = real_name

    def get_id_card(self):
        """ Get 证件号码

        :return: string, id_card
        """
        return self.id_card

    def set_id_card(self, id_card):
        """ Set 证件号码

        :type id_card: string
        :param id_card: 证件号码
        """
        self.id_card = id_card 

class GetApiUserSignStatusResponse(BaseRequest):
    """
    
    :type signed_at: string
    :param signed_at: 签约时间
    
    :type status: int
    :param status: 用户签约状态
    """
    def __init__(self, signed_at=None, status=None):
        super().__init__() 
        self.signed_at = signed_at 
        self.status = status

    def get_signed_at(self):
        """ Get 签约时间

        :return: string, signed_at
        """
        return self.signed_at

    def set_signed_at(self, signed_at):
        """ Set 签约时间

        :type signed_at: string
        :param signed_at: 签约时间
        """
        self.signed_at = signed_at

    def get_status(self):
        """ Get 用户签约状态

        :return: int, status
        """
        return self.status

    def set_status(self, status):
        """ Set 用户签约状态

        :type status: int
        :param status: 用户签约状态
        """
        self.status = status 

class ApiUserSignReleaseRequest(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type id_card: string
    :param id_card: 证件号码
    
    :type card_type: string
    :param card_type: 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证
    """
    def __init__(self, broker_id=None, dealer_id=None, real_name=None, id_card=None, card_type=None):
        super().__init__() 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.real_name = real_name 
        self.id_card = id_card 
        self.card_type = card_type

    def get_broker_id(self):
        """ Get 综合服务主体 ID

        :return: string, broker_id
        """
        return self.broker_id

    def set_broker_id(self, broker_id):
        """ Set 综合服务主体 ID

        :type broker_id: string
        :param broker_id: 综合服务主体 ID
        """
        self.broker_id = broker_id

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

    def get_real_name(self):
        """ Get 姓名

        :return: string, real_name
        """
        return self.real_name

    def set_real_name(self, real_name):
        """ Set 姓名

        :type real_name: string
        :param real_name: 姓名
        """
        self.real_name = real_name

    def get_id_card(self):
        """ Get 证件号码

        :return: string, id_card
        """
        return self.id_card

    def set_id_card(self, id_card):
        """ Set 证件号码

        :type id_card: string
        :param id_card: 证件号码
        """
        self.id_card = id_card

    def get_card_type(self):
        """ Get 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证

        :return: string, card_type
        """
        return self.card_type

    def set_card_type(self, card_type):
        """ Set 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证

        :type card_type: string
        :param card_type: 证件类型 idcard：身份证 mtphkm：港澳居民来往内地通行证 passport：护照 mtpt：台湾居民往来大陆通行证
        """
        self.card_type = card_type 

class ApiUserSignReleaseResponse(BaseRequest):
    """
    
    :type status: string
    :param status: 是否解约成功
    """
    def __init__(self, status=None):
        super().__init__() 
        self.status = status

    def get_status(self):
        """ Get 是否解约成功

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 是否解约成功

        :type status: string
        :param status: 是否解约成功
        """
        self.status = status