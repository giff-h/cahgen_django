from django.contrib.auth.models import User
from rest_framework import mixins, permissions, views, viewsets
from rest_framework.response import Response

from .models import PackProfile, CardsList, RenderSpec, PDF
from .permissions import IsOwner
from .serializers import UserSerializer, PackProfileSerializer, CardsListSerializer,\
                         RenderSpecSerializer, PDFSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BaseViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (IsOwner, permissions.IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PackProfileViewSet(BaseViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, and `destroy` actions.
    """
    queryset = PackProfile.objects.all()
    serializer_class = PackProfileSerializer


class CardsListViewSet(BaseViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, and `destroy` actions.
    """
    queryset = CardsList.objects.all()
    serializer_class = CardsListSerializer


class RenderSpecViewSet(BaseViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, and `destroy` actions.
    """
    queryset = RenderSpec.objects.all()
    serializer_class = RenderSpecSerializer


class PDFViewSet(BaseViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer


class PDFDownload(views.APIView):
    """
    View to download the generated PDF content.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Stream the application/pdf content, or 404 if it's not rendered yet.
        """
        return Response(headers={'filename': 'name.pdf'}, content_type='application/pdf')
