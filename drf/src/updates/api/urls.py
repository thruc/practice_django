from django.conf.urls import url

from .views import (
            UpdateModelDetailAPIView,
            UpdateModelListAPIView,
    )

from ..views import (
    JsonCBV2,
    JsonCBV
)

urlpatterns = [
    url(r'^$', UpdateModelListAPIView.as_view()), # api/updates/ - List/Create
    url(r'^(?P<id>\d+)/$', UpdateModelDetailAPIView.as_view()),
    url(r'^vba/$', JsonCBV2.as_view()),
    url(r'^vba2/$', JsonCBV.as_view()),

]