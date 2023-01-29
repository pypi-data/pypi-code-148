"""
This is a example for jira release
"""
__version__ = "1.0.0"

import os
from datetime import datetime, timezone, timedelta
import pkg_resources
from jira import JIRA
import re


class DailyReleaseModel:
    
    date_format = '%Y.%m.%d'
    
    @staticmethod
    def match_version(version: str):    
        semver_pattern = "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)-(19|20)\d{2}(\.|-)(0[1-9]|1[012])\.(0[1-9]|[12]\d|3[01])$"
        return True if re.match(semver_pattern, version) else False
    
    def __init__(self, vers: list, base_version: str, eod_hour: int)-> dict:
        version = {}
        today_date = datetime.now(timezone(offset=timedelta(hours=eod_hour))).strftime(self.date_format)
        matched_version = [v for v in vers if self.match_version(v)]
        
        if matched_version:
            for v in matched_version:
                arr = v.split('-')
                version.setdefault(arr[0], set())
                version[arr[0]].add(arr[1])
                
            latest_ver = max(version.keys(), key=pkg_resources.parse_version)
            latest_date = max(version[latest_ver], key=lambda d: datetime.strptime(d, self.date_format))
            print("matched versions:", version) 
        else:
            latest_ver = base_version
            latest_date = today_date
        
        self.today_ver = f"{latest_ver}-{today_date}"
        self.latest_ver = f"{latest_ver}-{latest_date}"
        self.today_date = today_date
    
    def daily_version(self)-> str:
        return self.today_ver
    
    def semantic_version(self):
        return self.daily_version().split('-')[0]
    
    def has_unreleased_version(self):
        return self.today_ver != self.latest_ver

        
class JiraTimeBasedDailyRelease:
    
    def __init__(self, base_version: str, eod_hour=11, domain: str=None, email: str=None, secret: str=None):
        self.base_version = base_version
        self.eod_hour = eod_hour
        
        jira_domain = domain or os.getenv("JIRA_DOMAIN")
        jira_email = email or os.getenv("JIRA_EMAIL")
        jira_secret = secret or os.getenv("JIRA_SECRET")
        
        self.jira = JIRA("https://" + jira_domain, basic_auth=(jira_email, jira_secret))
        
    def _create_versions(self, jira_project: str, model: DailyReleaseModel, versions: list):
        
        sem_versions = [v for v in versions if v.name == model.semantic_version()]
        daily_versions = [v for v in versions if v.name == model.daily_version()]
        
        
        s_version = self.jira.create_version(
            project=jira_project, 
            name=model.semantic_version()
        )if not sem_versions else sem_versions[0]
        
        d_version = self.jira.create_version(
            project=jira_project, 
            name=model.daily_version()
        )if not daily_versions else daily_versions[0]
        
        return s_version, d_version
        
    def include_issue(self, jira_issue: str, release_previous=True):
        issue = self.jira.issue(jira_issue)
        project = jira_issue.split('-')[0]
        
        versions = self.jira.project_versions(project)
        version_names = [v.name for v in versions]
        
        model = DailyReleaseModel(
            vers=version_names, 
            base_version=self.base_version, 
            eod_hour=self.eod_hour
        )
        
        assignable_versions = self._create_versions(project, model, versions)
        
        for v in assignable_versions:
            issue.update(fields={'fixVersions': [{'id': v.id}]})
            
        if release_previous and model.has_unreleased_version():
            latest_version = [v for v in versions if v.name == model.latest_ver][0]
            print(latest_version)
            latest_version.update(released=True)
