from ...base import BaseRequest
 

class CreateBankpayOrderRequest(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type card_no: string
    :param card_no: 银行卡号
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type phone_no: string
    :param phone_no: 手机号
    
    :type pay: string
    :param pay: 订单金额
    
    :type pay_remark: string
    :param pay_remark: 订单备注
    
    :type notify_url: string
    :param notify_url: 回调地址
    
    :type project_id: string
    :param project_id: 项目标识
    """
    def __init__(self, order_id=None, dealer_id=None, broker_id=None, real_name=None, card_no=None, id_card=None, phone_no=None, pay=None, pay_remark=None, notify_url=None, project_id=None):
        super().__init__() 
        self.order_id = order_id 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.real_name = real_name 
        self.card_no = card_no 
        self.id_card = id_card 
        self.phone_no = phone_no 
        self.pay = pay 
        self.pay_remark = pay_remark 
        self.notify_url = notify_url 
        self.project_id = project_id

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

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

    def get_phone_no(self):
        """ Get 手机号

        :return: string, phone_no
        """
        return self.phone_no

    def set_phone_no(self, phone_no):
        """ Set 手机号

        :type phone_no: string
        :param phone_no: 手机号
        """
        self.phone_no = phone_no

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay

    def get_pay_remark(self):
        """ Get 订单备注

        :return: string, pay_remark
        """
        return self.pay_remark

    def set_pay_remark(self, pay_remark):
        """ Set 订单备注

        :type pay_remark: string
        :param pay_remark: 订单备注
        """
        self.pay_remark = pay_remark

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

    def get_project_id(self):
        """ Get 项目标识

        :return: string, project_id
        """
        return self.project_id

    def set_project_id(self, project_id):
        """ Set 项目标识

        :type project_id: string
        :param project_id: 项目标识
        """
        self.project_id = project_id 

class CreateBankpayOrderResponse(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 
    
    :type ref: string
    :param ref: 综合服务平台流水号
    
    :type pay: string
    :param pay: 订单金额
    """
    def __init__(self, order_id=None, ref=None, pay=None):
        super().__init__() 
        self.order_id = order_id 
        self.ref = ref 
        self.pay = pay

    def get_order_id(self):
        """ Get 

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 

        :type order_id: string
        :param order_id: 
        """
        self.order_id = order_id

    def get_ref(self):
        """ Get 综合服务平台流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号

        :type ref: string
        :param ref: 综合服务平台流水号
        """
        self.ref = ref

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay 

class CreateAlipayOrderRequest(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type card_no: string
    :param card_no: 支付宝账户
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type phone_no: string
    :param phone_no: 手机号
    
    :type pay: string
    :param pay: 订单金额
    
    :type pay_remark: string
    :param pay_remark: 订单备注
    
    :type notify_url: string
    :param notify_url: 回调地址
    
    :type project_id: string
    :param project_id: 项目标识
    
    :type check_name: string
    :param check_name: 校验支付宝账户姓名，固定值：Check
    """
    def __init__(self, order_id=None, dealer_id=None, broker_id=None, real_name=None, card_no=None, id_card=None, phone_no=None, pay=None, pay_remark=None, notify_url=None, project_id=None, check_name=None):
        super().__init__() 
        self.order_id = order_id 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.real_name = real_name 
        self.card_no = card_no 
        self.id_card = id_card 
        self.phone_no = phone_no 
        self.pay = pay 
        self.pay_remark = pay_remark 
        self.notify_url = notify_url 
        self.project_id = project_id 
        self.check_name = check_name

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

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

    def get_card_no(self):
        """ Get 支付宝账户

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 支付宝账户

        :type card_no: string
        :param card_no: 支付宝账户
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

    def get_phone_no(self):
        """ Get 手机号

        :return: string, phone_no
        """
        return self.phone_no

    def set_phone_no(self, phone_no):
        """ Set 手机号

        :type phone_no: string
        :param phone_no: 手机号
        """
        self.phone_no = phone_no

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay

    def get_pay_remark(self):
        """ Get 订单备注

        :return: string, pay_remark
        """
        return self.pay_remark

    def set_pay_remark(self, pay_remark):
        """ Set 订单备注

        :type pay_remark: string
        :param pay_remark: 订单备注
        """
        self.pay_remark = pay_remark

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

    def get_project_id(self):
        """ Get 项目标识

        :return: string, project_id
        """
        return self.project_id

    def set_project_id(self, project_id):
        """ Set 项目标识

        :type project_id: string
        :param project_id: 项目标识
        """
        self.project_id = project_id

    def get_check_name(self):
        """ Get 校验支付宝账户姓名，固定值：Check

        :return: string, check_name
        """
        return self.check_name

    def set_check_name(self, check_name):
        """ Set 校验支付宝账户姓名，固定值：Check

        :type check_name: string
        :param check_name: 校验支付宝账户姓名，固定值：Check
        """
        self.check_name = check_name 

class CreateAlipayOrderResponse(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type ref: string
    :param ref: 综合服务平台流水号
    
    :type pay: string
    :param pay: 订单金额
    """
    def __init__(self, order_id=None, ref=None, pay=None):
        super().__init__() 
        self.order_id = order_id 
        self.ref = ref 
        self.pay = pay

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_ref(self):
        """ Get 综合服务平台流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号

        :type ref: string
        :param ref: 综合服务平台流水号
        """
        self.ref = ref

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay 

class CreateWxpayOrderRequest(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type openid: string
    :param openid: 微信用户 openid
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type phone_no: string
    :param phone_no: 手机号
    
    :type pay: string
    :param pay: 订单金额
    
    :type pay_remark: string
    :param pay_remark: 订单备注
    
    :type notify_url: string
    :param notify_url: 回调地址
    
    :type wx_app_id: string
    :param wx_app_id: 平台企业微信 AppID
    
    :type wxpay_mode: string
    :param wxpay_mode: 微信支付模式，固定值：transfer
    
    :type project_id: string
    :param project_id: 项目标识
    
    :type notes: string
    :param notes: 描述信息，该字段已废弃
    """
    def __init__(self, order_id=None, dealer_id=None, broker_id=None, real_name=None, openid=None, id_card=None, phone_no=None, pay=None, pay_remark=None, notify_url=None, wx_app_id=None, wxpay_mode=None, project_id=None, notes=None):
        super().__init__() 
        self.order_id = order_id 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.real_name = real_name 
        self.openid = openid 
        self.id_card = id_card 
        self.phone_no = phone_no 
        self.pay = pay 
        self.pay_remark = pay_remark 
        self.notify_url = notify_url 
        self.wx_app_id = wx_app_id 
        self.wxpay_mode = wxpay_mode 
        self.project_id = project_id 
        self.notes = notes

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

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

    def get_openid(self):
        """ Get 微信用户 openid

        :return: string, openid
        """
        return self.openid

    def set_openid(self, openid):
        """ Set 微信用户 openid

        :type openid: string
        :param openid: 微信用户 openid
        """
        self.openid = openid

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

    def get_phone_no(self):
        """ Get 手机号

        :return: string, phone_no
        """
        return self.phone_no

    def set_phone_no(self, phone_no):
        """ Set 手机号

        :type phone_no: string
        :param phone_no: 手机号
        """
        self.phone_no = phone_no

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay

    def get_pay_remark(self):
        """ Get 订单备注

        :return: string, pay_remark
        """
        return self.pay_remark

    def set_pay_remark(self, pay_remark):
        """ Set 订单备注

        :type pay_remark: string
        :param pay_remark: 订单备注
        """
        self.pay_remark = pay_remark

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

    def get_wx_app_id(self):
        """ Get 平台企业微信 AppID

        :return: string, wx_app_id
        """
        return self.wx_app_id

    def set_wx_app_id(self, wx_app_id):
        """ Set 平台企业微信 AppID

        :type wx_app_id: string
        :param wx_app_id: 平台企业微信 AppID
        """
        self.wx_app_id = wx_app_id

    def get_wxpay_mode(self):
        """ Get 微信支付模式，固定值：transfer

        :return: string, wxpay_mode
        """
        return self.wxpay_mode

    def set_wxpay_mode(self, wxpay_mode):
        """ Set 微信支付模式，固定值：transfer

        :type wxpay_mode: string
        :param wxpay_mode: 微信支付模式，固定值：transfer
        """
        self.wxpay_mode = wxpay_mode

    def get_project_id(self):
        """ Get 项目标识

        :return: string, project_id
        """
        return self.project_id

    def set_project_id(self, project_id):
        """ Set 项目标识

        :type project_id: string
        :param project_id: 项目标识
        """
        self.project_id = project_id

    def get_notes(self):
        """ Get 描述信息，该字段已废弃

        :return: string, notes
        """
        return self.notes

    def set_notes(self, notes):
        """ Set 描述信息，该字段已废弃

        :type notes: string
        :param notes: 描述信息，该字段已废弃
        """
        self.notes = notes 

class CreateWxpayOrderResponse(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type ref: string
    :param ref: 综合服务平台流水号，唯一
    
    :type pay: string
    :param pay: 订单金额
    """
    def __init__(self, order_id=None, ref=None, pay=None):
        super().__init__() 
        self.order_id = order_id 
        self.ref = ref 
        self.pay = pay

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_ref(self):
        """ Get 综合服务平台流水号，唯一

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号，唯一

        :type ref: string
        :param ref: 综合服务平台流水号，唯一
        """
        self.ref = ref

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay 

class GetOrderRequest(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type channel: string
    :param channel: 支付路径名，银行卡（默认）、支付宝、微信
    
    :type data_type: string
    :param data_type: 数据类型，如果为 encryption，则对返回的 data 进行加密
    """
    def __init__(self, order_id=None, channel=None, data_type=None):
        super().__init__() 
        self.order_id = order_id 
        self.channel = channel 
        self.data_type = data_type

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_channel(self):
        """ Get 支付路径名，银行卡（默认）、支付宝、微信

        :return: string, channel
        """
        return self.channel

    def set_channel(self, channel):
        """ Set 支付路径名，银行卡（默认）、支付宝、微信

        :type channel: string
        :param channel: 支付路径名，银行卡（默认）、支付宝、微信
        """
        self.channel = channel

    def get_data_type(self):
        """ Get 数据类型，如果为 encryption，则对返回的 data 进行加密

        :return: string, data_type
        """
        return self.data_type

    def set_data_type(self, data_type):
        """ Set 数据类型，如果为 encryption，则对返回的 data 进行加密

        :type data_type: string
        :param data_type: 数据类型，如果为 encryption，则对返回的 data 进行加密
        """
        self.data_type = data_type 

class GetOrderResponse(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type pay: string
    :param pay: 订单金额
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type card_no: string
    :param card_no: 收款人账号
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type phone_no: string
    :param phone_no: 手机号
    
    :type status: string
    :param status: 订单状态码
    
    :type status_detail: string
    :param status_detail: 订单详细状态码
    
    :type status_message: string
    :param status_message: 订单状态码描述
    
    :type status_detail_message: string
    :param status_detail_message: 订单详细状态码描述
    
    :type broker_amount: string
    :param broker_amount: 综合服务主体支付金额
    
    :type ref: string
    :param ref: 综合服务平台流水号
    
    :type broker_bank_bill: string
    :param broker_bank_bill: 支付交易流水号
    
    :type withdraw_platform: string
    :param withdraw_platform: 支付路径
    
    :type created_at: string
    :param created_at: 订单接收时间，精确到秒
    
    :type finished_time: string
    :param finished_time: 订单完成时间，精确到秒
    
    :type broker_fee: string
    :param broker_fee: 综合服务主体加成服务费
    
    :type broker_real_fee: string
    :param broker_real_fee: 余额账户支出加成服务费
    
    :type broker_deduct_fee: string
    :param broker_deduct_fee: 抵扣账户支出加成服务费
    
    :type pay_remark: string
    :param pay_remark: 订单备注
    
    :type user_fee: string
    :param user_fee: 用户加成服务费
    
    :type bank_name: string
    :param bank_name: 银行名称
    
    :type project_id: string
    :param project_id: 项目标识
    
    :type anchor_id: string
    :param anchor_id: 新就业形态劳动者 ID，该字段已废弃
    
    :type notes: string
    :param notes: 描述信息，该字段已废弃
    
    :type sys_amount: string
    :param sys_amount: 系统支付金额，该字段已废弃
    
    :type tax: string
    :param tax: 税费，该字段已废弃
    
    :type sys_fee: string
    :param sys_fee: 系统支付费用，该字段已废弃
    """
    def __init__(self, order_id=None, pay=None, broker_id=None, dealer_id=None, real_name=None, card_no=None, id_card=None, phone_no=None, status=None, status_detail=None, status_message=None, status_detail_message=None, broker_amount=None, ref=None, broker_bank_bill=None, withdraw_platform=None, created_at=None, finished_time=None, broker_fee=None, broker_real_fee=None, broker_deduct_fee=None, pay_remark=None, user_fee=None, bank_name=None, project_id=None, anchor_id=None, notes=None, sys_amount=None, tax=None, sys_fee=None):
        super().__init__() 
        self.order_id = order_id 
        self.pay = pay 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.real_name = real_name 
        self.card_no = card_no 
        self.id_card = id_card 
        self.phone_no = phone_no 
        self.status = status 
        self.status_detail = status_detail 
        self.status_message = status_message 
        self.status_detail_message = status_detail_message 
        self.broker_amount = broker_amount 
        self.ref = ref 
        self.broker_bank_bill = broker_bank_bill 
        self.withdraw_platform = withdraw_platform 
        self.created_at = created_at 
        self.finished_time = finished_time 
        self.broker_fee = broker_fee 
        self.broker_real_fee = broker_real_fee 
        self.broker_deduct_fee = broker_deduct_fee 
        self.pay_remark = pay_remark 
        self.user_fee = user_fee 
        self.bank_name = bank_name 
        self.project_id = project_id 
        self.anchor_id = anchor_id 
        self.notes = notes 
        self.sys_amount = sys_amount 
        self.tax = tax 
        self.sys_fee = sys_fee

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay

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

    def get_card_no(self):
        """ Get 收款人账号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 收款人账号

        :type card_no: string
        :param card_no: 收款人账号
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

    def get_phone_no(self):
        """ Get 手机号

        :return: string, phone_no
        """
        return self.phone_no

    def set_phone_no(self, phone_no):
        """ Set 手机号

        :type phone_no: string
        :param phone_no: 手机号
        """
        self.phone_no = phone_no

    def get_status(self):
        """ Get 订单状态码

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 订单状态码

        :type status: string
        :param status: 订单状态码
        """
        self.status = status

    def get_status_detail(self):
        """ Get 订单详细状态码

        :return: string, status_detail
        """
        return self.status_detail

    def set_status_detail(self, status_detail):
        """ Set 订单详细状态码

        :type status_detail: string
        :param status_detail: 订单详细状态码
        """
        self.status_detail = status_detail

    def get_status_message(self):
        """ Get 订单状态码描述

        :return: string, status_message
        """
        return self.status_message

    def set_status_message(self, status_message):
        """ Set 订单状态码描述

        :type status_message: string
        :param status_message: 订单状态码描述
        """
        self.status_message = status_message

    def get_status_detail_message(self):
        """ Get 订单详细状态码描述

        :return: string, status_detail_message
        """
        return self.status_detail_message

    def set_status_detail_message(self, status_detail_message):
        """ Set 订单详细状态码描述

        :type status_detail_message: string
        :param status_detail_message: 订单详细状态码描述
        """
        self.status_detail_message = status_detail_message

    def get_broker_amount(self):
        """ Get 综合服务主体支付金额

        :return: string, broker_amount
        """
        return self.broker_amount

    def set_broker_amount(self, broker_amount):
        """ Set 综合服务主体支付金额

        :type broker_amount: string
        :param broker_amount: 综合服务主体支付金额
        """
        self.broker_amount = broker_amount

    def get_ref(self):
        """ Get 综合服务平台流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号

        :type ref: string
        :param ref: 综合服务平台流水号
        """
        self.ref = ref

    def get_broker_bank_bill(self):
        """ Get 支付交易流水号

        :return: string, broker_bank_bill
        """
        return self.broker_bank_bill

    def set_broker_bank_bill(self, broker_bank_bill):
        """ Set 支付交易流水号

        :type broker_bank_bill: string
        :param broker_bank_bill: 支付交易流水号
        """
        self.broker_bank_bill = broker_bank_bill

    def get_withdraw_platform(self):
        """ Get 支付路径

        :return: string, withdraw_platform
        """
        return self.withdraw_platform

    def set_withdraw_platform(self, withdraw_platform):
        """ Set 支付路径

        :type withdraw_platform: string
        :param withdraw_platform: 支付路径
        """
        self.withdraw_platform = withdraw_platform

    def get_created_at(self):
        """ Get 订单接收时间，精确到秒

        :return: string, created_at
        """
        return self.created_at

    def set_created_at(self, created_at):
        """ Set 订单接收时间，精确到秒

        :type created_at: string
        :param created_at: 订单接收时间，精确到秒
        """
        self.created_at = created_at

    def get_finished_time(self):
        """ Get 订单完成时间，精确到秒

        :return: string, finished_time
        """
        return self.finished_time

    def set_finished_time(self, finished_time):
        """ Set 订单完成时间，精确到秒

        :type finished_time: string
        :param finished_time: 订单完成时间，精确到秒
        """
        self.finished_time = finished_time

    def get_broker_fee(self):
        """ Get 综合服务主体加成服务费

        :return: string, broker_fee
        """
        return self.broker_fee

    def set_broker_fee(self, broker_fee):
        """ Set 综合服务主体加成服务费

        :type broker_fee: string
        :param broker_fee: 综合服务主体加成服务费
        """
        self.broker_fee = broker_fee

    def get_broker_real_fee(self):
        """ Get 余额账户支出加成服务费

        :return: string, broker_real_fee
        """
        return self.broker_real_fee

    def set_broker_real_fee(self, broker_real_fee):
        """ Set 余额账户支出加成服务费

        :type broker_real_fee: string
        :param broker_real_fee: 余额账户支出加成服务费
        """
        self.broker_real_fee = broker_real_fee

    def get_broker_deduct_fee(self):
        """ Get 抵扣账户支出加成服务费

        :return: string, broker_deduct_fee
        """
        return self.broker_deduct_fee

    def set_broker_deduct_fee(self, broker_deduct_fee):
        """ Set 抵扣账户支出加成服务费

        :type broker_deduct_fee: string
        :param broker_deduct_fee: 抵扣账户支出加成服务费
        """
        self.broker_deduct_fee = broker_deduct_fee

    def get_pay_remark(self):
        """ Get 订单备注

        :return: string, pay_remark
        """
        return self.pay_remark

    def set_pay_remark(self, pay_remark):
        """ Set 订单备注

        :type pay_remark: string
        :param pay_remark: 订单备注
        """
        self.pay_remark = pay_remark

    def get_user_fee(self):
        """ Get 用户加成服务费

        :return: string, user_fee
        """
        return self.user_fee

    def set_user_fee(self, user_fee):
        """ Set 用户加成服务费

        :type user_fee: string
        :param user_fee: 用户加成服务费
        """
        self.user_fee = user_fee

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

    def get_project_id(self):
        """ Get 项目标识

        :return: string, project_id
        """
        return self.project_id

    def set_project_id(self, project_id):
        """ Set 项目标识

        :type project_id: string
        :param project_id: 项目标识
        """
        self.project_id = project_id

    def get_anchor_id(self):
        """ Get 新就业形态劳动者 ID，该字段已废弃

        :return: string, anchor_id
        """
        return self.anchor_id

    def set_anchor_id(self, anchor_id):
        """ Set 新就业形态劳动者 ID，该字段已废弃

        :type anchor_id: string
        :param anchor_id: 新就业形态劳动者 ID，该字段已废弃
        """
        self.anchor_id = anchor_id

    def get_notes(self):
        """ Get 描述信息，该字段已废弃

        :return: string, notes
        """
        return self.notes

    def set_notes(self, notes):
        """ Set 描述信息，该字段已废弃

        :type notes: string
        :param notes: 描述信息，该字段已废弃
        """
        self.notes = notes

    def get_sys_amount(self):
        """ Get 系统支付金额，该字段已废弃

        :return: string, sys_amount
        """
        return self.sys_amount

    def set_sys_amount(self, sys_amount):
        """ Set 系统支付金额，该字段已废弃

        :type sys_amount: string
        :param sys_amount: 系统支付金额，该字段已废弃
        """
        self.sys_amount = sys_amount

    def get_tax(self):
        """ Get 税费，该字段已废弃

        :return: string, tax
        """
        return self.tax

    def set_tax(self, tax):
        """ Set 税费，该字段已废弃

        :type tax: string
        :param tax: 税费，该字段已废弃
        """
        self.tax = tax

    def get_sys_fee(self):
        """ Get 系统支付费用，该字段已废弃

        :return: string, sys_fee
        """
        return self.sys_fee

    def set_sys_fee(self, sys_fee):
        """ Set 系统支付费用，该字段已废弃

        :type sys_fee: string
        :param sys_fee: 系统支付费用，该字段已废弃
        """
        self.sys_fee = sys_fee 

class GetDealerVARechargeAccountRequest(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    """
    def __init__(self, broker_id=None, dealer_id=None):
        super().__init__() 
        self.broker_id = broker_id 
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

class GetDealerVARechargeAccountResponse(BaseRequest):
    """
    
    :type acct_name: string
    :param acct_name: 账户名称
    
    :type acct_no: string
    :param acct_no: 专属账户
    
    :type bank_name: string
    :param bank_name: 银行名称
    
    :type dealer_acct_name: string
    :param dealer_acct_name: 付款账户
    """
    def __init__(self, acct_name=None, acct_no=None, bank_name=None, dealer_acct_name=None):
        super().__init__() 
        self.acct_name = acct_name 
        self.acct_no = acct_no 
        self.bank_name = bank_name 
        self.dealer_acct_name = dealer_acct_name

    def get_acct_name(self):
        """ Get 账户名称

        :return: string, acct_name
        """
        return self.acct_name

    def set_acct_name(self, acct_name):
        """ Set 账户名称

        :type acct_name: string
        :param acct_name: 账户名称
        """
        self.acct_name = acct_name

    def get_acct_no(self):
        """ Get 专属账户

        :return: string, acct_no
        """
        return self.acct_no

    def set_acct_no(self, acct_no):
        """ Set 专属账户

        :type acct_no: string
        :param acct_no: 专属账户
        """
        self.acct_no = acct_no

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

    def get_dealer_acct_name(self):
        """ Get 付款账户

        :return: string, dealer_acct_name
        """
        return self.dealer_acct_name

    def set_dealer_acct_name(self, dealer_acct_name):
        """ Set 付款账户

        :type dealer_acct_name: string
        :param dealer_acct_name: 付款账户
        """
        self.dealer_acct_name = dealer_acct_name 

class CancelOrderRequest(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type ref: string
    :param ref: 综合服务平台流水号
    
    :type channel: string
    :param channel: 支付路径名，银行卡（默认）、支付宝、微信
    """
    def __init__(self, dealer_id=None, order_id=None, ref=None, channel=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.order_id = order_id 
        self.ref = ref 
        self.channel = channel

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

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_ref(self):
        """ Get 综合服务平台流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号

        :type ref: string
        :param ref: 综合服务平台流水号
        """
        self.ref = ref

    def get_channel(self):
        """ Get 支付路径名，银行卡（默认）、支付宝、微信

        :return: string, channel
        """
        return self.channel

    def set_channel(self, channel):
        """ Set 支付路径名，银行卡（默认）、支付宝、微信

        :type channel: string
        :param channel: 支付路径名，银行卡（默认）、支付宝、微信
        """
        self.channel = channel 

class CancelOrderResponse(BaseRequest):
    """
    
    :type ok: string
    :param ok: 
    """
    def __init__(self, ok=None):
        super().__init__() 
        self.ok = ok

    def get_ok(self):
        """ Get 

        :return: string, ok
        """
        return self.ok

    def set_ok(self, ok):
        """ Set 

        :type ok: string
        :param ok: 
        """
        self.ok = ok 

class ListAccountRequest(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    """
    def __init__(self, dealer_id=None):
        super().__init__() 
        self.dealer_id = dealer_id

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

class ListAccountResponse(BaseRequest):
    """
    
    :type dealer_infos: list
    :param dealer_infos: 
    """
    def __init__(self, dealer_infos=None):
        super().__init__() 
        self.dealer_infos = dealer_infos

    def get_dealer_infos(self):
        """ Get 

        :return: list, dealer_infos
        """
        return self.dealer_infos

    def set_dealer_infos(self, dealer_infos):
        """ Set 

        :type dealer_infos: list
        :param dealer_infos: 
        """
        self.dealer_infos = dealer_infos 

class AccountInfo(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type bank_card_balance: string
    :param bank_card_balance: 银行卡余额
    
    :type is_bank_card: bool
    :param is_bank_card: 是否开通银行卡支付路径
    
    :type alipay_balance: string
    :param alipay_balance: 支付宝余额
    
    :type is_alipay: bool
    :param is_alipay: 是否开通支付宝支付路径
    
    :type wxpay_balance: string
    :param wxpay_balance: 微信余额
    
    :type is_wxpay: bool
    :param is_wxpay: 是否开通微信支付路径
    
    :type rebate_fee_balance: string
    :param rebate_fee_balance: 加成服务费返点余额
    
    :type acct_balance: string
    :param acct_balance: 业务服务费余额
    
    :type total_balance: string
    :param total_balance: 总余额
    """
    def __init__(self, broker_id=None, bank_card_balance=None, is_bank_card=None, alipay_balance=None, is_alipay=None, wxpay_balance=None, is_wxpay=None, rebate_fee_balance=None, acct_balance=None, total_balance=None):
        super().__init__() 
        self.broker_id = broker_id 
        self.bank_card_balance = bank_card_balance 
        self.is_bank_card = is_bank_card 
        self.alipay_balance = alipay_balance 
        self.is_alipay = is_alipay 
        self.wxpay_balance = wxpay_balance 
        self.is_wxpay = is_wxpay 
        self.rebate_fee_balance = rebate_fee_balance 
        self.acct_balance = acct_balance 
        self.total_balance = total_balance

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

    def get_bank_card_balance(self):
        """ Get 银行卡余额

        :return: string, bank_card_balance
        """
        return self.bank_card_balance

    def set_bank_card_balance(self, bank_card_balance):
        """ Set 银行卡余额

        :type bank_card_balance: string
        :param bank_card_balance: 银行卡余额
        """
        self.bank_card_balance = bank_card_balance

    def get_is_bank_card(self):
        """ Get 是否开通银行卡支付路径

        :return: bool, is_bank_card
        """
        return self.is_bank_card

    def set_is_bank_card(self, is_bank_card):
        """ Set 是否开通银行卡支付路径

        :type is_bank_card: bool
        :param is_bank_card: 是否开通银行卡支付路径
        """
        self.is_bank_card = is_bank_card

    def get_alipay_balance(self):
        """ Get 支付宝余额

        :return: string, alipay_balance
        """
        return self.alipay_balance

    def set_alipay_balance(self, alipay_balance):
        """ Set 支付宝余额

        :type alipay_balance: string
        :param alipay_balance: 支付宝余额
        """
        self.alipay_balance = alipay_balance

    def get_is_alipay(self):
        """ Get 是否开通支付宝支付路径

        :return: bool, is_alipay
        """
        return self.is_alipay

    def set_is_alipay(self, is_alipay):
        """ Set 是否开通支付宝支付路径

        :type is_alipay: bool
        :param is_alipay: 是否开通支付宝支付路径
        """
        self.is_alipay = is_alipay

    def get_wxpay_balance(self):
        """ Get 微信余额

        :return: string, wxpay_balance
        """
        return self.wxpay_balance

    def set_wxpay_balance(self, wxpay_balance):
        """ Set 微信余额

        :type wxpay_balance: string
        :param wxpay_balance: 微信余额
        """
        self.wxpay_balance = wxpay_balance

    def get_is_wxpay(self):
        """ Get 是否开通微信支付路径

        :return: bool, is_wxpay
        """
        return self.is_wxpay

    def set_is_wxpay(self, is_wxpay):
        """ Set 是否开通微信支付路径

        :type is_wxpay: bool
        :param is_wxpay: 是否开通微信支付路径
        """
        self.is_wxpay = is_wxpay

    def get_rebate_fee_balance(self):
        """ Get 加成服务费返点余额

        :return: string, rebate_fee_balance
        """
        return self.rebate_fee_balance

    def set_rebate_fee_balance(self, rebate_fee_balance):
        """ Set 加成服务费返点余额

        :type rebate_fee_balance: string
        :param rebate_fee_balance: 加成服务费返点余额
        """
        self.rebate_fee_balance = rebate_fee_balance

    def get_acct_balance(self):
        """ Get 业务服务费余额

        :return: string, acct_balance
        """
        return self.acct_balance

    def set_acct_balance(self, acct_balance):
        """ Set 业务服务费余额

        :type acct_balance: string
        :param acct_balance: 业务服务费余额
        """
        self.acct_balance = acct_balance

    def get_total_balance(self):
        """ Get 总余额

        :return: string, total_balance
        """
        return self.total_balance

    def set_total_balance(self, total_balance):
        """ Set 总余额

        :type total_balance: string
        :param total_balance: 总余额
        """
        self.total_balance = total_balance 

class GetEleReceiptFileRequest(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type ref: string
    :param ref: 综合服务平台流水号
    """
    def __init__(self, order_id=None, ref=None):
        super().__init__() 
        self.order_id = order_id 
        self.ref = ref

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_ref(self):
        """ Get 综合服务平台流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号

        :type ref: string
        :param ref: 综合服务平台流水号
        """
        self.ref = ref 

class GetEleReceiptFileResponse(BaseRequest):
    """
    
    :type expire_time: string
    :param expire_time: 链接失效时间
    
    :type file_name: string
    :param file_name: 回单名
    
    :type url: string
    :param url: 下载链接
    """
    def __init__(self, expire_time=None, file_name=None, url=None):
        super().__init__() 
        self.expire_time = expire_time 
        self.file_name = file_name 
        self.url = url

    def get_expire_time(self):
        """ Get 链接失效时间

        :return: string, expire_time
        """
        return self.expire_time

    def set_expire_time(self, expire_time):
        """ Set 链接失效时间

        :type expire_time: string
        :param expire_time: 链接失效时间
        """
        self.expire_time = expire_time

    def get_file_name(self):
        """ Get 回单名

        :return: string, file_name
        """
        return self.file_name

    def set_file_name(self, file_name):
        """ Set 回单名

        :type file_name: string
        :param file_name: 回单名
        """
        self.file_name = file_name

    def get_url(self):
        """ Get 下载链接

        :return: string, url
        """
        return self.url

    def set_url(self, url):
        """ Set 下载链接

        :type url: string
        :param url: 下载链接
        """
        self.url = url 

class NotifyOrderRequest(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type pay: string
    :param pay: 订单金额
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type card_no: string
    :param card_no: 收款人账号
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type phone_no: string
    :param phone_no: 手机号
    
    :type status: string
    :param status: 订单状态码
    
    :type status_detail: string
    :param status_detail: 订单详细状态码
    
    :type status_message: string
    :param status_message: 订单状态码描述
    
    :type status_detail_message: string
    :param status_detail_message: 订单详细状态码描述
    
    :type broker_amount: string
    :param broker_amount: 综合服务主体支付金额
    
    :type ref: string
    :param ref: 综合服务平台流水号
    
    :type broker_bank_bill: string
    :param broker_bank_bill: 支付交易流水号
    
    :type withdraw_platform: string
    :param withdraw_platform: 支付路径
    
    :type created_at: string
    :param created_at: 订单接收时间，精确到秒
    
    :type finished_time: string
    :param finished_time: 订单完成时间，精确到秒
    
    :type broker_fee: string
    :param broker_fee: 综合服务主体加成服务费
    
    :type broker_real_fee: string
    :param broker_real_fee: 余额账户支出加成服务费
    
    :type broker_deduct_fee: string
    :param broker_deduct_fee: 抵扣账户支出加成服务费
    
    :type pay_remark: string
    :param pay_remark: 订单备注
    
    :type user_fee: string
    :param user_fee: 用户加成服务费
    
    :type bank_name: string
    :param bank_name: 银行名称
    
    :type project_id: string
    :param project_id: 项目标识
    
    :type anchor_id: string
    :param anchor_id: 新就业形态劳动者 ID，该字段已废弃
    
    :type notes: string
    :param notes: 描述信息，该字段已废弃
    
    :type sys_amount: string
    :param sys_amount: 系统支付金额，该字段已废弃
    
    :type tax: string
    :param tax: 税费，该字段已废弃
    
    :type sys_fee: string
    :param sys_fee: 系统支付费用，该字段已废弃
    """
    def __init__(self, order_id=None, pay=None, broker_id=None, dealer_id=None, real_name=None, card_no=None, id_card=None, phone_no=None, status=None, status_detail=None, status_message=None, status_detail_message=None, broker_amount=None, ref=None, broker_bank_bill=None, withdraw_platform=None, created_at=None, finished_time=None, broker_fee=None, broker_real_fee=None, broker_deduct_fee=None, pay_remark=None, user_fee=None, bank_name=None, project_id=None, anchor_id=None, notes=None, sys_amount=None, tax=None, sys_fee=None):
        super().__init__() 
        self.order_id = order_id 
        self.pay = pay 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.real_name = real_name 
        self.card_no = card_no 
        self.id_card = id_card 
        self.phone_no = phone_no 
        self.status = status 
        self.status_detail = status_detail 
        self.status_message = status_message 
        self.status_detail_message = status_detail_message 
        self.broker_amount = broker_amount 
        self.ref = ref 
        self.broker_bank_bill = broker_bank_bill 
        self.withdraw_platform = withdraw_platform 
        self.created_at = created_at 
        self.finished_time = finished_time 
        self.broker_fee = broker_fee 
        self.broker_real_fee = broker_real_fee 
        self.broker_deduct_fee = broker_deduct_fee 
        self.pay_remark = pay_remark 
        self.user_fee = user_fee 
        self.bank_name = bank_name 
        self.project_id = project_id 
        self.anchor_id = anchor_id 
        self.notes = notes 
        self.sys_amount = sys_amount 
        self.tax = tax 
        self.sys_fee = sys_fee

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay

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

    def get_card_no(self):
        """ Get 收款人账号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 收款人账号

        :type card_no: string
        :param card_no: 收款人账号
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

    def get_phone_no(self):
        """ Get 手机号

        :return: string, phone_no
        """
        return self.phone_no

    def set_phone_no(self, phone_no):
        """ Set 手机号

        :type phone_no: string
        :param phone_no: 手机号
        """
        self.phone_no = phone_no

    def get_status(self):
        """ Get 订单状态码

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 订单状态码

        :type status: string
        :param status: 订单状态码
        """
        self.status = status

    def get_status_detail(self):
        """ Get 订单详细状态码

        :return: string, status_detail
        """
        return self.status_detail

    def set_status_detail(self, status_detail):
        """ Set 订单详细状态码

        :type status_detail: string
        :param status_detail: 订单详细状态码
        """
        self.status_detail = status_detail

    def get_status_message(self):
        """ Get 订单状态码描述

        :return: string, status_message
        """
        return self.status_message

    def set_status_message(self, status_message):
        """ Set 订单状态码描述

        :type status_message: string
        :param status_message: 订单状态码描述
        """
        self.status_message = status_message

    def get_status_detail_message(self):
        """ Get 订单详细状态码描述

        :return: string, status_detail_message
        """
        return self.status_detail_message

    def set_status_detail_message(self, status_detail_message):
        """ Set 订单详细状态码描述

        :type status_detail_message: string
        :param status_detail_message: 订单详细状态码描述
        """
        self.status_detail_message = status_detail_message

    def get_broker_amount(self):
        """ Get 综合服务主体支付金额

        :return: string, broker_amount
        """
        return self.broker_amount

    def set_broker_amount(self, broker_amount):
        """ Set 综合服务主体支付金额

        :type broker_amount: string
        :param broker_amount: 综合服务主体支付金额
        """
        self.broker_amount = broker_amount

    def get_ref(self):
        """ Get 综合服务平台流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号

        :type ref: string
        :param ref: 综合服务平台流水号
        """
        self.ref = ref

    def get_broker_bank_bill(self):
        """ Get 支付交易流水号

        :return: string, broker_bank_bill
        """
        return self.broker_bank_bill

    def set_broker_bank_bill(self, broker_bank_bill):
        """ Set 支付交易流水号

        :type broker_bank_bill: string
        :param broker_bank_bill: 支付交易流水号
        """
        self.broker_bank_bill = broker_bank_bill

    def get_withdraw_platform(self):
        """ Get 支付路径

        :return: string, withdraw_platform
        """
        return self.withdraw_platform

    def set_withdraw_platform(self, withdraw_platform):
        """ Set 支付路径

        :type withdraw_platform: string
        :param withdraw_platform: 支付路径
        """
        self.withdraw_platform = withdraw_platform

    def get_created_at(self):
        """ Get 订单接收时间，精确到秒

        :return: string, created_at
        """
        return self.created_at

    def set_created_at(self, created_at):
        """ Set 订单接收时间，精确到秒

        :type created_at: string
        :param created_at: 订单接收时间，精确到秒
        """
        self.created_at = created_at

    def get_finished_time(self):
        """ Get 订单完成时间，精确到秒

        :return: string, finished_time
        """
        return self.finished_time

    def set_finished_time(self, finished_time):
        """ Set 订单完成时间，精确到秒

        :type finished_time: string
        :param finished_time: 订单完成时间，精确到秒
        """
        self.finished_time = finished_time

    def get_broker_fee(self):
        """ Get 综合服务主体加成服务费

        :return: string, broker_fee
        """
        return self.broker_fee

    def set_broker_fee(self, broker_fee):
        """ Set 综合服务主体加成服务费

        :type broker_fee: string
        :param broker_fee: 综合服务主体加成服务费
        """
        self.broker_fee = broker_fee

    def get_broker_real_fee(self):
        """ Get 余额账户支出加成服务费

        :return: string, broker_real_fee
        """
        return self.broker_real_fee

    def set_broker_real_fee(self, broker_real_fee):
        """ Set 余额账户支出加成服务费

        :type broker_real_fee: string
        :param broker_real_fee: 余额账户支出加成服务费
        """
        self.broker_real_fee = broker_real_fee

    def get_broker_deduct_fee(self):
        """ Get 抵扣账户支出加成服务费

        :return: string, broker_deduct_fee
        """
        return self.broker_deduct_fee

    def set_broker_deduct_fee(self, broker_deduct_fee):
        """ Set 抵扣账户支出加成服务费

        :type broker_deduct_fee: string
        :param broker_deduct_fee: 抵扣账户支出加成服务费
        """
        self.broker_deduct_fee = broker_deduct_fee

    def get_pay_remark(self):
        """ Get 订单备注

        :return: string, pay_remark
        """
        return self.pay_remark

    def set_pay_remark(self, pay_remark):
        """ Set 订单备注

        :type pay_remark: string
        :param pay_remark: 订单备注
        """
        self.pay_remark = pay_remark

    def get_user_fee(self):
        """ Get 用户加成服务费

        :return: string, user_fee
        """
        return self.user_fee

    def set_user_fee(self, user_fee):
        """ Set 用户加成服务费

        :type user_fee: string
        :param user_fee: 用户加成服务费
        """
        self.user_fee = user_fee

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

    def get_project_id(self):
        """ Get 项目标识

        :return: string, project_id
        """
        return self.project_id

    def set_project_id(self, project_id):
        """ Set 项目标识

        :type project_id: string
        :param project_id: 项目标识
        """
        self.project_id = project_id

    def get_anchor_id(self):
        """ Get 新就业形态劳动者 ID，该字段已废弃

        :return: string, anchor_id
        """
        return self.anchor_id

    def set_anchor_id(self, anchor_id):
        """ Set 新就业形态劳动者 ID，该字段已废弃

        :type anchor_id: string
        :param anchor_id: 新就业形态劳动者 ID，该字段已废弃
        """
        self.anchor_id = anchor_id

    def get_notes(self):
        """ Get 描述信息，该字段已废弃

        :return: string, notes
        """
        return self.notes

    def set_notes(self, notes):
        """ Set 描述信息，该字段已废弃

        :type notes: string
        :param notes: 描述信息，该字段已废弃
        """
        self.notes = notes

    def get_sys_amount(self):
        """ Get 系统支付金额，该字段已废弃

        :return: string, sys_amount
        """
        return self.sys_amount

    def set_sys_amount(self, sys_amount):
        """ Set 系统支付金额，该字段已废弃

        :type sys_amount: string
        :param sys_amount: 系统支付金额，该字段已废弃
        """
        self.sys_amount = sys_amount

    def get_tax(self):
        """ Get 税费，该字段已废弃

        :return: string, tax
        """
        return self.tax

    def set_tax(self, tax):
        """ Set 税费，该字段已废弃

        :type tax: string
        :param tax: 税费，该字段已废弃
        """
        self.tax = tax

    def get_sys_fee(self):
        """ Get 系统支付费用，该字段已废弃

        :return: string, sys_fee
        """
        return self.sys_fee

    def set_sys_fee(self, sys_fee):
        """ Set 系统支付费用，该字段已废弃

        :type sys_fee: string
        :param sys_fee: 系统支付费用，该字段已废弃
        """
        self.sys_fee = sys_fee 

class CreateBatchOrderRequest(BaseRequest):
    """
    
    :type batch_id: string
    :param batch_id: 平台企业批次号
    
    :type dealer_id: string
    :param dealer_id: 平台企业ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体ID
    
    :type channel: string
    :param channel: 支付路径
    
    :type wx_app_id: string
    :param wx_app_id: 平台企业的微信AppID
    
    :type total_pay: string
    :param total_pay: 订单总金额
    
    :type total_count: string
    :param total_count: 总笔数
    
    :type order_list: list
    :param order_list: 订单列表
    """
    def __init__(self, batch_id=None, dealer_id=None, broker_id=None, channel=None, wx_app_id=None, total_pay=None, total_count=None, order_list=None):
        super().__init__() 
        self.batch_id = batch_id 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.channel = channel 
        self.wx_app_id = wx_app_id 
        self.total_pay = total_pay 
        self.total_count = total_count 
        self.order_list = order_list

    def get_batch_id(self):
        """ Get 平台企业批次号

        :return: string, batch_id
        """
        return self.batch_id

    def set_batch_id(self, batch_id):
        """ Set 平台企业批次号

        :type batch_id: string
        :param batch_id: 平台企业批次号
        """
        self.batch_id = batch_id

    def get_dealer_id(self):
        """ Get 平台企业ID

        :return: string, dealer_id
        """
        return self.dealer_id

    def set_dealer_id(self, dealer_id):
        """ Set 平台企业ID

        :type dealer_id: string
        :param dealer_id: 平台企业ID
        """
        self.dealer_id = dealer_id

    def get_broker_id(self):
        """ Get 综合服务主体ID

        :return: string, broker_id
        """
        return self.broker_id

    def set_broker_id(self, broker_id):
        """ Set 综合服务主体ID

        :type broker_id: string
        :param broker_id: 综合服务主体ID
        """
        self.broker_id = broker_id

    def get_channel(self):
        """ Get 支付路径

        :return: string, channel
        """
        return self.channel

    def set_channel(self, channel):
        """ Set 支付路径

        :type channel: string
        :param channel: 支付路径
        """
        self.channel = channel

    def get_wx_app_id(self):
        """ Get 平台企业的微信AppID

        :return: string, wx_app_id
        """
        return self.wx_app_id

    def set_wx_app_id(self, wx_app_id):
        """ Set 平台企业的微信AppID

        :type wx_app_id: string
        :param wx_app_id: 平台企业的微信AppID
        """
        self.wx_app_id = wx_app_id

    def get_total_pay(self):
        """ Get 订单总金额

        :return: string, total_pay
        """
        return self.total_pay

    def set_total_pay(self, total_pay):
        """ Set 订单总金额

        :type total_pay: string
        :param total_pay: 订单总金额
        """
        self.total_pay = total_pay

    def get_total_count(self):
        """ Get 总笔数

        :return: string, total_count
        """
        return self.total_count

    def set_total_count(self, total_count):
        """ Set 总笔数

        :type total_count: string
        :param total_count: 总笔数
        """
        self.total_count = total_count

    def get_order_list(self):
        """ Get 订单列表

        :return: list, order_list
        """
        return self.order_list

    def set_order_list(self, order_list):
        """ Set 订单列表

        :type order_list: list
        :param order_list: 订单列表
        """
        self.order_list = order_list 

class BatchOrderInfo(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type real_name: string
    :param real_name: 姓名
    
    :type id_card: string
    :param id_card: 身份证号码
    
    :type card_no: string
    :param card_no: 收款账号
    
    :type openid: string
    :param openid: 微信用户openid
    
    :type phone_no: string
    :param phone_no: 手机号
    
    :type project_id: string
    :param project_id: 项目标识
    
    :type pay: string
    :param pay: 订单金额
    
    :type pay_remark: string
    :param pay_remark: 订单备注
    
    :type notify_url: string
    :param notify_url: 回调地址
    """
    def __init__(self, order_id=None, real_name=None, id_card=None, card_no=None, openid=None, phone_no=None, project_id=None, pay=None, pay_remark=None, notify_url=None):
        super().__init__() 
        self.order_id = order_id 
        self.real_name = real_name 
        self.id_card = id_card 
        self.card_no = card_no 
        self.openid = openid 
        self.phone_no = phone_no 
        self.project_id = project_id 
        self.pay = pay 
        self.pay_remark = pay_remark 
        self.notify_url = notify_url

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

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

    def get_card_no(self):
        """ Get 收款账号

        :return: string, card_no
        """
        return self.card_no

    def set_card_no(self, card_no):
        """ Set 收款账号

        :type card_no: string
        :param card_no: 收款账号
        """
        self.card_no = card_no

    def get_openid(self):
        """ Get 微信用户openid

        :return: string, openid
        """
        return self.openid

    def set_openid(self, openid):
        """ Set 微信用户openid

        :type openid: string
        :param openid: 微信用户openid
        """
        self.openid = openid

    def get_phone_no(self):
        """ Get 手机号

        :return: string, phone_no
        """
        return self.phone_no

    def set_phone_no(self, phone_no):
        """ Set 手机号

        :type phone_no: string
        :param phone_no: 手机号
        """
        self.phone_no = phone_no

    def get_project_id(self):
        """ Get 项目标识

        :return: string, project_id
        """
        return self.project_id

    def set_project_id(self, project_id):
        """ Set 项目标识

        :type project_id: string
        :param project_id: 项目标识
        """
        self.project_id = project_id

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay

    def get_pay_remark(self):
        """ Get 订单备注

        :return: string, pay_remark
        """
        return self.pay_remark

    def set_pay_remark(self, pay_remark):
        """ Set 订单备注

        :type pay_remark: string
        :param pay_remark: 订单备注
        """
        self.pay_remark = pay_remark

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

class CreateBatchOrderResponse(BaseRequest):
    """
    
    :type batch_id: string
    :param batch_id: 平台企业批次号
    
    :type result_list: list
    :param result_list: 订单结果列表
    """
    def __init__(self, batch_id=None, result_list=None):
        super().__init__() 
        self.batch_id = batch_id 
        self.result_list = result_list

    def get_batch_id(self):
        """ Get 平台企业批次号

        :return: string, batch_id
        """
        return self.batch_id

    def set_batch_id(self, batch_id):
        """ Set 平台企业批次号

        :type batch_id: string
        :param batch_id: 平台企业批次号
        """
        self.batch_id = batch_id

    def get_result_list(self):
        """ Get 订单结果列表

        :return: list, result_list
        """
        return self.result_list

    def set_result_list(self, result_list):
        """ Set 订单结果列表

        :type result_list: list
        :param result_list: 订单结果列表
        """
        self.result_list = result_list 

class BatchOrderResult(BaseRequest):
    """
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type ref: string
    :param ref: 综合服务平台流水号
    
    :type pay: string
    :param pay: 订单金额
    """
    def __init__(self, order_id=None, ref=None, pay=None):
        super().__init__() 
        self.order_id = order_id 
        self.ref = ref 
        self.pay = pay

    def get_order_id(self):
        """ Get 平台企业订单号

        :return: string, order_id
        """
        return self.order_id

    def set_order_id(self, order_id):
        """ Set 平台企业订单号

        :type order_id: string
        :param order_id: 平台企业订单号
        """
        self.order_id = order_id

    def get_ref(self):
        """ Get 综合服务平台流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 综合服务平台流水号

        :type ref: string
        :param ref: 综合服务平台流水号
        """
        self.ref = ref

    def get_pay(self):
        """ Get 订单金额

        :return: string, pay
        """
        return self.pay

    def set_pay(self, pay):
        """ Set 订单金额

        :type pay: string
        :param pay: 订单金额
        """
        self.pay = pay 

class ConfirmBatchOrderRequest(BaseRequest):
    """
    
    :type batch_id: string
    :param batch_id: 平台企业批次号
    
    :type dealer_id: string
    :param dealer_id: 平台企业ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体ID
    
    :type channel: string
    :param channel: 支付路径
    """
    def __init__(self, batch_id=None, dealer_id=None, broker_id=None, channel=None):
        super().__init__() 
        self.batch_id = batch_id 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.channel = channel

    def get_batch_id(self):
        """ Get 平台企业批次号

        :return: string, batch_id
        """
        return self.batch_id

    def set_batch_id(self, batch_id):
        """ Set 平台企业批次号

        :type batch_id: string
        :param batch_id: 平台企业批次号
        """
        self.batch_id = batch_id

    def get_dealer_id(self):
        """ Get 平台企业ID

        :return: string, dealer_id
        """
        return self.dealer_id

    def set_dealer_id(self, dealer_id):
        """ Set 平台企业ID

        :type dealer_id: string
        :param dealer_id: 平台企业ID
        """
        self.dealer_id = dealer_id

    def get_broker_id(self):
        """ Get 综合服务主体ID

        :return: string, broker_id
        """
        return self.broker_id

    def set_broker_id(self, broker_id):
        """ Set 综合服务主体ID

        :type broker_id: string
        :param broker_id: 综合服务主体ID
        """
        self.broker_id = broker_id

    def get_channel(self):
        """ Get 支付路径

        :return: string, channel
        """
        return self.channel

    def set_channel(self, channel):
        """ Set 支付路径

        :type channel: string
        :param channel: 支付路径
        """
        self.channel = channel 

class ConfirmBatchOrderResponse(BaseRequest):
    """
    """
    def __init__(self):
        super().__init__()