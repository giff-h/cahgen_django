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


class PackProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    value = serializers.CharField(max_length=6)  # FIXME validate hex
    color_name = serializers.CharField(max_length=30, required=False)

    def create(self, validated_data):
        """
        Create and return a new `PackProfile` instance, given the validated data.
        """
        return PackProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `PackProfile` instance, given the validated data.
        """
        instance.value = validated_data.get('value', instance.value)
        instance.color_name = validated_data.get('color_name', instance.color_name)


class CardsListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    created = serializers.DateTimeField(read_only=True)
    # profile = serializers.ForeignKey(PackProfile, null=True, on_delete=models.SET_NULL)
    cards = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `CardsList` instance, given the validated data.
        """
        return CardsList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `CardsList` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.cards = validated_data.get('cards', instance.cards)


class RenderSpecSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        """
        Create and return a new `RenderSpec` instance, given the validated data.
        """
        return RenderSpec.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `RenderSpec` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)


class PDFSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    # pdf = serializers.FileField()  # TODO find custom BinaryField

    def create(self, validated_data):
        """
        Create and return a new `RenderSpec` instance, given the validated data.
        """
        return RenderSpec.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `RenderSpec` instance, given the validated data.
        """
        pass
