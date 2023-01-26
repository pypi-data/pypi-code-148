
import factory
from .project import Project


class ProjectFactory(factory.Factory):
    
    class Meta:
        model = Project
        
    personal_access_token = None
    sonar_url = None

