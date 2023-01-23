from AIH_SDK.Risks.RisksObject import RisksObject


class RiskAssessmentTechnique(RisksObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'RiskAssessmentTechniques'
        self._version = api_version