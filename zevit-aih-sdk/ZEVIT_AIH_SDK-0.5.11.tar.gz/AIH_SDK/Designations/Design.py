from AIH_SDK.Designations.DesignationsObject import DesignationsObject


class Design(DesignationsObject):
    
    def __init__(self, api_version='1.1'):
        super().__init__()
        self._endpoint = 'designs'
        self._version = api_version

    def get_objects(self, parameters:dict={}):
        """
        get_objects gets the objects in the design.

        OUT: if self.value is a dict it returns a DesignObject object with the objects of the design.
             if self.value is a list it will return a list of DesignObject objects.
        """
        if isinstance(self.value, dict):
            objects = DesignObject(self.get_value('id')).get(parameters=parameters)
        
        elif isinstance(self.value, list):
            objects = [
                DesignObject(design_id).get(parameters=parameters)
                for design_id
                in self.get_value('id')
            ]
        
        return objects



class DesignObject(DesignationsObject):
    
    def __init__(self, design_id:str):
        super().__init__()
        self.design_id = design_id
        self._endpoint = f'designs/{design_id}/objects'

