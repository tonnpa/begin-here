# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 22:05
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodmap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationpoint',
            name='bigpoly_pts',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326),
        ),
    ]
