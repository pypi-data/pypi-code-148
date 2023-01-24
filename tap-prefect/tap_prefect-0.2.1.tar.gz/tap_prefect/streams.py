"""Stream type classes for tap-prefect."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.typing import PropertiesList, Property, StringType, ObjectType, DateTimeType, ArrayType, IntegerType

# from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_prefect.client import PrefectStream

# # TODO: Delete this is if not using json files for schema definition
# SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# # TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
# #       - Copy-paste as many times as needed to create multiple stream types.


class FlowRunsStream(PrefectStream):
    name = "flow_runs"
    # primary_keys = ["id"]
    replication_key = None  # Incremental bookmarks not needed
    # schema_filepath = SCHEMAS_DIR / "flow-runs.json"
    schema = PropertiesList(
        Property("id", StringType, required=True),
        Property("name", StringType, required=True),
        Property("version", IntegerType, required=True),
        Property(
            "project", ObjectType(Property("id", StringType, required=True), Property("name", StringType, required=True)), required=True
        ),
        Property(
            "flow_runs",
            ArrayType(ObjectType(Property("id", StringType), Property("state", StringType), Property("start_time", DateTimeType))),
            required=True,
        ),
    ).to_dict()
    url_base = "https://api.prefect.io"
    query = """        
        flow {
            id
            name
            version
            project {
                id
                name
            }
            flow_runs{
                id
                state
                start_time
            }
        }
    """


# class UsersStream(PrefectStream):
#     """Define custom stream."""

#     name = "users"
#     # Optionally, you may also use `schema_filepath` in place of `schema`:
#     # schema_filepath = SCHEMAS_DIR / "users.json"
#     schema = th.PropertiesList(
#         th.Property("name", th.StringType),
#         th.Property("id", th.StringType, description="The user's system ID"),
#         th.Property("age", th.IntegerType, description="The user's age in years"),
#         th.Property("email", th.StringType, description="The user's email address"),
#         th.Property(
#             "address",
#             th.ObjectType(
#                 th.Property("street", th.StringType),
#                 th.Property("city", th.StringType),
#                 th.Property("state", th.StringType, description="State name in ISO 3166-2 format"),
#                 th.Property("zip", th.StringType),
#             ),
#         ),
#     ).to_dict()
#     primary_keys = ["id"]
#     replication_key = None
#     graphql_query = """
#         users {
#             name
#             id
#             age
#             email
#             address {
#                 street
#                 city
#                 state
#                 zip
#             }
#         }
#         """


# class GroupsStream(PrefectStream):
#     """Define custom stream."""

#     name = "groups"
#     schema = th.PropertiesList(
#         th.Property("name", th.StringType),
#         th.Property("id", th.StringType),
#         th.Property("modified", th.DateTimeType),
#     ).to_dict()
#     primary_keys = ["id"]
#     replication_key = "modified"
#     graphql_query = """
#         groups {
#             name
#             id
#             modified
#         }
#         """
