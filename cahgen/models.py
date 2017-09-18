from re import IGNORECASE
from uuid import uuid4

from django.core.validators import RegexValidator
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PackProfile(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='packprofiles', on_delete=models.CASCADE)
    value = models.CharField(max_length=6, validators=[RegexValidator(regex=r'[0-9a-f]{6}', flags=IGNORECASE)])
    color_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'#{self.value} {self.color_name}'


class CardsList(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='cardslists', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cards = models.TextField(default="Example card")
    profile = models.ForeignKey(PackProfile, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RenderSpec(BaseModel):
    WHITECARDSPDF = 0
    BLACKCARDSPDF = 1
    STYLE_CHOICES = ((WHITECARDSPDF, 'White cards'),
                     (BLACKCARDSPDF, 'Black cards'))

    owner = models.ForeignKey('auth.User', related_name='renderspecs', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    style = models.PositiveSmallIntegerField(choices=STYLE_CHOICES)
    packs = models.ManyToManyField(CardsList)

    def __str__(self):
        return f'{self.name} :: {", ".join(map(str, self.packs.all()))}'


class PDF(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='pdfs', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    generated_content = models.BinaryField()
    render_spec = models.ForeignKey(RenderSpec, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'PDF :: {self.render_spec}'
