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

    income = models.PositiveIntegerField(null=True)
    population = models.PositiveIntegerField(null=True)
    no_eval_pts = models.PositiveSmallIntegerField(null=True)
    pop_density = models.FloatField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    location = models.PointField(srid=4269)
    price = models.CharField(max_length=6)
    rating = models.FloatField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class EvaluationPoint(models.Model):
    location = models.PointField(srid=4269)
    poly_pts = models.PolygonField(srid=4269)
    bigpoly_pts = models.PolygonField(srid=4269)
    favorability_score = models.FloatField()
    ct_geoid = models.CharField(max_length=11)


class Crime(models.Model):
    location = models.PointField(srid=4269)
    occur_date = models.DateField()
    category = models.PositiveSmallIntegerField()
