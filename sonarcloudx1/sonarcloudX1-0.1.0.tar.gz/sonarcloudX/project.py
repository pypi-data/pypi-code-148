import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudX.abstract import AbstractSonar

# Represents a software Project
class Project(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(Project,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_all(self, today=False): 
		projects = []
		try:
			logging.info("Start function: get_projects")
			
			result = self.sonar.projects.search_projects(organization=self.organization_name)
			
			if today == False:
				projects = result['components']
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Projects")
		
		return projects	
