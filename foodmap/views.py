import json
import logging

from django.db.models import F, Min, Max
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Category
from .models import EvaluationPoint
from .models import Restaurant


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
    data = eval(request.body)

    def count_partners_and_competitors(filters):
        def reset_restaurant_count():
            EvaluationPoint.objects.update(competitor_restaurant_count=0)
            EvaluationPoint.objects.update(partner_restaurant_count=0)

        def count_partners():
            # TODO
            partner_categories = ['donuts', 'cafes']
            categories = [Category.objects.get(name=cuisine) for cuisine in partner_categories]
            partners = Restaurant.objects.filter(categories__in=categories)
            for restaurant in partners:
                EvaluationPoint.objects.filter(id=restaurant.eval_pt_id).update(
                    partner_restaurant_count=F('partner_restaurant_count') + 1)

        def count_competitors(f_cuisines, f_price, f_rating):
            categories = [Category.objects.get(name=cuisine) for cuisine in f_cuisines]
            competitors = Restaurant.objects.filter(price__in=f_price).\
                filter(rating__gte=f_rating).\
                filter(categories__in=categories).distinct()

            for restaurant in competitors:
                EvaluationPoint.objects.filter(id=restaurant.eval_pt_id).update(
                    competitor_restaurant_count=F('competitor_restaurant_count') + 1)

        f_price = filters['price']
        f_rating = filters['rating']
        f_cuisines = filters['categories']

        reset_restaurant_count()
        count_partners()
        count_competitors(f_cuisines, f_price, f_rating)

    def score(weights):
        def get_ranges():
            def calculate_range(attribute_name):
                max_val = eval_pts.aggregate(Max(attribute_name)).get(attribute_name + '__max')
                min_val = eval_pts.aggregate(Min(attribute_name)).get(attribute_name + '__min')
                return max_val - min_val

            eval_pts = EvaluationPoint.objects.all()
            return dict([(attribute, calculate_range(attribute)) for attribute in
                         ['income', 'population', 'crime_count_local', 'crime_count_neighborhood',
                          'competitor_restaurant_count', 'partner_restaurant_count']])

        def calculate_score(weights):
            def normalize(attribute_name):
                return F(attribute_name) / ranges[attribute_name]

            w1, w2, w3, w4, w5, w6 = weights
            income_norm = normalize('income')
            population_norm = normalize('population')
            local_cr_norm = normalize('crime_count_local')
            nbhd_cr_norm = normalize('crime_count_neighborhood')
            comptetitor_norm = normalize('competitor_restaurant_count')
            partner_norm = normalize('partner_restaurant_count')

            score_val = w1 * income_norm + w2 * population_norm + w3 * local_cr_norm + \
                        w4 * nbhd_cr_norm + w5 * comptetitor_norm + w6 * partner_norm
            return score_val

        # Priorities
        p_partner = float(weights['partner'])
        p_income = float(weights['income'])
        p_crime = float(weights['crime'])
        p_population = float(weights['population'])
        ranges = get_ranges()
        EvaluationPoint.objects.update(favorability_score=calculate_score([
            p_income, p_population, p_crime, p_crime, p_partner, p_partner]))

    count_partners_and_competitors(filters=data['filter'])
    score(weights=data['priority'])
    return evalgrids_view(request)


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
