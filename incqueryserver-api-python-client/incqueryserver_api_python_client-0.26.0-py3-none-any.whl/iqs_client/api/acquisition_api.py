# coding: utf-8

"""
    IncQuery Server Web API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: placeHolderApiVersion
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from iqs_client.api_client import ApiClient
from iqs_client.exceptions import (
    ApiTypeError,
    ApiValueError
)


class AcquisitionApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def acquire_linked_data(self, linked_data_acquisition_request_multipart, **kwargs):  # noqa: E501
        """Acquire a linked data document as a model compartment.  # noqa: E501

        Upload one or more RDF documents (in various formats) and add their contents to the model index under the specified model compartment URI.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.acquire_linked_data(linked_data_acquisition_request_multipart, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param LinkedDataAcquisitionRequestMultipart linked_data_acquisition_request_multipart: Upload a linked data file.  (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SimpleMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.acquire_linked_data_with_http_info(linked_data_acquisition_request_multipart, **kwargs)  # noqa: E501

    def acquire_linked_data_with_http_info(self, linked_data_acquisition_request_multipart, **kwargs):  # noqa: E501
        """Acquire a linked data document as a model compartment.  # noqa: E501

        Upload one or more RDF documents (in various formats) and add their contents to the model index under the specified model compartment URI.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.acquire_linked_data_with_http_info(linked_data_acquisition_request_multipart, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param LinkedDataAcquisitionRequestMultipart linked_data_acquisition_request_multipart: Upload a linked data file.  (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SimpleMessage, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['linked_data_acquisition_request_multipart']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method acquire_linked_data" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'linked_data_acquisition_request_multipart' is set
        if self.api_client.client_side_validation and ('linked_data_acquisition_request_multipart' not in local_var_params or  # noqa: E501
                                                        local_var_params['linked_data_acquisition_request_multipart'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `linked_data_acquisition_request_multipart` when calling `acquire_linked_data`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'linked_data_acquisition_request_multipart' in local_var_params:
            body_params = local_var_params['linked_data_acquisition_request_multipart']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/demo.acquireLinkedData', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SimpleMessage',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def close_acquisition(self, close_acquisition_request, **kwargs):  # noqa: E501
        """End the acquistion of a compartment, either by finalizing or discarding  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.close_acquisition(close_acquisition_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CloseAcquisitionRequest close_acquisition_request: Close an open acquisition, either successfully or with failure (discard).  (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CloseAcquisitionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.close_acquisition_with_http_info(close_acquisition_request, **kwargs)  # noqa: E501

    def close_acquisition_with_http_info(self, close_acquisition_request, **kwargs):  # noqa: E501
        """End the acquistion of a compartment, either by finalizing or discarding  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.close_acquisition_with_http_info(close_acquisition_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CloseAcquisitionRequest close_acquisition_request: Close an open acquisition, either successfully or with failure (discard).  (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(CloseAcquisitionResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['close_acquisition_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method close_acquisition" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'close_acquisition_request' is set
        if self.api_client.client_side_validation and ('close_acquisition_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['close_acquisition_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `close_acquisition_request` when calling `close_acquisition`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'close_acquisition_request' in local_var_params:
            body_params = local_var_params['close_acquisition_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/acquisition.close', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CloseAcquisitionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def start_acquisition(self, model_compartment, **kwargs):  # noqa: E501
        """Start the acquistion of a compartment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.start_acquisition(model_compartment, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ModelCompartment model_compartment: Model compartment descriptor.  (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: StartAcquisitionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.start_acquisition_with_http_info(model_compartment, **kwargs)  # noqa: E501

    def start_acquisition_with_http_info(self, model_compartment, **kwargs):  # noqa: E501
        """Start the acquistion of a compartment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.start_acquisition_with_http_info(model_compartment, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ModelCompartment model_compartment: Model compartment descriptor.  (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(StartAcquisitionResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['model_compartment']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method start_acquisition" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'model_compartment' is set
        if self.api_client.client_side_validation and ('model_compartment' not in local_var_params or  # noqa: E501
                                                        local_var_params['model_compartment'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `model_compartment` when calling `start_acquisition`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'model_compartment' in local_var_params:
            body_params = local_var_params['model_compartment']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/acquisition.start', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='StartAcquisitionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def upload_acquisition_chunk(self, upload_chunk_request, **kwargs):  # noqa: E501
        """Uploads a chunk of content as part of an open acquisition  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_acquisition_chunk(upload_chunk_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param UploadChunkRequest upload_chunk_request: Contribute a chunk of model data to a compartment.  (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SimpleMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.upload_acquisition_chunk_with_http_info(upload_chunk_request, **kwargs)  # noqa: E501

    def upload_acquisition_chunk_with_http_info(self, upload_chunk_request, **kwargs):  # noqa: E501
        """Uploads a chunk of content as part of an open acquisition  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_acquisition_chunk_with_http_info(upload_chunk_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param UploadChunkRequest upload_chunk_request: Contribute a chunk of model data to a compartment.  (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SimpleMessage, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['upload_chunk_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_acquisition_chunk" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'upload_chunk_request' is set
        if self.api_client.client_side_validation and ('upload_chunk_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['upload_chunk_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `upload_chunk_request` when calling `upload_acquisition_chunk`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'upload_chunk_request' in local_var_params:
            body_params = local_var_params['upload_chunk_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/acquisition.uploadChunk', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SimpleMessage',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
