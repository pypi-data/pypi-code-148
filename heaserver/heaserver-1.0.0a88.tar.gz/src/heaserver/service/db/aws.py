import configparser
from abc import ABC
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import partial

import base64
import boto3
import json
from aiohttp import hdrs, web
from aiohttp.web_request import Request

from heaobject.account import AWSAccount
from heaobject.bucket import AWSBucket
from heaobject.keychain import AWSCredentials, Credentials, CredentialTypeVar
from heaobject.registry import Property
from heaobject.root import DesktopObjectDict, DesktopObjectTypeVar
from heaobject.folder import AWSS3Folder
from heaobject.data import AWSS3FileObject
from heaobject.volume import AWSFileSystem, FileSystemTypeVar, Volume
from ..heaobjectsupport import type_to_resource_url
from heaserver.service import client
from yarl import URL
from . import database
from .database import Database, MicroserviceDatabaseManager
from ..testcase.collection import query_fixtures, query_content
from .awss3bucketobjectkey import decode_key
from typing import Optional, Any, Generator, Callable, Mapping, Type, Tuple, List
from configparser import ConfigParser
import asyncio
from io import BytesIO
import logging


class AWS(Database, ABC):
    """
    Connectivity to Amazon Web Services (AWS) for HEA microservices. Subclasses must call this constructor.
    """

    def __init__(self, config: Optional[configparser.ConfigParser], **kwargs) -> None:
        super().__init__(config, **kwargs)


class S3(AWS):
    """
    Connectivity to AWS Simple Storage Service (S3) for HEA microservices.
    """
    CLOUD_AWS_CRED_URL = "CLOUD_AWS_CRED_URL"
    EXPIRATION_LIMIT = 30  # aws constrains the max session to an hour so this value <= to that in minutes

    def __init__(self, config: Optional[ConfigParser], **kwargs):
        super().__init__(config, **kwargs)

    async def update_credentials(self, request: Request, credentials: AWSCredentials) -> None:
        """
        This is a wrapper function to be extended by tests
        It obtains credential's url from the registry and that makes PUT

        :param request:
        :param credentials:
        :returns: None if it succeeds otherwise it will raise ValueError or HTTPError
        """
        resource_url = await type_to_resource_url(request, Credentials)
        if not resource_url:
            raise ValueError(f'No service for type {Credentials.get_type_name()}')
        await client.put(app=request.app, url=URL(resource_url) / credentials.id, data=credentials,
                         headers=request.headers)

    async def get_property(self, app: web.Application, name: str) -> Optional[Property]:
        """
        This is a wrapper function to be extended by tests
        Gets the Property with the given name from the HEA registry service.

        :param app: the aiohttp app.
        :param name: the property's name.
        :return: a Property instance or None (if not found).
        """
        return await client.get_property(app=app, name=name)

    async def generate_cloud_credentials(self, request: Request, url: str, arn: str) -> Optional[AWSCredentials]:
        return await generate_cloud_credentials(request=request, url=url, arn=arn)

    async def get_file_system_and_credentials_from_volume(self, request: Request, volume_id) -> Tuple[
        FileSystemTypeVar, Optional[CredentialTypeVar]]:
        return await database.get_file_system_and_credentials_from_volume(request, volume_id, AWSFileSystem,
                                                                          AWSCredentials)

    async def get_client(self, request: Request, service_name: str, volume_id: str) -> Any:
        """
        Gets an AWS service client.  If the volume has no credentials, it uses the boto3 library to try and find them.
        This method is not designed to be overridden.

        :param request: the HTTP request (required).
        :param service_name: AWS service name (required).
        :param volume_id: the id string of a volume (required).
        :return: a Mongo client for the file system specified by the volume's file_system_name attribute. If no volume_id
        was provided, the return value will be the "default" Mongo client for the microservice found in the HEA_DB
        application-level property.
        :raise ValueError: if there is no volume with the provided volume id, the volume's file system does not exist,
        the volume's credentials were not found, or a necessary service is not registered.
        """
        logger = logging.getLogger(__name__)
        if volume_id is not None:
            file_system, credentials = \
                await self.get_file_system_and_credentials_from_volume(request, volume_id)
            logger.info(
                "credentials retrieved from database checking if expired: %s" % credentials.to_dict() if credentials else None)
            loop = asyncio.get_running_loop()
            cloud_aws_cred_prop = await self.get_property(app=request.app, name=S3.CLOUD_AWS_CRED_URL)
            if cloud_aws_cred_prop:
                # not sure this code for 'POST' makes sense because if you can't get the arn from credentials you can't
                # call generate_cloud_creds. Likely need call POST credentials just after user
                # if credentials is None:
                #     logger.info("generating new credentials from api gateway")
                #     cloud_creds = await generate_cloud_credentials(request=request, url=cloud_aws_cred_url, account_id="")
                #     resp_url = await client.post(app=request.app, url=resource_url, data=cloud_creds, headers={hdrs.CONTENT_TYPE:"application/json"} )
                #     cloud_creds.id = resp_url[len(resource_url) + 1:] if type(resp_url) is str else None
                #     if not cloud_creds.id:
                #         raise ValueError("Credentials could not be created")
                #     volume.credential_id = cloud_creds.id
                #     await client.put(app=request.app, url= resource_url, data=volume, headers= request.headers)
                #     credentials = cloud_creds

                if credentials:
                    cloud_aws_cred_url = cloud_aws_cred_prop.value
                    logger.info("retrieved the aws api gateway %s" % cloud_aws_cred_url)
                    if credentials.has_expired(S3.EXPIRATION_LIMIT):
                        cloud_creds = await self.generate_cloud_credentials(request=request,
                                                                            url=cloud_aws_cred_url,
                                                                            arn=credentials.role_arn)
                        if not cloud_creds:
                            raise ValueError(f'Could not generate cloud credentials with {cloud_aws_cred_url} '
                                             f'and these params {credentials.role_arn}')
                        credentials.account = cloud_creds.account
                        credentials.password = cloud_creds.password
                        credentials.session_token = cloud_creds.session_token
                        credentials.expiration = cloud_creds.expiration
                        logger.info("credentials retrieved from cloud to be updated: %s" % credentials.to_dict())
                        await self.update_credentials(request=request, credentials=credentials)
                else:
                    raise ValueError('No credentials associated with volume')

            if not credentials:  # delegate to boto3 to find the credentials
                return await loop.run_in_executor(None, boto3.client, service_name)

            return await loop.run_in_executor(None, partial(boto3.client, service_name,
                                                            region_name=credentials.where,
                                                            aws_access_key_id=credentials.account,
                                                            aws_secret_access_key=credentials.password,
                                                            aws_session_token=credentials.session_token))

        else:
            raise ValueError('volume_id is required')

    async def get_resource(self, request: Request, service_name: str, volume_id: str) -> Any:
        """
        Gets an AWS resource. If the volume has no credentials, it uses the boto3 library to try and find them. This
        method is not designed to be overridden.

        :param request: the HTTP request (required).
        :param service_name: AWS service name (required).
        :param volume_id: the id string of a volume (required).
        :return: a Mongo client for the file system specified by the volume's file_system_name attribute. If no volume_id
        was provided, the return value will be the "default" Mongo client for the microservice found in the HEA_DB
        application-level property.
        :raise ValueError: if there is no volume with the provided volume id, the volume's file system does not exist,
        the volume's credentials were not found, or a necessary service is not registered.
        """
        logger = logging.getLogger(__name__)
        if volume_id is not None:
            file_system, credentials = await self.get_file_system_and_credentials_from_volume(request,volume_id)
            logger.info(
                "credentials retrieved from database checking if expired: %s" % credentials.to_dict() if credentials else None)
            loop = asyncio.get_running_loop()
            cloud_aws_cred_prop = await self.get_property(app=request.app, name=S3.CLOUD_AWS_CRED_URL)
            if cloud_aws_cred_prop:
                if credentials:
                    cloud_aws_cred_url = cloud_aws_cred_prop.value
                    logger.info("retrieved the aws api gateway %s" % cloud_aws_cred_url)
                    if credentials.has_expired(S3.EXPIRATION_LIMIT):
                        cloud_creds = await self.generate_cloud_credentials(request=request,
                                                                            url=cloud_aws_cred_url,
                                                                            arn=credentials.role_arn)
                        if not cloud_creds:
                            raise ValueError(f'Could not generate cloud credentials with {cloud_aws_cred_url} '
                                             f'and these params {credentials.role_arn}')
                        credentials.account = cloud_creds.account
                        credentials.password = cloud_creds.password
                        credentials.session_token = cloud_creds.session_token
                        credentials.expiration = cloud_creds.expiration
                        logger.info("credentials retrieved from cloud to be updated: %s" % credentials.to_dict())
                        await self.update_credentials(request=request, credentials=credentials)
                else:
                    raise ValueError('No credentials associated with volume')

            if not credentials:  # delegate to boto3 to find the credentials
                return await loop.run_in_executor(None, boto3.resource, service_name)

            return await loop.run_in_executor(None, partial(boto3.resource, service_name,
                                                            region_name=credentials.where,
                                                            aws_access_key_id=credentials.account,
                                                            aws_secret_access_key=credentials.password,
                                                            aws_session_token=credentials.session_token))
        else:
            raise ValueError('volume_id is required')


class S3Manager(MicroserviceDatabaseManager):
    """
    Database manager for mock Amazon Web Services S3 buckets. It will not make any calls to actual S3 buckets. This
    class is not designed to be subclassed.
    """

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[S3, None, None]:
        yield S3(config)

    def insert_desktop_objects(self, desktop_objects: Optional[Mapping[str, list[DesktopObjectDict]]]):
        super().insert_desktop_objects(desktop_objects)
        logger = logging.getLogger(__name__)
        for coll, objs in query_fixtures(desktop_objects, db_manager=self).items():
            logger.debug('Inserting %s collection object %s', coll, objs)
            inserters = self.get_desktop_object_inserters()
            if coll in inserters:
                inserters[coll](objs)

    def insert_content(self, content: Optional[Mapping[str, Mapping[str, bytes]]]):
        super().insert_content(content)
        if content is not None:
            client = boto3.client('s3')
            for key, contents in query_content(content, db_manager=self).items():
                if key == 'awss3files':
                    for id_, content_ in contents.items():
                        with BytesIO(content_) as f:
                            client.upload_fileobj(f, 'arp-scale-2-cloud-bucket-with-tags11', decode_key(id_))
                else:
                    raise KeyError(f'Unexpected key {key}')

    @classmethod
    def get_desktop_object_inserters(cls) -> dict[str, Callable[[list[DesktopObjectDict]], None]]:
        return {'awsaccounts': cls.__awsaccount_inserter,
                'buckets': cls.__bucket_inserter,
                'awss3folders': cls.__awss3folder_inserter,
                'awss3files': cls.__awss3file_inserter}

    @classmethod
    def __awss3file_inserter(cls, v):
        for awss3file_dict in v:
            awss3file = AWSS3FileObject()
            awss3file.from_dict(awss3file_dict)
            cls.__create_awss3file(awss3file)

    @classmethod
    def __awss3folder_inserter(cls, v):
        for awss3folder_dict in v:
            awss3folder = AWSS3Folder()
            awss3folder.from_dict(awss3folder_dict)
            cls.__create_awss3folder(awss3folder)

    @classmethod
    def __bucket_inserter(cls, v):
        for bucket_dict in v:
            awsbucket = AWSBucket()
            awsbucket.from_dict(bucket_dict)
            cls.__create_bucket(awsbucket)

    @classmethod
    def __awsaccount_inserter(cls, v):
        for awsaccount_dict in v:
            awsaccount = AWSAccount()
            awsaccount.from_dict(awsaccount_dict)
            cls.__create_awsaccount(awsaccount)

    @staticmethod
    def __create_awsaccount(account: AWSAccount):
        client = boto3.client('organizations')
        client.create_account(Email=account.email_address, AccountName=account.display_name)

    @staticmethod
    def __create_bucket(bucket: AWSBucket):
        client = boto3.client('s3')
        if bucket is not None:
            if bucket.name is None:
                raise ValueError('bucket.name cannot be None')
            else:
                if bucket.region != 'us-east-1' and bucket.region:
                    client.create_bucket(Bucket=bucket.name,
                                         CreateBucketConfiguration={'LocationConstraint': bucket.region})
                else:
                    client.create_bucket(Bucket=bucket.name)

    @staticmethod
    def __create_awss3folder(awss3folder: AWSS3Folder):
        client = boto3.client('s3')
        client.put_object(Bucket='arp-scale-2-cloud-bucket-with-tags11', Key=awss3folder.display_name + '/')

    @staticmethod
    def __create_awss3file(awss3file):
        client = boto3.client('s3')
        client.put_object(Bucket='arp-scale-2-cloud-bucket-with-tags11', Key=awss3file.display_name)


async def generate_cloud_credentials(request: Request, url: str, arn: str) -> Optional[AWSCredentials]:
    """
    :param request: the HTTP request (required).
    :param url: the aws api gateway url to make the http request
    :param arn: The aws role arn that to be assumed
    :returns the AWSCredentials populated with the resource's content, None if no such resource exists, or another HTTP
    status code if an error occurred.
    """
    if not arn:
        raise ValueError('Cannot get credentials arn which is required')
    auth: List[str] = request.headers.get(hdrs.AUTHORIZATION, '').split(' ')

    if not len(auth) == 2:
        raise ValueError("Bearer Token is required in header")

    params_ = {"role": arn}
    return await client.get(app=request.app, url=url, type_or_obj=AWSCredentials, query_params=params_,
                            headers={hdrs.AUTHORIZATION: request.headers[hdrs.AUTHORIZATION]})
