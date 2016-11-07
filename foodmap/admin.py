from django.contrib.gis import admin
from .models import CensusTract

# Register your models here.
admin.site.register(CensusTract, admin.GeoModelAdmin)
