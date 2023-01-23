from AIH_SDK.Risks.RisksObject import RisksObject


class Mitigation(RisksObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Mitigations'
        self._version = api_version
    

    def get(self, riskId:str):
        # super().get(parameters={'riskId': riskId})
        return super().get(parameters=[('riskId', riskId)])