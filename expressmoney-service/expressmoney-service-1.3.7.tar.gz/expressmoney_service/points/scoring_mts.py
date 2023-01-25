__all__ = ('ScoringMTSPoint',)

from expressmoney_service.api import *

_SERVICE = 'services'


class ScoringMTSCreateContract(Contract):
    msisdn = serializers.IntegerField()


class ScoringMTSID(ID):
    _service = _SERVICE
    _app = 'scoring_mts'
    _view_set = 'scoring'


class ScoringMTSPoint(CreatePointMixin, ContractPoint):
    _point_id = ScoringMTSID()
    _create_contract = ScoringMTSCreateContract
