from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

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


@csrf_exempt
def pack_profile_list(request):
    """
    List all pack profiles, or create a new one.
    """
    if request.method == 'GET':
        pp = PackProfile.objects.all()
        serializer = PackProfileSerializer(pp, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PackProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def pack_profile_detail(request, pk):
    """
    Retrieve, update or delete a pack profile.
    """
    try:
        pp = PackProfile.objects.get(pk=pk)
    except PackProfile.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PackProfileSerializer(pp)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PackProfileSerializer(pp, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        pp.delete()
        return HttpResponse(status=204)
