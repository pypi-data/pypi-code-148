from django.urls import path
from .views import FeatureToggleView
from django.conf import settings
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register(r"feature-toggle", FeatureToggleView, "Feature Toggle")

urlpatterns = router.urls
