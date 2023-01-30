import inspect
import logging
import os
import shutil
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

from aws_cdk import Duration
from aws_cdk import Resource as AwsResource
from aws_cdk import (
    Stack,
    aws_apigateway,
    aws_ec2,
    aws_events,
    aws_events_targets,
    aws_lambda,
    aws_lambda_event_sources,
    aws_lambda_python_alpha,
    aws_s3,
    aws_sqs,
)
from constructs import Construct

from viburnum.application import (
    S3,
    Application,
    Handler,
    Resource,
    ResourceConnector,
    S3Permission,
    Sqs,
    SqsPermission,
)
from viburnum.application.connectors import S3Connector, SqsConnector
from viburnum.application.handlers import ApiHandler, JobHandler, S3Handler, SqsHandler
from viburnum.deployer.configuration import Configuration


class BuilderException(Exception):
    pass


class ResourceAlreadyRegistered(BuilderException):
    def __init__(self, resource_name: str) -> None:
        self.resource_name = resource_name
        super().__init__(f"Resource '{resource_name}' already defined in stack!")


class ResourceNotDefined(BuilderException):
    def __init__(self, resource_name: str) -> None:
        self.resource_name = resource_name
        super().__init__(f"Resource '{resource_name}' not defined!")


def get_builder_class(primitive):
    return getattr(sys.modules[__name__], f"{primitive.__class__.__name__}Builder")


def prepare_name(name: str) -> str:
    return "".join([s.capitalize() for s in name.replace("_", "-").split("-")])


class AppStack(Stack):
    def __init__(self, scope: Construct, app: Application, **kwargs) -> None:
        self.app_ = app
        self.built_resources_ = {}
        self.required_layers = []
        self.config = Configuration.get_configuration()

        super().__init__(scope, app.name, env=self.config.env, **kwargs)

        self._build_layers()
        self._build_resources()
        self._build_handlers()

    def _build_resources(self):
        for resource in self.app_.resources.values():
            builder_class = getattr(
                sys.modules[__name__], f"{resource.__class__.__name__}Builder"
            )
            # FIXME: raise error if there were resources with identical names
            aws_resource = builder_class(self, resource).build()
            self._register_resource(resource.name, aws_resource)

    def _register_resource(self, name: str, resource: AwsResource) -> None:
        """Register resource in application

        Args:
            name (str): resource unique name
            resource (AwsResource): construct that represent aws resource

        Raises:
            ResourceAlreadyRegistered: if resource with such name already registered
        """
        if name in self.built_resources_:
            raise ResourceAlreadyRegistered(name)
        self.built_resources_[name] = resource

    def _build_handlers(self):
        for handler in self.app_.handlers:
            handler_class = getattr(
                sys.modules[__name__], f"{handler.__class__.__name__}Builder"
            )
            handler_class(self, handler).build()

    def _build_layers(self):
        lib_folder = Path("./.layers")
        if not lib_folder.exists():
            os.mkdir(str(lib_folder))

        if Path("./shared").exists():
            self._prepare_shared_layer()
            self._build_shared_layer()
        self._prepare_libraries_layer()
        self._build_lib_layer()

    def _prepare_shared_layer(self):
        logging.info("Preparing shared layer")
        shared_layer_folder = Path("./.layers/shared")
        if os.path.exists(shared_layer_folder):
            shutil.rmtree(shared_layer_folder)
        os.mkdir(shared_layer_folder)
        shutil.copytree("shared", str(shared_layer_folder.joinpath("shared")))

    def _prepare_libraries_layer(self):
        # TODO: create requirements only if requirements.txt was changed
        logging.info("Preparing libraries layer")
        lib_layer_folder = Path("./.layers/lib")
        if os.path.exists(lib_layer_folder):
            shutil.rmtree(lib_layer_folder)
        os.mkdir(lib_layer_folder)
        shutil.copy("requirements.txt", str(lib_layer_folder))

    def _build_shared_layer(self):
        self._shared_layer = aws_lambda_python_alpha.PythonLayerVersion(
            self,
            "SharedLayer",
            entry=str(Path("./.layers/shared")),
            compatible_runtimes=[self.config.python_version],
        )
        self.required_layers.append(self._shared_layer)

    def _build_lib_layer(self):
        self._lib_layer = aws_lambda_python_alpha.PythonLayerVersion(
            self,
            "LibLayer",
            entry=str(Path("./.layers/lib")),
            compatible_runtimes=[self.config.python_version],
        )
        self.required_layers.append(self._lib_layer)

    def _build_sqs(self, sqs: Sqs):
        queue = aws_sqs.Queue(
            self, sqs.name, visibility_timeout=Duration.seconds(sqs.visibility_timeout)
        )
        self.built_resources_[sqs.name] = queue
        return queue

    def get_built_resource(self, name: str):
        if name not in self.built_resources_:
            raise ResourceNotDefined(name)
        return self.built_resources_[name]


# ______________ Handler Builders __________________ #


HandlerType = TypeVar("HandlerType", bound=Handler)


class HandlerBuilder(Generic[HandlerType]):
    def __init__(self, context: "AppStack", handler: HandlerType) -> None:
        self.context = context
        self.handler = handler

    def _build_lambda(self):
        dir_ = Path(inspect.getfile(self.handler.func)).parent

        # TODO: add more config options
        lambda_fn = aws_lambda.Function(
            self.context,
            prepare_name(self.handler.name),
            **{
                **{
                    "runtime": self.context.config.python_version,
                    "handler": f"handler.{self.handler.func.__name__}",
                    "code": aws_lambda.Code.from_asset(str(dir_)),
                    "environment": {
                        "APP_NAME": self.context.app_.name,
                    },
                    "layers": self.context.required_layers,
                },
                **self._get_vpc_config(),
                **self._get_handler_config(),
            },
        )

        return lambda_fn

    def _get_vpc_config(self) -> dict:
        # TODO: add vpc config only if we allow it for lambda
        vpc_config = {}
        if self.context.config.vpc_id:
            vpc_config.update(
                {
                    "vpc": aws_ec2.Vpc.from_lookup(
                        self.context,
                        self.context.config.vpc_id,
                        vpc_id=self.context.config.vpc_id,
                    ),
                    "vpc_subnets": aws_ec2.SubnetSelection(
                        subnets=[
                            aws_ec2.Subnet.from_subnet_id(self.context, s_id, s_id)
                            for s_id in self.context.config.subnets_ids  # type: ignore
                        ]
                    ),
                    "security_groups": [
                        aws_ec2.SecurityGroup.from_lookup_by_id(
                            self.context,
                            self.context.config.security_group_id,  # type: ignore
                            self.context.config.security_group_id,  # type: ignore
                        )
                    ],
                    "allow_public_subnet": self.context.config.allow_public_subnet,
                }
            )
        return vpc_config

    def _get_handler_config(self) -> dict:
        return {
            "reserved_concurrent_executions": self.handler.reserved_concurrent_executions
            or self.context.config.lambda_defaults.reserved_concurrent_executions,
            "memory_size": self.handler.memory
            or self.context.config.lambda_defaults.memory_size,
            "timeout": Duration.seconds(
                self.handler.timeout or self.context.config.lambda_defaults.timeout
            ),
            "environment": {
                **self.context.config.lambda_defaults.env_variables,
                **self.handler.env_variables,
            },
        }

    def _connect_resources(self, lambda_: aws_lambda.Function):
        # FIXME: very bad pattern
        for connector in self.handler.resources:
            get_builder_class(connector)(self.context, connector, lambda_).build()

    def build(self):
        # TODO: rework inheritance
        lambda_ = self._build_lambda()
        self._connect_resources(lambda_)
        return lambda_


class ApiHandlerBuilder(HandlerBuilder[ApiHandler]):
    api_ = None

    @property
    def api(self) -> aws_apigateway.RestApi:
        if not self.__class__.api_:
            self.__class__.api_ = aws_apigateway.RestApi(
                self.context,
                f"RestApi",
                deploy_options=aws_apigateway.StageOptions(
                    stage_name=self.context.config.env_name
                ),
            )
        return self.__class__.api_

    def build(self):
        lambda_ = super().build()
        self._build_endpoint(lambda_)
        return lambda_

    def _build_endpoint(self, lambda_: aws_lambda.Function):
        # TODO: investigate what is allow_test_invoke
        integration = aws_apigateway.LambdaIntegration(lambda_, allow_test_invoke=False)  # type: ignore

        endpoint = self.api.root
        for path_part in (p for p in self.handler.path.split("/") if p):
            endpoint = endpoint.get_resource(path_part) or endpoint.add_resource(
                path_part
            )
        for method in self.handler.methods:
            endpoint.add_method(method, integration)


class JobHandlerBuilder(HandlerBuilder[JobHandler]):
    def build(self):
        lambda_ = super().build()
        self._build_rule(lambda_)
        return lambda_

    def _build_rule(self, lambda_):
        aws_events.Rule(
            self.context,
            f"{prepare_name(self.handler.name)}Rule",
            schedule=aws_events.Schedule.expression(self.handler.schedule),
            targets=[aws_events_targets.LambdaFunction(lambda_)],
        )


class SqsHandlerBuilder(HandlerBuilder[SqsHandler]):
    def build(self):
        lambda_ = super().build()
        self._handler_connect_queue(lambda_)
        return lambda_

    def _handler_connect_queue(self, lambda_: aws_lambda.Function):
        queue: aws_sqs.Queue = self.context.get_built_resource(self.handler.queue_name)
        # TODO: add more config options including enabling report_batch_item_failure
        _sqs_event_source = aws_lambda_event_sources.SqsEventSource(queue)
        lambda_.add_event_source(_sqs_event_source)


class S3HandlerBuilder(HandlerBuilder[S3Handler]):
    def build(self):
        lambda_ = super().build()
        self._handler_connect_bucket(lambda_)

    def _handler_connect_bucket(self, lambda_: aws_lambda.Function):
        bucket = aws_s3.Bucket = self.context.get_built_resource(
            self.handler.bucket_name
        )
        # FIXME: add events
        events_ = [getattr(aws_s3.EventType, e.name) for e in self.handler.events]
        filters_ = []
        _s3_event_source = aws_lambda_event_sources.S3EventSource(
            bucket, events=events_, filters=filters_
        )
        lambda_.add_event_source(_s3_event_source)


# ______________ Resource Builders __________________ #


ResourceType = TypeVar("ResourceType", bound=Resource)


class ResourceBuilder(ABC, Generic[ResourceType]):
    def __init__(self, context: "AppStack", resource: ResourceType) -> None:
        self.context = context
        self.resource = resource

    @abstractmethod
    def build(self):
        ...


class SqsBuilder(ResourceBuilder[Sqs]):
    def build(self):
        # TODO: add more config options
        queue = aws_sqs.Queue(
            self.context,
            prepare_name(self.resource.name),
            visibility_timeout=Duration.seconds(self.resource.visibility_timeout),
        )
        return queue


class S3Builder(ResourceBuilder[S3]):
    def build(self):
        bucket = aws_s3.Bucket(
            self.context,
            prepare_name(self.resource.name),
            # bucket_name=f"{self.resource.name}-{uuid.uuid4()}",
        )
        return bucket


# _____________________ Resource Connector Builder ________________________

ConnectorType = TypeVar("ConnectorType", bound=ResourceConnector)


class ResourceConnectorBuilder(ABC, Generic[ConnectorType]):
    def __init__(
        self,
        context: "AppStack",
        connector: ConnectorType,
        lambda_: aws_lambda.Function,
    ) -> None:
        self.context = context
        self.connector = connector
        self.lambda_ = lambda_

    @abstractmethod
    def build(self):
        ...


class SqsConnectorBuilder(ResourceConnectorBuilder[SqsConnector]):
    def build(self):
        # TODO: validate resource type
        resource: aws_sqs.Queue = self.context.get_built_resource(
            self.connector.resource_name
        )
        if self.connector.permission in [SqsPermission.read, SqsPermission.full_access]:
            resource.grant_consume_messages(self.lambda_)
        if self.connector.permission in [
            SqsPermission.write,
            SqsPermission.full_access,
        ]:
            resource.grant_send_messages(self.lambda_)
        self.lambda_.add_environment(
            f"{self.connector.resource_name.upper()}_URL", resource.queue_url
        )


class S3ConnectorBuilder(ResourceConnectorBuilder[S3Connector]):
    def build(self):
        bucket: aws_s3.Bucket = self.context.get_built_resource(
            self.connector.resource_name
        )
        if self.connector.permission is S3Permission.read:
            bucket.grant_read(self.lambda_)
        elif self.connector.permission is S3Permission.write:
            # Rework permissions
            bucket.grant_write(self.lambda_)
            bucket.grant_delete(self.lambda_)
        elif self.connector.permission is S3Permission.full_access:
            bucket.grant_read_write(self.lambda_)
            bucket.grant_delete(self.lambda_)
        self.lambda_.add_environment(
            f"{self.connector.resource_name.upper()}_NAME", bucket.bucket_name
        )
