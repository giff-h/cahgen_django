from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CardsList, PackProfile, PDF, RenderSpec


class UserSerializer(serializers.HyperlinkedModelSerializer):
    packprofiles = serializers.HyperlinkedRelatedField(many=True,
                                                       view_name='packprofile-detail',
                                                       read_only=True)
    cardslists = serializers.HyperlinkedRelatedField(many=True,
                                                     view_name='cardslist-detail',
                                                     read_only=True)
    renderspecs = serializers.HyperlinkedRelatedField(many=True,
                                                      view_name='renderspec-detail',
                                                      read_only=True)
    pdfs = serializers.HyperlinkedRelatedField(many=True,
                                               view_name='pdf-detail',
                                               read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'packprofiles', 'cardslists', 'renderspecs', 'pdfs')


class BaseSerializerMixin:
    owner = serializers.ReadOnlyField(source='owner.username')
    common_fields = ('url', 'id', 'owner', 'created')


class PackProfileSerializer(serializers.HyperlinkedModelSerializer, BaseSerializerMixin):
    class Meta:
        model = PackProfile
        fields = BaseSerializerMixin.common_fields + ('value', 'color_name')


class CardsListSerializer(serializers.HyperlinkedModelSerializer, BaseSerializerMixin):
    class Meta:
        model = CardsList
        fields = BaseSerializerMixin.common_fields + ('name', 'cards', 'profile')


class RenderSpecSerializer(serializers.HyperlinkedModelSerializer, BaseSerializerMixin):
    class Meta:
        model = RenderSpec
        fields = BaseSerializerMixin.common_fields + ('name', 'packs')


class PDFSerializer(serializers.HyperlinkedModelSerializer, BaseSerializerMixin):
    class Meta:
        model = PDF
        fields = BaseSerializerMixin.common_fields + ('pdf', 'render_spec')
