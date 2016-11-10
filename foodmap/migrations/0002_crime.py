# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 17:54
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodmap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('occur_date', models.DateField()),
                ('category', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
