from django.contrib.gis import admin
from .models import CensusTract, Restaurant, Category, Crime

# Register your models here.
admin.site.register(CensusTract, admin.GeoModelAdmin)
admin.site.register(Restaurant, admin.GeoModelAdmin)
admin.site.register(Category, admin.GeoModelAdmin)
admin.site.register(Crime, admin.GeoModelAdmin)
