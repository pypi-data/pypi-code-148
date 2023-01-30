'''
# Turbo Layers for CDK

[![NPM](https://img.shields.io/npm/v/@cloudsnorkel/cdk-turbo-layers?label=npm&logo=npm)](https://www.npmjs.com/package/@cloudsnorkel/cdk-turbo-layers)
[![PyPI](https://img.shields.io/pypi/v/cloudsnorkel.cdk-turbo-layers?label=pypi&logo=pypi)](https://pypi.org/project/cloudsnorkel.cdk-turbo-layers)
[![Maven Central](https://img.shields.io/maven-central/v/com.cloudsnorkel/cdk.turbo-layers.svg?label=Maven%20Central&logo=java)](https://search.maven.org/search?q=g:%22com.cloudsnorkel%22%20AND%20a:%22cdk.turbo-layers%22)
[![Go](https://img.shields.io/github/v/tag/CloudSnorkel/cdk-turbo-layers?color=red&label=go&logo=go)](https://pkg.go.dev/github.com/CloudSnorkel/cdk-turbo-layers-go/cloudsnorkelcdkturbolayers)
[![Nuget](https://img.shields.io/nuget/v/CloudSnorkel.Cdk.TurboLayers?color=red&&logo=nuget)](https://www.nuget.org/packages/CloudSnorkel.Cdk.TurboLayers/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/CloudSnorkel/cdk-turbo-layers/blob/main/LICENSE)

Speed up deployment of Lambda functions by creating dependency layers in AWS instead of locally.

* Easily separate dependency deployment from Lambda code deployment
* Never re-package dependencies just because of a small code change
* Never download another single dependency package locally again
* Never upload oversized code packages again
* Edit your code in the browser -- no more "deployment package too large to enable inline code editing" errors
* Uninstall Docker from your laptop and extend your battery life
* Take shorter coffee breaks when deploying

Supported Lambda runtimes:

* Python
* Node.js
* Ruby

## API

The best way to browse API documentation is on [Constructs Hub](https://constructs.dev/packages/@cloudsnorkel/cdk-turbo-layers/). It is available in all supported programming languages.

## Installation

1. Confirm you're using CDK v2
2. Install the appropriate package

   1. [Python](https://pypi.org/project/cloudsnorkel.cdk-turbo-layers)

      ```
      pip install cloudsnorkel.cdk-turbo-layers
      ```
   2. [TypeScript or JavaScript](https://www.npmjs.com/package/@cloudsnorkel/cdk-turbo-layers)

      ```
      npm i @cloudsnorkel/cdk-turbo-layers
      ```
   3. [Java](https://search.maven.org/search?q=g:%22com.cloudsnorkel%22%20AND%20a:%22cdk.turbo-layers%22)

      ```xml
      <dependency>
      <groupId>com.cloudsnorkel</groupId>
      <artifactId>cdk.turbo-layers</artifactId>
      </dependency>
      ```
   4. [Go](https://pkg.go.dev/github.com/CloudSnorkel/cdk-turbo-layers-go/cloudsnorkelcdkturbolayers)

      ```
      go get github.com/CloudSnorkel/cdk-turbo-layers-go/cloudsnorkelcdkturbolayers
      ```
   5. [.NET](https://www.nuget.org/packages/CloudSnorkel.Cdk.TurboLayers/)

      ```
      dotnet add package CloudSnorkel.Cdk.TurboLayers
      ```

## Example

```python
 const packager = new PythonDependencyPackager(this, 'Packager', {
    runtime: lambda.Runtime.PYTHON_3_9,
    type: DependencyPackagerType.LAMBDA,
});
new Function(this, 'Function with inline requirements', {
    handler: 'index.handler',
    code: lambda.Code.fromInline('def handler(event, context):\n  import requests'),
    runtime: lambda.Runtime.PYTHON_3_9,
    // this will create a layer from with requests and Scrapy in a Lambda function instead of locally
    layers: [packager.layerFromInline('inline requirements', ['requests', 'Scrapy'])],
});
new Function(this, 'Function with external source and requirements', {
    handler: 'index.handler',
    code: lambda.Code.fromAsset('lambda-src'),
    runtime: lambda.Runtime.PYTHON_3_9,
    // this will read pyproject.toml and poetry.lock and create a layer from the requirements in a Lambda function instead of locally
    layers: [packager.layerFromPoetry('poetry requirements', 'lambda-src')],
});
```

## Older Implementations

* [lovage](https://github.com/CloudSnorkel/lovage): standalone Python framework that uses the same trick to deploy decorated functions to AWS
* [serverless-pydeps](https://github.com/CloudSnorkel/serverless-pydeps): plugin for [Serverless Framework](https://www.serverless.com/) that speeds up deployment
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-turbo-layers.DependencyPackagerProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "preinstall_commands": "preinstallCommands",
        "runtime": "runtime",
        "subnet_selection": "subnetSelection",
        "type": "type",
        "vpc": "vpc",
    },
)
class DependencyPackagerProps:
    def __init__(
        self,
        *,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional["DependencyPackagerType"] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param architecture: (experimental) Target Lambda architecture. Packages will be installed for this architecture so make sure it fits your Lambda functions.
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param preinstall_commands: (experimental) Additional commands to run before installing packages. Use this to authenticate your package repositories like CodeArtifact. Default: []
        :param runtime: (experimental) Target Lambda runtime. Packages will be installed for this runtime so make sure it fits your Lambda functions.
        :param subnet_selection: (experimental) VPC subnets used for packager. Default: default subnets, if VPC is used
        :param type: (experimental) Type of dependency packager. Use Lambda for speed and CodeBuild for complex dependencies that require building native extensions. Default: {@link DependencyPackagerType.LAMBDA}
        :param vpc: (experimental) VPC used for packager. Use this if your package repositories are only available from within a VPC. Default: no VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49755eda8d64f261ee5548778ab2e88d80326d26340eccc0a642160aa86a5cf)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument preinstall_commands", value=preinstall_commands, expected_type=type_hints["preinstall_commands"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if preinstall_commands is not None:
            self._values["preinstall_commands"] = preinstall_commands
        if runtime is not None:
            self._values["runtime"] = runtime
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if type is not None:
            self._values["type"] = type
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''(experimental) Target Lambda architecture.

        Packages will be installed for this architecture so make sure it fits your Lambda functions.

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def preinstall_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional commands to run before installing packages.

        Use this to authenticate your package repositories like CodeArtifact.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("preinstall_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runtime(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime]:
        '''(experimental) Target Lambda runtime.

        Packages will be installed for this runtime so make sure it fits your Lambda functions.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) VPC subnets used for packager.

        :default: default subnets, if VPC is used

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def type(self) -> typing.Optional["DependencyPackagerType"]:
        '''(experimental) Type of dependency packager.

        Use Lambda for speed and CodeBuild for complex dependencies that require building native extensions.

        :default: {@link DependencyPackagerType.LAMBDA}

        :stability: experimental
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["DependencyPackagerType"], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC used for packager.

        Use this if your package repositories are only available from within a VPC.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DependencyPackagerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cloudsnorkel/cdk-turbo-layers.DependencyPackagerType")
class DependencyPackagerType(enum.Enum):
    '''(experimental) Type of dependency packager.

    This affects timeouts and capabilities of the packager.

    :stability: experimental
    '''

    LAMBDA = "LAMBDA"
    '''(experimental) Use Lambda function to package dependencies.

    It is much faster than the alternative, but limited to 15 minutes and can't build native extensions.

    :stability: experimental
    '''
    CODEBUILD = "CODEBUILD"
    '''(experimental) Use CodeBuild to package dependencies.

    It is capable of everything your local machine can do, but takes a little longer to startup.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-turbo-layers.LayerProps",
    jsii_struct_bases=[],
    name_mapping={"always_rebuild": "alwaysRebuild"},
)
class LayerProps:
    def __init__(
        self,
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87eed72f9a37d0c3dccc3b4ae25ce7b0751f94dc9a720b10313bc2b9bd2522b9)
            check_type(argname="argument always_rebuild", value=always_rebuild, expected_type=type_hints["always_rebuild"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if always_rebuild is not None:
            self._values["always_rebuild"] = always_rebuild

    @builtins.property
    def always_rebuild(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Always rebuild the layer, even when the dependencies definition files haven't changed.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("always_rebuild")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable, _aws_cdk_aws_ec2_ceddda9d.IConnectable)
class NodejsDependencyPackager(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-turbo-layers.NodejsDependencyPackager",
):
    '''(experimental) Packager for creating Lambda layers for Node.js dependencies in AWS. Nothing is done locally so this doesn't require Docker, doesn't download any packages and doesn't upload huge files to S3.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[DependencyPackagerType] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Target Lambda architecture. Packages will be installed for this architecture so make sure it fits your Lambda functions.
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param preinstall_commands: (experimental) Additional commands to run before installing packages. Use this to authenticate your package repositories like CodeArtifact. Default: []
        :param runtime: (experimental) Target Lambda runtime. Packages will be installed for this runtime so make sure it fits your Lambda functions.
        :param subnet_selection: (experimental) VPC subnets used for packager. Default: default subnets, if VPC is used
        :param type: (experimental) Type of dependency packager. Use Lambda for speed and CodeBuild for complex dependencies that require building native extensions. Default: {@link DependencyPackagerType.LAMBDA}
        :param vpc: (experimental) VPC used for packager. Use this if your package repositories are only available from within a VPC. Default: no VPC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e395015d42926104dcf44bedbc6a4554e1b69be339eef7cd356896513eec0de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DependencyPackagerProps(
            architecture=architecture,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            preinstall_commands=preinstall_commands,
            runtime=runtime,
            subnet_selection=subnet_selection,
            type=type,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="layerFromInline")
    def layer_from_inline(
        self,
        id: builtins.str,
        libraries: typing.Sequence[builtins.str],
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies passed as an argument and installed with npm.

        :param id: -
        :param libraries: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca255b74874572ceb3994368f94b78e9624986d0f0ff5f251313ec83d485670)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument libraries", value=libraries, expected_type=type_hints["libraries"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromInline", [id, libraries, props]))

    @jsii.member(jsii_name="layerFromPackageJson")
    def layer_from_package_json(
        self,
        id: builtins.str,
        path: builtins.str,
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies defined in package.json and (optionally) package-lock.json and installed with npm.

        :param id: -
        :param path: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52706f6503de417ed1f45418de30ab065cd6548cea4d31929877cc111f768f92)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromPackageJson", [id, path, props]))

    @jsii.member(jsii_name="layerFromYarn")
    def layer_from_yarn(
        self,
        id: builtins.str,
        path: builtins.str,
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies defined in package.json and yarn.lock and installed with yarn.

        :param id: -
        :param path: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a82a7cb9424d6b760f629db04b71a9bb851a52a8ab536b418779f65ae8532e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromYarn", [id, path, props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable, _aws_cdk_aws_ec2_ceddda9d.IConnectable)
class PythonDependencyPackager(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-turbo-layers.PythonDependencyPackager",
):
    '''(experimental) Packager for creating Lambda layers for Python dependencies in AWS.

    Nothing is done locally so this doesn't require Docker, doesn't download any packages and doesn't upload huge files to S3.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[DependencyPackagerType] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Target Lambda architecture. Packages will be installed for this architecture so make sure it fits your Lambda functions.
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param preinstall_commands: (experimental) Additional commands to run before installing packages. Use this to authenticate your package repositories like CodeArtifact. Default: []
        :param runtime: (experimental) Target Lambda runtime. Packages will be installed for this runtime so make sure it fits your Lambda functions.
        :param subnet_selection: (experimental) VPC subnets used for packager. Default: default subnets, if VPC is used
        :param type: (experimental) Type of dependency packager. Use Lambda for speed and CodeBuild for complex dependencies that require building native extensions. Default: {@link DependencyPackagerType.LAMBDA}
        :param vpc: (experimental) VPC used for packager. Use this if your package repositories are only available from within a VPC. Default: no VPC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013f7260349d8118a2d080375d72aae8123ce90e1efe110e2c2d1451dec055f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DependencyPackagerProps(
            architecture=architecture,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            preinstall_commands=preinstall_commands,
            runtime=runtime,
            subnet_selection=subnet_selection,
            type=type,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="layerFromInline")
    def layer_from_inline(
        self,
        id: builtins.str,
        requirements: typing.Sequence[builtins.str],
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies passed as an argument and installed with pip.

        :param id: -
        :param requirements: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f3b7c08e229e2e3bfb751ac0617b041fcfc485cdb9696443509b6e5e1af417)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument requirements", value=requirements, expected_type=type_hints["requirements"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromInline", [id, requirements, props]))

    @jsii.member(jsii_name="layerFromPipenv")
    def layer_from_pipenv(
        self,
        id: builtins.str,
        path: builtins.str,
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies defined in Pipfile and (optionally) Pipfile.lock and installed with pipenv.

        :param id: -
        :param path: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbac2533c883a6bc1854e54f9f9ac90adc4af3bb948a44d90e9d027c4193bcb2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromPipenv", [id, path, props]))

    @jsii.member(jsii_name="layerFromPoetry")
    def layer_from_poetry(
        self,
        id: builtins.str,
        path: builtins.str,
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies defined in pyproject.toml and (optionally) poetry.lock and installed with poetry.

        :param id: -
        :param path: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9768610efbeae613d5c58ea39a0bde75d42683502228fe47411d75da6984e717)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromPoetry", [id, path, props]))

    @jsii.member(jsii_name="layerFromRequirementsTxt")
    def layer_from_requirements_txt(
        self,
        id: builtins.str,
        path: builtins.str,
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies defined in requirements.txt and installed with pip.

        :param id: -
        :param path: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d910c8f82362f9f54dd2512aec7ec299a5cd40d937abbae5140cf577f10bca)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromRequirementsTxt", [id, path, props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable, _aws_cdk_aws_ec2_ceddda9d.IConnectable)
class RubyDependencyPackager(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-turbo-layers.RubyDependencyPackager",
):
    '''(experimental) Packager for creating Lambda layers for Ruby dependencies in AWS.

    Nothing is done locally so this doesn't require Docker, doesn't download any packages and doesn't upload huge files to S3.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[DependencyPackagerType] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Target Lambda architecture. Packages will be installed for this architecture so make sure it fits your Lambda functions.
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param preinstall_commands: (experimental) Additional commands to run before installing packages. Use this to authenticate your package repositories like CodeArtifact. Default: []
        :param runtime: (experimental) Target Lambda runtime. Packages will be installed for this runtime so make sure it fits your Lambda functions.
        :param subnet_selection: (experimental) VPC subnets used for packager. Default: default subnets, if VPC is used
        :param type: (experimental) Type of dependency packager. Use Lambda for speed and CodeBuild for complex dependencies that require building native extensions. Default: {@link DependencyPackagerType.LAMBDA}
        :param vpc: (experimental) VPC used for packager. Use this if your package repositories are only available from within a VPC. Default: no VPC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7740d66034151afa4aa24422b7754751baf98d6ae258a16f302d88b1838b5f6e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DependencyPackagerProps(
            architecture=architecture,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            preinstall_commands=preinstall_commands,
            runtime=runtime,
            subnet_selection=subnet_selection,
            type=type,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="layerFromBundler")
    def layer_from_bundler(
        self,
        id: builtins.str,
        path: builtins.str,
        *,
        always_rebuild: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.LayerVersion:
        '''(experimental) Create a layer for dependencies defined in Gemfile and (optionally) Gemfile.lock and installed with Bundler.

        :param id: -
        :param path: -
        :param always_rebuild: (experimental) Always rebuild the layer, even when the dependencies definition files haven't changed. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63c6dfce6ff58c82a4e0b82c3b3c20b407fa367d5d41ffd30de5690d9c66376)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        props = LayerProps(always_rebuild=always_rebuild)

        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.LayerVersion, jsii.invoke(self, "layerFromBundler", [id, path, props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))


__all__ = [
    "DependencyPackagerProps",
    "DependencyPackagerType",
    "LayerProps",
    "NodejsDependencyPackager",
    "PythonDependencyPackager",
    "RubyDependencyPackager",
]

publication.publish()

def _typecheckingstub__d49755eda8d64f261ee5548778ab2e88d80326d26340eccc0a642160aa86a5cf(
    *,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[DependencyPackagerType] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87eed72f9a37d0c3dccc3b4ae25ce7b0751f94dc9a720b10313bc2b9bd2522b9(
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e395015d42926104dcf44bedbc6a4554e1b69be339eef7cd356896513eec0de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[DependencyPackagerType] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca255b74874572ceb3994368f94b78e9624986d0f0ff5f251313ec83d485670(
    id: builtins.str,
    libraries: typing.Sequence[builtins.str],
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52706f6503de417ed1f45418de30ab065cd6548cea4d31929877cc111f768f92(
    id: builtins.str,
    path: builtins.str,
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a82a7cb9424d6b760f629db04b71a9bb851a52a8ab536b418779f65ae8532e(
    id: builtins.str,
    path: builtins.str,
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013f7260349d8118a2d080375d72aae8123ce90e1efe110e2c2d1451dec055f5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[DependencyPackagerType] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f3b7c08e229e2e3bfb751ac0617b041fcfc485cdb9696443509b6e5e1af417(
    id: builtins.str,
    requirements: typing.Sequence[builtins.str],
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbac2533c883a6bc1854e54f9f9ac90adc4af3bb948a44d90e9d027c4193bcb2(
    id: builtins.str,
    path: builtins.str,
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9768610efbeae613d5c58ea39a0bde75d42683502228fe47411d75da6984e717(
    id: builtins.str,
    path: builtins.str,
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d910c8f82362f9f54dd2512aec7ec299a5cd40d937abbae5140cf577f10bca(
    id: builtins.str,
    path: builtins.str,
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7740d66034151afa4aa24422b7754751baf98d6ae258a16f302d88b1838b5f6e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    preinstall_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[DependencyPackagerType] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63c6dfce6ff58c82a4e0b82c3b3c20b407fa367d5d41ffd30de5690d9c66376(
    id: builtins.str,
    path: builtins.str,
    *,
    always_rebuild: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
