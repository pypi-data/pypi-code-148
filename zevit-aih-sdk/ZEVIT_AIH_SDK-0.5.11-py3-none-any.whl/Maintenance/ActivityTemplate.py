from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject


class ActivityTemplate(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'ActivityTemplates'
        self._version = api_version
        
    def get_inputs(self, parameters:dict={}):
        """
        get_inputs gets the inputs for the activityTemplate.

        OUT: if self.value is a dict it returns a input object with the inputs of the activityTemplate.
                if self.value is a list it will return a list of inputs objects.
        """
        if isinstance(self.value, dict):
            inputs = TemplateInput(self.get_value('id')).get(parameters=parameters)

        elif isinstance(self.value, list):
            inputs = [
                TemplateInput(activityTemplate_id).get(parameters=parameters)
                for activityTemplate_id
                in self.get_value('id') 
            ]

        return inputs

class TemplateInput(MaintenanceObject):
    
    def __init__(self, ActivityTemplateId:str):
        super().__init__()
        self.ActivityTemplateId = ActivityTemplateId
        self._endpoint = f'ActivityTemplates/{ActivityTemplateId}/inputs'

