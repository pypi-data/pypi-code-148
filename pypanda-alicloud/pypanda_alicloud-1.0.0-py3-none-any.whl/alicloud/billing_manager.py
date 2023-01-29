from alibabacloud_bssopenapi20171214 import models as bss_models
from alibabacloud_bssopenapi20171214.client import Client as BssClient
from alibabacloud_tea_openapi.models import Config as SessionConfig

from pypanda.alicloud._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class BillingManager(_Manager):
    def __init__(self, config: SessionConfig):
        config.endpoint = 'business.aliyuncs.com'
        super().__init__(config)
        self.client = BssClient(self.config)

    @page_reader(nodes=["items", "item"])
    @tea_request_wrapper
    def iterate_all_bill_settles(self, month, next_token=None, max_results=100) -> bss_models.QuerySettleBillResponseBodyDataItemsItem:
        """
        month: Y-M like 2022-09
        """

        req = bss_models.QuerySettleBillRequest(
            billing_cycle=month,
            next_token=next_token,
            max_results=max_results
        )
        res = self.client.query_settle_bill_with_options(req, self.runtimeOptions)
        return res.body.data

    def query_account_balance(self) -> bss_models.QueryAccountBalanceResponseBodyData:
        res = self.client.query_account_balance_with_options(self.runtimeOptions)
        return res.body.data

    @page_reader(nodes=["items"])
    @tea_request_wrapper
    def iterate_instance_bill(self, month, day=None, next_token=None, max_results=100) -> bss_models.DescribeInstanceBillResponseBodyDataItems:
        req = bss_models.DescribeInstanceBillRequest(
            billing_cycle=month,
            next_token=next_token,
            max_results=max_results
        )
        if day:
            req.billing_date = f'{month}-{day}'
            req.granularity = 'DAILY'

        res = self.client.describe_instance_bill_with_options(req, self.runtimeOptions)
        return res.body.data
