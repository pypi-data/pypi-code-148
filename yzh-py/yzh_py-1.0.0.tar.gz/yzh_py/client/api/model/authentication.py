from ...base import BaseRequest
 

class BankCardFourAuthVerifyRequest(BaseRequest):
    """
    
    :type card_no: string
    :param card_no: 银行卡号
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type real_name: string
    :param real_name: 姓名
    
    :type mobile: string
    :param mobile: 银行预留手机号
    """
    def __init__(self, card_no=None, id_card=None, real_name=None, mobile=None):
        super().__init__() 
        self.card_no = card_no 
        self.id_card = id_card 
        self.real_name = real_name 
        self.mobile = mobile

    def get_card_no(self):
        """ Get 银行卡号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 银行卡号

        :type card_no: string
        :param card_no: 银行卡号
        """
        self.card_no = card_no

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

    def get_mobile(self):
        """ Get 银行预留手机号

        :return: string, mobile
        """
        return self.mobile

    def set_mobile(self, mobile):
        """ Set 银行预留手机号

        :type mobile: string
        :param mobile: 银行预留手机号
        """
        self.mobile = mobile 

class BankCardFourAuthVerifyResponse(BaseRequest):
    """
    
    :type ref: string
    :param ref: 交易凭证
    """
    def __init__(self, ref=None):
        super().__init__() 
        self.ref = ref

    def get_ref(self):
        """ Get 交易凭证

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 交易凭证

        :type ref: string
        :param ref: 交易凭证
        """
        self.ref = ref 

class BankCardFourAuthConfirmRequest(BaseRequest):
    """
    
    :type card_no: string
    :param card_no: 银行卡号
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type real_name: string
    :param real_name: 姓名
    
    :type mobile: string
    :param mobile: 银行预留手机号
    
    :type captcha: string
    :param captcha: 短信验证码
    
    :type ref: string
    :param ref: 交易凭证
    """
    def __init__(self, card_no=None, id_card=None, real_name=None, mobile=None, captcha=None, ref=None):
        super().__init__() 
        self.card_no = card_no 
        self.id_card = id_card 
        self.real_name = real_name 
        self.mobile = mobile 
        self.captcha = captcha 
        self.ref = ref

    def get_card_no(self):
        """ Get 银行卡号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 银行卡号

        :type card_no: string
        :param card_no: 银行卡号
        """
        self.card_no = card_no

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

    def get_mobile(self):
        """ Get 银行预留手机号

        :return: string, mobile
        """
        return self.mobile

    def set_mobile(self, mobile):
        """ Set 银行预留手机号

        :type mobile: string
        :param mobile: 银行预留手机号
        """
        self.mobile = mobile

    def get_captcha(self):
        """ Get 短信验证码

        :return: string, captcha
        """
        return self.captcha

    def set_captcha(self, captcha):
        """ Set 短信验证码

        :type captcha: string
        :param captcha: 短信验证码
        """
        self.captcha = captcha

    def get_ref(self):
        """ Get 交易凭证

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 交易凭证

        :type ref: string
        :param ref: 交易凭证
        """
        self.ref = ref 

class BankCardFourAuthConfirmResponse(BaseRequest):
    """
    """
    def __init__(self):
        super().__init__() 

class BankCardFourVerifyRequest(BaseRequest):
    """
    
    :type card_no: string
    :param card_no: 银行卡号
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type real_name: string
    :param real_name: 姓名
    
    :type mobile: string
    :param mobile: 银行预留手机号
    """
    def __init__(self, card_no=None, id_card=None, real_name=None, mobile=None):
        super().__init__() 
        self.card_no = card_no 
        self.id_card = id_card 
        self.real_name = real_name 
        self.mobile = mobile

    def get_card_no(self):
        """ Get 银行卡号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 银行卡号

        :type card_no: string
        :param card_no: 银行卡号
        """
        self.card_no = card_no

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

    def get_mobile(self):
        """ Get 银行预留手机号

        :return: string, mobile
        """
        return self.mobile

    def set_mobile(self, mobile):
        """ Set 银行预留手机号

        :type mobile: string
        :param mobile: 银行预留手机号
        """
        self.mobile = mobile 

class BankCardFourVerifyResponse(BaseRequest):
    """
    """
    def __init__(self):
        super().__init__() 

class BankCardThreeVerifyRequest(BaseRequest):
    """
    
    :type card_no: string
    :param card_no: 银行卡号
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type real_name: string
    :param real_name: 姓名
    """
    def __init__(self, card_no=None, id_card=None, real_name=None):
        super().__init__() 
        self.card_no = card_no 
        self.id_card = id_card 
        self.real_name = real_name

    def get_card_no(self):
        """ Get 银行卡号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 银行卡号

        :type card_no: string
        :param card_no: 银行卡号
        """
        self.card_no = card_no

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

class BankCardThreeVerifyResponse(BaseRequest):
    """
    """
    def __init__(self):
        super().__init__() 

class IDCardVerifyRequest(BaseRequest):
    """
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type real_name: string
    :param real_name: 姓名
    """
    def __init__(self, id_card=None, real_name=None):
        super().__init__() 
        self.id_card = id_card 
        self.real_name = real_name

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

class IDCardVerifyResponse(BaseRequest):
    """
    """
    def __init__(self):
        super().__init__() 

class UserExemptedInfoRequest(BaseRequest):
    """
    
    :type card_type: string
    :param card_type: 证件类型码
    
    :type id_card: string
    :param id_card: 证件号码
    
    :type real_name: string
    :param real_name: 姓名
    
    :type comment_apply: string
    :param comment_apply: 申请备注
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type user_images: list
    :param user_images: 人员信息图片
    
    :type country: string
    :param country: 国别（地区）代码
    
    :type birthday: string
    :param birthday: 出生日期
    
    :type gender: string
    :param gender: 性别
    
    :type notify_url: string
    :param notify_url: 回调地址
    
    :type ref: string
    :param ref: 请求流水号
    """
    def __init__(self, card_type=None, id_card=None, real_name=None, comment_apply=None, broker_id=None, dealer_id=None, user_images=None, country=None, birthday=None, gender=None, notify_url=None, ref=None):
        super().__init__() 
        self.card_type = card_type 
        self.id_card = id_card 
        self.real_name = real_name 
        self.comment_apply = comment_apply 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.user_images = user_images 
        self.country = country 
        self.birthday = birthday 
        self.gender = gender 
        self.notify_url = notify_url 
        self.ref = ref

    def get_card_type(self):
        """ Get 证件类型码

        :return: string, card_type
        """
        return self.card_type

    def set_card_type(self, card_type):
        """ Set 证件类型码

        :type card_type: string
        :param card_type: 证件类型码
        """
        self.card_type = card_type

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

    def get_comment_apply(self):
        """ Get 申请备注

        :return: string, comment_apply
        """
        return self.comment_apply

    def set_comment_apply(self, comment_apply):
        """ Set 申请备注

        :type comment_apply: string
        :param comment_apply: 申请备注
        """
        self.comment_apply = comment_apply

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

    def get_user_images(self):
        """ Get 人员信息图片

        :return: list, user_images
        """
        return self.user_images

    def set_user_images(self, user_images):
        """ Set 人员信息图片

        :type user_images: list
        :param user_images: 人员信息图片
        """
        self.user_images = user_images

    def get_country(self):
        """ Get 国别（地区）代码

        :return: string, country
        """
        return self.country

    def set_country(self, country):
        """ Set 国别（地区）代码

        :type country: string
        :param country: 国别（地区）代码
        """
        self.country = country

    def get_birthday(self):
        """ Get 出生日期

        :return: string, birthday
        """
        return self.birthday

    def set_birthday(self, birthday):
        """ Set 出生日期

        :type birthday: string
        :param birthday: 出生日期
        """
        self.birthday = birthday

    def get_gender(self):
        """ Get 性别

        :return: string, gender
        """
        return self.gender

    def set_gender(self, gender):
        """ Set 性别

        :type gender: string
        :param gender: 性别
        """
        self.gender = gender

    def get_notify_url(self):
        """ Get 回调地址

        :return: string, notify_url
        """
        return self.notify_url

    def set_notify_url(self, notify_url):
        """ Set 回调地址

        :type notify_url: string
        :param notify_url: 回调地址
        """
        self.notify_url = notify_url

    def get_ref(self):
        """ Get 请求流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 请求流水号

        :type ref: string
        :param ref: 请求流水号
        """
        self.ref = ref 

class UserExemptedInfoResponse(BaseRequest):
    """
    
    :type ok: string
    :param ok: 是否上传成功
    """
    def __init__(self, ok=None):
        super().__init__() 
        self.ok = ok

    def get_ok(self):
        """ Get 是否上传成功

        :return: string, ok
        """
        return self.ok

    def set_ok(self, ok):
        """ Set 是否上传成功

        :type ok: string
        :param ok: 是否上传成功
        """
        self.ok = ok 

class UserWhiteCheckRequest(BaseRequest):
    """
    
    :type id_card: string
    :param id_card: 证件号码
    
    :type real_name: string
    :param real_name: 姓名
    """
    def __init__(self, id_card=None, real_name=None):
        super().__init__() 
        self.id_card = id_card 
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

class UserWhiteCheckResponse(BaseRequest):
    """
    
    :type ok: bool
    :param ok: 
    """
    def __init__(self, ok=None):
        super().__init__() 
        self.ok = ok

    def get_ok(self):
        """ Get 

        :return: bool, ok
        """
        return self.ok

    def set_ok(self, ok):
        """ Set 

        :type ok: bool
        :param ok: 
        """
        self.ok = ok 

class GetBankCardInfoRequest(BaseRequest):
    """
    
    :type card_no: string
    :param card_no: 银行卡号
    
    :type bank_name: string
    :param bank_name: 银行名称
    """
    def __init__(self, card_no=None, bank_name=None):
        super().__init__() 
        self.card_no = card_no 
        self.bank_name = bank_name

    def get_card_no(self):
        """ Get 银行卡号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 银行卡号

        :type card_no: string
        :param card_no: 银行卡号
        """
        self.card_no = card_no

    def get_bank_name(self):
        """ Get 银行名称

        :return: string, bank_name
        """
        return self.bank_name

    def set_bank_name(self, bank_name):
        """ Set 银行名称

        :type bank_name: string
        :param bank_name: 银行名称
        """
        self.bank_name = bank_name 

class GetBankCardInfoResponse(BaseRequest):
    """
    
    :type bank_code: string
    :param bank_code: 银行代码
    
    :type bank_name: string
    :param bank_name: 银行名称
    
    :type card_type: string
    :param card_type: 卡类型
    
    :type is_support: bool
    :param is_support: 云账户是否支持向该银行支付
    """
    def __init__(self, bank_code=None, bank_name=None, card_type=None, is_support=None):
        super().__init__() 
        self.bank_code = bank_code 
        self.bank_name = bank_name 
        self.card_type = card_type 
        self.is_support = is_support

    def get_bank_code(self):
        """ Get 银行代码

        :return: string, bank_code
        """
        return self.bank_code

    def set_bank_code(self, bank_code):
        """ Set 银行代码

        :type bank_code: string
        :param bank_code: 银行代码
        """
        self.bank_code = bank_code

    def get_bank_name(self):
        """ Get 银行名称

        :return: string, bank_name
        """
        return self.bank_name

    def set_bank_name(self, bank_name):
        """ Set 银行名称

        :type bank_name: string
        :param bank_name: 银行名称
        """
        self.bank_name = bank_name

    def get_card_type(self):
        """ Get 卡类型

        :return: string, card_type
        """
        return self.card_type

    def set_card_type(self, card_type):
        """ Set 卡类型

        :type card_type: string
        :param card_type: 卡类型
        """
        self.card_type = card_type

    def get_is_support(self):
        """ Get 云账户是否支持向该银行支付

        :return: bool, is_support
        """
        return self.is_support

    def set_is_support(self, is_support):
        """ Set 云账户是否支持向该银行支付

        :type is_support: bool
        :param is_support: 云账户是否支持向该银行支付
        """
        self.is_support = is_support