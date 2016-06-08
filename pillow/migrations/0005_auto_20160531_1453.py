# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pillow', '0004_auto_20160531_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='picture',
        ),
        migrations.AddField(
            model_name='produto',
            name='picture_max_size',
            field=models.ImageField(default='', upload_to=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='picture_regular_size',
            field=models.ImageField(default='', upload_to=b''),
            preserve_default=False,
        ),
    ]
