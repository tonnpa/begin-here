from django.contrib.gis import admin
from .models import CensusTracts

# Register your models here.
admin.site.register(CensusTracts, admin.GeoModelAdmin)
