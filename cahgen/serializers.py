from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import CardsList, PackProfile, PDF, RenderSpec


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PackProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackProfile
        fields = ('id', 'created', 'value', 'color_name')


class CardsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardsList
        fields = ('id', 'created', 'name', 'cards', 'profile')


class RenderSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenderSpec
        fields = ('id', 'created', 'name', 'packs')


class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ('id', 'created', 'pdf', 'render_spec')
