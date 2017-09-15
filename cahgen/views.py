from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets

from .models import PackProfile, CardsList, RenderSpec, PDF
from .serializers import UserSerializer, PackProfileSerializer, CardsListSerializer,\
                         RenderSpecSerializer, PDFSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PackProfileList(generics.ListCreateAPIView):
    """
    List all pack profiles, or create a new one.
    """
    queryset = PackProfile.objects.all()
    serializer_class = PackProfileSerializer


class PackProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a pack profile.
    """
    queryset = PackProfile.objects.all()
    serializer_class = PackProfileSerializer
