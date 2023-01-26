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
        elif self.key == 'events':
            return stream(instance._data.get(self.key)).map(LogEvent).to_list()
        else:
            return instance._data.get(self.key)


class _Base:
    def __init__(self, data: dict):
        self._data = data

    def __repr__(self):
        r = f"{self.__class__.__name__}("
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                r += f"{k}={repr(getattr(self, k))}, "
        r = r.rstrip(" ,") + ")"
        return r


class ResponseMetadata(_Base):
    RequestId: str = Field('RequestId')
    HTTPStatusCode: int = Field('HTTPStatusCode')
    HTTPHeaders: HTTPHeaders = Field('HTTPHeaders')
    RetryAttempts: int = Field('RetryAttempts')


class HTTPHeaders(_Base):
    x_amzn_requestid: str = Field('x-amzn-requestid')
    content_type: str = Field('content-type')
    content_length: str = Field('content-length')
    date: str = Field('date')


class Response(_Base):
    ResponseMetadata: ResponseMetadata = Field('ResponseMetadata')


class DescribeLogGroupsResponse(Response):
    logGroups: List[LogGroup] = Field('logGroups')


class LogGroup(_Base):
    logGroupName: str = Field('logGroupName')
    creationTime: int = Field('creationTime')
    retentionInDays: int = Field('retentionInDays')
    metricFilterCount: int = Field('metricFilterCount')
    arn: str = Field('arn')
    storedBytes: int = Field('storedBytes')
    kmsKeyId: str = Field('kmsKeyId')
    dataProtectionStatus: str = Field('dataProtectionStatus')


class DescribeLogStreamsResponse(Response):
    logStreams: List[LogStream] = Field('logStreams')


class LogStream(_Base):
    logStreamName: str = Field('logStreamName')
    creationTime: int = Field('creationTime')
    firstEventTimestamp: int = Field('firstEventTimestamp')
    lastEventTimestamp: int = Field('lastEventTimestamp')
    lastIngestionTime: int = Field('lastIngestionTime')
    uploadSequenceToken: str = Field('uploadSequenceToken')
    arn: str = Field('arn')
    storedBytes: int = Field('storedBytes')


class GetLogEventsResponse(Response):
    nextBackwardToken: str = Field('nextBackwardToken')
    nextForwardToken: str = Field('nextForwardToken')
    events: List[LogEvent] = Field('events')


class LogEvent(_Base):
    ingestionTime: int = Field('ingestionTime')
    timestamp: int = Field('timestamp')
    message: str = Field('message')
