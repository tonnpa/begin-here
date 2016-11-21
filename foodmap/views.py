import json

from foodmap.models import Category
from foodmap.models import Restaurant
from django.shortcuts import render
from .models import EvaluationPoint
from django.core.serializers import serialize
from django.http import HttpResponse


# Create your views here.


def index(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurant_list': restaurants,
    }
    return render(request, 'HelloLeaflet.html', context)


def get_categories(request):
    categories = {'African': ['south african', 'senegalese'],
                  'Asian': ['ramen',
                            'himalayan',
                            'mongolian',
                            'noodles',
                            'szechuan',
                            'cantonese',
                            'dimsum',
                            'mediterranean',
                            'japanese',
                            'pakistani',
                            'taiwanese',
                            'burmese',
                            'korean',
                            'indonesian',
                            'sushi',
                            'loatian',
                            'indpak',
                            'bangladeshi',
                            'malaysian',
                            'chinese',
                            'vietnamese'],
                  'European': ['italian',
                               'greek',
                               'creperies',
                               'hungarian',
                               'scandanavian',
                               'tapas',
                               'german',
                               'irish',
                               'russian',
                               'belgian',
                               'spanish',
                               'french',
                               'british',
                               'ethiopian'],
                  'Fast Food': ['burgers',
                                'cafes',
                                'pizza',
                                'hotdogs',
                                'chicken_wings',
                                'tacos',
                                'sandwiches',
                                'hotdog',
                                'falafel',
                                'donuts',
                                'waffles'],
                  'Latin American': ['mexican',
                                     'latin',
                                     'caribbean',
                                     'puertorican',
                                     'dominican',
                                     'cuban',
                                     'north american',
                                     'hawaiian'],
                  'Middle-East': ['lebanese', 'persian', 'turkish', 'moroccan'],
                  'South American': ['brazilian',
                                     'southern',
                                     'venezuelan',
                                     'columbian',
                                     'peruvian']}

    return HttpResponse(json.dumps(categories), content_type="application/json");


def get_restaurants(request):
    restaurants = serialize('geojson', Restaurant.objects.all())
    return HttpResponse(restaurants, content_type='application/json')


def heatmap(request):
    PtData = EvaluationPoint.objects.all()
    context = {'PtData': PtData}
    return render(request, 'Heatmap.html', context)


def evalgrids_view(request):
    evalgrids_as_geojson = serialize('geojson', EvaluationPoint.objects.all(),
                                     geometry_field='poly_pts',
                                     fields=('income','population', 'crime_count_local', 'crime_count_neighborhood','favorability_score'))
    return HttpResponse(evalgrids_as_geojson, content_type='application/json')


def choropleth(request):
    return render(request, 'HelloChoropleth.html')
