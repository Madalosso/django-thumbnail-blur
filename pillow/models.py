from __future__ import unicode_literals
from django.db import models


def rename_picture(instance, filename):
    return '{0}_{1}'.format(instance.id, filename)


class Picture(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=3000, null=True, blank=True)
    img_l = models.ImageField(upload_to=rename_picture, null=False)
    img_m = models.ImageField(upload_to=rename_picture)
    img_s = models.ImageField(upload_to=rename_picture)
    img_blur = models.CharField(max_length=3000)

    def __unicode__(self):
        return str(self.nome)
