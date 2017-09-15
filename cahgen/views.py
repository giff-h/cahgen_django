from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .models import PackProfile, CardsList, RenderSpec, PDF
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, PackProfileSerializer, CardsListSerializer,\
                         RenderSpecSerializer, PDFSerializer


class UserList(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PackProfileList(generics.ListCreateAPIView):
    """
    List all pack profiles, or create a new one.
    """
    queryset = PackProfile.objects.all()
    serializer_class = PackProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PackProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a pack profile.
    """
    queryset = PackProfile.objects.all()
    serializer_class = PackProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
