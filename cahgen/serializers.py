from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CardsList, PackProfile, PDF, RenderSpec


class UserSerializer(serializers.HyperlinkedModelSerializer):
    packprofiles = serializers.HyperlinkedRelatedField(many=True,
                                                       view_name='packprofile-detail',
                                                       read_only=True)  # FIXME not showing up properly, throws 500

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'packprofiles')


class PackProfileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = PackProfile
        fields = ('url', 'id', 'owner', 'created', 'value', 'color_name')


class CardsListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CardsList
        fields = ('url', 'id', 'created', 'name', 'cards', 'profile')


class RenderSpecSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RenderSpec
        fields = ('url', 'id', 'created', 'name', 'packs')


class PDFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
        fields = ('url', 'id', 'created', 'pdf', 'render_spec')
