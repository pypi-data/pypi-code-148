# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)


class ZADBaseAPI(object):
    API_BASE_URL = None

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, **kwargs)

    def _put(self, url, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.put(url, **kwargs)


class ZADAPI(ZADBaseAPI):

    def get_header(self):
        return {}

    def _get(self, url, params=None, **kwargs):
        kwargs['params'] = params
        kwargs['headers'] = self.get_header()
        return super(ZADAPI, self)._get(url, **kwargs)

    def _post(self, url, params=None, data=None, **kwargs):
        kwargs['params'] = params
        kwargs['data'] = data
        kwargs['headers'] = self.get_header()
        return super(ZADAPI, self)._post(url, **kwargs)

    def _put(self, url, params=None, data=None, **kwargs):
        kwargs['params'] = params
        kwargs['data'] = data
        kwargs['headers'] = self.get_header()
        return super(ZADAPI, self)._put(url, **kwargs)

    def get(self, url, params=None, **kwargs):
        return self._get(url, params, **kwargs)

    def post(self, url, data=None, params=None, **kwargs):
        return self._post(url, params, data, **kwargs)

    def put(self, url, data=None, params=None, **kwargs):
        return self._put(url, params, data, **kwargs)

    def download(self, url, params=None, **kwargs):
        kwargs['stream'] = True
        return self._get(url, params, **kwargs)



class ZADAuthAPI(ZADAPI):

    def get_header(self):
        _headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "charset": "UTF-8",
            "Connection": "close"
        }

        return _headers


class ZADOpenAPI(ZADAPI):

    def get_header(self):
        _headers = {
            'Amazon-Advertising-API-ClientId': self._client.client_id,
            'Authorization': 'Bearer %s' % self._client.access_token,
            'Content-Type': 'application/json',
            'Connection': 'close',
        }

        if self._client.profile_id is not None:
            _headers.update(
                {
                    "Amazon-Advertising-API-Scope": self._client.profile_id
                }
            )

        return _headers


# TN-US-US
payload = {'account_station': {'profile_id': '2954747900155745',
                               'merchant_id': 'AM9QN2RFHQLKZ',
                               'merchant_type': 'seller',
                               'marketplace_id': 'ATVPDKIKX0DER',
                               'country': 'US'},
           'auth_info': {
               'access_token': 'Atza|IwEBIAIU6Z5oqFi8wVarUiB45OYwxGBqjcARSjBJVH4YL6smgGZWGfeVvEEESuyqmRaOhla_xUIp2zUAc9LVBqvjvaF6nVWZYkb3jlTnLxpzMoDmPC1WfT5aJNBgbYD95aTXlIuIGw7uRVe3pAYMWPuZxFngxaCGcQI4Wu_g4JwX6IRBCxmOnCgB59SRy8tuWbbn-IZbiqr-EXMxPMnxDmd3UixlYnrY2a1JJM7ZZUSsATZsMrTHns1ciFdVxyt4MKT6YFSwrwQkZMOi95BfBOMwVWjGK-9wqjYPFzv4wqnzu7VdqsYNye5SQ2LqvgJ7Hj2Vel6FqMVSGNfdLL_JZOgnpyLj7GDRolMEYN8Jti5dDRlSw3RALDfSqgcMPuIHgY9l77A_DbAFJFqQ5JoWxg6vC7ZhgQutXl8epphBT8-VxZa7qcylEPOYQ68jc--d8-wQt4Q',
               'expired_at': '2022-12-07 06:25:17+00:00',
               'client_id': 'amzn1.application-oa2-client.5f22ade077114ef980883e2045a2fde0'}}


def subscribe(payload, abbreviation):
    """
    Step 3: Subscribe to Amazon Marketing Stream datasets
    """
    import requests
    import json
    from requests.adapters import HTTPAdapter

    queue_arn = 'arn:aws:sqs:us-east-1:204669422762:sp-traffic'

    url = 'https://advertising-api.amazon.com/streams/subscriptions'

    _headers = {
        'Amazon-Advertising-API-ClientId': payload['auth_info']['client_id'],
        'Amazon-Advertising-API-Scope': payload['account_station']['profile_id'],
        'Authorization': 'Bearer %s' % payload['auth_info']['access_token'],
        'Content-Type': 'application/vnd.MarketingStreamSubscriptions.StreamSubscriptionResource.v1.0+json',
    }
    _data = {
        "clientRequestToken": 'clientRequestToken:%s' % payload['account_station']['profile_id'],  # TODO 长度必需超过 22
        "dataSetId": "sp-traffic",
        "notes": "%s sp-traffic subscription" % abbreviation,  # TODO 添加账号信息
        "destinationArn": queue_arn,
    }
    request_kwargs = dict(
        timeout=300,
        headers=_headers,
        data=json.dumps(_data).encode('utf-8'),
        stream=False
    )


    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))

    response = s.request(
        'POST',
        url,
        **request_kwargs
    )
    # '{"clientRequestToken":"clientRequestToken:2954747900155745","subscriptionId":"amzn1.fead.cs1.rBMSKQcxFT6jfeUOkYxC6A"}'  # TN-US
    # '{"clientRequestToken":"clientRequestToken:452773493838954","subscriptionId":"amzn1.fead.cs1.vE0tK57g6xSuPA3-Po5Lmg"}'   # LH-US
    return response


def confirm_subscription(delete_message=False):
    """
    Step 4: Confirm your subscription in SQS

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.confirm_subscription


    messages = {'Messages': [{'MessageId': 'dfe4751a-316f-4197-84c5-dbdf1e02f1cd',
   'ReceiptHandle': 'AQEBJNXkaPWhsVnqfCLYUNc5jjm6HbOW5nxKluTkyLU7ecqqnvZGHAjlIW8Hzcw0mELb6HgIK+KdLlANlZ5s47+mkO+PEptclDnvJ69QElh9W05X6D/TEObvnl69Hv5zFlo1X0EtT319/IfsIBvNtfcYdG9d/7d7yxZMzeZCBECT73zVUnZWpQSf5FcXp+k8JJcguCuRdTmZLbpaZxJpfsaAp7PSUUfuamgJ6fs5MFOkdxsuhAtZu5G6cnaa81AU2+6mUnIihZ7zhf5ymRx7O9UzA+b6RPqhi1nc21v4jAoEV6QuvwA0r39iHDGgphL/jk7zsGbgqEQKU7qx6lSOLm21I+fBPkkpJ0hP56FR0ILxR1GjhDMAZ753ACXRhMZnh1bD',
   'MD5OfBody': '818afffea9e1700f22b08c2afdef5ad3',
   'Body': '{\n  "Type" : "SubscriptionConfirmation",\n  "MessageId" : "98caea8d-34d7-45c3-99d8-14ab1eb2c4e5",\n  "Token" : "2336412f37fb687f5d51e6e2425dacba6c5878ccabebd6273e499c460b9d0a0e03b336146217204d486093f846614d77d2a1785562115358f7a61307035664076d476780cd7a367783b3ef7c30eec9c9973cbf10d98250e8e725b47c6d38de68ed47dcf41c75890447c33b82dbd252415c179b201021fb0756ef2681b9131c2e657d3ba9bbed48e167c10fae5e82d1139845abf77d6aab4e86c810f0ca96f8d0e3ed3e0557d4d32cee37eae675ff1b76",\n  "TopicArn" : "arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY2N1TFCBGOXRM5",\n  "Message" : "You have chosen to subscribe to the topic arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY2N1TFCBGOXRM5.\\nTo confirm the subscription, visit the SubscribeURL included in this message.",\n  "SubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=ConfirmSubscription&TopicArn=arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY2N1TFCBGOXRM5&Token=2336412f37fb687f5d51e6e2425dacba6c5878ccabebd6273e499c460b9d0a0e03b336146217204d486093f846614d77d2a1785562115358f7a61307035664076d476780cd7a367783b3ef7c30eec9c9973cbf10d98250e8e725b47c6d38de68ed47dcf41c75890447c33b82dbd252415c179b201021fb0756ef2681b9131c2e657d3ba9bbed48e167c10fae5e82d1139845abf77d6aab4e86c810f0ca96f8d0e3ed3e0557d4d32cee37eae675ff1b76",\n  "Timestamp" : "2022-12-07T06:08:00.665Z",\n  "SignatureVersion" : "1",\n  "Signature" : "ZMDM7UcPjDsM4ZDjKUB4P5A81rvUGiWSptTzn9jJPKw2nnFOa/iE7+XV+XHETZoazZW5bxFQ/gmXGVz2o1wdns2VaIGCaeiS6CMRmTvduEIFPQNSDmmnl7TkeXY+3+xrZPmeWBCuquvOnWRjDtwlkNCyqGrvoZfb/bFFSa74KsFTTs0LNLebKFtcUDnyqbUNMR3YU9Map4rp1HhQHq9hrMcrKmVxuUlIpSXwc6xpyc+heQERBDbt1nJCrRt/yww9qNr769CnZEbsKgm1DbQO9L0SWk6ykAGuZzCJ741XSHtQxvemkv3CE9wQq+SFN7CxHxbaj+t5eDm8hjCtbDvSUw==",\n  "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-56e67fcb41f6fec09b0196692625d385.pem"\n}'}],
 'ResponseMetadata': {'RequestId': '82ceb293-ce8c-5479-b561-ee99f496b93b',
  'HTTPStatusCode': 200,
  'HTTPHeaders': {'x-amzn-requestid': '82ceb293-ce8c-5479-b561-ee99f496b93b',
   'date': 'Wed, 07 Dec 2022 06:51:06 GMT',
   'content-type': 'text/xml',
   'content-length': '2985'},
  'RetryAttempts': 0}}


    content = {'Type': 'SubscriptionConfirmation',
 'MessageId': '98caea8d-34d7-45c3-99d8-14ab1eb2c4e5',
 'Token': '2336412f37fb687f5d51e6e2425dacba6c5878ccabebd6273e499c460b9d0a0e03b336146217204d486093f846614d77d2a1785562115358f7a61307035664076d476780cd7a367783b3ef7c30eec9c9973cbf10d98250e8e725b47c6d38de68ed47dcf41c75890447c33b82dbd252415c179b201021fb0756ef2681b9131c2e657d3ba9bbed48e167c10fae5e82d1139845abf77d6aab4e86c810f0ca96f8d0e3ed3e0557d4d32cee37eae675ff1b76',
 'TopicArn': 'arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY2N1TFCBGOXRM5',
 'Message': 'You have chosen to subscribe to the topic arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY2N1TFCBGOXRM5.\nTo confirm the subscription, visit the SubscribeURL included in this message.',
 'SubscribeURL': 'https://sns.us-east-1.amazonaws.com/?Action=ConfirmSubscription&TopicArn=arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY2N1TFCBGOXRM5&Token=2336412f37fb687f5d51e6e2425dacba6c5878ccabebd6273e499c460b9d0a0e03b336146217204d486093f846614d77d2a1785562115358f7a61307035664076d476780cd7a367783b3ef7c30eec9c9973cbf10d98250e8e725b47c6d38de68ed47dcf41c75890447c33b82dbd252415c179b201021fb0756ef2681b9131c2e657d3ba9bbed48e167c10fae5e82d1139845abf77d6aab4e86c810f0ca96f8d0e3ed3e0557d4d32cee37eae675ff1b76',
 'Timestamp': '2022-12-07T06:08:00.665Z',
 'SignatureVersion': '1',
 'Signature': 'ZMDM7UcPjDsM4ZDjKUB4P5A81rvUGiWSptTzn9jJPKw2nnFOa/iE7+XV+XHETZoazZW5bxFQ/gmXGVz2o1wdns2VaIGCaeiS6CMRmTvduEIFPQNSDmmnl7TkeXY+3+xrZPmeWBCuquvOnWRjDtwlkNCyqGrvoZfb/bFFSa74KsFTTs0LNLebKFtcUDnyqbUNMR3YU9Map4rp1HhQHq9hrMcrKmVxuUlIpSXwc6xpyc+heQERBDbt1nJCrRt/yww9qNr769CnZEbsKgm1DbQO9L0SWk6ykAGuZzCJ741XSHtQxvemkv3CE9wQq+SFN7CxHxbaj+t5eDm8hjCtbDvSUw==',
 'SigningCertURL': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-56e67fcb41f6fec09b0196692625d385.pem'}

    confirm_result = {'SubscriptionArn': 'arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY2N1TFCBGOXRM5:06168291-d98a-46a9-9467-dcaba12354be',
 'ResponseMetadata': {'RequestId': '3714ef94-5660-53fe-8c9b-b39e1609a052',
  'HTTPStatusCode': 200,
  'HTTPHeaders': {'x-amzn-requestid': '3714ef94-5660-53fe-8c9b-b39e1609a052',
   'content-type': 'text/xml',
   'content-length': '459',
   'date': 'Wed, 07 Dec 2022 07:18:01 GMT'},
  'RetryAttempts': 0}}

  # LH-US
  confirm_result = {'SubscriptionArn': 'arn:aws:sns:us-east-1:906013806264:FEADMessageDeliveryTopic-sp-traffic-ATVPDKIKX0DER-ENTITY1FTVMIUKA5OGW:360c3898-3929-4cb7-bd24-100d0e1e7573',
 'ResponseMetadata': {'RequestId': 'e4f6ec95-ee49-5d85-93dd-b09fa485f5b9',
  'HTTPStatusCode': 200,
  'HTTPHeaders': {'x-amzn-requestid': 'e4f6ec95-ee49-5d85-93dd-b09fa485f5b9',
   'content-type': 'text/xml',
   'content-length': '459',
   'date': 'Wed, 07 Dec 2022 08:02:19 GMT'},
  'RetryAttempts': 0}}

    """
    import boto3
    import json

    _queue_name = 'sp-traffic'

    _region_name = 'us-east-1'
    _aws_access_key_id = 'AKIAS7JZ7RSVJBH4QQBK'
    _aws_secret_access_key = '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'

    _session = boto3.session.Session()

    # 用来接收消息
    sqs = _session.client(
        'sqs',
        region_name=_region_name,
        aws_access_key_id=_aws_access_key_id,
        aws_secret_access_key=_aws_secret_access_key,
    )
    queues = sqs.list_queues(QueueNamePrefix=_queue_name)  # 根据队列名称去查队列的信息
    print(queues)  # TODO 是个列表，要做处理选出真正的队列 URL
    queue_url = 'https://sqs.us-east-1.amazonaws.com/204669422762/sp-traffic'  # 先简单从 queues里拿出来直接使用

    qs = sqs.get_queue_url(QueueName=_queue_name)
    _queue_url = qs['QueueUrl']  # 'https://sqs.us-east-1.amazonaws.com/204669422762/sp-traffic'

    # 可以用while True 语句去遍历，再用 sqs.delete_message去删除处理过的消息，避免循环
    _message_attribute_names= []
    _attribute_names = ['All']
    _wait_time = 0
    _max_number_of_messages = 1
    messages = sqs.receive_message(
        QueueUrl=_queue_url,
        MessageAttributeNames=_message_attribute_names,
        AttributeNames=_attribute_names,
        WaitTimeSeconds=_wait_time,
        MaxNumberOfMessages=_max_number_of_messages,
    )

    assert len(messages['Messages']) == 1

    content = json.loads(messages['Messages'][0]['Body'])

    # 处理sqs队列中收到的消息，即执行确认订阅的操作
    if "Type" in content and content['Type'] == 'SubscriptionConfirmation':
        sns = _session.client(
            'sns',
            region_name=_region_name,
            aws_access_key_id=_aws_access_key_id,
            aws_secret_access_key=_aws_secret_access_key,
        )

        token = content['Token']
        topic_arn = content['TopicArn']
        print(f"Confirming subscription for {topic_arn}")
        confirm_result = sns.confirm_subscription(TopicArn=topic_arn, Token=token)

        if delete_message:
            receipt_handle = messages['Messages'][0]['ReceiptHandle']
            del_response = sqs.delete_message(
                QueueUrl=_queue_url,
                ReceiptHandle=receipt_handle
            )
            print('========== 删除消息 ==========')
            print(del_response)
        else:
            print('========== 消息暂不删除 ==========')

        return confirm_result


def view_all_subscriptions(payload):
    """
    查看XX账号所有订阅
    """

    import requests
    import json
    from requests.adapters import HTTPAdapter

    url = 'https://advertising-api.amazon.com/streams/subscriptions?maxResults=100'

    _headers = {
        'Amazon-Advertising-API-ClientId': payload['auth_info']['client_id'],
        'Amazon-Advertising-API-Scope': payload['account_station']['profile_id'],
        'Authorization': 'Bearer %s' % payload['auth_info']['access_token'],
    }

    request_kwargs = dict(
        timeout=300,
        headers=_headers,
        stream=False
    )

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))

    response = s.request(
        'GET',
        url,
        **request_kwargs
    )
    data = json.loads(response.text)
    # data = {'subscriptions': [{'createdDate': '2022-12-07T06:07:47.109Z',
    #                            'dataSetId': 'sp-traffic',
    #                            'destinationArn': 'arn:aws:sqs:us-east-1:204669422762:sp-traffic',
    #                            'notes': 'Advertiser 1 sp-traffic subscription',
    #                            'status': 'ACTIVE',
    #                            'subscriptionId': 'amzn1.fead.cs1.rBMSKQcxFT6jfeUOkYxC6A',
    #                            'updatedDate': '2022-12-07T07:20:10.252Z'}]}

    # {'subscriptions': [{'createdDate': '2022-12-07T07:58:01.974Z',
    #                     'dataSetId': 'sp-traffic',
    #                     'destinationArn': 'arn:aws:sqs:us-east-1:204669422762:sp-traffic',
    #                     'notes': 'LH-US-US sp-traffic subscription',
    #                     'status': 'ACTIVE',
    #                     'subscriptionId': 'amzn1.fead.cs1.vE0tK57g6xSuPA3-Po5Lmg',
    #                     'updatedDate': '2022-12-07T08:05:53.531Z'}]}
    # return response
