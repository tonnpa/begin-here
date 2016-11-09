from django.contrib.gis.utils import LayerMapping
from django.contrib.gis import geos

import json
import os
import pandas as pd

from foodmap import models


BASE_DIR = os.path.dirname(__file__)


def load_census_tracts(verbose=True):
    census_tracts_mapping = {
        'geo_id': 'GEO_ID',
        'state': 'STATE',
        'county': 'COUNTY',
        'tract': 'TRACT',
        'name': 'NAME',
        'lsad': 'LSAD',
        'censusarea': 'CENSUSAREA',
        'geom': 'MULTIPOLYGON',
    }
    census_tracts_shp = os.path.abspath(
        os.path.join(BASE_DIR, 'data', 'census_tracts_2010', 'gz_2010_13_140_00_500k.shp'),
    )

    lm = LayerMapping(
        models.CensusTract, census_tracts_shp, census_tracts_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)


def load_categories():
    categories = json.load(open(os.path.join(BASE_DIR, 'data', 'restaurant_categories.json')))
    for category in categories:
        category_object = models.Category(name=category)
        category_object.save()


def load_yelp_businesses():
    def parse_categories(category_string):
        return json.loads(category_string.replace('\'', "\""))

    business_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'Yelp_Data_with_Prices.csv'))
    business_df.rename(columns={'average rating': 'rating'}, inplace=True)

    for business in business_df.itertuples():
        try:
            restaurant = models.Restaurant(
                name=business.name,
                location=geos.GEOSGeometry('POINT({lat} {lon})'.format(lat=float(business.latitude),
                                                                       lon=float(business.longitude))),
                price=business.Price,
                rating=business.rating,
            )
            restaurant.save()
        except ValueError:
            continue

        for category in parse_categories(business.Categories):
            restaurant.categories.add(models.Category.objects.get(name=category))

def load_eval_pts():
	evalpts_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'evaluation_points.csv'))
	for point in evalpts_df.itertuples():
		try:
			evalutation_point = models.EvaluationPoint(
				location=geos.GEOSGeometry('POINT({lat} {lon})'.format(lat=float(point.latitude),
                                                                       lon=float(point.longitude))),
				income_level = point.score,
				)
			evalutation_point.save()
		except ValueError:
			continue

def load_all_data():
    print('Loading census tracts')
    load_census_tracts()
    print('Loading categories')
    load_categories()
    print('Loading restaurants')
    load_yelp_businesses()
    print('Loading evaluation points')
    load_eval_pts()

