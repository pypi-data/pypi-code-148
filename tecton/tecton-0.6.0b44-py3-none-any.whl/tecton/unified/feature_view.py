from __future__ import annotations

import datetime
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import numpy as np
import pandas
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming
from typeguard import typechecked

from tecton import conf
from tecton import types
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import fco as internal_fco
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals import type_utils
from tecton._internals import utils as internal_utils
from tecton.declarative import base as declarative_base
from tecton.declarative import feature_view as declarative_feature_view
from tecton.declarative import filtered_source
from tecton.features_common import feature_configs
from tecton.interactive import athena_api
from tecton.interactive import data_frame as tecton_dataframe
from tecton.interactive import query_helper
from tecton.interactive import run_api
from tecton.interactive import snowflake_api
from tecton.interactive import spark_api
from tecton.unified import common as unified_common
from tecton.unified import data_source as unified_data_source
from tecton.unified import entity as unified_entity
from tecton.unified import transformation as unified_transformation
from tecton.unified import utils
from tecton_core import errors as core_errors
from tecton_core import fco_container
from tecton_core import feature_definition_wrapper
from tecton_core import feature_set_config
from tecton_core import id_helper
from tecton_core import specs
from tecton_core import time_utils
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.common import id_pb2
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_spark import request_context
from tecton_spark import spark_schema_wrapper


@attrs.define(eq=False)
class FeatureView(unified_common.BaseTectonObject, declarative_base.BaseFeatureDefinition):
    """Base class for Feature View classes (including Feature Tables).

    Attributes:
        _feature_definition: A FeatureDefinitionWrapper instance, which contains the Feature View spec for this Feature
            View and dependent FCO specs (e.g. Data Source specs). Set only after the object has been validated. Remote
            objects, i.e. applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.
        sources: The Data Sources for this Feature View.
        entities: The Entities for this Feature View.
        tranformations: The Transformations for this Feature View.
    """

    _feature_definition: Optional[feature_definition_wrapper.FeatureDefinitionWrapper] = attrs.field(repr=False)
    _args: Optional[feature_view__args_pb2.FeatureViewArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    sources: Tuple[unified_data_source.DataSource, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    entities: Tuple[unified_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    transformations: Tuple[unified_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @property
    def _spec(self) -> Optional[specs.FeatureViewSpec]:
        return self._feature_definition.fv_spec if self._feature_definition is not None else None

    @utils.requires_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(feature_view=self._args)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.FeatureViewSpec, fco_container: fco_container.FcoContainer) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container)
        info = unified_common.TectonObjectInfo.from_spec(spec)

        sources = []
        for data_source_spec in feature_definition.data_sources:
            if data_source_spec.stream_source is not None:
                sources.append(unified_data_source.StreamSource._from_spec(data_source_spec))
            else:
                sources.append(unified_data_source.BatchSource._from_spec(data_source_spec))

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(unified_entity.Entity._from_spec(entity_spec))

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(unified_transformation.Transformation._from_spec(transformation_spec))

        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=tuple(sources),
            entities=tuple(entities),
            transformations=tuple(transformations),
        )
        return obj

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    def _derive_schemas(self) -> feature_view__data_pb2.FeatureViewSchemas:
        raise NotImplementedError

    @property
    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def join_keys(self) -> List[str]:
        """The join key column names."""
        return self._feature_definition.join_keys

    @property
    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def features(self) -> List[str]:
        """The features produced by this FeatureView."""
        return self._feature_definition.features

    @sdk_decorators.sdk_public_method
    def validate(self) -> None:
        if self._is_valid:
            # Already valid.
            print("This object has already been validated.")
            return

        print(f"Validating dependencies for feature view {self.info.name}.")
        for dependent_object in self.sources + self.entities + self.transformations:
            dependent_object.validate()

        # TODO(TEC-11914): Support snowflake schema derivation
        feature_view_schemas = self._derive_schemas()
        supplement = specs.FeatureViewSpecArgsSupplement(
            view_schema=feature_view_schemas.view_schema,
            materialization_schema=feature_view_schemas.materialization_schema,
        )

        # TODO(jake): Implement backend validation for the feature view.
        fv_spec = specs.create_feature_view_spec_from_args_proto(self._args, supplement)

        transformation_specs = [transformation._spec for transformation in self.transformations]
        data_source_specs = [source._spec for source in self.sources]
        entity_specs = [entity._spec for entity in self.entities]
        fco_container_specs = transformation_specs + data_source_specs + entity_specs + [fv_spec]
        fco_container_ = fco_container.FcoContainer.from_specs(specs=fco_container_specs, root_ids=[fv_spec.id])

        self._feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(fv_spec, fco_container_)

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this data source."""
        request = metadata_service_pb2.GetFeatureViewSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self.info.workspace)
        )
        response = metadata_service.instance().GetFeatureViewSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> feature_set_config.FeatureSetConfig:
        return feature_set_config.FeatureSetConfig.from_feature_definition(self._feature_definition)

    @property
    @utils.requires_validation
    def _dependent_specs(self) -> List[specs.TectonObjectSpec]:
        """Returns all of the specs dependend on by this Feature View including this Feature View's spec."""
        # TODO(jake): For ODFVs, we'll need to recursively add dependent objects from dependent Feature Views.
        assert not isinstance(self._spec, specs.OnDemandFeatureViewSpec), "Not properly implemented for ODFVs."
        transformation_specs = [transformation._spec for transformation in self.transformations]
        data_source_specs = [source._spec for source in self.sources]
        entity_specs = [entity._spec for entity in self.entities]
        return transformation_specs + data_source_specs + entity_specs + [self._spec]

    @property
    # TODO(jake): Remove this base data source property after deleting declarative code.
    def name(self) -> str:
        return self.info.name

    @property
    # TODO(jake): Remove this base data source property after deleting declarative code.
    def _id(self) -> id_pb2.Id:
        return self.info._id_proto

    # TODO(samantha): add delete keys and materialization methods from interactive class


@attrs.define
class MaterializedFeatureView(FeatureView):
    """Class for BatchFeatureView and StreamFeatureView to inherit common methods from."""

    def _derive_schemas(self) -> feature_view__data_pb2.FeatureViewSchemas:
        assert all(
            [obj._is_valid for obj in self.transformations + self.sources]
        ), "_derive_schemas expects that dependent objects have been validated."
        transformation_specs = [transformation._spec for transformation in self.transformations]
        data_source_specs = [source._spec for source in self.sources]

        view_schema = spark_api.derive_view_schema_for_feature_view(self._args, transformation_specs, data_source_specs)
        # TODO(TEC-12599): Implement materialized schema derivation. Needed for aggregate features.
        materialization_schema = view_schema
        return feature_view__data_pb2.FeatureViewSchemas(
            view_schema=view_schema, materialization_schema=materialization_schema
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def get_historical_features(
        self,
        spine: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame, str]
        ] = None,
        timestamp_key: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame]
        ] = None,
        from_source: bool = False,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(jake): Port over docs. Deferring to avoid skew while in development."""

        # TODO(jake): Port over get_historical_features() error checking. Deferring because we'll be reworking
        # from_source defaults. See TEC-10489.

        is_local_mode = self._feature_definition.fv_spec.is_local_object
        is_dev_workspace = not is_local_mode and not internal_utils.is_live_workspace(self.info.workspace)

        if self._feature_definition.is_incremental_backfill:
            if is_local_mode:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_IN_LOCAL_MODE(
                    self.name,
                )
            if is_dev_workspace:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                    self.name, self.info.workspace
                )
            if from_source:
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE

        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
                append_prefix=False,
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            if self.info.workspace is None or not internal_utils.is_live_workspace(self.info.workspace):
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return spark_api.get_historical_features_for_feature_definition(
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=from_source,
            save=save,
            save_as=save_as,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def run(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        aggregation_level: Optional[str] = None,
        **mock_sources: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(samantha): Port over docs."""
        if self._feature_definition.is_temporal and aggregation_level is not None:
            raise errors.FV_UNSUPPORTED_AGGREGATION

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.run_batch(
                fd=self._feature_definition,
                feature_start_time=start_time,
                feature_end_time=end_time,
                mock_inputs=mock_sources,
                aggregate_tiles=None,
                aggregation_level=aggregation_level,
            )

        return run_api.run_batch(
            self._feature_definition,
            start_time,
            end_time,
            mock_sources,
            feature_definition_wrapper.FrameworkVersion.FWV5,
            aggregate_tiles=None,
            aggregation_level=aggregation_level,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> tecton_dataframe.FeatureVector:
        """TODO(samantha): Port over docs."""
        if not self._feature_definition.writes_to_online_store:
            raise errors.UNSUPPORTED_OPERATION("get_online_features", "online=True is not set for this FeatureView.")
        internal_utils.validate_join_key_types(join_keys)

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys or {},
            include_join_keys_in_response,
            {},
            request_context.RequestContext({}),
        )


@attrs.define(eq=False)
class BatchFeatureView(MaterializedFeatureView):
    """Tecton class for BatchFeatureViews.

    TODO(samantha): add more info for public docs.
    """

    def __init__(
        self,
        *,
        name: str,
        feature_view_function: Callable,
        sources: Sequence[Union[unified_data_source.BatchSource, filtered_source.FilteredSource]],
        entities: Sequence[unified_entity.Entity],
        mode: str,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
        online: Optional[bool] = False,
        offline: Optional[bool] = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        offline_store: Optional[
            Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
        ] = feature_configs.ParquetConfig(),
        online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
        monitor_freshness: bool = False,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        timestamp_field: Optional[str] = None,
        max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
        incremental_backfills: bool = False,
    ):
        from tecton.cli import common as cli_common

        if mode == declarative_feature_view.PIPELINE_MODE:
            pipeline_function = feature_view_function
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = unified_transformation.transformation(mode, name, description, owner, tags=tags)(
                feature_view_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        stream_processing_mode = declarative_feature_view.StreamProcessingMode.TIME_INTERVAL if aggregations else None

        pipeline_root = declarative_feature_view.build_pipeline(
            name, feature_view_function, pipeline_function, data_source_type_pb2.DataSourceType.BATCH, sources
        )

        args = declarative_feature_view.build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=None,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=data_source_type_pb2.DataSourceType.BATCH,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=None,
            incremental_backfills=incremental_backfills,
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = tuple(
            source.source if isinstance(source, filtered_source.FilteredSource) else source for source in sources
        )

        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
        )
        internal_fco.Fco._register(self)


@typechecked
def batch_feature_view(
    *,
    mode: str,
    sources: Sequence[Union[unified_data_source.BatchSource, filtered_source.FilteredSource]],
    entities: Sequence[unified_entity.Entity],
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]] = None,
    offline_store: Optional[
        Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
    ] = feature_configs.ParquetConfig(),
    online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
    monitor_freshness: bool = False,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    incremental_backfills: bool = False,
):
    """TODO(jake): Port over docs. Deferring to avoid skew while in development."""

    def decorator(feature_view_function):
        return BatchFeatureView(
            name=name or feature_view_function.__name__,
            feature_view_function=feature_view_function,
            mode=mode,
            sources=sources,
            entities=entities,
            aggregation_interval=aggregation_interval,
            aggregations=aggregations,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            offline_store=offline_store,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            incremental_backfills=incremental_backfills,
        )

    return decorator


@attrs.define(eq=False)
class StreamFeatureView(MaterializedFeatureView):
    """Tecton class for StreamFeatureViews.

    TODO(samantha): add more info for public docs.
    """

    def __init__(
        self,
        *,
        name: str,
        feature_view_function: Optional[Callable] = None,
        source: Union[unified_data_source.StreamSource, filtered_source.FilteredSource],
        entities: Sequence[unified_entity.Entity],
        mode: str,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
        stream_processing_mode: Optional[declarative_feature_view.StreamProcessingMode] = None,
        online: Optional[bool] = False,
        offline: Optional[bool] = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        stream_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        offline_store: Optional[
            Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
        ] = feature_configs.ParquetConfig(),
        online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
        monitor_freshness: bool = False,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        timestamp_field: Optional[str] = None,
        max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
        output_stream: Optional[declarative_base.OutputStream] = None,
    ):
        from tecton.cli import common as cli_common

        if mode == declarative_feature_view.PIPELINE_MODE:
            pipeline_function = feature_view_function
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = unified_transformation.transformation(mode, name, description, owner, tags=tags)(
                feature_view_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        if aggregations:
            stream_processing_mode_ = (
                stream_processing_mode or declarative_feature_view.StreamProcessingMode.TIME_INTERVAL
            )
        else:
            stream_processing_mode_ = stream_processing_mode

        pipeline_root = declarative_feature_view.build_pipeline(
            name,
            feature_view_function,
            pipeline_function,
            data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
            [source],
        )

        args = declarative_feature_view.build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode_,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=output_stream,
            incremental_backfills=False,
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = (source.source if isinstance(source, filtered_source.FilteredSource) else source,)

        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
        )
        internal_fco.Fco._register(self)

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def run_stream(self, output_temp_table: str) -> streaming.StreamingQuery:
        """TODO(samantha): Port over docs."""
        return run_api.run_stream(self._feature_definition, output_temp_table)


@typechecked
def stream_feature_view(
    *,
    source: Union[unified_data_source.StreamSource, filtered_source.FilteredSource],
    entities: Sequence[unified_entity.Entity],
    mode: str,
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
    stream_processing_mode: Optional[declarative_feature_view.StreamProcessingMode] = None,
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]] = None,
    stream_compute: Optional[Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]] = None,
    offline_store: Optional[
        Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
    ] = feature_configs.ParquetConfig(),
    online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
    monitor_freshness: bool = False,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[declarative_base.OutputStream] = None,
):
    """TODO(samantha): Port over docs. Deferring to avoid skew while in development."""

    def decorator(feature_view_function):
        return StreamFeatureView(
            name=name or feature_view_function.__name__,
            feature_view_function=feature_view_function,
            source=source,
            entities=entities,
            mode=mode,
            aggregation_interval=aggregation_interval,
            aggregations=aggregations,
            stream_processing_mode=stream_processing_mode,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            offline_store=offline_store,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=output_stream,
        )

    return decorator


@attrs.define
class FeatureTable(FeatureView):
    @typechecked
    def __init__(
        self,
        *,
        name: str,
        entities: List[unified_entity.Entity],
        schema: List[types.Field],
        ttl: Optional[datetime.timedelta] = None,
        online: Optional[bool] = False,
        offline: Optional[bool] = False,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        offline_store: feature_configs.DeltaConfig = feature_configs.DeltaConfig(),
        online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
        batch_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        online_serving_index: Optional[List[str]] = None,
    ):
        """Instantiate a new FeatureTable.

        :param name: Unique, human friendly name that identifies the FeatureTable.
        :param entities: A list of Entity objects, used to organize features.
        :param schema: A schema for the FeatureTable. Supported types are: Int64, Float64, String, Bool and Array with Int64, Float32, Float64 and String typed elements. Additionally you must have exactly one Timestamp typed column for the feature timestamp.
        :param ttl: The TTL (or "look back window") for features defined by this feature table. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
        :param online: Enable writing to online feature store. (Default: False)
        :param offline: Enable writing to offline feature store. (Default: False)
        :param description: A human readable description.
        :param owner: Owner name (typically the email of the primary maintainer).
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param offline_store: Configuration for how data is written to the offline feature store.
        :param online_store: Configuration for how data is written to the online feature store.
        :param batch_compute: Batch materialization cluster configuration. Should be one of:
            [``EMRClusterConfig``, ``DatabricksClusterConfig``]
        :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
            Defaults to the complete set of join keys. Up to one join key may be omitted. If one key is omitted, online requests to a Feature Service will
            return all feature vectors that match the specified join keys.
        :returns: A Feature Table

        An example declaration of a FeatureTable

        .. code-block:: python

            from tecton import Entity, FeatureTable
            from tecton.types import Field, String, Timestamp, Int64
            import datetime

            # Declare your user Entity instance here or import it if defined elsewhere in
            # your Tecton repo.

            user = ...

            schema = [
                Field('user_id', String),
                Field('timestamp', Timestamp),
                Field('user_login_count_7d', Int64),
                Field('user_login_count_30d', Int64)
            ]

            user_login_counts = FeatureTable(
                name='user_login_counts',
                entities=[user],
                schema=schema,
                online=True,
                offline=True,
                ttl=datetime.timedelta(days=30)
            )
        """
        from tecton.cli import common as cli_common

        if isinstance(schema, list):
            wrapper = type_utils.to_spark_schema_wrapper(schema)
        else:
            wrapper = spark_schema_wrapper.SparkSchemaWrapper(schema)

        if batch_compute:
            batch_compute_proto = batch_compute._to_cluster_proto()
        else:
            batch_compute_proto = feature_view__args_pb2.ClusterConfig(
                implicit_config=feature_view__args_pb2.DefaultClusterConfig(**feature_configs.DEFAULT_SPARK_VERSIONS)
            )

        feature_table_args = feature_view__args_pb2.FeatureTableArgs(
            schema=wrapper.to_proto(),
            serving_ttl=time_utils.timedelta_to_proto(ttl),
            batch_compute=batch_compute_proto,
            offline_store=offline_store._to_proto(),
            online_store=online_store._to_proto() if online_store else None,
        )

        # If unspecified, online_serving_index defaults to the join_keys of the Feature Table.
        join_keys = []
        for entity in entities:
            join_keys.extend(entity.join_keys)

        basic_info = basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner)
        args = feature_view__args_pb2.FeatureViewArgs(
            feature_table_args=feature_table_args,
            feature_view_id=id_helper.IdHelper.generate_id(),
            info=basic_info,
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FEATURE_TABLE,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            entities=[
                feature_view__args_pb2.EntityKeyOverride(entity_id=entity.info._id_proto, join_keys=entity.join_keys)
                for entity in entities
            ],
            online_enabled=online,
            offline_enabled=offline,
            online_serving_index=online_serving_index if online_serving_index else join_keys,
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)
        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=tuple(),
            entities=tuple(entities),
            transformations=tuple(),
        )
        internal_fco.Fco._register(self)

    def _derive_schemas(self) -> feature_view__data_pb2.FeatureViewSchemas:
        view_schema = spark_api.derive_view_schema_for_feature_table(self._args)
        return feature_view__data_pb2.FeatureViewSchemas(
            view_schema=view_schema,
            materialization_schema=view_schema,  # For feature tables, materialization and view schema are the same.
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame]] = None,
        timestamp_key: Optional[str] = None,
        entities: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame]
        ] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(samantha): port over docs"""
        is_dev_workspace = not internal_utils.is_live_workspace(self.info.workspace)
        if is_dev_workspace:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if not self._feature_definition.writes_to_offline_store:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE(self.info.name)

        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=False,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return spark_api.get_historical_features_for_feature_definition(
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=False,
            save=save,
            save_as=save_as,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> tecton_dataframe.FeatureVector:
        """TODO(samantha): port over docs."""
        if not internal_utils.is_live_workspace(self.info.workspace):
            raise errors.FEATURE_TABLE_GET_ONLINE_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if not self._feature_definition.writes_to_online_store:
            raise errors.UNSUPPORTED_OPERATION(
                "get_online_features", "online_serving_enabled was not defined for this Feature Table."
            )

        internal_utils.validate_join_key_types(join_keys)
        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_context_map={},
            request_context_schema=request_context.RequestContext({}),
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def ingest(self, df: Union[pyspark_dataframe.DataFrame, pandas.DataFrame]):
        """TODO(samantha): port over docs."""

        if not internal_utils.is_live_workspace(self.info.workspace):
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("ingest")

        get_upload_info_request = metadata_service_pb2.GetNewIngestDataframeInfoRequest(
            feature_definition_id=self._spec.id_proto
        )
        upload_info_response = metadata_service.instance().GetNewIngestDataframeInfo(get_upload_info_request)

        df_path = upload_info_response.df_path
        upload_url = upload_info_response.signed_url_for_df_upload
        spark_api.write_dataframe_to_path_or_url(df, df_path, upload_url, self._feature_definition.view_schema)

        ingest_request = metadata_service_pb2.IngestDataframeRequest(
            workspace=self.info.workspace, feature_definition_id=self._spec.id_proto, df_path=df_path
        )
        response = metadata_service.instance().IngestDataframe(ingest_request)
