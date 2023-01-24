from netbox.api.routers import NetBoxRouter
from .views import DeviceGroupViewSet, ChangeLogViewSet

router = NetBoxRouter()
router.register('device-group', DeviceGroupViewSet)
router.register('changelog', ChangeLogViewSet)
urlpatterns = router.urls