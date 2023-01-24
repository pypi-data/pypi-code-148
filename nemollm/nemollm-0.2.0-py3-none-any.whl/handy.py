from multiprocessing.pool import ApplyResult
from typing import Any, Dict, List, Optional, Tuple, Union

from nemollm.api.default_api import DefaultApi
from nemollm.api_client import ApiClient
from nemollm.configuration import Configuration
from nemollm.model.completion_request_body import CompletionRequestBody
from nemollm.model.completion_response_body import CompletionResponseBody
from nemollm.model.create_customizations_request_body import CreateCustomizationsRequestBody
from nemollm.model.create_customizations_request_body_additional_hyperparameters import (
    CreateCustomizationsRequestBodyAdditionalHyperparameters,
)
from nemollm.model.customization import Customization
from nemollm.model.customizations_list_response_body import CustomizationsListResponseBody
from nemollm.model.file import File
from nemollm.model.file_format import FileFormat
from nemollm.model.models_list_response import ModelsListResponse
from nemollm.model.p_tuning_hyperparms import PTuningHyperparms


class Connection:
    """
    A wrapper which contains instances of ``nemollm.api_client.ApiClient`` and
    ``nemollm.api.default_api.DefaultApi`` and routes create_customization(), delete_customization(), delete_file(), fetch_model_file_for_customization(), generate_completion(), generate_customization_completion(), get_customization(), get_file(), list_customizations(), list_customizations_for_model(), list_files(), list_models(), upload_file(),  to
    corresponding methods of ``nemollm.api.default_api.DefaultApi``.
    """

    def __init__(
        self,
        # `nemollm.configuration.Configuration.__init__()` parameters
        host: Optional[str] = "https://api.llm.ngc.nvidia.com/v1",
        api_key: Optional[Dict[str, str]] = None,
        api_key_prefix: Optional[Dict[str, str]] = None,
        access_token: str = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        discard_unknown_keys: bool = False,
        disabled_client_side_validations: str = "",
        server_index: Optional[int] = None,
        server_variables: Dict[str, Any] = None,
        server_operation_index: Optional[Dict[str, int]] = None,
        server_operation_variables: Optional[Dict[str, Dict[str, str]]] = None,
        ssl_ca_cert: Optional[str] = None,
        # `nemollm.api_client.ApiClient.__init__()` parameters except for `configuration`
        header_name: Optional[str] = None,
        header_value: Optional[str] = None,
        cookie=None,
        pool_threads: int = 1,
        **kwargs
    ):

        """
        This constructor accepts parameters of `nemollm.configuration.Configuration.__init__()` and
        `nemollm.api_client.ApiClient.__init__()`.

        Ref: https://openapi-generator.tech
        Do not edit the class manually.

        :param host: Base url, defaults to "https://api.llm.ngc.nvidia.com/v1"
        :param api_key: Dict to store API key(s).
            Each entry in the dict specifies an API key.
            The dict key is the name of the security scheme in the OAS specification.
            The dict value is the API key secret.
        :param api_key_prefix: Dict to store API prefix (e.g. Bearer)
            The dict key is the name of the security scheme in the OAS specification.
            The dict value is an API key prefix when generating the auth data.
        :param username: Username for HTTP basic authentication
        :param password: Password for HTTP basic authentication
        :param discard_unknown_keys: Boolean value indicating whether to discard
            unknown properties. A server may send a response that includes additional
            properties that are not known by the client in the following scenarios:
            1. The OpenAPI document is incomplete, i.e. it does not match the server
             implementation.
            2. The client was generated using an older version of the OpenAPI document
             and the server has been upgraded since then.
            If a schema in the OpenAPI document defines the additionalProperties attribute,
            then all undeclared properties received by the server are injected into the
            additional properties map. In that case, there are undeclared properties, and
            nothing to discard.
        :param disabled_client_side_validations (string): Comma-separated list of
            JSON schema validation keywords to disable JSON schema structural validation
            rules. The following keywords may be specified: multipleOf, maximum,
            exclusiveMaximum, minimum, exclusiveMinimum, maxLength, minLength, pattern,
            maxItems, minItems.
            By default, the validation is performed for data generated locally by the client
            and data received from the server, independent of any validation performed by
            the server side. If the input data does not satisfy the JSON schema validation
            rules specified in the OpenAPI document, an exception is raised.
            If disabled_client_side_validations is set, structural validation is
            disabled. This can be useful to troubleshoot data validation problem, such as
            when the OpenAPI document validation rules do not match the actual API data
            received by the server.
        :param server_index: Index to servers configuration.
        :param server_variables: Mapping with string values to replace variables in
            templated server configuration. The validation of enums is performed for
            variables with defined enum values before.
        :param server_operation_index: Mapping from operation ID to an index to server
            configuration.
        :param server_operation_variables: Mapping from operation ID to a mapping with
            string values to replace variables in templated server configuration.
            The validation of enums is performed for variables with defined enum values before.
        :param ssl_ca_cert: str - the path to a file of concatenated CA certificates
            in PEM format
        :param header_name: a header to pass when making calls to the API.
        :param header_value: a header value to pass when making calls to
            the API.
        :param cookie: a cookie to include in the header when making calls
            to the API
        :param pool_threads: The number of threads to use for async requests
            to the API. More threads means more concurrent API requests.
        """
        configuration = Configuration(
            host=host,
            api_key=api_key,
            api_key_prefix=api_key_prefix,
            access_token=access_token,
            username=username,
            password=password,
            discard_unknown_keys=discard_unknown_keys,
            disabled_client_side_validations=disabled_client_side_validations,
            server_index=server_index,
            server_variables=server_variables,
            server_operation_index=server_operation_index,
            server_operation_variables=server_operation_variables,
            ssl_ca_cert=ssl_ca_cert,
        )
        self.api_client = ApiClient(
            configuration, header_name=header_name, header_value=header_value, cookie=cookie, pool_threads=pool_threads
        )
        self.api_instance = DefaultApi(self.api_client)

    def create_customization(
        self,
        model_id="gpt530b",
        name="",
        description="",
        prompt_template="",
        shared="private",
        training_dataset_file_id="",
        validation_dataset_file_id="",
        batch_size=64,
        epochs=25,
        learning_rate=0.00010,
        additional_hyperparameters: Union[
            CreateCustomizationsRequestBodyAdditionalHyperparameters, PTuningHyperparms
        ] = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        model_id = model_id
        create_customizations_request_body = CreateCustomizationsRequestBody(
            name=name,
            description=description,
            prompt_template=prompt_template,
            shared=shared,
            training_dataset_file_id=training_dataset_file_id,
            validation_dataset_file_id=validation_dataset_file_id,
            batch_size=batch_size,
            epochs=epochs,
            learning_rate=learning_rate,
            additional_hyperparameters=additional_hyperparameters,
        )

        # Create model customization
        return self.api_instance.create_customization(
            model_id,
            create_customizations_request_body=create_customizations_request_body,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def delete_customization(
        self,
        model_id="gpt530b",
        customization_id="QnA",
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        model_id = model_id
        customization_id = customization_id

        # Delete the custom model
        return self.api_instance.delete_customization(
            model_id,
            customization_id,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def delete_file(
        self,
        file_id="file_id_example",
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        file_id = file_id

        # Delete file
        return self.api_instance.delete_file(
            file_id,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def fetch_model_file_for_customization(
        self,
        model_id="gpt530b",
        customization_id="QnA",
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        model_id = model_id
        customization_id = customization_id

        # Fetch NEMO file with trained prompt tokens
        return self.api_instance.fetch_model_file_for_customization(
            model_id,
            customization_id,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def generate_completion(
        self,
        model_id="gpt530b",
        prompt="",
        tokens_to_generate=24,
        logprobs=False,
        temperature=1.0,
        top_p=1.0,
        top_k=1,
        stop=[],
        random_seed=0,
        repetition_penalty=1.0,
        beam_search_diversity_rate=1.0,
        beam_width=1,
        length_penalty=1.0,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        model_id = model_id
        completion_request_body = CompletionRequestBody(
            prompt=prompt,
            tokens_to_generate=tokens_to_generate,
            logprobs=logprobs,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            random_seed=random_seed,
            repetition_penalty=repetition_penalty,
            beam_search_diversity_rate=beam_search_diversity_rate,
            beam_width=beam_width,
            length_penalty=length_penalty,
        )

        # Create text completion
        return self.api_instance.generate_completion(
            model_id,
            completion_request_body=completion_request_body,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def generate_customization_completion(
        self,
        model_id="gpt530b",
        customization_id="QnA",
        prompt="",
        tokens_to_generate=24,
        logprobs=False,
        temperature=1.0,
        top_p=1.0,
        top_k=1,
        stop=[],
        random_seed=0,
        repetition_penalty=1.0,
        beam_search_diversity_rate=1.0,
        beam_width=1,
        length_penalty=1.0,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        model_id = model_id
        customization_id = customization_id
        completion_request_body = CompletionRequestBody(
            prompt=prompt,
            tokens_to_generate=tokens_to_generate,
            logprobs=logprobs,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            random_seed=random_seed,
            repetition_penalty=repetition_penalty,
            beam_search_diversity_rate=beam_search_diversity_rate,
            beam_width=beam_width,
            length_penalty=length_penalty,
        )

        # Create text completion with customized model
        return self.api_instance.generate_customization_completion(
            model_id,
            customization_id,
            completion_request_body=completion_request_body,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def get_customization(
        self,
        model_id="gpt530b",
        customization_id="QnA",
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        model_id = model_id
        customization_id = customization_id

        # Get info about model customization
        return self.api_instance.get_customization(
            model_id,
            customization_id,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def get_file(
        self,
        file_id="file_id_example",
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        file_id = file_id

        # Get file
        return self.api_instance.get_file(
            file_id,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def list_customizations(
        self,
        shared="private",
        page=1,
        page_size=15,
        sort_by="created_at",
        order="desc",
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        shared = shared
        page = page
        page_size = page_size
        sort_by = sort_by
        order = order

    def list_customizations_for_model(
        self,
        model_id="gpt530b",
        shared="private",
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        model_id = model_id
        shared = shared

        # List customizations for a specific model
        return self.api_instance.list_customizations_for_model(
            model_id,
            shared=shared,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )

    def list_files(
        self,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        return self.api_instance.list_files()

    def list_models(
        self,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        return self.api_instance.list_models()

    def upload_file(
        self,
        file='/path/to/file',
        format=FileFormat("jsonl"),
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
        _check_input_type: bool = True,
        _check_return_type: bool = True,
        _content_type: Optional[str] = None,
        _host_index: Optional[int] = None,
        _request_auths: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        file = open(file, 'rb')
        format = format

        # Upload file
        return self.api_instance.upload_file(
            file,
            format,
            async_req=async_req,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
            _check_input_type=_check_input_type,
            _check_return_type=_check_return_type,
            _content_type=_content_type,
            _host_index=_host_index,
            _request_auths=_request_auths,
            **kwargs
        )
