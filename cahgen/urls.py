from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^pack_profiles/$', views.PackProfileList.as_view()),
    url(r'^pack_profiles/(?P<pk>[0-9]+)/$', views.PackProfileDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls'))
]
