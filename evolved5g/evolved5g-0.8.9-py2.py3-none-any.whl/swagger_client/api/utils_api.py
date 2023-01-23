# coding: utf-8

"""
    NEF_Emulator

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.1.0

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from evolved5g.swagger_client.api_client import ApiClient


class UtilsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_item_api_v1_utils_monitoring_callback_post(self, body, **kwargs):  # noqa: E501
        """Create Item  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_item_api_v1_utils_monitoring_callback_post(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MonitoringEventReport body: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_item_api_v1_utils_monitoring_callback_post_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_item_api_v1_utils_monitoring_callback_post_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_item_api_v1_utils_monitoring_callback_post_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create Item  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_item_api_v1_utils_monitoring_callback_post_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MonitoringEventReport body: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_item_api_v1_utils_monitoring_callback_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_item_api_v1_utils_monitoring_callback_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/v1/utils/monitoring/callback', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def initiate_movement_api_v1_utils_start_loop_post(self, body, **kwargs):  # noqa: E501
        """Initiate Movement  # noqa: E501

        Start the loop.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.initiate_movement_api_v1_utils_start_loop_post(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Msg body: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.initiate_movement_api_v1_utils_start_loop_post_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.initiate_movement_api_v1_utils_start_loop_post_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def initiate_movement_api_v1_utils_start_loop_post_with_http_info(self, body, **kwargs):  # noqa: E501
        """Initiate Movement  # noqa: E501

        Start the loop.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.initiate_movement_api_v1_utils_start_loop_post_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Msg body: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method initiate_movement_api_v1_utils_start_loop_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `initiate_movement_api_v1_utils_start_loop_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            '/api/v1/utils/start-loop/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def state_movement_api_v1_utils_state_loop_supi_get(self, supi, **kwargs):  # noqa: E501
        """State Movement  # noqa: E501

        Get the state  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.state_movement_api_v1_utils_state_loop_supi_get(supi, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str supi: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.state_movement_api_v1_utils_state_loop_supi_get_with_http_info(supi, **kwargs)  # noqa: E501
        else:
            (data) = self.state_movement_api_v1_utils_state_loop_supi_get_with_http_info(supi, **kwargs)  # noqa: E501
            return data

    def state_movement_api_v1_utils_state_loop_supi_get_with_http_info(self, supi, **kwargs):  # noqa: E501
        """State Movement  # noqa: E501

        Get the state  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.state_movement_api_v1_utils_state_loop_supi_get_with_http_info(supi, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str supi: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['supi']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method state_movement_api_v1_utils_state_loop_supi_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'supi' is set
        if ('supi' not in params or
                params['supi'] is None):
            raise ValueError("Missing the required parameter `supi` when calling `state_movement_api_v1_utils_state_loop_supi_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'supi' in params:
            path_params['supi'] = params['supi']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            '/api/v1/utils/state-loop/{supi}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def terminate_movement_api_v1_utils_stop_loop_post(self, body, **kwargs):  # noqa: E501
        """Terminate Movement  # noqa: E501

        Stop the loop.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.terminate_movement_api_v1_utils_stop_loop_post(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Msg body: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.terminate_movement_api_v1_utils_stop_loop_post_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.terminate_movement_api_v1_utils_stop_loop_post_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def terminate_movement_api_v1_utils_stop_loop_post_with_http_info(self, body, **kwargs):  # noqa: E501
        """Terminate Movement  # noqa: E501

        Stop the loop.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.terminate_movement_api_v1_utils_stop_loop_post_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Msg body: (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method terminate_movement_api_v1_utils_stop_loop_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `terminate_movement_api_v1_utils_stop_loop_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            '/api/v1/utils/stop-loop/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def test_celery_api_v1_utils_test_celery_post(self, body, **kwargs):  # noqa: E501
        """Test Celery  # noqa: E501

        Test Celery worker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_celery_api_v1_utils_test_celery_post(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Msg body: (required)
        :return: Msg
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.test_celery_api_v1_utils_test_celery_post_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.test_celery_api_v1_utils_test_celery_post_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def test_celery_api_v1_utils_test_celery_post_with_http_info(self, body, **kwargs):  # noqa: E501
        """Test Celery  # noqa: E501

        Test Celery worker.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_celery_api_v1_utils_test_celery_post_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Msg body: (required)
        :return: Msg
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method test_celery_api_v1_utils_test_celery_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `test_celery_api_v1_utils_test_celery_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            '/api/v1/utils/test-celery/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Msg',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def test_email_api_v1_utils_test_email_post(self, email_to, **kwargs):  # noqa: E501
        """Test Email  # noqa: E501

        Test emails.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_email_api_v1_utils_test_email_post(email_to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str email_to: (required)
        :return: Msg
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.test_email_api_v1_utils_test_email_post_with_http_info(email_to, **kwargs)  # noqa: E501
        else:
            (data) = self.test_email_api_v1_utils_test_email_post_with_http_info(email_to, **kwargs)  # noqa: E501
            return data

    def test_email_api_v1_utils_test_email_post_with_http_info(self, email_to, **kwargs):  # noqa: E501
        """Test Email  # noqa: E501

        Test emails.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_email_api_v1_utils_test_email_post_with_http_info(email_to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str email_to: (required)
        :return: Msg
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['email_to']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method test_email_api_v1_utils_test_email_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'email_to' is set
        if ('email_to' not in params or
                params['email_to'] is None):
            raise ValueError("Missing the required parameter `email_to` when calling `test_email_api_v1_utils_test_email_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'email_to' in params:
            query_params.append(('email_to', params['email_to']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            '/api/v1/utils/test-email/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Msg',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
