from django.conf.urls import url
from django.urls import path
from .models import Annotation, Tag, AnnotationTarget, NeedleActivity
from .views import AnnotationViewset, AnnotationTargetViewset, TagViewset, AnnotationTargetIntersectionViewset, \
    AnnotationIntersectionsAfterViewset, AnnotationIntersectionsBeforeViewset

urlpatterns = [
    url(r'^annotations/', AnnotationViewset.urls(model_prefix="annotation", model=Annotation)),
    url(r'^annotationtargets/', AnnotationTargetViewset.urls(model_prefix="annotationtarget", model=AnnotationTarget)),
    path('annotationtargetsintersection/<url>/<date>', AnnotationTargetIntersectionViewset.as_view({'get': 'list'}, model=AnnotationTarget)),
    path('annotationintersections/before/<url>/<date>',
        AnnotationIntersectionsBeforeViewset.as_view({'get': 'list'}, model=Annotation)),
    path('annotationintersections/after/<url>/<date>',
        AnnotationIntersectionsAfterViewset.as_view({'get': 'list'}, model=Annotation)),
    url(r'^users/(?P<slug>[\w\-\.]+)/yarn/', AnnotationViewset.urls(model_prefix="yarn", model=Annotation)),
    url(r'^users/(?P<slug>[\w\-\.]+)/tags', TagViewset.urls(model_prefix="tags", model=Tag)),
]
