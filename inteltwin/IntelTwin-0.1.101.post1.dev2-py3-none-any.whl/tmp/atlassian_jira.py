# Refer to the following guide
# https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/
# https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get
# https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/#api-group-issue-worklogs
# https://developer.atlassian.com/console/myapps/87fce578-508e-479f-ac52-4c8a5760046c/authorization/auth-code-grant

from collections import Counter
from typing import cast
from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
import json


# Some Authentication Methods
class JiraAccess:
    _jira_handle: JIRA = None
    _jira_config = None
    _jira_myself = None
    _jira_properties = None

    def __init__(self):
        pass

    def init_auth(self, json_file_path='/Users/vincent/.pythonbot/jira_access.json'):
        self._jira_config = json.load(open(json_file_path, 'r'))
        self._jira_handle = JIRA(
            server="https://wavelet.atlassian.net",
            basic_auth=(self._jira_config['email'], self._jira_config['access_token']))
        self._jira_myself = self._jira_handle.myself()
        self._jira_properties = self._jira_handle.application_properties()

    def test_jira(self):
        issues = cast(ResultList[Issue], self._jira_handle.search_issues("assignee=leehongfay"))
        # Find the top three projects containing issues reported by admin
        print(issues)
        top_three = Counter([issue.fields.project.key for issue in issues]).most_common(3)
        print(top_three)
