from re import IGNORECASE
from uuid import uuid4

from django.core.validators import RegexValidator
from django.db import models


class PackProfile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=6, validators=[RegexValidator(regex=r'[0-9a-f]{6}', flags=IGNORECASE)])
    color_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'#{self.value} {self.color_name}'


class CardsList(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    cards = models.TextField(default="Example card")
    profile = models.ForeignKey(PackProfile, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class RenderSpec(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    packs = models.ManyToManyField(CardsList)

    def __str__(self):
        return f'{self.name} :: {self.packs.all()}'


class PDF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    created = models.DateTimeField(auto_now_add=True)
    pdf = models.BinaryField()
    render_spec = models.ForeignKey(RenderSpec, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.render_spec)
