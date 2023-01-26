from __future__ import annotations
import os
from functools import cached_property
from typing import Dict, List

import boto3

from .cloud_watch_logs_dto import Response, DescribeLogGroupsResponse, DescribeLogStreamsResponse


class CloudWatchLogs:
    def __init__(self,
                 region_name: str = None,
                 aws_access_key_id: str = None,
                 aws_secret_access_key: str = None,
                 ):
        self.region_name = region_name or os.environ.get('aws.cloud_watch_logs.region_name', None)
        self.aws_access_key_id = aws_access_key_id or os.environ.get('aws.cloud_watch_logs.aws_access_key_id', None)
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get('aws.cloud_watch_logs.aws_secret_access_key', None)

    @cached_property
    def client(self):
        kwargs = {
            'region_name': self.region_name,
            'aws_access_key_id': self.aws_access_key_id,
            'aws_secret_access_key': self.aws_secret_access_key,
        }

        return boto3.client('logs', **{k: v for k, v in kwargs.items() if v is not None})

    @staticmethod
    def _params_resolve(p: dict) -> dict:
        return {k: v for k, v in p.items() if v is not None}

    def describe_log_groups(self,
                            accountIdentifiers: List[str] = None,
                            logGroupNamePrefix: str = None,
                            logGroupNamePattern: str = None,
                            nextToken: str = None,
                            limit: int = None,
                            includeLinkedAccounts: bool = None,
                            ) -> DescribeLogGroupsResponse:
        """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_log_groups"""
        params = {
            'accountIdentifiers': accountIdentifiers,
            'logGroupNamePrefix': logGroupNamePrefix,
            'logGroupNamePattern': logGroupNamePattern,
            'nextToken': nextToken,
            'limit': limit,
            'includeLinkedAccounts': includeLinkedAccounts,
        }
        result = self.client.describe_log_groups(**self._params_resolve(params))
        return DescribeLogGroupsResponse(result)

    def describe_log_streams(self, *,
                             logGroupName: str,
                             logGroupIdentifier: str = None,
                             logStreamNamePrefix: str = None,
                             orderBy: str = None,
                             descending: bool = None,
                             nextToken: str = None,
                             limit: int = None,
                             ):
        """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_log_streams"""
        params = {
            'logGroupName': logGroupName,
            'logGroupIdentifier': logGroupIdentifier,
            'logStreamNamePrefix': logStreamNamePrefix,
            'orderBy': orderBy,
            'descending': descending,
            'nextToken': nextToken,
            'limit': limit,
        }
        result = self.client.describe_log_streams(**self._params_resolve(params))
        return DescribeLogStreamsResponse(result)

    def create_log_group(self, *,
                         logGroupName: str,
                         kmsKeyId: str = None,
                         tags: Dict[str, str] = None,
                         ) -> Response:
        """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.create_log_group"""
        params = {
            'logGroupName': logGroupName,
            'kmsKeyId': kmsKeyId,
            'tags': tags,
        }
        result = self.client.create_log_group(**self._params_resolve(params))
        return Response(result)

    def delete_log_group(self, *,
                         logGroupName: str,
                         ) -> Response:
        """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_log_group"""
        params = {
            'logGroupName': logGroupName,
        }
        result = self.client.delete_log_group(**self._params_resolve(params))
        return Response(result)

    def create_log_stream(self, *,
                          logGroupName: str,
                          logStreamName: str,
                          ) -> Response:
        """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.create_log_stream"""
        params = {
            'logGroupName': logGroupName,
            'logStreamName': logStreamName,
        }
        result = self.client.create_log_stream(**self._params_resolve(params))
        return Response(result)

    def delete_log_stream(self, *,
                          logGroupName: str,
                          logStreamName: str,
                          ) -> Response:
        """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_log_stream"""
        params = {
            'logGroupName': logGroupName,
            'logStreamName': logStreamName,
        }
        result = self.client.delete_log_stream(**self._params_resolve(params))
        return Response(result)

    def put_log_events(self, *,
                       logGroupName: str,
                       logStreamName: str,
                       logEvents: List[Dict[str, str]],
                       sequenceToken: str = None,
                       ) -> Response:
        """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_log_events"""
        params = {
            'logGroupName': logGroupName,
            'logStreamName': logStreamName,
            'logEvents': logEvents,
            'sequenceToken': sequenceToken,
        }
        result = self.client.put_log_events(**self._params_resolve(params))
        return Response(result)

    def put_log_event(self, *,
                      logGroupName: str,
                      logStreamName: str,
                      timestamp: int,
                      message: str,
                      sequenceToken: str = None,
                      ) -> Response:
        return self.put_log_events(
            logGroupName=logGroupName,
            logStreamName=logStreamName,
            logEvents=[
                {'timestamp': timestamp, 'message': message},
            ],
            sequenceToken=sequenceToken,
        )
