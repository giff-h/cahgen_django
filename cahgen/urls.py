from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^pack_profiles/$',                views.PackProfileList.as_view(),   name='packprofile-list'),
    url(r'^pack_profiles/(?P<pk>[0-9]+)/$', views.PackProfileDetail.as_view(), name='packprofile-detail'),
    url(r'^users/$',                views.UserList.as_view(),   name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
])

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls'))
]
