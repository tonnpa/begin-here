from django.core.exceptions import ValidationError
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis import geos

import json
import os
import pandas as pd

from foodmap import models

BASE_DIR = os.path.dirname(__file__)


def load_census_tracts(verbose=True):
    census_tract_mapping = {
        'statefp': 'STATEFP',
        'countyfp': 'COUNTYFP',
        'tractce': 'TRACTCE',
        'geoid': 'GEOID',
        'name': 'NAME',
        'namelsad': 'NAMELSAD',
        'mtfcc': 'MTFCC',
        'funcstat': 'FUNCSTAT',
        'aland': 'ALAND',
        'awater': 'AWATER',
        'intptlat': 'INTPTLAT',
        'intptlon': 'INTPTLON',
        'geom': 'MULTIPOLYGON',
    }

    census_tracts_shp = os.path.abspath(
        os.path.join(BASE_DIR, 'data', 'census_tracts_2014', 'tl_2014_13_tract.shp'),
    )

    lm = LayerMapping(
        models.CensusTract, census_tracts_shp, census_tract_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)


def load_census_tract_incomes():
    for county in ['atlanta', 'cobb', 'dekalb', 'fulton', 'clayton']:
        print('Processing {}'.format(county))
        income_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'income', 'income_' + county + '.csv'))
        income_2014 = income_df[income_df.year == 2014]
        for record in income_2014.itertuples():
            geoid = record.geo.split('US')[1]
            census_tract = models.CensusTract.objects.get(geoid=geoid)
            try:
                census_tract.income = int(float(record.income))
                census_tract.save()
            except ValueError:
                continue


def load_census_tract_population():
    population_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'population', 'population_georgia.csv'))
    for record in population_df.itertuples():
        try:
            census_tract = models.CensusTract.objects.get(geoid=record[2])  # 2: Id2
            census_tract.population = record[4]  # 4: Estimate
            census_tract.save()
        except models.CensusTract.DoesNotExist:
            print('Census tract #{} does not exist'.format(record.Id2))
        except ValueError:
            print('No population data for #{}: {}'.format(record.Id2, record.Estimation))


def load_categories():
    categories = json.load(open(os.path.join(BASE_DIR, 'data', 'restaurant_categories.json')))
    for category in categories:
        category_object = models.Category(name=category)
        category_object.save()


def load_restaurants():
    def parse_categories(category_string):
        return json.loads(category_string.replace('\'', "\""))

    business_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'Yelp_Data_with_Prices.csv'))
    business_df.rename(columns={'average rating': 'rating'}, inplace=True)

    for business in business_df.itertuples():
        try:
            restaurant = models.Restaurant(
                name=business.name,
                location=geos.GEOSGeometry('POINT({lon} {lat})'.format(lat=float(business.latitude),
                                                                       lon=float(business.longitude))),
                price=business.Price,
                rating=business.rating,
            )
            restaurant.save()
        except ValueError:
            continue

        for category in parse_categories(business.Categories):
            restaurant.categories.add(models.Category.objects.get(name=category))


def load_common_category_for_restuarants():
    try:
        cat_all = models.Category.objects.get(name='all')
    except models.Category.DoesNotExist:
        cat_all = models.Category(name='all')
        cat_all.save()

    for restaurant in models.Restaurant.objects.all():
        restaurant.categories.add(cat_all)


def load_eval_pts():
    evalpts_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'evaluation_points.csv'))
    for point in evalpts_df.itertuples():
        try:
            evaluation_point = models.EvaluationPoint(
                location=geos.GEOSGeometry('POINT({lon} {lat})'.format(lat=float(point.latitude),
                                                                       lon=float(point.longitude))),
                favorability_score=point.score,
                poly_pts=geos.GEOSGeometry(
                    '{{\'type\': \'Polygon\', \'coordinates\': [{coords}]}}'.format(coords=eval(point.jsonpoly_pts))),
                bigpoly_pts=geos.GEOSGeometry(
                    '{{\'type\': \'Polygon\', \'coordinates\': [{coords}]}}'.format(coords=eval(point.bigjsonpoly_pts)))
            )
            evaluation_point.save()
        except ValueError:
            continue


def load_crimes(verbose=True, limit=None):
    crime_df = pd.read_csv(os.path.join(BASE_DIR, 'data', '2008-2015_NPU_Joined.csv'))
    crime_df = crime_df[['Latitude', 'Longitude', 'occur_date', 'UC']].dropna()
    if limit:
        crime_df = crime_df[:limit]

    for crime_record in crime_df.itertuples():
        try:
            crime = models.Crime(
                location=geos.GEOSGeometry('POINT({lon} {lat})'.format(lat=float(crime_record.Latitude),
                                                                       lon=float(crime_record.Longitude))),
                occur_date=crime_record.occur_date,
                category=crime_record.UC
            )
            crime.save()
        except (ValueError, ValidationError):
            print('Error at record #{}'.format(crime_record.Index))
            continue
        if verbose:
            if (crime_record.Index % 10000) == 0:
                print('Processed {} records out of {}'.format(crime_record.Index, len(crime_df)))
