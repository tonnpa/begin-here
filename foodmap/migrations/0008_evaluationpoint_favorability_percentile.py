# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodmap', '0007_auto_20161202_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationpoint',
            name='favorability_percentile',
            field=models.FloatField(default=0),
        ),
    ]
