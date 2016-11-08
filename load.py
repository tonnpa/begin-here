from django.contrib.gis.utils import LayerMapping
from django.contrib.gis import geos

import json
import os

from foodmap import models

# Auto-generated `LayerMapping` dictionary for WorldBorder model
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
    os.path.join(os.path.dirname(__file__), 'data', 'census_tracts_2010','gz_2010_13_140_00_500k.shp'),
)


def load_census_tracts(verbose=True):
    lm = LayerMapping(
        models.CensusTract, census_tracts_shp, census_tracts_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)


def load_categories():
    #TODO
    categories = json.load(open(os.path.join()))
    pass


def load_yelp_businesses(verbose=True):
    pass
