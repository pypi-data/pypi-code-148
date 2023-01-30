from ...base import BaseRequest
 

class GetInvoiceStatRequest(BaseRequest):
    """
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type year: int
    :param year: 查询年份
    """
    def __init__(self, broker_id=None, dealer_id=None, year=None):
        super().__init__() 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.year = year

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

    def get_year(self):
        """ Get 查询年份

        :return: int, year
        """
        return self.year

    def set_year(self, year):
        """ Set 查询年份

        :type year: int
        :param year: 查询年份
        """
        self.year = year 

class GetInvoiceStatResponse(BaseRequest):
    """
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type invoiced: string
    :param invoiced: 已开具发票金额
    
    :type not_invoiced: string
    :param not_invoiced: 待开具发票金额
    """
    def __init__(self, dealer_id=None, broker_id=None, invoiced=None, not_invoiced=None):
        super().__init__() 
        self.dealer_id = dealer_id 
        self.broker_id = broker_id 
        self.invoiced = invoiced 
        self.not_invoiced = not_invoiced

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

    def get_invoiced(self):
        """ Get 已开具发票金额

        :return: string, invoiced
        """
        return self.invoiced

    def set_invoiced(self, invoiced):
        """ Set 已开具发票金额

        :type invoiced: string
        :param invoiced: 已开具发票金额
        """
        self.invoiced = invoiced

    def get_not_invoiced(self):
        """ Get 待开具发票金额

        :return: string, not_invoiced
        """
        return self.not_invoiced

    def set_not_invoiced(self, not_invoiced):
        """ Set 待开具发票金额

        :type not_invoiced: string
        :param not_invoiced: 待开具发票金额
        """
        self.not_invoiced = not_invoiced 

class GetInvoiceAmountRequest(BaseRequest):
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

class GetInvoiceAmountResponse(BaseRequest):
    """
    
    :type amount: string
    :param amount: 可开票额度
    
    :type bank_name_account: list
    :param bank_name_account: 系统支持的开户行及账号
    
    :type goods_services_name: list
    :param goods_services_name: 系统支持的货物或应税劳务、服务名称
    """
    def __init__(self, amount=None, bank_name_account=None, goods_services_name=None):
        super().__init__() 
        self.amount = amount 
        self.bank_name_account = bank_name_account 
        self.goods_services_name = goods_services_name

    def get_amount(self):
        """ Get 可开票额度

        :return: string, amount
        """
        return self.amount

    def set_amount(self, amount):
        """ Set 可开票额度

        :type amount: string
        :param amount: 可开票额度
        """
        self.amount = amount

    def get_bank_name_account(self):
        """ Get 系统支持的开户行及账号

        :return: list, bank_name_account
        """
        return self.bank_name_account

    def set_bank_name_account(self, bank_name_account):
        """ Set 系统支持的开户行及账号

        :type bank_name_account: list
        :param bank_name_account: 系统支持的开户行及账号
        """
        self.bank_name_account = bank_name_account

    def get_goods_services_name(self):
        """ Get 系统支持的货物或应税劳务、服务名称

        :return: list, goods_services_name
        """
        return self.goods_services_name

    def set_goods_services_name(self, goods_services_name):
        """ Set 系统支持的货物或应税劳务、服务名称

        :type goods_services_name: list
        :param goods_services_name: 系统支持的货物或应税劳务、服务名称
        """
        self.goods_services_name = goods_services_name 

class ApplyInvoiceRequest(BaseRequest):
    """
    
    :type invoice_apply_id: string
    :param invoice_apply_id: 发票申请编号
    
    :type broker_id: string
    :param broker_id: 综合服务主体 ID
    
    :type dealer_id: string
    :param dealer_id: 平台企业 ID
    
    :type amount: string
    :param amount: 申请开票金额
    
    :type invoice_type: string
    :param invoice_type: 发票类型
    
    :type bank_name_account: string
    :param bank_name_account: 开户行及账号
    
    :type goods_services_name: string
    :param goods_services_name: 货物或应税劳务、服务名称
    
    :type remark: string
    :param remark: 发票备注
    """
    def __init__(self, invoice_apply_id=None, broker_id=None, dealer_id=None, amount=None, invoice_type=None, bank_name_account=None, goods_services_name=None, remark=None):
        super().__init__() 
        self.invoice_apply_id = invoice_apply_id 
        self.broker_id = broker_id 
        self.dealer_id = dealer_id 
        self.amount = amount 
        self.invoice_type = invoice_type 
        self.bank_name_account = bank_name_account 
        self.goods_services_name = goods_services_name 
        self.remark = remark

    def get_invoice_apply_id(self):
        """ Get 发票申请编号

        :return: string, invoice_apply_id
        """
        return self.invoice_apply_id

    def set_invoice_apply_id(self, invoice_apply_id):
        """ Set 发票申请编号

        :type invoice_apply_id: string
        :param invoice_apply_id: 发票申请编号
        """
        self.invoice_apply_id = invoice_apply_id

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

    def get_amount(self):
        """ Get 申请开票金额

        :return: string, amount
        """
        return self.amount

    def set_amount(self, amount):
        """ Set 申请开票金额

        :type amount: string
        :param amount: 申请开票金额
        """
        self.amount = amount

    def get_invoice_type(self):
        """ Get 发票类型

        :return: string, invoice_type
        """
        return self.invoice_type

    def set_invoice_type(self, invoice_type):
        """ Set 发票类型

        :type invoice_type: string
        :param invoice_type: 发票类型
        """
        self.invoice_type = invoice_type

    def get_bank_name_account(self):
        """ Get 开户行及账号

        :return: string, bank_name_account
        """
        return self.bank_name_account

    def set_bank_name_account(self, bank_name_account):
        """ Set 开户行及账号

        :type bank_name_account: string
        :param bank_name_account: 开户行及账号
        """
        self.bank_name_account = bank_name_account

    def get_goods_services_name(self):
        """ Get 货物或应税劳务、服务名称

        :return: string, goods_services_name
        """
        return self.goods_services_name

    def set_goods_services_name(self, goods_services_name):
        """ Set 货物或应税劳务、服务名称

        :type goods_services_name: string
        :param goods_services_name: 货物或应税劳务、服务名称
        """
        self.goods_services_name = goods_services_name

    def get_remark(self):
        """ Get 发票备注

        :return: string, remark
        """
        return self.remark

    def set_remark(self, remark):
        """ Set 发票备注

        :type remark: string
        :param remark: 发票备注
        """
        self.remark = remark 

class ApplyInvoiceResponse(BaseRequest):
    """
    
    :type application_id: string
    :param application_id: 发票申请单 ID
    
    :type count: int
    :param count: 发票张数
    """
    def __init__(self, application_id=None, count=None):
        super().__init__() 
        self.application_id = application_id 
        self.count = count

    def get_application_id(self):
        """ Get 发票申请单 ID

        :return: string, application_id
        """
        return self.application_id

    def set_application_id(self, application_id):
        """ Set 发票申请单 ID

        :type application_id: string
        :param application_id: 发票申请单 ID
        """
        self.application_id = application_id

    def get_count(self):
        """ Get 发票张数

        :return: int, count
        """
        return self.count

    def set_count(self, count):
        """ Set 发票张数

        :type count: int
        :param count: 发票张数
        """
        self.count = count 

class GetInvoiceStatusRequest(BaseRequest):
    """
    
    :type invoice_apply_id: string
    :param invoice_apply_id: 发票申请编号
    
    :type application_id: string
    :param application_id: 发票申请单 ID
    """
    def __init__(self, invoice_apply_id=None, application_id=None):
        super().__init__() 
        self.invoice_apply_id = invoice_apply_id 
        self.application_id = application_id

    def get_invoice_apply_id(self):
        """ Get 发票申请编号

        :return: string, invoice_apply_id
        """
        return self.invoice_apply_id

    def set_invoice_apply_id(self, invoice_apply_id):
        """ Set 发票申请编号

        :type invoice_apply_id: string
        :param invoice_apply_id: 发票申请编号
        """
        self.invoice_apply_id = invoice_apply_id

    def get_application_id(self):
        """ Get 发票申请单 ID

        :return: string, application_id
        """
        return self.application_id

    def set_application_id(self, application_id):
        """ Set 发票申请单 ID

        :type application_id: string
        :param application_id: 发票申请单 ID
        """
        self.application_id = application_id 

class GetInvoiceStatusResponse(BaseRequest):
    """
    
    :type status: string
    :param status: 申请结果
    
    :type count: int
    :param count: 发票张数
    
    :type price_tax_amount: string
    :param price_tax_amount: 价税合计
    
    :type price_amount: string
    :param price_amount: 不含税金额
    
    :type tax_amount: string
    :param tax_amount: 税额
    
    :type invoice_type: string
    :param invoice_type: 发票类型
    
    :type customer_name: string
    :param customer_name: 购方名称
    
    :type customer_tax_num: string
    :param customer_tax_num: 纳税人识别号
    
    :type customer_address_tel: string
    :param customer_address_tel: 购方地址、电话
    
    :type bank_name_account: string
    :param bank_name_account: 开户行及账号
    
    :type goods_services_name: string
    :param goods_services_name: 货物或应税劳务、服务名称
    
    :type remark: string
    :param remark: 发票备注
    
    :type post_type: string
    :param post_type: 邮寄类型
    
    :type waybill_number: list
    :param waybill_number: 快递单号
    """
    def __init__(self, status=None, count=None, price_tax_amount=None, price_amount=None, tax_amount=None, invoice_type=None, customer_name=None, customer_tax_num=None, customer_address_tel=None, bank_name_account=None, goods_services_name=None, remark=None, post_type=None, waybill_number=None):
        super().__init__() 
        self.status = status 
        self.count = count 
        self.price_tax_amount = price_tax_amount 
        self.price_amount = price_amount 
        self.tax_amount = tax_amount 
        self.invoice_type = invoice_type 
        self.customer_name = customer_name 
        self.customer_tax_num = customer_tax_num 
        self.customer_address_tel = customer_address_tel 
        self.bank_name_account = bank_name_account 
        self.goods_services_name = goods_services_name 
        self.remark = remark 
        self.post_type = post_type 
        self.waybill_number = waybill_number

    def get_status(self):
        """ Get 申请结果

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 申请结果

        :type status: string
        :param status: 申请结果
        """
        self.status = status

    def get_count(self):
        """ Get 发票张数

        :return: int, count
        """
        return self.count

    def set_count(self, count):
        """ Set 发票张数

        :type count: int
        :param count: 发票张数
        """
        self.count = count

    def get_price_tax_amount(self):
        """ Get 价税合计

        :return: string, price_tax_amount
        """
        return self.price_tax_amount

    def set_price_tax_amount(self, price_tax_amount):
        """ Set 价税合计

        :type price_tax_amount: string
        :param price_tax_amount: 价税合计
        """
        self.price_tax_amount = price_tax_amount

    def get_price_amount(self):
        """ Get 不含税金额

        :return: string, price_amount
        """
        return self.price_amount

    def set_price_amount(self, price_amount):
        """ Set 不含税金额

        :type price_amount: string
        :param price_amount: 不含税金额
        """
        self.price_amount = price_amount

    def get_tax_amount(self):
        """ Get 税额

        :return: string, tax_amount
        """
        return self.tax_amount

    def set_tax_amount(self, tax_amount):
        """ Set 税额

        :type tax_amount: string
        :param tax_amount: 税额
        """
        self.tax_amount = tax_amount

    def get_invoice_type(self):
        """ Get 发票类型

        :return: string, invoice_type
        """
        return self.invoice_type

    def set_invoice_type(self, invoice_type):
        """ Set 发票类型

        :type invoice_type: string
        :param invoice_type: 发票类型
        """
        self.invoice_type = invoice_type

    def get_customer_name(self):
        """ Get 购方名称

        :return: string, customer_name
        """
        return self.customer_name

    def set_customer_name(self, customer_name):
        """ Set 购方名称

        :type customer_name: string
        :param customer_name: 购方名称
        """
        self.customer_name = customer_name

    def get_customer_tax_num(self):
        """ Get 纳税人识别号

        :return: string, customer_tax_num
        """
        return self.customer_tax_num

    def set_customer_tax_num(self, customer_tax_num):
        """ Set 纳税人识别号

        :type customer_tax_num: string
        :param customer_tax_num: 纳税人识别号
        """
        self.customer_tax_num = customer_tax_num

    def get_customer_address_tel(self):
        """ Get 购方地址、电话

        :return: string, customer_address_tel
        """
        return self.customer_address_tel

    def set_customer_address_tel(self, customer_address_tel):
        """ Set 购方地址、电话

        :type customer_address_tel: string
        :param customer_address_tel: 购方地址、电话
        """
        self.customer_address_tel = customer_address_tel

    def get_bank_name_account(self):
        """ Get 开户行及账号

        :return: string, bank_name_account
        """
        return self.bank_name_account

    def set_bank_name_account(self, bank_name_account):
        """ Set 开户行及账号

        :type bank_name_account: string
        :param bank_name_account: 开户行及账号
        """
        self.bank_name_account = bank_name_account

    def get_goods_services_name(self):
        """ Get 货物或应税劳务、服务名称

        :return: string, goods_services_name
        """
        return self.goods_services_name

    def set_goods_services_name(self, goods_services_name):
        """ Set 货物或应税劳务、服务名称

        :type goods_services_name: string
        :param goods_services_name: 货物或应税劳务、服务名称
        """
        self.goods_services_name = goods_services_name

    def get_remark(self):
        """ Get 发票备注

        :return: string, remark
        """
        return self.remark

    def set_remark(self, remark):
        """ Set 发票备注

        :type remark: string
        :param remark: 发票备注
        """
        self.remark = remark

    def get_post_type(self):
        """ Get 邮寄类型

        :return: string, post_type
        """
        return self.post_type

    def set_post_type(self, post_type):
        """ Set 邮寄类型

        :type post_type: string
        :param post_type: 邮寄类型
        """
        self.post_type = post_type

    def get_waybill_number(self):
        """ Get 快递单号

        :return: list, waybill_number
        """
        return self.waybill_number

    def set_waybill_number(self, waybill_number):
        """ Set 快递单号

        :type waybill_number: list
        :param waybill_number: 快递单号
        """
        self.waybill_number = waybill_number 

class BankNameAccount(BaseRequest):
    """
    
    :type item: string
    :param item: 开户行及账号
    
    :type default: bool
    :param default: 是否为默认值
    """
    def __init__(self, item=None, default=None):
        super().__init__() 
        self.item = item 
        self.default = default

    def get_item(self):
        """ Get 开户行及账号

        :return: string, item
        """
        return self.item

    def set_item(self, item):
        """ Set 开户行及账号

        :type item: string
        :param item: 开户行及账号
        """
        self.item = item

    def get_default(self):
        """ Get 是否为默认值

        :return: bool, default
        """
        return self.default

    def set_default(self, default):
        """ Set 是否为默认值

        :type default: bool
        :param default: 是否为默认值
        """
        self.default = default 

class GoodsServicesName(BaseRequest):
    """
    
    :type item: string
    :param item: 货物或应税劳务、服务名称
    
    :type default: bool
    :param default: 是否为默认值
    """
    def __init__(self, item=None, default=None):
        super().__init__() 
        self.item = item 
        self.default = default

    def get_item(self):
        """ Get 货物或应税劳务、服务名称

        :return: string, item
        """
        return self.item

    def set_item(self, item):
        """ Set 货物或应税劳务、服务名称

        :type item: string
        :param item: 货物或应税劳务、服务名称
        """
        self.item = item

    def get_default(self):
        """ Get 是否为默认值

        :return: bool, default
        """
        return self.default

    def set_default(self, default):
        """ Set 是否为默认值

        :type default: bool
        :param default: 是否为默认值
        """
        self.default = default 

class GetInvoiceFileRequest(BaseRequest):
    """
    
    :type invoice_apply_id: string
    :param invoice_apply_id: 发票申请编号
    
    :type application_id: string
    :param application_id: 发票申请单 ID
    """
    def __init__(self, invoice_apply_id=None, application_id=None):
        super().__init__() 
        self.invoice_apply_id = invoice_apply_id 
        self.application_id = application_id

    def get_invoice_apply_id(self):
        """ Get 发票申请编号

        :return: string, invoice_apply_id
        """
        return self.invoice_apply_id

    def set_invoice_apply_id(self, invoice_apply_id):
        """ Set 发票申请编号

        :type invoice_apply_id: string
        :param invoice_apply_id: 发票申请编号
        """
        self.invoice_apply_id = invoice_apply_id

    def get_application_id(self):
        """ Get 发票申请单 ID

        :return: string, application_id
        """
        return self.application_id

    def set_application_id(self, application_id):
        """ Set 发票申请单 ID

        :type application_id: string
        :param application_id: 发票申请单 ID
        """
        self.application_id = application_id 

class GetInvoiceFileResponse(BaseRequest):
    """
    
    :type url: string
    :param url: 下载地址
    
    :type name: string
    :param name: 文件名称
    """
    def __init__(self, url=None, name=None):
        super().__init__() 
        self.url = url 
        self.name = name

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

class SendReminderEmailRequest(BaseRequest):
    """
    
    :type invoice_apply_id: string
    :param invoice_apply_id: 发票申请编号
    
    :type application_id: string
    :param application_id: 发票申请单 ID
    """
    def __init__(self, invoice_apply_id=None, application_id=None):
        super().__init__() 
        self.invoice_apply_id = invoice_apply_id 
        self.application_id = application_id

    def get_invoice_apply_id(self):
        """ Get 发票申请编号

        :return: string, invoice_apply_id
        """
        return self.invoice_apply_id

    def set_invoice_apply_id(self, invoice_apply_id):
        """ Set 发票申请编号

        :type invoice_apply_id: string
        :param invoice_apply_id: 发票申请编号
        """
        self.invoice_apply_id = invoice_apply_id

    def get_application_id(self):
        """ Get 发票申请单 ID

        :return: string, application_id
        """
        return self.application_id

    def set_application_id(self, application_id):
        """ Set 发票申请单 ID

        :type application_id: string
        :param application_id: 发票申请单 ID
        """
        self.application_id = application_id 

class SendReminderEmailResponse(BaseRequest):
    """
    """
    def __init__(self):
        super().__init__() 

class NotifyInvoiceDoneRequest(BaseRequest):
    """
    
    :type application_id: string
    :param application_id: 发票申请编号
    
    :type invoice_apply_id: string
    :param invoice_apply_id: 发票申请编号
    
    :type status: string
    :param status: 申请结果
    
    :type count: int
    :param count: 发票张数
    
    :type price_tax_amount: string
    :param price_tax_amount: 价税合计
    
    :type price_amount: string
    :param price_amount: 不含税金额
    
    :type tax_amount: string
    :param tax_amount: 税额
    
    :type invoice_type: string
    :param invoice_type: 发票类型
    
    :type customer_name: string
    :param customer_name: 购方名称
    
    :type customer_tax_num: string
    :param customer_tax_num: 纳税人识别号
    
    :type customer_address_tel: string
    :param customer_address_tel: 购方地址、电话
    
    :type bank_name_account: string
    :param bank_name_account: 开户行及账号
    
    :type goods_services_name: string
    :param goods_services_name: 货物或应税劳务、服务名称
    
    :type remark: string
    :param remark: 发票备注
    
    :type post_type: string
    :param post_type: 邮寄类型
    
    :type waybill_number: list
    :param waybill_number: 快递单号
    
    :type reject_reason: string
    :param reject_reason: 驳回原因
    """
    def __init__(self, application_id=None, invoice_apply_id=None, status=None, count=None, price_tax_amount=None, price_amount=None, tax_amount=None, invoice_type=None, customer_name=None, customer_tax_num=None, customer_address_tel=None, bank_name_account=None, goods_services_name=None, remark=None, post_type=None, waybill_number=None, reject_reason=None):
        super().__init__() 
        self.application_id = application_id 
        self.invoice_apply_id = invoice_apply_id 
        self.status = status 
        self.count = count 
        self.price_tax_amount = price_tax_amount 
        self.price_amount = price_amount 
        self.tax_amount = tax_amount 
        self.invoice_type = invoice_type 
        self.customer_name = customer_name 
        self.customer_tax_num = customer_tax_num 
        self.customer_address_tel = customer_address_tel 
        self.bank_name_account = bank_name_account 
        self.goods_services_name = goods_services_name 
        self.remark = remark 
        self.post_type = post_type 
        self.waybill_number = waybill_number 
        self.reject_reason = reject_reason

    def get_application_id(self):
        """ Get 发票申请编号

        :return: string, application_id
        """
        return self.application_id

    def set_application_id(self, application_id):
        """ Set 发票申请编号

        :type application_id: string
        :param application_id: 发票申请编号
        """
        self.application_id = application_id

    def get_invoice_apply_id(self):
        """ Get 发票申请编号

        :return: string, invoice_apply_id
        """
        return self.invoice_apply_id

    def set_invoice_apply_id(self, invoice_apply_id):
        """ Set 发票申请编号

        :type invoice_apply_id: string
        :param invoice_apply_id: 发票申请编号
        """
        self.invoice_apply_id = invoice_apply_id

    def get_status(self):
        """ Get 申请结果

        :return: string, status
        """
        return self.status

    def set_status(self, status):
        """ Set 申请结果

        :type status: string
        :param status: 申请结果
        """
        self.status = status

    def get_count(self):
        """ Get 发票张数

        :return: int, count
        """
        return self.count

    def set_count(self, count):
        """ Set 发票张数

        :type count: int
        :param count: 发票张数
        """
        self.count = count

    def get_price_tax_amount(self):
        """ Get 价税合计

        :return: string, price_tax_amount
        """
        return self.price_tax_amount

    def set_price_tax_amount(self, price_tax_amount):
        """ Set 价税合计

        :type price_tax_amount: string
        :param price_tax_amount: 价税合计
        """
        self.price_tax_amount = price_tax_amount

    def get_price_amount(self):
        """ Get 不含税金额

        :return: string, price_amount
        """
        return self.price_amount

    def set_price_amount(self, price_amount):
        """ Set 不含税金额

        :type price_amount: string
        :param price_amount: 不含税金额
        """
        self.price_amount = price_amount

    def get_tax_amount(self):
        """ Get 税额

        :return: string, tax_amount
        """
        return self.tax_amount

    def set_tax_amount(self, tax_amount):
        """ Set 税额

        :type tax_amount: string
        :param tax_amount: 税额
        """
        self.tax_amount = tax_amount

    def get_invoice_type(self):
        """ Get 发票类型

        :return: string, invoice_type
        """
        return self.invoice_type

    def set_invoice_type(self, invoice_type):
        """ Set 发票类型

        :type invoice_type: string
        :param invoice_type: 发票类型
        """
        self.invoice_type = invoice_type

    def get_customer_name(self):
        """ Get 购方名称

        :return: string, customer_name
        """
        return self.customer_name

    def set_customer_name(self, customer_name):
        """ Set 购方名称

        :type customer_name: string
        :param customer_name: 购方名称
        """
        self.customer_name = customer_name

    def get_customer_tax_num(self):
        """ Get 纳税人识别号

        :return: string, customer_tax_num
        """
        return self.customer_tax_num

    def set_customer_tax_num(self, customer_tax_num):
        """ Set 纳税人识别号

        :type customer_tax_num: string
        :param customer_tax_num: 纳税人识别号
        """
        self.customer_tax_num = customer_tax_num

    def get_customer_address_tel(self):
        """ Get 购方地址、电话

        :return: string, customer_address_tel
        """
        return self.customer_address_tel

    def set_customer_address_tel(self, customer_address_tel):
        """ Set 购方地址、电话

        :type customer_address_tel: string
        :param customer_address_tel: 购方地址、电话
        """
        self.customer_address_tel = customer_address_tel

    def get_bank_name_account(self):
        """ Get 开户行及账号

        :return: string, bank_name_account
        """
        return self.bank_name_account

    def set_bank_name_account(self, bank_name_account):
        """ Set 开户行及账号

        :type bank_name_account: string
        :param bank_name_account: 开户行及账号
        """
        self.bank_name_account = bank_name_account

    def get_goods_services_name(self):
        """ Get 货物或应税劳务、服务名称

        :return: string, goods_services_name
        """
        return self.goods_services_name

    def set_goods_services_name(self, goods_services_name):
        """ Set 货物或应税劳务、服务名称

        :type goods_services_name: string
        :param goods_services_name: 货物或应税劳务、服务名称
        """
        self.goods_services_name = goods_services_name

    def get_remark(self):
        """ Get 发票备注

        :return: string, remark
        """
        return self.remark

    def set_remark(self, remark):
        """ Set 发票备注

        :type remark: string
        :param remark: 发票备注
        """
        self.remark = remark

    def get_post_type(self):
        """ Get 邮寄类型

        :return: string, post_type
        """
        return self.post_type

    def set_post_type(self, post_type):
        """ Set 邮寄类型

        :type post_type: string
        :param post_type: 邮寄类型
        """
        self.post_type = post_type

    def get_waybill_number(self):
        """ Get 快递单号

        :return: list, waybill_number
        """
        return self.waybill_number

    def set_waybill_number(self, waybill_number):
        """ Set 快递单号

        :type waybill_number: list
        :param waybill_number: 快递单号
        """
        self.waybill_number = waybill_number

    def get_reject_reason(self):
        """ Get 驳回原因

        :return: string, reject_reason
        """
        return self.reject_reason

    def set_reject_reason(self, reject_reason):
        """ Set 驳回原因

        :type reject_reason: string
        :param reject_reason: 驳回原因
        """
        self.reject_reason = reject_reason