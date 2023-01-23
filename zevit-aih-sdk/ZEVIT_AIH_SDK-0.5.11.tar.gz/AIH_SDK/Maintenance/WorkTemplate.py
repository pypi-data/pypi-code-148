from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject


class WorkTemplate(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'WorkTemplates'
        self._version = api_version
    def get_activities(self, parameters:dict={}):
        """
        get_activities gets the workTemplateActivity for the workTemplate.

        OUT: if self.value is a dict it returns a input object with the workTemplateActivity of the workTemplate.
                if self.value is a list it will return a list of workTemplateActivity objects.
        """
        if isinstance(self.value, dict):
            workTemplateActivity = WorkTemplateActivity(self.get_value('id')).get(parameters=parameters)

        elif isinstance(self.value, list):
            workTemplateActivity = [
                WorkTemplateActivity(design_id).get(parameters=parameters)
                for design_id
                in self.get_value('id')
            ]

        return workTemplateActivity

class WorkTemplateActivity(MaintenanceObject):

    def __init__(self, workTemplate_id:str):
        super().__init__()
        self.workTemplate_id = workTemplate_id
        self._endpoint = f'workTemplates/{workTemplate_id}/activities'