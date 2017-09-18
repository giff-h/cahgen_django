from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'pack_profiles', views.PackProfileViewSet)
router.register(r'cards_lists', views.CardsListViewSet)
router.register(r'render_specs', views.RenderSpecViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
