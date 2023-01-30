from .model.invoice import *
from ..base import *
from ...utils import *


class InvoiceClient(BaseClient):
    def __init__(self, config):
        super().__init__(config)
    

    def get_invoice_stat(self, request: GetInvoiceStatRequest):
        """ 查询平台企业已开具和待开具发票金额
   
        :type request: GetInvoiceStatRequest
        :param request: the GetInvoiceStatRequest request parameters class.
    
        :return: GetInvoiceStatResponse
        """
        return self._get("/api/payment/v1/invoice-stat", request.request_id, Utils.copy_dict(request.__dict__))

    def get_invoice_amount(self, request: GetInvoiceAmountRequest):
        """ 查询可开票额度和开票信息
   
        :type request: GetInvoiceAmountRequest
        :param request: the GetInvoiceAmountRequest request parameters class.
    
        :return: GetInvoiceAmountResponse
        """
        return self._post("/api/invoice/v2/invoice-amount", request.request_id, Utils.copy_dict(request.__dict__))

    def apply_invoice(self, request: ApplyInvoiceRequest):
        """ 开票申请
   
        :type request: ApplyInvoiceRequest
        :param request: the ApplyInvoiceRequest request parameters class.
    
        :return: ApplyInvoiceResponse
        """
        return self._post("/api/invoice/v2/apply", request.request_id, Utils.copy_dict(request.__dict__))

    def get_invoice_status(self, request: GetInvoiceStatusRequest):
        """ 查询开票申请状态
   
        :type request: GetInvoiceStatusRequest
        :param request: the GetInvoiceStatusRequest request parameters class.
    
        :return: GetInvoiceStatusResponse
        """
        return self._post("/api/invoice/v2/invoice/invoice-status", request.request_id, Utils.copy_dict(request.__dict__))

    def get_invoice_file(self, request: GetInvoiceFileRequest):
        """ 下载 PDF 版发票
   
        :type request: GetInvoiceFileRequest
        :param request: the GetInvoiceFileRequest request parameters class.
    
        :return: GetInvoiceFileResponse
        """
        return self._post("/api/invoice/v2/invoice/invoice-pdf", request.request_id, Utils.copy_dict(request.__dict__))

    def send_reminder_email(self, request: SendReminderEmailRequest):
        """ 发送发票扫描件压缩包下载链接邮件
   
        :type request: SendReminderEmailRequest
        :param request: the SendReminderEmailRequest request parameters class.
    
        :return: SendReminderEmailResponse
        """
        return self._post("/api/invoice/v2/invoice/reminder/email", request.request_id, Utils.copy_dict(request.__dict__))
     