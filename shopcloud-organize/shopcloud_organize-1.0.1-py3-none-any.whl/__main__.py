import argparse
import sys

from . import cli

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Organize',
        prog='shopcloud-organize'
    )

    subparsers = parser.add_subparsers(help='commands', title='commands')
    parser.add_argument('--debug', '-d', help='Debug', action='store_true')
    parser.add_argument('--simulate', '-s', help='Simulate the process', action='store_true')
    parser.add_argument('--secrethub-token', help='Secrethub-Token', type=str)

    parser_deploy = subparsers.add_parser('tasks', help='task namespace')
    parser_deploy.add_argument(
        'action',
        const='generate',
        nargs='?',
        choices=['list', 'describe', 'create-issue', 'create-issues']
    )
    parser_deploy.add_argument('pk', const='generate', nargs='?')
    parser_deploy.set_defaults(which='tasks')

    parser_init = subparsers.add_parser('init', help='init the organize')
    parser_init.add_argument('--repo-owner', help='Repo Owner', type=str)
    parser_init.add_argument('--repo-name', help='Repo name', type=str)
    parser_init.add_argument('--data-dir', help='data directory', type=str)
    parser_init.add_argument('--github-username', help='Authorization on github username', type=str)
    parser_init.add_argument('--github-token', help='Authorization on github token', type=str)
    parser_init.set_defaults(which='init')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    rc = cli.main(args)
    if rc != 0:
        sys.exit(rc)
