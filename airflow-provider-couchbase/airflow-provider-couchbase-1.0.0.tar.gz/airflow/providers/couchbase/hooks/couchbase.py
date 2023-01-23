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
from datetime import timedelta

# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions

from airflow.hooks.base import BaseHook


class CouchbaseHook(BaseHook):
    """
    Wrapper for connection to interact with couchbase in-memory data structure store.

    Couchbase Connection Documentation
    https://docs.couchbase.com/python-sdk/current/hello-world/start-using-sdk.html
    """

    conn_name_attr = "couchbase_conn_id"
    default_conn_name = "couchbase_default"
    conn_type = "couchbase"
    hook_name = "couchbase"

    def __init__(self, conn_id: str = default_conn_name, *arg, **kwargs) -> None:
        """
        Prepares hook to connect to a couchbase.

        param couchbase_conn_id:   the name of the connection that has the parameters
                                    that we need to connect to couchbase.
        """
        super().__init__(*arg, **kwargs)
        self.couchbase_conn_id = conn_id
        self.host = None
        self.username = None
        self.password = None
        self.port = None
        self.extra = None
        self.uri = self._create_uri()
        self.scheme = None
        self.client = None

    def _create_uri(self) -> dict:
        """
        Create URI string & check if ssl enabled from the given credentials.
        :return: Dict uri string + ssl filepath.
        """
        cnx = self.get_connection(self.couchbase_conn_id)
        self.host = cnx.host
        self.extra = cnx.extra_dejson.copy()

        # check for ssl parameters in cnx.extra
        ssl_arg_names = [
            "cert_path",
            "ssl",
            "ssl_cert_reqs",
            "ssl_ca_certs",
            "ssl_keyfile",
            "ssl_cert_file",
            "ssl_check_hostname",
        ]

        # Retrieve TLS certificate path
        cert_path_value = next((value for key, value in self.extra.items() if key in ssl_arg_names), None)
        self.scheme = "couchbases" if cert_path_value else "couchbase"
        self.port = "" if cnx.port is None else f":{cnx.port}"
        return {
            "cert_path": cert_path_value,
            "uri": f"{self.scheme}://{self.host}{self.port}"
        }

    def get_conn(self) -> Cluster:
        """Returns a couchbase connection."""

        cnx = self.get_connection(self.couchbase_conn_id)
        self.username = cnx.login
        self.password = cnx.password

        # Check if couchbase client already exist
        if not self.client:
            self.log.debug(
                'Initializing couchbase object for conn_id "%s" on %s',
                self.couchbase_conn_id,
                self.uri
            )
            authentication = PasswordAuthenticator(
                    self.username,
                    self.password,
                    cert_path=self.uri["cert_path"]
            )

            # Get a reference to your cluster
            self.client = Cluster(self.uri["uri"], ClusterOptions(authentication))

            # Wait until the cluster is ready for use.
            self.client.wait_until_ready(timedelta(seconds=5))

        return self.client

    def close_conn(self) -> None:
        """Closes connection"""
        client = self.client
        if client is not None:
            client.close()
            self.client = None
