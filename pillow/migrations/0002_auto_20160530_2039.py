# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pillow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='picture_sm',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='picture',
            field=models.CharField(max_length=200),
        ),
    ]