from AIH_SDK.Risks.RisksObject import RisksObject


class RiskAssessmentResult(RisksObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'RiskAssessmentResults'
        self._version = api_version