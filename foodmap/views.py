from foodmap.models import Category
from foodmap.models import Restaurant
from django.shortcuts import render
from .models import EvaluationPoint
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import JsonResponse
import json
import ast
# Create your views here.

def index(request):
    restaurants = Restaurant.objects.all()
    categories = Category.objects.all()
    context = {
        'restaurant_list': restaurants,
        'category_list': categories,
    }
    return render(request, 'HelloLeaflet.html', context)


def heatmap(request):
    PtData = EvaluationPoint.objects.all()
    context = {'PtData': PtData}
    return render(request, 'Heatmap.html', context)


def evalgrids_view(request):
    evalgrids_as_geojson = serialize('geojson', EvaluationPoint.objects.all()[:1],
                         geometry_field='poly_pts',
                         fields=('income_level',))
    return HttpResponse(evalgrids_as_geojson, content_type='application/json')


def choropleth(request):
    return render(request, 'HelloChoropleth.html')




