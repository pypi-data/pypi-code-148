from sonarqube import SonarCloudClient
from abc import ABC


class AbstractSonar(ABC):

    def __init__(self, personal_access_token, sonar_url):

        self.sonar = SonarCloudClient(sonarcloud_url = sonar_url, token = personal_access_token)

    
    def set_organization_name (self, organization_name):

        self.organization_name = organization_name