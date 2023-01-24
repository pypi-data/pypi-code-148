import argparse
import sys

from . import cli

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='EventBus',
        prog='shopcloud-eventbus'
    )

    subparsers = parser.add_subparsers(help='commands', title='commands')
    parser.add_argument('--debug', '-d', help='Debug', action='store_true')
    parser.add_argument('--secrethub-token', help='Secrethub-Token', type=str)

    parser_deploy = subparsers.add_parser('deploy', help='deploy the eventbus')
    parser_deploy.add_argument('--simulate', '-s', help='Simulate the process', action='store_true')
    parser_deploy.set_defaults(which='deploy')

    parser_init = subparsers.add_parser('init', help='init the eventbus')
    parser_init.add_argument('--project', help='Project', type=str)
    parser_init.add_argument('--region', help='Region like europe-west3', type=str)
    parser_init.add_argument('--app-endpoint', help='App endpoint like https://<project>.ey.r.appspot.com)', type=str)
    parser_init.add_argument('--secrethub-endpoint-user', help='Secrethub path for auth user like talk-point/app-eventbus-test/production/evenbus-user', type=str)
    parser_init.add_argument('--secrethub-endpoint-pwd', help='Secrethub path for auth pwd like talk-point/app-eventbus-test/production/evenbus-pwd', type=str)
    parser_init.set_defaults(which='init')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    rc = cli.main(args)
    if rc != 0:
        sys.exit(rc)
