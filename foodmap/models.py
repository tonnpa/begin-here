# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class CensusTract(models.Model):
    geo_id = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=3)
    tract = models.CharField(max_length=6)
    name = models.CharField(max_length=90)
    lsad = models.CharField(max_length=7)
    censusarea = models.FloatField()
    geom = models.MultiPolygonField(srid=4269)


class Category(models.Model):
    name = models.CharField(max_length=32)


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    location = models.PointField()
    price = models.PositiveSmallIntegerField()
    rating = models.FloatField()
    categories = models.ManyToManyField(Category)


class EvaluationPoint(models.Model):
    location = models.PointField()
    income_level = models.IntegerField()
