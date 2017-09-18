from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CardsList, PackProfile, PDF, RenderSpec


class UserSerializer(serializers.HyperlinkedModelSerializer):
    packprofiles = serializers.HyperlinkedRelatedField(many=True,
                                                       view_name='packprofile-detail',
                                                       read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'packprofiles')


class OwnerMixin:
    owner = serializers.ReadOnlyField(source='owner.username')
    common_fields = ('url', 'id', 'owner', 'created')


class PackProfileSerializer(serializers.HyperlinkedModelSerializer, OwnerMixin):
    class Meta:
        model = PackProfile
        fields = OwnerMixin.common_fields + ('value', 'color_name')


class CardsListSerializer(serializers.HyperlinkedModelSerializer, OwnerMixin):
    class Meta:
        model = CardsList
        fields = OwnerMixin.common_fields + ('name', 'cards', 'profile')


class RenderSpecSerializer(serializers.HyperlinkedModelSerializer, OwnerMixin):
    class Meta:
        model = RenderSpec
        fields = OwnerMixin.common_fields + ('name', 'packs')


class PDFSerializer(serializers.HyperlinkedModelSerializer, OwnerMixin):
    class Meta:
        model = PDF
        fields = OwnerMixin.common_fields + ('pdf', 'render_spec')
