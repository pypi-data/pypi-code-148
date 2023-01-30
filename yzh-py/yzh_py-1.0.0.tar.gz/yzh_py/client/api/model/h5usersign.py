from ...base import BaseRequest
 

class H5UserPresignRequest(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type id_card: string
    :param id_card: 证件号码
    
    :type certificate_type: int
    :param certificate_type: 证件类型 0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证
    """
    def __init__(self, dealer_id=None, broker_id=None, real_name=None, id_card=None, certificate_type=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.real_name = real_name 
        self.id_card = id_card 
        self.certificate_type = certificate_type

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

    def get_certificate_type(self):
        """ Get 证件类型 0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证

        :return: int, certificate_type
        """
        return self.certificate_type

    def set_certificate_type(self, certificate_type):
        """ Set 证件类型 0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证

        :type certificate_type: int
        :param certificate_type: 证件类型 0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证
        """
        self.certificate_type = certificate_type 

class H5UserPresignResponse(BaseRequest):
    """
    
    :type uid: string
    :param uid: 用户 ID（废弃字段）
    
    :type token: string
    :param token: H5 签约 token
    """
    def __init__(self, uid=None, token=None):
        super().__init__() 
        self.uid = uid 
        self.token = token

    def get_uid(self):
        """ Get 用户 ID（废弃字段）

        :return: string, uid
        """
        return self.uid

    def set_uid(self, uid):
        """ Set 用户 ID（废弃字段）

        :type uid: string
        :param uid: 用户 ID（废弃字段）
        """
        self.uid = uid

    def get_token(self):
        """ Get H5 签约 token

        :return: string, token
        """
        return self.token

    def set_token(self, token):
        """ Set H5 签约 token

        :type token: string
        :param token: H5 签约 token
        """
        self.token = token 

class H5UserSignRequest(BaseRequest):
    """
    
    :type token: string
    :param token: H5 签约 token
    
    :type color: string
    :param color: H5 页面主题颜色
    
    :type url: string
    :param url: 回调 URL 地址
    
    :type redirect_url: string
    :param redirect_url: 跳转 URL
    """
    def __init__(self, token=None, color=None, url=None, redirect_url=None):
        super().__init__() 
        self.token = token 
        self.color = color 
        self.url = url 
        self.redirect_url = redirect_url

    def get_token(self):
        """ Get H5 签约 token

        :return: string, token
        """
        return self.token

    def set_token(self, token):
        """ Set H5 签约 token

        :type token: string
        :param token: H5 签约 token
        """
        self.token = token

    def get_color(self):
        """ Get H5 页面主题颜色

        :return: string, color
        """
        return self.color

    def set_color(self, color):
        """ Set H5 页面主题颜色

        :type color: string
        :param color: H5 页面主题颜色
        """
        self.color = color

    def get_url(self):
        """ Get 回调 URL 地址

        :return: string, url
        """
        return self.url

    def set_url(self, url):
        """ Set 回调 URL 地址

        :type url: string
        :param url: 回调 URL 地址
        """
        self.url = url

    def get_redirect_url(self):
        """ Get 跳转 URL

        :return: string, redirect_url
        """
        return self.redirect_url

    def set_redirect_url(self, redirect_url):
        """ Set 跳转 URL

        :type redirect_url: string
        :param redirect_url: 跳转 URL
        """
        self.redirect_url = redirect_url 

class H5UserSignResponse(BaseRequest):
    """
    
    :type url: string
    :param url: H5 签约页面 URL
    """
    def __init__(self, url=None):
        super().__init__() 
        self.url = url

    def get_url(self):
        """ Get H5 签约页面 URL

        :return: string, url
        """
        return self.url

    def set_url(self, url):
        """ Set H5 签约页面 URL

        :type url: string
        :param url: H5 签约页面 URL
        """
        self.url = url 

class GetH5UserSignStatusRequest(BaseRequest):
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

class GetH5UserSignStatusResponse(BaseRequest):
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

class H5UserReleaseRequest(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type id_card: string
    :param id_card: 证件号码
    
    :type certificate_type: int
    :param certificate_type: 证件类型   0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证
    """
    def __init__(self, broker_id=None, dealer_id=None, real_name=None, id_card=None, certificate_type=None):
        super().__init__() 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.real_name = real_name 
        self.id_card = id_card 
        self.certificate_type = certificate_type

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

    def get_certificate_type(self):
        """ Get 证件类型   0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证

        :return: int, certificate_type
        """
        return self.certificate_type

    def set_certificate_type(self, certificate_type):
        """ Set 证件类型   0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证

        :type certificate_type: int
        :param certificate_type: 证件类型   0：身份证 2：港澳居民来往内地通行证 3：护照 5：台湾居民来往大陆通行证
        """
        self.certificate_type = certificate_type 

class H5UserReleaseResponse(BaseRequest):
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