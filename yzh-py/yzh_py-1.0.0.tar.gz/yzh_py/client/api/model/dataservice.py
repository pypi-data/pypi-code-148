from ...base import BaseRequest
 

class GetDailyOrderFileRequest(BaseRequest):
    """
    
    :type order_date: string
    :param order_date: 订单查询日期, 格式：yyyy-MM-dd
    """
    def __init__(self, order_date=None):
        super().__init__() 
        self.order_date = order_date

    def get_order_date(self):
        """ Get 订单查询日期, 格式：yyyy-MM-dd

        :return: string, order_date
        """
        return self.order_date

    def set_order_date(self, order_date):
        """ Set 订单查询日期, 格式：yyyy-MM-dd

        :type order_date: string
        :param order_date: 订单查询日期, 格式：yyyy-MM-dd
        """
        self.order_date = order_date 

class GetDailyOrderFileResponse(BaseRequest):
    """
    
    :type order_download_url: string
    :param order_download_url: 下载地址
    """
    def __init__(self, order_download_url=None):
        super().__init__() 
        self.order_download_url = order_download_url

    def get_order_download_url(self):
        """ Get 下载地址

        :return: string, order_download_url
        """
        return self.order_download_url

    def set_order_download_url(self, order_download_url):
        """ Set 下载地址

        :type order_download_url: string
        :param order_download_url: 下载地址
        """
        self.order_download_url = order_download_url 

class GetDailyBillFileV2Request(BaseRequest):
    """
    
    :type bill_date: string
    :param bill_date: 所需获取的日流水日期，格式：yyyy-MM-dd
    """
    def __init__(self, bill_date=None):
        super().__init__() 
        self.bill_date = bill_date

    def get_bill_date(self):
        """ Get 所需获取的日流水日期，格式：yyyy-MM-dd

        :return: string, bill_date
        """
        return self.bill_date

    def set_bill_date(self, bill_date):
        """ Set 所需获取的日流水日期，格式：yyyy-MM-dd

        :type bill_date: string
        :param bill_date: 所需获取的日流水日期，格式：yyyy-MM-dd
        """
        self.bill_date = bill_date 

class GetDailyBillFileV2Response(BaseRequest):
    """
    
    :type bill_download_url: string
    :param bill_download_url: 下载地址
    """
    def __init__(self, bill_download_url=None):
        super().__init__() 
        self.bill_download_url = bill_download_url

    def get_bill_download_url(self):
        """ Get 下载地址

        :return: string, bill_download_url
        """
        return self.bill_download_url

    def set_bill_download_url(self, bill_download_url):
        """ Set 下载地址

        :type bill_download_url: string
        :param bill_download_url: 下载地址
        """
        self.bill_download_url = bill_download_url 

class ListDealerRechargeRecordV2Request(BaseRequest):
    """
    
    :type begin_at: string
    :param begin_at: 开始时间，格式：yyyy-MM-dd
    
    :type end_at: string
    :param end_at: 结束时间，格式：yyyy-MM-dd
    """
    def __init__(self, begin_at=None, end_at=None):
        super().__init__() 
        self.begin_at = begin_at 
        self.end_at = end_at

    def get_begin_at(self):
        """ Get 开始时间，格式：yyyy-MM-dd

        :return: string, begin_at
        """
        return self.begin_at

    def set_begin_at(self, begin_at):
        """ Set 开始时间，格式：yyyy-MM-dd

        :type begin_at: string
        :param begin_at: 开始时间，格式：yyyy-MM-dd
        """
        self.begin_at = begin_at

    def get_end_at(self):
        """ Get 结束时间，格式：yyyy-MM-dd

        :return: string, end_at
        """
        return self.end_at

    def set_end_at(self, end_at):
        """ Set 结束时间，格式：yyyy-MM-dd

        :type end_at: string
        :param end_at: 结束时间，格式：yyyy-MM-dd
        """
        self.end_at = end_at 

class ListDealerRechargeRecordV2Response(BaseRequest):
    """
    
    :type data: list
    :param data: 预付业务服务费记录
    """
    def __init__(self, data=None):
        super().__init__() 
        self.data = data

    def get_data(self):
        """ Get 预付业务服务费记录

        :return: list, data
        """
        return self.data

    def set_data(self, data):
        """ Set 预付业务服务费记录

        :type data: list
        :param data: 预付业务服务费记录
        """
        self.data = data 

class RechargeRecordInfo(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type recharge_id: string
    :param recharge_id: 预付业务服务费记录 ID
    
    :type amount: string
    :param amount: 预付业务服务费
    
    :type actual_amount: string
    :param actual_amount: 实际到账金额
    
    :type created_at: string
    :param created_at: 创建时间
    
    :type recharge_channel: string
    :param recharge_channel: 资金用途
    
    :type remark: string
    :param remark: 预付业务服务费备注
    
    :type recharge_account_no: string
    :param recharge_account_no: 平台企业付款银行账号
    """
    def __init__(self, dealer_id=None, broker_id=None, recharge_id=None, amount=None, actual_amount=None, created_at=None, recharge_channel=None, remark=None, recharge_account_no=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.recharge_id = recharge_id 
        self.amount = amount 
        self.actual_amount = actual_amount 
        self.created_at = created_at 
        self.recharge_channel = recharge_channel 
        self.remark = remark 
        self.recharge_account_no = recharge_account_no

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

    def get_recharge_id(self):
        """ Get 预付业务服务费记录 ID

        :return: string, recharge_id
        """
        return self.recharge_id

    def set_recharge_id(self, recharge_id):
        """ Set 预付业务服务费记录 ID

        :type recharge_id: string
        :param recharge_id: 预付业务服务费记录 ID
        """
        self.recharge_id = recharge_id

    def get_amount(self):
        """ Get 预付业务服务费

        :return: string, amount
        """
        return self.amount

    def set_amount(self, amount):
        """ Set 预付业务服务费

        :type amount: string
        :param amount: 预付业务服务费
        """
        self.amount = amount

    def get_actual_amount(self):
        """ Get 实际到账金额

        :return: string, actual_amount
        """
        return self.actual_amount

    def set_actual_amount(self, actual_amount):
        """ Set 实际到账金额

        :type actual_amount: string
        :param actual_amount: 实际到账金额
        """
        self.actual_amount = actual_amount

    def get_created_at(self):
        """ Get 创建时间

        :return: string, created_at
        """
        return self.created_at

    def set_created_at(self, created_at):
        """ Set 创建时间

        :type created_at: string
        :param created_at: 创建时间
        """
        self.created_at = created_at

    def get_recharge_channel(self):
        """ Get 资金用途

        :return: string, recharge_channel
        """
        return self.recharge_channel

    def set_recharge_channel(self, recharge_channel):
        """ Set 资金用途

        :type recharge_channel: string
        :param recharge_channel: 资金用途
        """
        self.recharge_channel = recharge_channel

    def get_remark(self):
        """ Get 预付业务服务费备注

        :return: string, remark
        """
        return self.remark

    def set_remark(self, remark):
        """ Set 预付业务服务费备注

        :type remark: string
        :param remark: 预付业务服务费备注
        """
        self.remark = remark

    def get_recharge_account_no(self):
        """ Get 平台企业付款银行账号

        :return: string, recharge_account_no
        """
        return self.recharge_account_no

    def set_recharge_account_no(self, recharge_account_no):
        """ Set 平台企业付款银行账号

        :type recharge_account_no: string
        :param recharge_account_no: 平台企业付款银行账号
        """
        self.recharge_account_no = recharge_account_no 

class ListDailyOrderRequest(BaseRequest):
    """
    
    :type order_date: string
    :param order_date: 订单查询日期, 格式：yyyy-MM-dd格式：yyyy-MM-dd
    
    :type offset: int
    :param offset: 偏移量
    
    :type length: int
    :param length: 长度
    
    :type channel: string
    :param channel: 支付路径名，银行卡（默认）、支付宝、微信
    
    :type data_type: string
    :param data_type: 如果为 encryption，则对返回的 data 进行加密
    """
    def __init__(self, order_date=None, offset=None, length=None, channel=None, data_type=None):
        super().__init__() 
        self.order_date = order_date 
        self.offset = offset 
        self.length = length 
        self.channel = channel 
        self.data_type = data_type

    def get_order_date(self):
        """ Get 订单查询日期, 格式：yyyy-MM-dd格式：yyyy-MM-dd

        :return: string, order_date
        """
        return self.order_date

    def set_order_date(self, order_date):
        """ Set 订单查询日期, 格式：yyyy-MM-dd格式：yyyy-MM-dd

        :type order_date: string
        :param order_date: 订单查询日期, 格式：yyyy-MM-dd格式：yyyy-MM-dd
        """
        self.order_date = order_date

    def get_offset(self):
        """ Get 偏移量

        :return: int, offset
        """
        return self.offset

    def set_offset(self, offset):
        """ Set 偏移量

        :type offset: int
        :param offset: 偏移量
        """
        self.offset = offset

    def get_length(self):
        """ Get 长度

        :return: int, length
        """
        return self.length

    def set_length(self, length):
        """ Set 长度

        :type length: int
        :param length: 长度
        """
        self.length = length

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
        """ Get 如果为 encryption，则对返回的 data 进行加密

        :return: string, data_type
        """
        return self.data_type

    def set_data_type(self, data_type):
        """ Set 如果为 encryption，则对返回的 data 进行加密

        :type data_type: string
        :param data_type: 如果为 encryption，则对返回的 data 进行加密
        """
        self.data_type = data_type 

class ListDailyOrderResponse(BaseRequest):
    """
    
    :type total_num: int
    :param total_num: 总数目
    
    :type list: list
    :param list: 条目信息
    """
    def __init__(self, total_num=None, list=None):
        super().__init__() 
        self.total_num = total_num 
        self.list = list

    def get_total_num(self):
        """ Get 总数目

        :return: int, total_num
        """
        return self.total_num

    def set_total_num(self, total_num):
        """ Set 总数目

        :type total_num: int
        :param total_num: 总数目
        """
        self.total_num = total_num

    def get_list(self):
        """ Get 条目信息

        :return: list, list
        """
        return self.list

    def set_list(self, list):
        """ Set 条目信息

        :type list: list
        :param list: 条目信息
        """
        self.list = list 

class DealerOrderInfo(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type ref: string
    :param ref: 订单流水号
    
    :type batch_id: string
    :param batch_id: 批次ID
    
    :type real_name: string
    :param real_name: 姓名
    
    :type card_no: string
    :param card_no: 收款账号
    
    :type broker_amount: string
    :param broker_amount: 综合服务主体订单金额
    
    :type broker_fee: string
    :param broker_fee: 综合服务主体加成服务费
    
    :type bill: string
    :param bill: 支付路径流水号
    
    :type status: string
    :param status: 订单状态
    
    :type status_detail: string
    :param status_detail: 订单详情
    
    :type status_detail_message: string
    :param status_detail_message: 订单详细状态码描述
    
    :type statement_id: string
    :param statement_id: 短周期授信账单号
    
    :type fee_statement_id: string
    :param fee_statement_id: 服务费账单号
    
    :type bal_statement_id: string
    :param bal_statement_id: 余额账单号
    
    :type channel: string
    :param channel: 支付路径
    
    :type created_at: string
    :param created_at: 创建时间
    
    :type finished_time: string
    :param finished_time: 完成时间
    """
    def __init__(self, broker_id=None, dealer_id=None, order_id=None, ref=None, batch_id=None, real_name=None, card_no=None, broker_amount=None, broker_fee=None, bill=None, status=None, status_detail=None, status_detail_message=None, statement_id=None, fee_statement_id=None, bal_statement_id=None, channel=None, created_at=None, finished_time=None):
        super().__init__() 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.order_id = order_id 
        self.ref = ref 
        self.batch_id = batch_id 
        self.real_name = real_name 
        self.card_no = card_no 
        self.broker_amount = broker_amount 
        self.broker_fee = broker_fee 
        self.bill = bill 
        self.status = status 
        self.status_detail = status_detail 
        self.status_detail_message = status_detail_message 
        self.statement_id = statement_id 
        self.fee_statement_id = fee_statement_id 
        self.bal_statement_id = bal_statement_id 
        self.channel = channel 
        self.created_at = created_at 
        self.finished_time = finished_time

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
        """ Get 订单流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 订单流水号

        :type ref: string
        :param ref: 订单流水号
        """
        self.ref = ref

    def get_batch_id(self):
        """ Get 批次ID

        :return: string, batch_id
        """
        return self.batch_id

    def set_batch_id(self, batch_id):
        """ Set 批次ID

        :type batch_id: string
        :param batch_id: 批次ID
        """
        self.batch_id = batch_id

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

    def get_broker_amount(self):
        """ Get 综合服务主体订单金额

        :return: string, broker_amount
        """
        return self.broker_amount

    def set_broker_amount(self, broker_amount):
        """ Set 综合服务主体订单金额

        :type broker_amount: string
        :param broker_amount: 综合服务主体订单金额
        """
        self.broker_amount = broker_amount

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

    def get_bill(self):
        """ Get 支付路径流水号

        :return: string, bill
        """
        return self.bill

    def set_bill(self, bill):
        """ Set 支付路径流水号

        :type bill: string
        :param bill: 支付路径流水号
        """
        self.bill = bill

    def get_status(self):
        """ Get 订单状态

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 订单状态

        :type status: string
        :param status: 订单状态
        """
        self.status = status

    def get_status_detail(self):
        """ Get 订单详情

        :return: string, status_detail
        """
        return self.status_detail

    def set_status_detail(self, status_detail):
        """ Set 订单详情

        :type status_detail: string
        :param status_detail: 订单详情
        """
        self.status_detail = status_detail

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

    def get_statement_id(self):
        """ Get 短周期授信账单号

        :return: string, statement_id
        """
        return self.statement_id

    def set_statement_id(self, statement_id):
        """ Set 短周期授信账单号

        :type statement_id: string
        :param statement_id: 短周期授信账单号
        """
        self.statement_id = statement_id

    def get_fee_statement_id(self):
        """ Get 服务费账单号

        :return: string, fee_statement_id
        """
        return self.fee_statement_id

    def set_fee_statement_id(self, fee_statement_id):
        """ Set 服务费账单号

        :type fee_statement_id: string
        :param fee_statement_id: 服务费账单号
        """
        self.fee_statement_id = fee_statement_id

    def get_bal_statement_id(self):
        """ Get 余额账单号

        :return: string, bal_statement_id
        """
        return self.bal_statement_id

    def set_bal_statement_id(self, bal_statement_id):
        """ Set 余额账单号

        :type bal_statement_id: string
        :param bal_statement_id: 余额账单号
        """
        self.bal_statement_id = bal_statement_id

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

    def get_created_at(self):
        """ Get 创建时间

        :return: string, created_at
        """
        return self.created_at

    def set_created_at(self, created_at):
        """ Set 创建时间

        :type created_at: string
        :param created_at: 创建时间
        """
        self.created_at = created_at

    def get_finished_time(self):
        """ Get 完成时间

        :return: string, finished_time
        """
        return self.finished_time

    def set_finished_time(self, finished_time):
        """ Set 完成时间

        :type finished_time: string
        :param finished_time: 完成时间
        """
        self.finished_time = finished_time 

class ListDailyBillRequest(BaseRequest):
    """
    
    :type bill_date: string
    :param bill_date: 流水查询日期
    
    :type offset: int
    :param offset: 偏移量
    
    :type length: int
    :param length: 长度
    
    :type data_type: string
    :param data_type: 如果为 encryption，则对返回的 data 进行加密
    """
    def __init__(self, bill_date=None, offset=None, length=None, data_type=None):
        super().__init__() 
        self.bill_date = bill_date 
        self.offset = offset 
        self.length = length 
        self.data_type = data_type

    def get_bill_date(self):
        """ Get 流水查询日期

        :return: string, bill_date
        """
        return self.bill_date

    def set_bill_date(self, bill_date):
        """ Set 流水查询日期

        :type bill_date: string
        :param bill_date: 流水查询日期
        """
        self.bill_date = bill_date

    def get_offset(self):
        """ Get 偏移量

        :return: int, offset
        """
        return self.offset

    def set_offset(self, offset):
        """ Set 偏移量

        :type offset: int
        :param offset: 偏移量
        """
        self.offset = offset

    def get_length(self):
        """ Get 长度

        :return: int, length
        """
        return self.length

    def set_length(self, length):
        """ Set 长度

        :type length: int
        :param length: 长度
        """
        self.length = length

    def get_data_type(self):
        """ Get 如果为 encryption，则对返回的 data 进行加密

        :return: string, data_type
        """
        return self.data_type

    def set_data_type(self, data_type):
        """ Set 如果为 encryption，则对返回的 data 进行加密

        :type data_type: string
        :param data_type: 如果为 encryption，则对返回的 data 进行加密
        """
        self.data_type = data_type 

class ListDailyBillResponse(BaseRequest):
    """
    
    :type total_num: int
    :param total_num: 总条数
    
    :type bills: list
    :param bills: 条目信息
    """
    def __init__(self, total_num=None, bills=None):
        super().__init__() 
        self.total_num = total_num 
        self.bills = bills

    def get_total_num(self):
        """ Get 总条数

        :return: int, total_num
        """
        return self.total_num

    def set_total_num(self, total_num):
        """ Set 总条数

        :type total_num: int
        :param total_num: 总条数
        """
        self.total_num = total_num

    def get_bills(self):
        """ Get 条目信息

        :return: list, bills
        """
        return self.bills

    def set_bills(self, bills):
        """ Set 条目信息

        :type bills: list
        :param bills: 条目信息
        """
        self.bills = bills 

class DealerBillInfo(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type order_id: string
    :param order_id: 平台企业订单号
    
    :type ref: string
    :param ref: 资金流水号
    
    :type broker_product_name: string
    :param broker_product_name: 综合服务主体名称
    
    :type dealer_product_name: string
    :param dealer_product_name: 平台企业名称
    
    :type biz_ref: string
    :param biz_ref: 业务订单流水号
    
    :type acct_type: string
    :param acct_type: 账户类型
    
    :type amount: string
    :param amount: 入账金额
    
    :type balance: string
    :param balance: 账户余额
    
    :type business_category: string
    :param business_category: 业务分类
    
    :type business_type: string
    :param business_type: 业务类型
    
    :type consumption_type: string
    :param consumption_type: 收支类型
    
    :type created_at: string
    :param created_at: 入账时间
    
    :type remark: string
    :param remark: 备注
    """
    def __init__(self, broker_id=None, dealer_id=None, order_id=None, ref=None, broker_product_name=None, dealer_product_name=None, biz_ref=None, acct_type=None, amount=None, balance=None, business_category=None, business_type=None, consumption_type=None, created_at=None, remark=None):
        super().__init__() 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.order_id = order_id 
        self.ref = ref 
        self.broker_product_name = broker_product_name 
        self.dealer_product_name = dealer_product_name 
        self.biz_ref = biz_ref 
        self.acct_type = acct_type 
        self.amount = amount 
        self.balance = balance 
        self.business_category = business_category 
        self.business_type = business_type 
        self.consumption_type = consumption_type 
        self.created_at = created_at 
        self.remark = remark

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
        """ Get 资金流水号

        :return: string, ref
        """
        return self.ref

    def set_ref(self, ref):
        """ Set 资金流水号

        :type ref: string
        :param ref: 资金流水号
        """
        self.ref = ref

    def get_broker_product_name(self):
        """ Get 综合服务主体名称

        :return: string, broker_product_name
        """
        return self.broker_product_name

    def set_broker_product_name(self, broker_product_name):
        """ Set 综合服务主体名称

        :type broker_product_name: string
        :param broker_product_name: 综合服务主体名称
        """
        self.broker_product_name = broker_product_name

    def get_dealer_product_name(self):
        """ Get 平台企业名称

        :return: string, dealer_product_name
        """
        return self.dealer_product_name

    def set_dealer_product_name(self, dealer_product_name):
        """ Set 平台企业名称

        :type dealer_product_name: string
        :param dealer_product_name: 平台企业名称
        """
        self.dealer_product_name = dealer_product_name

    def get_biz_ref(self):
        """ Get 业务订单流水号

        :return: string, biz_ref
        """
        return self.biz_ref

    def set_biz_ref(self, biz_ref):
        """ Set 业务订单流水号

        :type biz_ref: string
        :param biz_ref: 业务订单流水号
        """
        self.biz_ref = biz_ref

    def get_acct_type(self):
        """ Get 账户类型

        :return: string, acct_type
        """
        return self.acct_type

    def set_acct_type(self, acct_type):
        """ Set 账户类型

        :type acct_type: string
        :param acct_type: 账户类型
        """
        self.acct_type = acct_type

    def get_amount(self):
        """ Get 入账金额

        :return: string, amount
        """
        return self.amount

    def set_amount(self, amount):
        """ Set 入账金额

        :type amount: string
        :param amount: 入账金额
        """
        self.amount = amount

    def get_balance(self):
        """ Get 账户余额

        :return: string, balance
        """
        return self.balance

    def set_balance(self, balance):
        """ Set 账户余额

        :type balance: string
        :param balance: 账户余额
        """
        self.balance = balance

    def get_business_category(self):
        """ Get 业务分类

        :return: string, business_category
        """
        return self.business_category

    def set_business_category(self, business_category):
        """ Set 业务分类

        :type business_category: string
        :param business_category: 业务分类
        """
        self.business_category = business_category

    def get_business_type(self):
        """ Get 业务类型

        :return: string, business_type
        """
        return self.business_type

    def set_business_type(self, business_type):
        """ Set 业务类型

        :type business_type: string
        :param business_type: 业务类型
        """
        self.business_type = business_type

    def get_consumption_type(self):
        """ Get 收支类型

        :return: string, consumption_type
        """
        return self.consumption_type

    def set_consumption_type(self, consumption_type):
        """ Set 收支类型

        :type consumption_type: string
        :param consumption_type: 收支类型
        """
        self.consumption_type = consumption_type

    def get_created_at(self):
        """ Get 入账时间

        :return: string, created_at
        """
        return self.created_at

    def set_created_at(self, created_at):
        """ Set 入账时间

        :type created_at: string
        :param created_at: 入账时间
        """
        self.created_at = created_at

    def get_remark(self):
        """ Get 备注

        :return: string, remark
        """
        return self.remark

    def set_remark(self, remark):
        """ Set 备注

        :type remark: string
        :param remark: 备注
        """
        self.remark = remark 

class GetDailyOrderFileV2Request(BaseRequest):
    """
    
    :type order_date: string
    :param order_date: 订单查询日期, 格式：yyyy-MM-dd
    """
    def __init__(self, order_date=None):
        super().__init__() 
        self.order_date = order_date

    def get_order_date(self):
        """ Get 订单查询日期, 格式：yyyy-MM-dd

        :return: string, order_date
        """
        return self.order_date

    def set_order_date(self, order_date):
        """ Set 订单查询日期, 格式：yyyy-MM-dd

        :type order_date: string
        :param order_date: 订单查询日期, 格式：yyyy-MM-dd
        """
        self.order_date = order_date 

class GetDailyOrderFileV2Response(BaseRequest):
    """
    
    :type url: string
    :param url: 下载地址
    """
    def __init__(self, url=None):
        super().__init__() 
        self.url = url

    def get_url(self):
        """ Get 下载地址

        :return: string, url
        """
        return self.url

    def set_url(self, url):
        """ Set 下载地址

        :type url: string
        :param url: 下载地址
        """
        self.url = url 

class ListBalanceDailyStatementRequest(BaseRequest):
    """
    
    :type statement_date: string
    :param statement_date: 账单查询日期 格式：yyyy-MM-dd
    """
    def __init__(self, statement_date=None):
        super().__init__() 
        self.statement_date = statement_date

    def get_statement_date(self):
        """ Get 账单查询日期 格式：yyyy-MM-dd

        :return: string, statement_date
        """
        return self.statement_date

    def set_statement_date(self, statement_date):
        """ Set 账单查询日期 格式：yyyy-MM-dd

        :type statement_date: string
        :param statement_date: 账单查询日期 格式：yyyy-MM-dd
        """
        self.statement_date = statement_date 

class ListBalanceDailyStatementResponse(BaseRequest):
    """
    
    :type list: list
    :param list: 条目信息
    """
    def __init__(self, list=None):
        super().__init__() 
        self.list = list

    def get_list(self):
        """ Get 条目信息

        :return: list, list
        """
        return self.list

    def set_list(self, list):
        """ Set 条目信息

        :type list: list
        :param list: 条目信息
        """
        self.list = list 

class StatementDetail(BaseRequest):
    """
    
    :type statement_id: string
    :param statement_id: 账单 ID
    
    :type statement_date: string
    :param statement_date: 账单日期
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_product_name: string
    :param broker_product_name: 综合服务主体名称
    
    :type dealer_product_name: string
    :param dealer_product_name: 平台企业名称
    
    :type biz_type: string
    :param biz_type: 业务类型
    
    :type total_money: string
    :param total_money: 账单金额
    
    :type amount: string
    :param amount: 订单金额
    
    :type reex_amount: string
    :param reex_amount: 退汇金额
    
    :type fee_amount: string
    :param fee_amount: 加成服务费金额
    
    :type deduct_rebate_fee_amount: string
    :param deduct_rebate_fee_amount: 加成服务费抵扣金额
    
    :type money_adjust: string
    :param money_adjust: 冲补金额
    
    :type status: string
    :param status: 账单状态
    
    :type invoice_status: string
    :param invoice_status: 开票状态
    
    :type project_id: string
    :param project_id: 项目 ID
    
    :type project_name: string
    :param project_name: 项目名称
    """
    def __init__(self, statement_id=None, statement_date=None, broker_id=None, dealer_id=None, broker_product_name=None, dealer_product_name=None, biz_type=None, total_money=None, amount=None, reex_amount=None, fee_amount=None, deduct_rebate_fee_amount=None, money_adjust=None, status=None, invoice_status=None, project_id=None, project_name=None):
        super().__init__() 
        self.statement_id = statement_id 
        self.statement_date = statement_date 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.broker_product_name = broker_product_name 
        self.dealer_product_name = dealer_product_name 
        self.biz_type = biz_type 
        self.total_money = total_money 
        self.amount = amount 
        self.reex_amount = reex_amount 
        self.fee_amount = fee_amount 
        self.deduct_rebate_fee_amount = deduct_rebate_fee_amount 
        self.money_adjust = money_adjust 
        self.status = status 
        self.invoice_status = invoice_status 
        self.project_id = project_id 
        self.project_name = project_name

    def get_statement_id(self):
        """ Get 账单 ID

        :return: string, statement_id
        """
        return self.statement_id

    def set_statement_id(self, statement_id):
        """ Set 账单 ID

        :type statement_id: string
        :param statement_id: 账单 ID
        """
        self.statement_id = statement_id

    def get_statement_date(self):
        """ Get 账单日期

        :return: string, statement_date
        """
        return self.statement_date

    def set_statement_date(self, statement_date):
        """ Set 账单日期

        :type statement_date: string
        :param statement_date: 账单日期
        """
        self.statement_date = statement_date

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

    def get_broker_product_name(self):
        """ Get 综合服务主体名称

        :return: string, broker_product_name
        """
        return self.broker_product_name

    def set_broker_product_name(self, broker_product_name):
        """ Set 综合服务主体名称

        :type broker_product_name: string
        :param broker_product_name: 综合服务主体名称
        """
        self.broker_product_name = broker_product_name

    def get_dealer_product_name(self):
        """ Get 平台企业名称

        :return: string, dealer_product_name
        """
        return self.dealer_product_name

    def set_dealer_product_name(self, dealer_product_name):
        """ Set 平台企业名称

        :type dealer_product_name: string
        :param dealer_product_name: 平台企业名称
        """
        self.dealer_product_name = dealer_product_name

    def get_biz_type(self):
        """ Get 业务类型

        :return: string, biz_type
        """
        return self.biz_type

    def set_biz_type(self, biz_type):
        """ Set 业务类型

        :type biz_type: string
        :param biz_type: 业务类型
        """
        self.biz_type = biz_type

    def get_total_money(self):
        """ Get 账单金额

        :return: string, total_money
        """
        return self.total_money

    def set_total_money(self, total_money):
        """ Set 账单金额

        :type total_money: string
        :param total_money: 账单金额
        """
        self.total_money = total_money

    def get_amount(self):
        """ Get 订单金额

        :return: string, amount
        """
        return self.amount

    def set_amount(self, amount):
        """ Set 订单金额

        :type amount: string
        :param amount: 订单金额
        """
        self.amount = amount

    def get_reex_amount(self):
        """ Get 退汇金额

        :return: string, reex_amount
        """
        return self.reex_amount

    def set_reex_amount(self, reex_amount):
        """ Set 退汇金额

        :type reex_amount: string
        :param reex_amount: 退汇金额
        """
        self.reex_amount = reex_amount

    def get_fee_amount(self):
        """ Get 加成服务费金额

        :return: string, fee_amount
        """
        return self.fee_amount

    def set_fee_amount(self, fee_amount):
        """ Set 加成服务费金额

        :type fee_amount: string
        :param fee_amount: 加成服务费金额
        """
        self.fee_amount = fee_amount

    def get_deduct_rebate_fee_amount(self):
        """ Get 加成服务费抵扣金额

        :return: string, deduct_rebate_fee_amount
        """
        return self.deduct_rebate_fee_amount

    def set_deduct_rebate_fee_amount(self, deduct_rebate_fee_amount):
        """ Set 加成服务费抵扣金额

        :type deduct_rebate_fee_amount: string
        :param deduct_rebate_fee_amount: 加成服务费抵扣金额
        """
        self.deduct_rebate_fee_amount = deduct_rebate_fee_amount

    def get_money_adjust(self):
        """ Get 冲补金额

        :return: string, money_adjust
        """
        return self.money_adjust

    def set_money_adjust(self, money_adjust):
        """ Set 冲补金额

        :type money_adjust: string
        :param money_adjust: 冲补金额
        """
        self.money_adjust = money_adjust

    def get_status(self):
        """ Get 账单状态

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 账单状态

        :type status: string
        :param status: 账单状态
        """
        self.status = status

    def get_invoice_status(self):
        """ Get 开票状态

        :return: string, invoice_status
        """
        return self.invoice_status

    def set_invoice_status(self, invoice_status):
        """ Set 开票状态

        :type invoice_status: string
        :param invoice_status: 开票状态
        """
        self.invoice_status = invoice_status

    def get_project_id(self):
        """ Get 项目 ID

        :return: string, project_id
        """
        return self.project_id

    def set_project_id(self, project_id):
        """ Set 项目 ID

        :type project_id: string
        :param project_id: 项目 ID
        """
        self.project_id = project_id

    def get_project_name(self):
        """ Get 项目名称

        :return: string, project_name
        """
        return self.project_name

    def set_project_name(self, project_name):
        """ Set 项目名称

        :type project_name: string
        :param project_name: 项目名称
        """
        self.project_name = project_name