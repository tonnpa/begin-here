import json
import logging

from django.views.decorators.csrf import csrf_exempt

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
    return render(request, 'index.html', context)


def heatmap(request):
    PtData = EvaluationPoint.objects.all()
    context = {'PtData': PtData}
    return render(request, 'heatmap.html', context)


def evalgrids_view(request):
    evalgrids_as_geojson = serialize('geojson', EvaluationPoint.objects.all(),
                                     geometry_field='poly_pts',
                                     fields=('income', 'population', 'crime_count_local', 'crime_count_neighborhood',
                                             'favorability_score'))
    return HttpResponse(evalgrids_as_geojson, content_type='application/json')


def choropleth(request):
    return render(request, 'choropleth.html')


@csrf_exempt
def highlight(request):
    data = json.loads(request.body.decode("utf-8"))
    logging.error(data.keys())
    return HttpResponse("Hello")


def get_restaurants(request):
    restaurants = serialize('geojson', Restaurant.objects.all())
    return HttpResponse(restaurants, content_type='application/json')


def get_categories(request):
    logging.error('')
    categories = {
        "African": [
            "senegalese",
            "southafrican"
        ],
        "Asian": [
            "bangladeshi",
            "burmese",
            "cantonese",
            "chinese",
            "dimsum",
            "himalayan",
            "indonesian",
            "indpak",
            "japanese",
            "korean",
            "laotian",
            "malaysian",
            "mediterranean",
            "mongolian",
            "noodles",
            "pakistani",
            "ramen",
            "sushi",
            "szechuan",
            "taiwanese",
            "vietnamese"
        ],
        "European": [
            "belgian",
            "british",
            "creperies",
            "ethiopian",
            "french",
            "german",
            "greek",
            "hungarian",
            "irish",
            "italian",
            "russian",
            "scandinavian",
            "spanish",
            "tapas"
        ],
        "Fast Food": [
            "burgers",
            "cafes",
            "chicken_wings",
            "donuts",
            "falafel",
            "hotdog",
            "hotdogs",
            "pizza",
            "sandwiches",
            "tacos",
            "waffles"
        ],
        "Latin American": [
            "caribbean",
            "cuban",
            "dominican",
            "hawaiian",
            "latin",
            "mexican",
            "puertorican"
        ],
        "Middle-East": [
            "lebanese",
            "moroccan",
            "persian",
            "turkish"
        ],
        "South American": [
            "brazilian",
            "colombian",
            "peruvian",
            "southern",
            "venezuelan"
        ]
    }
    return HttpResponse(json.dumps(categories), content_type='application/json')
