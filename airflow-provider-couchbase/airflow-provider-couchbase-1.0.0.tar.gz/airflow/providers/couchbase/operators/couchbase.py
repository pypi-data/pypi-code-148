#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Mapping, Sequence

from airflow.models import BaseOperator
from airflow.providers.couchbase.hooks.couchbase import CouchbaseHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class CouchbaseOperator(BaseOperator):
    """
    Executes N1QL code in a specific couchbase database

    :param n1ql: the n1ql code to be executed. Can receive a str representing a sql statement
    :param couchbase_conn_id: Reference to :ref:`Couchbase connection id <howto/connection:couchbase>`.
    """

    template_fields: Sequence[str] = ("n1ql",)
    ui_color = "#ea2328"

    def __init__(
        self,
        *,
        n1ql: str | list[str],
        couchbase_conn_id: str = "couchbase_default",
        parameters: Iterable | Mapping | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.couchbase_conn_id = couchbase_conn_id
        self.n1ql = n1ql
        self.parameters = parameters

    def execute(self, context: Context) -> None:
        self.log.info("Executing: %s", self.n1ql)
        hook = CouchbaseHook(conn_id=self.couchbase_conn_id).get_conn()
        result = hook.query(self.n1ql).execute()
        self.log.info("Query result: %s", result)

