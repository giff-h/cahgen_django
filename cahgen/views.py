from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
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


@api_view(['GET', 'POST'])
def pack_profile_list(request):
    """
    List all pack profiles, or create a new one.
    """
    if request.method == 'GET':
        pp = PackProfile.objects.all()
        serializer = PackProfileSerializer(pp, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PackProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def pack_profile_detail(request, pk):
    """
    Retrieve, update or delete a pack profile.
    """
    try:
        pp = PackProfile.objects.get(pk=pk)
    except PackProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PackProfileSerializer(pp)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PackProfileSerializer(pp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
