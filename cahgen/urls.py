from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pack_profiles/$', views.pack_profile_list),
    url(r'^pack_profiles/(?P<pk>[0-9]+)/$', views.pack_profile_detail),
]
