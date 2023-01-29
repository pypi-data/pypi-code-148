from copy import deepcopy
from typing import List

from alibabacloud_alidns20150109 import models as dns_models
from alibabacloud_alidns20150109.client import Client as DNSClient
from alibabacloud_tea_openapi.models import Config as SessionConfig
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class DNSManager:
    def __init__(self, config: SessionConfig):
        self.config = deepcopy(config)
        self.config.endpoint = 'alidns.cn-shanghai.aliyuncs.com'
        self.client = DNSClient(self.config)
        self.runtimeOptions = util_models.RuntimeOptions()

    def add_domain_record(self, domain_rr, domain_type, domain_name, record, ttl=600, priority=None, description=None):
        add_domain_record_request = dns_models.AddDomainRecordRequest(
            domain_name=domain_name,
            rr=domain_rr,
            type=domain_type,
            value=record,
            ttl=ttl
        )
        if domain_type == "MX":
            add_domain_record_request.priority = priority
        try:
            # 复制代码运行请自行打印 API 的返回值
            data = self.client.add_domain_record_with_options(add_domain_record_request, self.runtimeOptions)
            if description:
                self.update_domain_remark(data.body.record_id, remark=description)
            return data.body
        except Exception as error:
            # 如有需要，请打印 error
            error_msg = UtilClient.assert_as_string(error.message)
            print(error_msg)

    def update_domain_remark(self, record_id, remark):
        try:
            request = dns_models.UpdateDomainRecordRemarkRequest(
                record_id=record_id,
                remark=remark
            )
            return self.client.update_domain_record_remark_with_options(request, self.runtimeOptions)
        except Exception as error:
            UtilClient.assert_as_string(error.message)

    def list_domain_record(self, domain_name: str, domain_record: str, domain_value=None, domain_type=None) -> List[
        dns_models.DescribeDomainRecordsResponseBodyDomainRecordsRecord]:
        try:
            request = dns_models.DescribeDomainRecordsRequest(
                domain_name=domain_name,
                rrkey_word=domain_record,
                search_mode='ADVANCED',
                page_size=100
            )
            if domain_value:
                request.value_key_word = domain_value
            if domain_type:
                request.type = domain_type
            data = self.client.describe_domain_records_with_options(request, self.runtimeOptions).body
            assert data.total_count <= 100
            return data.domain_records.record
        except Exception as error:
            UtilClient.assert_as_string(error.message)

    def delete_domain_record(self, record_id) -> None:
        try:
            request = dns_models.DeleteDomainRecordRequest(
                record_id=record_id
            )
            self.client.delete_domain_record_with_options(request, self.runtimeOptions)
        except Exception as error:
            UtilClient.assert_as_string(error.message)
