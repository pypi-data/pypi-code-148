import itertools
import os
from pathlib import Path
from typing import List

import requests
import yaml
from shopcloud_secrethub import SecretHub
from tqdm import tqdm

from . import exceptions, helpers


class Config:
    FILENAME = '.organize.yaml'
    VERSION = 'V1'

    def __init__(self):
        self.version = None
        self.data_dir = None
        # Github
        self.repo_owner = None
        self.repo_name = None
        self.authorization_github_username = None
        self.authorization_github_pwd = None

    def load(self) -> bool:
        if not Path(Config.FILENAME).exists():
            return False
        with open(Config.FILENAME) as f:
            data = yaml.safe_load(f)
            self.version = data.get('version', '')
            self.data_dir = data.get('data_dir')
            self.repo_owner = data.get('repo_owner')
            self.repo_name = data.get('repo_name')
            self.authorization_github_username = data.get('authorization_github_username')
            self.authorization_github_pwd = data.get('authorization_github_pwd')

        if str(self.version).strip() != self.VERSION:
            raise exceptions.ConfigInvalidVersion()

        return True

    def save(self):
        with open(Config.FILENAME, 'w') as f:
            yaml.dump(self.dict(), f)

    def dict(self):
        return {
            'version': self.VERSION,
            'data_dir': self.data_dir,
            'repo_owner': self.repo_owner,
            'repo_name': self.repo_name,
            'authorization_github_username': self.authorization_github_username,
            'authorization_github_pwd': self.authorization_github_pwd,
        }


class Issue:
    def __init__(self, pk: str, name: str, **kwargs):
        self.pk = pk
        self.name = name
        self.title = kwargs.get('title', name)
        self.assignees = kwargs.get('assignees', [])
        self.labels = kwargs.get('labels', [])
        self.body = kwargs.get('body')

    def dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'title': self.title,
            'assignees': self.assignees,
            'labels': self.labels,
            'body': self.body,
        }

    def __repr__(self):
        return f'Issue: {self.name}'

    @staticmethod
    def from_file(filename: str, content: str, path: str):
        pieces = content.split('---')
        data = yaml.safe_load(pieces[0])
        last_dir = path.split('/')[-1]
        return Issue(
            f"{path}/{filename}",
            filename.replace('.yaml', ''),
            body=pieces[1].strip(),
            title=data.get('title'),
            assignees=[x.strip() for x in data.get('assignees', '').split(',')],
            labels=[f'organize-task-{last_dir}'],
        )

    def create_issue(self, owner: str, repo: str, **kwargs) -> str:
        data = {
            'title': self.title,
            'body': self.body,
            'assignees': self.assignees,
            'labels': self.labels,
        }

        if kwargs.get('simulate', False):
            return f'https://github.com/{owner}/{repo}/issues/<id>`'

        response = requests.post(
            f'https://api.github.com/repos/{owner}/{repo}/issues',
            auth=(
                kwargs.get('username'),
                kwargs.get('password'),
            ),
            json=data
        )
        if not (200 <= response.status_code < 300):
            raise exceptions.IssueCreateException(response.text)

        return response.json().get('html_url')


def parse_tasks(directory: str) -> List[Issue]:
    def extract(dir, sub_dirs, files):
        for file in files:
            if file.endswith('.yaml'):
                with open(os.path.join(dir, file)) as f:
                    content = f.read()
                    yield Issue.from_file(file, content, dir.split('/')[-1])

    issues = [list(extract(dir, sub_dirs, files)) for dir, sub_dirs, files in os.walk(directory) if "/tasks" in dir]
    issues = list(itertools.chain(*issues))
    return issues


def main(args) -> int:
    if not hasattr(args, 'which'):
        print(
            helpers.bcolors.FAIL
            + 'Can not parse action use --help'
            + helpers.bcolors.ENDC
        )
        return 1

    if hasattr(args, 'secrethub_token'):
        hub = SecretHub(user_app="organize-cli", api_token=args.secrethub_token)
    else:
        hub = SecretHub(user_app="organize-cli")

    if hasattr(args, 'debug') and args.debug:
        print(args)

    config = Config()

    if args.which == 'init':
        config.data_dir = args.data_dir or helpers.ask_for('Data-Dir', 'organize')
        print('# Github')
        config.repo_owner = args.repo_owner or helpers.ask_for('Repo-Owner', 'Talk-Point')
        config.repo_name = args.repo_name or helpers.ask_for('Repo-Name', 'IT')

        # secrethub
        print('# Github Authorization')
        username = args.github_username or helpers.ask_for('Username', 'TP-Server')
        token = args.github_token or helpers.ask_for('Token')
        config.authorization_github_username = f'talk-point/app-organize/credentials/{config.repo_owner.lower()}/{config.repo_name.lower()}/username'
        if not args.simulate:
            print(f'Write to secrethub {config.authorization_github_username}')
            hub.write(config.authorization_github_username, username)
        config.authorization_github_pwd = f'talk-point/app-organize/credentials/{config.repo_owner.lower()}/{config.repo_name.lower()}/token'
        if not args.simulate:
            print(f'Write to secrethub {config.authorization_github_pwd}')
            hub.write(config.authorization_github_pwd, token)

        config.save()
        print(helpers.bcolors.OKGREEN + f'Config saved under `{Config.FILENAME}`' + helpers.bcolors.ENDC)
    elif args.which == 'tasks':
        try:
            is_loaded = config.load()
        except exceptions.ConfigInvalidVersion:
            print(
                helpers.bcolors.FAIL
                + 'Config file is not compatible with this version. Please run `init` again.'
                + helpers.bcolors.ENDC
            )
            return 1

        if not is_loaded:
            print(
                helpers.bcolors.FAIL
                + 'No config file found. Please run `init` first.'
                + helpers.bcolors.ENDC
            )
            return 1

        if args.action == 'list':
            issues = parse_tasks(f'./{config.data_dir}')
            for issue in issues:
                print(f'+ {issue.pk}')
        elif args.action == 'describe':
            if args.pk is None:
                print(
                    helpers.bcolors.FAIL
                    + 'no pk specified'
                    + helpers.bcolors.ENDC
                )
                return 1
            issues = [x for x in parse_tasks(f'./{config.data_dir}') if x.pk == args.pk]
            if len(issues) == 0:
                print(
                    helpers.bcolors.FAIL
                    + 'no issue found'
                    + helpers.bcolors.ENDC
                )
                return 1
            issue = issues[0]
            print(f'Issue: {issue.pk}')
            print(f'+ title: {issue.title}')
            print(f'+ assignees: {issue.assignees}')
            print(f'+ labels: {issue.labels}')
            print('---')
            print(f'{issue.body}')
            print('---')
        elif args.action == 'create-issues':
            print('+ Create Issues')
            issues = list(parse_tasks(f'./{config.data_dir}'))
            is_success = True
            for issue in tqdm(issues):
                try:
                    url = issue.create_issue(
                        config.repo_owner,
                        config.repo_name,
                        username=helpers.fetch_secret(hub, config.authorization_github_username, simulate=args.simulate),
                        password=helpers.fetch_secret(hub, config.authorization_github_pwd, simulate=args.simulate),
                        simulate=args.simulate,
                    )
                    print(
                        helpers.bcolors.OKGREEN
                        + f'Issue created {url}`'
                        + helpers.bcolors.ENDC
                    )
                except exceptions.IssueCreateException:
                    print(
                        helpers.bcolors.OKGREEN
                        + f'Issue error {issue.pk}`'
                        + helpers.bcolors.ENDC
                    )
                    is_success = False
            if not is_success:
                return 1
        elif args.action == 'create-issue':
            if args.pk is None:
                print(
                    helpers.bcolors.FAIL
                    + 'no pk specified'
                    + helpers.bcolors.ENDC
                )
                return 1
            issues = [x for x in parse_tasks(f'./{config.data_dir}') if x.pk == args.pk]
            if len(issues) == 0:
                print(
                    helpers.bcolors.FAIL
                    + 'no issue found'
                    + helpers.bcolors.ENDC
                )
                return 1
            issue = issues[0]
            url = issue.create_issue(
                config.repo_owner,
                config.repo_name,
                username=helpers.fetch_secret(hub, config.authorization_github_username, simulate=args.simulate),
                password=helpers.fetch_secret(hub, config.authorization_github_pwd, simulate=args.simulate),
                simulate=args.simulate,
            )
            print(
                helpers.bcolors.OKGREEN
                + f'Issue created {url}`'
                + helpers.bcolors.ENDC
            )

    return 0
