from __future__ import unicode_literals

from django.db import models
from image_cropping import ImageRatioField, ImageCropField


def rename_max_size(instance, filename):
    return instance.nome + '_big.jpg'


class Produto(models.Model):
    nome = models.CharField(max_length=20)
    picture_max_size = ImageCropField(upload_to=rename_max_size)
    cropping = ImageRatioField('picture_max_size', '1366x768')
    picture_regular_size = models.ImageField()
    picture_sm = models.CharField(max_length=1000)

    def __unicode__(self):
        return str(self.nome)
