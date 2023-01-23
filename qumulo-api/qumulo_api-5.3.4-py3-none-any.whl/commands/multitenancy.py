# Copyright (c) 2022 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
import textwrap

import qumulo.lib.opts

from qumulo.lib.request import pretty_json
from qumulo.rest.multitenancy import TenantConfigCreate, TenantConfigCreateFirst, TenantConfigPatch
from qumulo.rest_client import RestClient


class CreateTenantCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_create_tenant'
    SYNOPSIS = 'Create a tenant'
    DESCRIPTION = textwrap.dedent(
        f"""
    {SYNOPSIS}

    Multitenancy allows access to different management and data protocols to be isolated to specific
    tenants by network, including tagged VLANs or the untagged network. Individual services can be
    enabled or disabled for each tenant to allow or disallow access to that protocol on the networks
    associated with the tenant.

    By default, when no tenants are configured, all multitenancy-aware services are available on all
    networks to which the cluster is connected, excepting those services which must be explicitly
    enabled cluster-wide through their own separate server settings.

    The first tenant must be created using multitenancy_enable.

    WARNING: It is possible for access to services to be disabled on all networks, including
    management services such as the REST API, Web UI, and SSH, effectively disabling remote
    administrative access to the cluster. Management services are always available locally through
    a remote or physical server console.
    """
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--name', type=str, help='Unique name of the tenant chosen by the user.', required=True
        )

        parser.add_argument(
            '--network-id',
            type=int,
            action='extend',
            nargs='*',
            default=None,
            help=(
                'List of zero or more network IDs associated with this tenant, as returned by the'
                ' `network_list_networks` command. Each network ID may be assigned to at most one'
                ' tenant.'
            ),
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-web-ui',
            dest='web_ui_enabled',
            action='store_true',
            default=None,
            help='Web UI is accessible from this tenant.',
        )
        group.add_argument(
            '--disable-web-ui',
            dest='web_ui_enabled',
            action='store_false',
            default=None,
            help='Web UI is not accessible from this tenant. This is the default.',
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-rest-api',
            dest='rest_api_enabled',
            action='store_true',
            default=None,
            help='REST API is accessible from this tenant.',
        )
        group.add_argument(
            '--disable-rest-api',
            dest='rest_api_enabled',
            action='store_false',
            default=None,
            help='REST API is not accessible from this tenant. This is the default.',
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-ssh',
            dest='ssh_enabled',
            action='store_true',
            default=None,
            help='SSH is accessible from this tenant.',
        )
        group.add_argument(
            '--disable-ssh',
            dest='ssh_enabled',
            action='store_false',
            default=None,
            help='SSH is not accessible from this tenant. This is the default.',
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-replication',
            dest='replication_enabled',
            action='store_true',
            default=None,
            help='Replication is accessible from this tenant.',
        )
        group.add_argument(
            '--disable-replication',
            dest='replication_enabled',
            action='store_false',
            default=None,
            help='Replication is not accessible from this tenant. This is the default.',
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-nfs',
            dest='nfs_enabled',
            action='store_true',
            default=None,
            help='NFS is accessible from this tenant.',
        )
        group.add_argument(
            '--disable-nfs',
            dest='nfs_enabled',
            action='store_false',
            default=None,
            help='NFS is not accessible from this tenant. This is the default.',
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-smb',
            dest='smb_enabled',
            action='store_true',
            default=None,
            help='SMB is accessible from this tenant.',
        )
        group.add_argument(
            '--disable-smb',
            dest='smb_enabled',
            action='store_false',
            default=None,
            help='SMB is not accessible from this tenant. This is the default.',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        config = TenantConfigCreate(
            name=args.name,
            web_ui_enabled=args.web_ui_enabled,
            rest_api_enabled=args.rest_api_enabled,
            ssh_enabled=args.ssh_enabled,
            replication_enabled=args.replication_enabled,
            nfs_enabled=args.nfs_enabled,
            smb_enabled=args.smb_enabled,
            networks=args.network_id,
        )
        print(pretty_json(rest_client.multitenancy.create_tenant(config).data.to_dict()))


class EnableMultitenancyCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_enable'
    SYNOPSIS = 'Enable multitenancy and create the first tenant'
    DESCRIPTION = textwrap.dedent(
        f"""
    {SYNOPSIS}

    Multitenancy allows access to different management and data protocols to be isolated to specific
    tenants by network, including tagged VLANs or the untagged network. Individual services can be
    enabled or disabled for each tenant to allow or disallow access to that protocol on the networks
    associated with the tenant.

    By default, when no tenants are configured, all multitenancy-aware services are available on all
    networks to which the cluster is connected, excepting those services which must be explicitly
    enabled cluster-wide through their own separate server settings.

    When multitenancy is enabled, the first tenant is created and all existing networks and
    tenant-assignable resources are automatically assigned to this tenant. All multitenancy-aware
    services are enabled to start but may be disabled through multitenancy_modify_tenant. Additional
    tenants may be created through multitenancy_create_tenant. New networks and tenant-assignable
    resources must be explicitly assigned to a tenant.

    WARNING: It is possible for access to services to be disabled on all networks, including
    management services such as the REST API, Web UI, and SSH, effectively disabling remote
    administrative access to the cluster. Management services are always available locally through
    a remote or physical server console.
    """
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--name', type=str, help='Unique name of the tenant chosen by the user.', required=True
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        config = TenantConfigCreateFirst(name=args.name)
        print(pretty_json(rest_client.multitenancy.create_first_tenant(config).data.to_dict()))


class GetTenantCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_get_tenant'
    SYNOPSIS = 'Get a tenant'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--id', type=int, help='The unique ID of the tenant to retrieve.', required=True
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(pretty_json(rest_client.multitenancy.get_tenant(args.id).data.to_dict()))


class ListTenantsCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_list_tenants'
    SYNOPSIS = 'List all tenants'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(pretty_json([config.to_dict() for config in rest_client.multitenancy.list_tenants()]))


class DeleteTenantCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_delete_tenant'
    SYNOPSIS = 'Delete a tenant'
    DESCRIPTION = textwrap.dedent(
        f"""
    {SYNOPSIS}

    A tenant may only be deleted if it has no networks assigned.  Use the
    `multitenancy_modify_tenant` or `multitenancy_reassign_network` commands to unassign or reassign
    any associated networks before deleting a tenant. See `multitenancy_disable` to remove the last
    tenant.
    """
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--id', type=int, help='The unique ID of the tenant to delete.', required=True
        )
        parser.add_argument('--force', action='store_true', help='Do not prompt')

    @staticmethod
    def _ask_confirmation(rest_client: RestClient, tenant_id: int) -> bool:
        cls = DeleteTenantCommand
        tenants = rest_client.multitenancy.list_tenants()
        if len(tenants) == 1:
            msg = (
                'Cannot delete the last tenant in this way. See `multitenancy_disable` to remove '
                'the last tenant.'
            )
            print(msg)
            return False
        else:
            exports = rest_client.nfs.nfs_list_exports()['entries']
            num_exports = sum(1 for export in exports if export['tenant_id'] == tenant_id)
            shares = rest_client.smb.smb_list_shares()['entries']
            num_shares = sum(1 for share in shares if share['tenant_id'] == tenant_id)
            confirmation = (
                'This action will delete the target tenant and permanently delete all NFS exports '
                'and SMB shares that are assigned on the target tenant. All tenant specific '
                'configuration will also be deleted.\n\n'
                'This action will delete {num_exports} NFS exports and {num_shares} SMB shares.'
            ).format(num_exports=num_exports, num_shares=num_shares)
        return qumulo.lib.opts.ask(cls.NAME, confirmation)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.force or DeleteTenantCommand._ask_confirmation(rest_client, args.id):
            rest_client.multitenancy.delete_tenant(args.id)


class DisableMultitenancyCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_disable'
    SYNOPSIS = 'Delete the last tenant and disable multitenancy'
    DESCRIPTION = textwrap.dedent(
        f"""
    {SYNOPSIS}

    Deletes the last and only tenant. See `multitenancy_delete_tenant` to delete tenants.

    WARNING: Disabling multitenancy will delete the last tenant, immediately unassigning any
    networks and making all services accessible on all configured networks.
    """
    )

    @staticmethod
    def main(rest_client: RestClient, _: argparse.Namespace) -> None:
        rest_client.multitenancy.delete_last_tenant()


class ModifyTenantCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_modify_tenant'
    SYNOPSIS = 'Modify a tenant'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--id', type=int, help='The unique ID of the tenant to modify.', required=True
        )

        parser.add_argument(
            '--name',
            type=str,
            help=(
                'Unique name of the tenant chosen by the user. If not specified, the existing name'
                ' will be preserved.'
            ),
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-web-ui',
            dest='web_ui_enabled',
            action='store_true',
            default=None,
            help=(
                'Web UI is accessible from this tenant. If neither --enable-web-ui nor'
                ' --disable-web-ui is specified, the existing setting will be preserved.'
            ),
        )
        group.add_argument(
            '--disable-web-ui',
            dest='web_ui_enabled',
            action='store_false',
            default=None,
            help=(
                'Web UI is not accessible from this tenant. If neither --enable-web-ui nor'
                ' --disable-web-ui is specified, the existing setting will be preserved.'
            ),
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-rest-api',
            dest='rest_api_enabled',
            action='store_true',
            default=None,
            help=(
                'REST API is accessible from this tenant. If neither --enable-rest-api nor'
                ' --disable-rest-api is specified, the existing setting will be preserved.'
            ),
        )
        group.add_argument(
            '--disable-rest-api',
            dest='rest_api_enabled',
            action='store_false',
            default=None,
            help=(
                'REST API is not accessible from this tenant. If neither --enable-rest-api nor'
                ' --disable-rest-api is specified, the existing setting will be preserved.'
            ),
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-ssh',
            dest='ssh_enabled',
            action='store_true',
            default=None,
            help=(
                'SSH is accessible from this tenant. If neither --enable-ssh nor --disable-ssh is'
                ' specified, the existing setting will be preserved.'
            ),
        )
        group.add_argument(
            '--disable-ssh',
            dest='ssh_enabled',
            action='store_false',
            default=None,
            help=(
                'SSH is not accessible from this tenant. If neither --enable-ssh nor --disable-ssh'
                ' is specified, the existing setting will be preserved.'
            ),
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-replication',
            dest='replication_enabled',
            action='store_true',
            default=None,
            help=(
                'Replication is accessible from this tenant. If neither --enable-replication nor'
                ' --disable-replication is specified, the existing setting will be preserved.'
            ),
        )
        group.add_argument(
            '--disable-replication',
            dest='replication_enabled',
            action='store_false',
            default=None,
            help=(
                'Replication is not accessible from this tenant. If neither --enable-replication'
                ' nor --disable-replication is specified, the existing setting will be preserved.'
            ),
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-nfs',
            dest='nfs_enabled',
            action='store_true',
            default=None,
            help=(
                'NFS is accessible from this tenant. If neither --enable-nfs nor --disable-nfs is'
                ' specified, the existing setting will be preserved.'
            ),
        )
        group.add_argument(
            '--disable-nfs',
            dest='nfs_enabled',
            action='store_false',
            default=None,
            help=(
                'NFS is not accessible from this tenant. If neither --enable-nfs nor --disable-nfs'
                ' is specified, the existing setting will be preserved.'
            ),
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable-smb',
            dest='smb_enabled',
            action='store_true',
            default=None,
            help=(
                'SMB is accessible from this tenant. If neither --enable-smb nor --disable-smb is'
                ' specified, the existing setting will be preserved.'
            ),
        )
        group.add_argument(
            '--disable-smb',
            dest='smb_enabled',
            action='store_false',
            default=None,
            help=(
                'SMB is not accessible from this tenant. If neither --enable-smb nor --disable-smb'
                ' is specified, the existing setting will be preserved.'
            ),
        )

        parser.add_argument(
            '--network-id',
            type=int,
            action='extend',
            nargs='*',
            default=None,
            help=(
                'List of zero or more network IDs associated with this tenant, as returned by the'
                ' `network_list_networks` command. Each network ID may be assigned to at most one'
                ' tenant. If specified, this must contain a complete list of all network IDs to be'
                ' assigned to the tenant. Any already-assigned networks not present will be'
                ' unassigned and services will be disabled on those networks. If not specified, the'
                ' existing networks will be preserved.'
            ),
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        config = TenantConfigPatch(
            name=args.name,
            web_ui_enabled=args.web_ui_enabled,
            rest_api_enabled=args.rest_api_enabled,
            ssh_enabled=args.ssh_enabled,
            replication_enabled=args.replication_enabled,
            nfs_enabled=args.nfs_enabled,
            smb_enabled=args.smb_enabled,
            networks=args.network_id,
        )
        print(pretty_json(rest_client.multitenancy.modify_tenant(args.id, config).data.to_dict()))


class ReassignNetworkCommand(qumulo.lib.opts.Subcommand):
    NAME = 'multitenancy_reassign_network'
    SYNOPSIS = 'Reassign a network to different tenant'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--source-tenant-id',
            type=int,
            help='The unique ID of the tenant that contains the network to be moved.',
            required=True,
        )
        parser.add_argument(
            '--target-tenant-id',
            type=int,
            help='The unique ID of the tenant that the network will be moved to.',
            required=True,
        )
        parser.add_argument(
            '--network-id',
            type=int,
            help='The unique ID of the network to be moved.',
            required=True,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.multitenancy.reassign_network(
            source_tenant_id=args.source_tenant_id,
            target_tenant_id=args.target_tenant_id,
            network_id=args.network_id,
        )
