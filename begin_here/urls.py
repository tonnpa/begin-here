"""begin_here URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.gis import admin
from foodmap import views as foodmap_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', foodmap_views.index),
    url(r'^choropleth$', foodmap_views.choropleth),          # The choropleth
    url(r'^choropleth/data', foodmap_views.evalgrids_view),  # The GeoJson evaluation grid data
    url(r'^categories$', foodmap_views.get_categories),
    url(r'^restaurants$', foodmap_views.get_restaurants),
    url(r'^highlight$', foodmap_views.highlight),
]
