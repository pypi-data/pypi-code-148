from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('event_participation_levels')
class EventParticipationLevels(Entity):
    LIST_URL = '/event/v1/participationlevels'
