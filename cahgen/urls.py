from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^pack_profiles/$', views.PackProfileList.as_view()),
    url(r'^pack_profiles/(?P<pk>[0-9]+)/$', views.PackProfileDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
