# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class CensusTract(models.Model):
    statefp = models.CharField(max_length=2)
    countyfp = models.CharField(max_length=3)
    tractce = models.CharField(max_length=6)
    geoid = models.CharField(max_length=11)
    name = models.CharField(max_length=7)
    namelsad = models.CharField(max_length=20)
    mtfcc = models.CharField(max_length=5)
    funcstat = models.CharField(max_length=1)
    aland = models.FloatField()
    awater = models.FloatField()
    intptlat = models.CharField(max_length=11)
    intptlon = models.CharField(max_length=12)
    geom = models.MultiPolygonField(srid=4269)
    income = models.IntegerField(null=True)
    population = models.IntegerField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    location = models.PointField()
    price = models.CharField(max_length=6)
    rating = models.FloatField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class EvaluationPoint(models.Model):
    location = models.PointField()
    income_level = models.IntegerField()
    poly_pts=models.PolygonField()

class Crime(models.Model):
    location = models.PointField()
    occur_date = models.DateField()
    category = models.PositiveSmallIntegerField()
