from django.contrib.gis.utils import LayerMapping

import os

from foodmap.models import CensusTract

# Auto-generated `LayerMapping` dictionary for WorldBorder model
censustracts_mapping = {
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


def run(verbose=True):
    lm = LayerMapping(
        CensusTract, census_tracts_shp, censustracts_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)
