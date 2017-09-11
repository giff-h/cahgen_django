from re import IGNORECASE
from uuid import uuid4

from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class PackProfile(models.Model):
    value = models.CharField(max_length=6, validators=[RegexValidator(regex=r'[0-9a-f]{6}', flags=IGNORECASE)])
    color_name = models.CharField(max_length=30, null=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.value} {self.color_name}'

    class Meta:
        ordering = ('value',)


class CardsList(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(PackProfile, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)


class RenderSpec(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    packs = models.ManyToManyField(CardsList)

    def __str__(self):
        return f'{self.name}: {self.packs}'


class PDF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    created = models.DateTimeField(auto_now_add=True)
    render_spec = models.OneToOneField(RenderSpec, null=True, on_delete=models.SET_NULL)
    pdf = models.BinaryField(null=True)

    def __str__(self):
        return str(self.render_spec)
