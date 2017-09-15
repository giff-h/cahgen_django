from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response

from .models import PackProfile, CardsList, RenderSpec, PDF
from .serializers import UserSerializer, GroupSerializer, PackProfileSerializer, CardsListSerializer,\
                         RenderSpecSerializer, PDFSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
