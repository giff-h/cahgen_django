from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import PackProfile, CardsList, RenderSpec, PDF
from .permissions import IsOwner
from .serializers import UserSerializer, PackProfileSerializer, CardsListSerializer,\
                         RenderSpecSerializer, PDFSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'packprofiles': reverse('packprofile-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser, IsOwner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PackProfileViewSet(BaseViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = PackProfile.objects.all()
    serializer_class = PackProfileSerializer


class CardsListViewSet(BaseViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = CardsList.objects.all()
    serializer_class = CardsListSerializer


class RenderSpecViewSet(BaseViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = RenderSpec.objects.all()
    serializer_class = RenderSpecSerializer
