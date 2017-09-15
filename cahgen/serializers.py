from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CardsList, PackProfile, PDF, RenderSpec


class UserSerializer(serializers.ModelSerializer):
    packprofiles = serializers.PrimaryKeyRelatedField(many=True, queryset=PackProfile.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'packprofiles')


class PackProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = PackProfile
        fields = ('owner', 'id', 'created', 'value', 'color_name')


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
