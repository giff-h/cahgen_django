from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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


class PackProfileList(APIView):
    """
    List all pack profiles, or create a new one.
    """
    def get(self, request, format=None):
        pp = PackProfile.objects.all()
        serializer = PackProfileSerializer(pp, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PackProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackProfileDetail(APIView):
    """
    Retrieve, update or delete a pack profile.
    """
    def get_object(self, pk):
        try:
            return PackProfile.objects.get(pk=pk)
        except PackProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pp = self.get_object(pk)
        serializer = PackProfileSerializer(pp)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pp = self.get_object(pk)
        serializer = PackProfileSerializer(pp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pp = self.get_object(pk)
        pp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
