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
        return f'{self.name} [{self.card_type}]'

    @property
    def card_type(self):
        return "black" if self.is_black else "white"

    def cards_as_list(self):
        return [card for card in self.cards.splitlines() if card]

    @property
    def color(self):
        return '#' + self.profile.value

    def get_profile(self):
        return pdf_gen.PackProfile(self.name, self.color) if self.profile else None


class RenderSpec(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='renderspecs', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    append_color = models.BooleanField(default=True)
    packs = models.ManyToManyField(CardsList)

    def __str__(self):
        return f'{self.name} :: {", ".join(map(str, self.packs.all()))}'

    @property
    def pack(self):
        return self.packs.first()

    @property
    def card_type(self):
        return self.pack.card_type

    @property
    def is_black(self):
        return self.pack.is_black

    def iter_packs(self):
        return self.packs.iterator()


class PDF(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='pdfs', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    generated_content = models.BinaryField()
    render_spec = models.ForeignKey(RenderSpec, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'PDF :: {self.render_spec}'

    def create_pdf(self):
        pdf = BytesIO()
        if self.render_spec.is_black:
            generator = pdf_gen.BlackCardWriter(pdf, 2.5, 3.5, 10, 10, 14, 35, 'Calling All Heretics',
                                                path.join(THIS_DIR, 'lib/cards.png'), 30, True, 5)
        else:
            generator = pdf_gen.WhiteCardWriter(pdf, 2.5, 3.5, 10, 10, 14, 35, 'Calling All Heretics',
                                                path.join(THIS_DIR, 'lib/cards.png'), 30, True)
        for cl in self.render_spec.iter_packs():
            generator.add_pack(cl.cards_as_list(), cl.get_profile())

        generator.write()
        self.generated_content = pdf.getvalue()

    @property
    def filename(self):  # FIXME valid filename character conversion
        filename = self.render_spec.name
        if self.render_spec.append_color:
            filename += f' [{self.render_spec.card_type}]'
        return filename


@receiver(models.signals.pre_save, sender=PDF)
def pdf_pre_save(sender, instance, **kwargs):
    instance.create_pdf()
