from base64 import b64encode
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
from pyspark.sql import DataFrame as pysparkDF
from pyspark.sql.functions import struct
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import utils
from tecton._internals.display import Displayable
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.fco import Fco
from tecton.interactive import spark_api
from tecton.tecton_context import TectonContext
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.id_helper import IdHelper
from tecton_core.logger import get_logger
from tecton_core.online_serving_index import OnlineServingIndex
from tecton_core.schema import Schema
from tecton_proto.data.materialization_status_pb2 import DataSourceType
from tecton_proto.data.materialization_status_pb2 import MaterializationStatus
from tecton_proto.metadataservice.metadata_service_pb2 import DeleteEntitiesRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetDeleteEntitiesInfoRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureFreshnessRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureViewSummaryRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetMaterializationStatusRequest
from tecton_proto.online_store.feature_value_pb2 import FeatureValueList
from tecton_proto.online_store.feature_value_pb2 import NullValue
from tecton_spark import ingest_utils

logger = get_logger("FeatureDefinition")


class FeatureDefinition(Fco):
    @property
    def _fco_metadata(self):
        return self._proto.fco_metadata

    @property
    def _view_schema(self):
        return Schema(self._proto.schemas.view_schema)

    @property
    def _materialization_schema(self):
        return Schema(self._proto.schemas.materialization_schema)

    @property
    def _id_proto(self):
        return self._proto.feature_view_id

    @property  # type: ignore
    @sdk_public_method
    def id(self) -> str:
        """
        Returns the id of this object
        """
        return IdHelper.to_string(self._id_proto)

    @property
    def join_keys(self) -> List[str]:
        """
        Returns the join key column names
        """
        return list(self._proto.join_keys)

    @property  # type: ignore
    @sdk_public_method
    def online_serving_index(self) -> OnlineServingIndex:
        """
        Returns Defines the set of join keys that will be indexed and queryable during online serving.
        Defaults to the complete join key.
        """
        return OnlineServingIndex.from_proto(self._proto.online_serving_index)

    @property
    def wildcard_join_key(self) -> Optional[str]:
        """
        Returns a wildcard join key column name if it exists;
        Otherwise returns None.
        """
        online_serving_index = self.online_serving_index
        wildcard_keys = [join_key for join_key in self.join_keys if join_key not in online_serving_index.join_keys]
        return wildcard_keys[0] if wildcard_keys else None

    @property  # type: ignore
    @sdk_public_method
    def entity_names(self) -> List[str]:
        """
        Returns the names of entities for this Feature View.
        """
        entity_specs = [self._fco_container.get_by_id_proto(id) for id in self._proto.entity_ids]
        return [entity.name for entity in entity_specs]

    @property
    def data_source_names(self) -> List[str]:
        """
        Returns the names of the data sources for this Feature View.
        """
        fd = FeatureDefinitionWrapper(self._spec, self._fco_container)
        return [ds.name for ds in fd.data_sources]

    @property
    def _timestamp_key(self) -> str:
        raise NotImplementedError

    @property  # type: ignore
    @sdk_public_method
    def features(self) -> List[str]:
        """
        Returns the names of the (output) features.
        """
        join_keys = self.join_keys
        timestamp_key = self._timestamp_key
        return [
            col_name
            for col_name in self._view_schema.column_names()
            if col_name not in join_keys and col_name != timestamp_key
        ]

    @property  # type: ignore
    @sdk_public_method
    def url(self) -> str:
        """
        Returns a link to the Tecton Web UI.
        """
        return self._proto.web_url

    @sdk_public_method
    def summary(self) -> Displayable:
        """
        Returns various information about this feature definition, including the most critical metadata such
        as the name, owner, features, etc.
        """
        request = GetFeatureViewSummaryRequest()
        request.fco_locator.id.CopyFrom(self._id_proto)
        request.fco_locator.workspace = self.workspace

        response = metadata_service.instance().GetFeatureViewSummary(request)

        return Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> FeatureSetConfig:
        feature_defintion = FeatureDefinitionWrapper(self._spec, self._fco_container)
        return FeatureSetConfig.from_feature_definition(feature_defintion)

    def _deletion_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        materialization_attempts = self._get_materialization_status().materialization_attempts
        deletion_attempts = [
            attempt
            for attempt in materialization_attempts
            if attempt.data_source_type == DataSourceType.DATA_SOURCE_TYPE_DELETION
        ]
        column_names, materialization_status_rows = utils.format_materialization_attempts(
            deletion_attempts, verbose, limit, sort_columns, errors_only
        )

        return self._create_materialization_table(column_names, materialization_status_rows)

    def _materialization_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        materialization_attempts = self._get_materialization_status().materialization_attempts
        column_names, materialization_status_rows = utils.format_materialization_attempts(
            materialization_attempts, verbose, limit, sort_columns, errors_only
        )

        return self._create_materialization_table(column_names, materialization_status_rows)

    def _create_materialization_table(self, column_names, materialization_status_rows):
        print("All the displayed times are in UTC time zone")

        # Setting `max_width=0` creates a table with an unlimited width.
        table = Displayable.from_table(headings=column_names, rows=materialization_status_rows, max_width=0)
        # Align columns in the middle horizontally
        table._text_table.set_cols_align(["c" for _ in range(len(column_names))])

        return table

    def _get_materialization_status(self) -> MaterializationStatus:
        """
        Returns MaterializationStatus proto for the FeatureView.
        """
        request = GetMaterializationStatusRequest()
        request.feature_package_id.CopyFrom(self._id_proto)

        response = metadata_service.instance().GetMaterializationStatus(request)
        return response.materialization_status

    def _delete_keys(
        self,
        keys: Union[pysparkDF, pd.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> None:
        if not offline and not online:
            raise errors.NO_STORE_SELECTED
        fd = FeatureDefinitionWrapper(self._spec, self._fco_container)
        if offline and any([x.offline_enabled for x in self._proto.materialization_state_transitions]):
            if not fd.offline_store_config.HasField("delta"):
                raise errors.OFFLINE_STORE_NOT_SUPPORTED
        if isinstance(keys, pd.DataFrame):
            if len(keys) == 0:
                raise errors.EMPTY_ARGUMENT("join_keys")
            if len(keys.columns[keys.columns.duplicated()]):
                raise errors.DUPLICATED_COLS_IN_KEYS(", ".join(list(keys.columns)))
            spark_df = ingest_utils.convert_pandas_to_spark_df(keys, self._view_schema)
        elif isinstance(keys, pysparkDF):
            spark_df = keys
        else:
            raise errors.INVALID_JOIN_KEY_TYPE(type(keys))
        utils.validate_entity_deletion_keys_dataframe(df=spark_df, join_keys=fd.join_keys, view_schema=fd.view_schema)
        is_live_workspace = utils.is_live_workspace(self.workspace)
        if not is_live_workspace:
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("delete_keys")

        if online and all([not x.online_enabled for x in self._proto.materialization_state_transitions]):
            print("Online materialization was never enabled. No data to be deleted in online store.")
            online = False

        if offline and all([not x.offline_enabled for x in self._proto.materialization_state_transitions]):
            print("Offline materialization was never enabled. No data to be deleted in offline store.")
            offline = False

        if online or offline:
            self._send_delete_keys_request(keys, online, offline)

    def _freshness(self):
        fresh_request = GetFeatureFreshnessRequest()
        fresh_request.fco_locator.id.CopyFrom(self._id_proto)
        fresh_request.fco_locator.workspace = self.workspace
        return metadata_service.instance().GetFeatureFreshness(fresh_request)

    def _serialize_join_keys(self, spark_keys_df: pysparkDF):
        def serialize_fn(x):
            ret = FeatureValueList()
            for item in x:
                if isinstance(item, int):
                    ret.feature_values.add().int64_value = item
                elif isinstance(item, str):
                    ret.feature_values.add().string_value = item
                elif item is None:
                    ret.feature_values.add().null_value.CopyFrom(NullValue())
                else:
                    raise Exception(f"Unknown type: {type(item)}")
            return b64encode(ret.SerializeToString()).decode()

        serialize = udf(serialize_fn, StringType())
        return spark_keys_df.select(struct(*self.join_keys).alias("join_keys_array")).select(
            serialize("join_keys_array")
        )

    def _send_delete_keys_request(self, keys: Union[pysparkDF, pd.DataFrame], online: bool, offline: bool):

        info_request = GetDeleteEntitiesInfoRequest()
        info_request.feature_definition_id.CopyFrom(self._id_proto)
        info_response = metadata_service.instance().GetDeleteEntitiesInfo(info_request)
        s3_path = info_response.df_path
        online_join_keys_path = s3_path + "/online"
        offline_join_keys_path = s3_path + "/offline"
        deletion_request = DeleteEntitiesRequest()
        deletion_request.fco_locator.id.CopyFrom(self._id_proto)
        deletion_request.fco_locator.workspace = self.workspace
        deletion_request.online = online
        deletion_request.offline = offline
        deletion_request.online_join_keys_path = online_join_keys_path
        deletion_request.offline_join_keys_path = offline_join_keys_path
        if online:
            # We actually generate the presigned url but it's not used for online case
            spark = TectonContext.get_instance()._spark
            if isinstance(keys, pd.DataFrame):
                spark_keys_df = spark.createDataFrame(keys)
            else:
                spark_keys_df = keys
            spark_keys_df = spark_keys_df.distinct()
            join_key_df = self._serialize_join_keys(spark_keys_df)

            # coalesce(1) causes it to write to 1 file, but the jvm code
            # is actually robust to multiple files here
            join_key_df.coalesce(1).write.csv(online_join_keys_path)

        if offline:
            upload_url = info_response.signed_url_for_df_upload_offline
            spark_api.write_dataframe_to_path_or_url(keys, offline_join_keys_path, upload_url, self._view_schema)

        metadata_service.instance().DeleteEntities(deletion_request)
        print(
            "A deletion job has been created. You can track the status of the job in the Web UI under Materialization section or with deletion_status(). The deletion jobs have a type 'Deletion'."
        )
