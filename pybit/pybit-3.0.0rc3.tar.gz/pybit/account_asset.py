from ._http_manager import _V3HTTPManager


class HTTP(_V3HTTPManager):
    def create_internal_transfer(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/asset/v3/private/transfer/inter-transfer",
            query=kwargs,
            auth=True
        )

    def create_subaccount_transfer(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/asset/v3/private/transfer/sub-member-transfer",
            query=kwargs,
            auth=True
        )

    def get_internal_transfer_list(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/transfer/inter-transfer/list/query",
            query=kwargs,
            auth=True
        )

    def get_subaccount_transfer_list(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/transfer/sub-member-transfer/list/query",
            query=kwargs,
            auth=True
        )

    def get_subaccount_list(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/transfer/sub-member/list/query",
            query=kwargs,
            auth=True
        )

    def enable_universal_transfer(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/asset/v3/private/transfer/transfer-sub-member-save",
            query=kwargs,
            auth=True
        )

    def create_universal_transfer(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/asset/v3/private/transfer/universal-transfer",
            query=kwargs,
            auth=True
        )

    def get_universal_transfer_list(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/asset/v3/private/transfer/universal-transfer/list/query",
            query=kwargs,
            auth=True
        )

    def get_transferable_coin_list(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/transfer/transfer-coin/list/query",
            query=kwargs,
            auth=True
        )

    def get_account_coin_balance(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/transfer/account-coin/balance/query",
            query=kwargs,
            auth=True
        )

    def get_asset_info(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/transfer/asset-info/query",
            query=kwargs,
            auth=True
        )

    def get_supported_deposit_list(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/public/deposit/allowed-deposit-list/query",
            query=kwargs,
            auth=True
        )

    def get_deposit_records(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/deposit/record/query",
            query=kwargs,
            auth=True
        )

    def get_withdraw_records(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/withdraw/record/query",
            query=kwargs,
            auth=True
        )

    def get_sub_deposit_records_by_master_key(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/deposit/sub-member-record/query",
            query=kwargs,
            auth=True
        )

    def get_coin_info(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/coin-info/query",
            query=kwargs,
            auth=True
        )

    def withdraw(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/asset/v3/private/withdraw/create",
            query=kwargs,
            auth=True
        )

    def cancel_withdrawal(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/asset/v3/private/withdraw/cancel",
            query=kwargs,
            auth=True
        )

    def get_master_deposit_addresses(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/deposit/address/query",
            query=kwargs,
            auth=True
        )

    def get_sub_deposit_addresses(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v3/private/deposit/sub-member-address/query",
            query=kwargs,
            auth=True
        )

    def create_sub_uid(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/user/v3/private/create-sub-member",
            query=kwargs,
            auth=True
        )

    def create_sub_uid_api_key(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/user/v3/private/create-sub-api",
            query=kwargs,
            auth=True
        )

    def get_sub_uid_list(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/user/v3/private/query-sub-members",
            query=kwargs,
            auth=True
        )

    def freeze_sub_uid(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/user/v3/private/frozen-sub-member",
            query=kwargs,
            auth=True
        )

    def modify_master_api_key(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/user/v3/private/update-api",
            query=kwargs,
            auth=True
        )

    def modify_sub_api_key(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/user/v3/private/update-sub-api",
            query=kwargs,
            auth=True
        )

    def delete_master_api_key(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/user/v3/private/delete-api",
            query=kwargs,
            auth=True
        )

    def delete_sub_api_key(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/user/v3/private/delete-sub-api",
            query=kwargs,
            auth=True
        )
