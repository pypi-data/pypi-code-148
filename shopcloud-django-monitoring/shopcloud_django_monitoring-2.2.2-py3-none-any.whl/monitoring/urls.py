from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter()
router.register(r"api/sources", views.SourceViewSet)
router.register(r"api/metrics", views.MetricViewSet)

urlpatterns = []
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
