from __future__ import annotations

from typing import List

from lazy_streams import stream


class Field:
    def __init__(self, key: str):
        self.key = key

    def __set__(self, instance, value):
        raise NotImplementedError()

    def __get__(self, instance, owner):
        if self.key == 'ResponseMetadata':
            return ResponseMetadata(instance._data.get(self.key))
        elif self.key == 'HTTPHeaders':
            return HTTPHeaders(instance._data.get(self.key))
        elif self.key == 'logGroups':
            return stream(instance._data.get(self.key)).map(LogGroup).to_list()
        elif self.key == 'logStreams':
            return stream(instance._data.get(self.key)).map(LogStream).to_list()
        else:
            return instance._data.get(self.key)


class _Base:
    def __init__(self, data: dict):
        self._data = data


class ResponseMetadata(_Base):
    RequestId: str = Field('RequestId')
    HTTPStatusCode: int = Field('HTTPStatusCode')
    HTTPHeaders: HTTPHeaders = Field('HTTPHeaders')
    RetryAttempts: int = Field('RetryAttempts')

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"RequestId={repr(self.RequestId)}, " \
               f"HTTPStatusCode={repr(self.HTTPStatusCode)}, " \
               f"HTTPHeaders={repr(self.HTTPHeaders)}, " \
               f"RetryAttempts={repr(self.RetryAttempts)}" \
               f")"


class HTTPHeaders(_Base):
    x_amzn_requestid: str = Field('x-amzn-requestid')
    content_type: str = Field('content-type')
    content_length: str = Field('content-length')
    date: str = Field('date')

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"x_amzn_requestid={repr(self.x_amzn_requestid)}, " \
               f"content_type={repr(self.content_type)}, " \
               f"content_length={repr(self.content_length)}, " \
               f"date={repr(self.date)}" \
               f")"


class Response(_Base):
    ResponseMetadata: ResponseMetadata = Field('ResponseMetadata')

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"ResponseMetadata={repr(self.ResponseMetadata)}" \
               f")"


class DescribeLogGroupsResponse(Response):
    logGroups: List[LogGroup] = Field('logGroups')

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"ResponseMetadata={repr(self.ResponseMetadata)}, " \
               f"logGroups={repr(self.logGroups)}" \
               f")"


class LogGroup(_Base):
    logGroupName: str = Field('logGroupName')
    creationTime: int = Field('creationTime')
    retentionInDays: int = Field('retentionInDays')
    metricFilterCount: int = Field('metricFilterCount')
    arn: str = Field('arn')
    storedBytes: int = Field('storedBytes')
    kmsKeyId: str = Field('kmsKeyId')
    dataProtectionStatus: str = Field('dataProtectionStatus')

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"logGroupName={repr(self.logGroupName)}, " \
               f"creationTime={repr(self.creationTime)}, " \
               f"retentionInDays={repr(self.retentionInDays)}, " \
               f"metricFilterCount={repr(self.metricFilterCount)}, " \
               f"arn={repr(self.arn)}, " \
               f"storedBytes={repr(self.storedBytes)}, " \
               f"kmsKeyId={repr(self.kmsKeyId)}, " \
               f"dataProtectionStatus={repr(self.dataProtectionStatus)}" \
               f")"


class DescribeLogStreamsResponse(Response):
    logStreams: List[LogStream] = Field('logStreams')

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"ResponseMetadata={repr(self.ResponseMetadata)}, " \
               f"logStreams={repr(self.logStreams)}" \
               f")"


class LogStream(_Base):
    logStreamName: str = Field('logStreamName')
    creationTime: int = Field('creationTime')
    firstEventTimestamp: int = Field('firstEventTimestamp')
    lastEventTimestamp: int = Field('lastEventTimestamp')
    lastIngestionTime: int = Field('lastIngestionTime')
    uploadSequenceToken: str = Field('uploadSequenceToken')
    arn: str = Field('arn')
    storedBytes: int = Field('storedBytes')

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"logStreamName={repr(self.logStreamName)}, " \
               f"creationTime={repr(self.creationTime)}, " \
               f"firstEventTimestamp={repr(self.firstEventTimestamp)}, " \
               f"lastEventTimestamp={repr(self.lastEventTimestamp)}, " \
               f"lastIngestionTime={repr(self.lastIngestionTime)}, " \
               f"uploadSequenceToken={repr(self.uploadSequenceToken)}, " \
               f"arn={repr(self.arn)}, " \
               f"storedBytes={repr(self.storedBytes)}" \
               f")"
