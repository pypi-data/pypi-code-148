from potencent.lib.CONST import NO_FILE_ERROR
from potencent.lib.Config import potencentConfig

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models


class OCR(potencentConfig):
    def __init__(self):
        self.TENCENT_AI_CFG = None
        self.TENCENTCLOUD_SECRET_ID = None
        self.TENCENTCLOUD_SECRET_KEY = None
        self.CLIENT = None

    def set_config(self, configPath):
        """
        加载配置信息，生成client
        :param configPath: 可以自定义config文件的名称和位置，有默认值
        :return:
        """
        self.TENCENT_AI_CFG = self.get_config(configPath)
        if self.TENCENT_AI_CFG['tencent-ai']['TENCENTCLOUD_SECRET_ID'] and self.TENCENT_AI_CFG['tencent-ai'][
            'TENCENTCLOUD_SECRET_KEY']:
            self.TENCENTCLOUD_SECRET_ID = self.TENCENT_AI_CFG['tencent-ai']['TENCENTCLOUD_SECRET_ID']
            self.TENCENTCLOUD_SECRET_KEY = self.TENCENT_AI_CFG['tencent-ai']['TENCENTCLOUD_SECRET_KEY']
        cred = credential.Credential(self.TENCENTCLOUD_SECRET_ID, self.TENCENTCLOUD_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
        return self.client

    def get_params(self, ImageBase64, ImageUrl):
        """
        图片的ImageUrl、ImageBase64必须提供一个，如果都提供，只使用ImageUrl。
        :param ImageBase64:
        :param ImageUrl:
        :return:
        """
        if ImageUrl:
            params = '{\"ImageUrl\":\"%s\"} ' % ImageUrl
        elif ImageBase64:
            params = '{\"ImageBase64\":\"%s\"} ' % ImageBase64
        else:
            return NO_FILE_ERROR
        return params

    def VatInvoiceOCR(self, ImageBase64, ImageUrl):
        """
        本接口支持增值税专用发票、增值税普通发票、增值税电子发票全字段的内容检测和识别，
        包括发票代码、发票号码、打印发票代码、打印发票号码、开票日期、合计金额、校验码、税率、合计税额、价税合计、购买方识别号、复核、销售方识别号、开票人、密码区1、密码区2、密码区3、密码区4、发票名称、购买方名称、销售方名称、服务名称、备注、规格型号、数量、单价、金额、税额、收款人等字段。

        默认接口请求频率限制：10次/秒。
        图片的 ImageUrl、ImageBase64 必须提供一个，如果都提供，只使用 ImageUrl。
        :param ImageBase64:
        :param ImageUrl:
        :return:
        """
        try:
            req = models.VatInvoiceOCRRequest()
            req.from_json_string(self.get_params(ImageBase64, ImageUrl))
            resp = self.client.VatInvoiceOCR(req)
            return resp

        except TencentCloudSDKException as err:
            print(err)

    def BankCardOCR(self, ImageBase64, ImageUrl):
        """
        本接口支持对中国大陆主流银行卡正反面关键字段的检测与识别，包括卡号、卡类型、卡名字、银行信息、有效期。
        支持竖排异形卡识别、多角度旋转图片识别。支持对复印件、翻拍件、边框遮挡的银行卡进行告警，可应用于各种银行卡信息有效性校验场景，如金融行业身份认证、第三方支付绑卡等场景。
        默认接口请求频率限制：10次/秒。
        图片的 ImageUrl、ImageBase64 必须提供一个，如果都提供，只使用 ImageUrl。
        :param ImageBase64: 图片的
        :return:
        """
        try:
            req = models.BankCardOCRRequest()
            req.from_json_string(self.get_params(ImageBase64, ImageUrl))
            resp = self.client.BankCardOCR(req)
            return resp

        except TencentCloudSDKException as err:
            print(err)
