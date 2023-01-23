from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject


class Activity(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Activities'
        self._version = api_version
    
    def get_inputs(self, parameters:dict={}):
        """
        get_inputs gets the inputs for the activity.

        OUT: if self.value is a dict it returns a input object with the inputs of the activity.
                if self.value is a list it will return a list of inputs objects.
        """
        if isinstance(self.value, dict):
            inputs = Input(self.get_value('id')).get(parameters=parameters)

        elif isinstance(self.value, list):
            inputs = [
                Input(activity_id).get(parameters=parameters)
                for activity_id
                in self.get_value('id') 
            ]

        return inputs
    
    def get_mediaReferences(self, parameters:dict={}):
        """
        get_mediaReferences gets the mediaReferences for the activity.

        OUT: if self.value is a dict it returns a input object with the inputs of the activity.
                if self.value is a list it will return a list of inputs objects.
        """
        if isinstance(self.value, dict):
            ActivityMediaReference = ActivityMediaReference(self.get_value('id')).get(parameters=parameters)

        elif isinstance(self.value, list):
            ActivityMediaReference = [
                ActivityMediaReference(activity_id).get(parameters=parameters)
                for activity_id
                in self.get_value('id') 
            ]

        return ActivityMediaReference

class Input(MaintenanceObject):
    
    def __init__(self, activities_id:str):
        super().__init__()
        self.activities_id = activities_id
        self._endpoint = f'activities/{activities_id}/inputs'

class ActivityMediaReference(MaintenanceObject):
    
    def __init__(self, activities_id:str):
        super().__init__()
        self.activities_id = activities_id
        self._endpoint = f'activities/{activities_id}/mediaReferences'
    
    def post(self, mediaReference_id:str):
        self._endpoint = f'activities/{self.activities_id}/mediaReferences/{mediaReference_id}'
        response = self._client._post(self._api, self._endpoint, self.value)
        self.value = response

        return self