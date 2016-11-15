from django.contrib.gis import admin
from .models import CensusTract, Restaurant, Category, Crime, EvaluationPoint

# Register Models Here
admin.site.register(CensusTract, admin.GeoModelAdmin)
admin.site.register(Restaurant, admin.GeoModelAdmin)
admin.site.register(Category, admin.GeoModelAdmin)
admin.site.register(Crime, admin.GeoModelAdmin)
admin.site.register(EvaluationPoint, admin.GeoModelAdmin)

