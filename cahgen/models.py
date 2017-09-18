from io import BytesIO
from os import path
from re import IGNORECASE
from uuid import uuid4

from django.core.validators import RegexValidator
from django.db import models
from django.dispatch import receiver

from .lib import pdf_gen


THIS_DIR = path.dirname(path.realpath(__file__))


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PackProfile(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='packprofiles', on_delete=models.CASCADE)
    value = models.CharField(max_length=6, validators=[RegexValidator(regex=r'[0-9a-f]{6}', flags=IGNORECASE)])
    color_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'{self.color_name} #{self.value}'


class CardsList(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='cardslists', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cards = models.TextField(default="Example card")
    is_black = models.BooleanField(default=False)
    profile = models.ForeignKey(PackProfile, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} [{"black" if self.is_black else "white"}]'


class RenderSpec(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='renderspecs', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    append_color = models.BooleanField(default=True)
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

    def create_pdf(self):
        pdf = BytesIO()
        if self.render_spec.packs.first().is_black:
            generator = pdf_gen.BlackCardWriter(pdf, 2.5, 3.5, 10, 10, 14, 35, 'Calling All Heretics',
                                                path.join(THIS_DIR, 'lib/cards.png'), 30, True, 5)
        else:
            generator = pdf_gen.WhiteCardWriter(pdf, 2.5, 3.5, 10, 10, 14, 35, 'Calling All Heretics',
                                                path.join(THIS_DIR, 'lib/cards.png'), 30, True)
        for cl in self.render_spec.packs:
            profile = pdf_gen.PackProfile(cl.name, '#' + cl.profile.value)
            generator.add_pack(cl.cards.splitlines(), profile)

        generator.write()
        return pdf.getvalue()


@receiver(models.signals.pre_save, sender=PDF)
def pdf_pre_save(sender, instance, **kwargs):
    return instance.create_pdf()
