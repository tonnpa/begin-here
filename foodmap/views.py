from __future__ import division  # fix division by integer errors

import json
import logging

from django.core.serializers import serialize
from django.db.models import F, Min, Max
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
                                             'favorability_score', 'favorability_percentile'))
    return HttpResponse(evalgrids_as_geojson, content_type='application/json')


def choropleth(request):
    return render(request, 'choropleth.html')


@csrf_exempt
def highlight(request):
    def count_partners_and_competitors(filters):
        def reset_restaurant_count():
            EvaluationPoint.objects.update(competitor_restaurant_count=0)
            EvaluationPoint.objects.update(partner_restaurant_count=0)

        def count_partners(partner_categories):
            categories = [Category.objects.get(name=cuisine) for cuisine in partner_categories]
            partners = Restaurant.objects.filter(categories__in=categories)
            for restaurant in partners:
                EvaluationPoint.objects.filter(id=restaurant.eval_pt_id).update(
                    partner_restaurant_count=F('partner_restaurant_count') + 1)

        def count_competitors(f_cuisines, f_price, rating_low, rating_high):
            categories = [Category.objects.get(name=cuisine) for cuisine in f_cuisines]
            competitors = Restaurant.objects.filter(price__in=f_price). \
                filter(rating__gte=rating_low). \
                filter(rating__lte=rating_high). \
                filter(categories__in=categories).distinct()

            for restaurant in competitors:
                EvaluationPoint.objects.filter(id=restaurant.eval_pt_id).update(
                    competitor_restaurant_count=F('competitor_restaurant_count') + 1)

        reset_restaurant_count()

        f_partners = filters['partners']
        count_partners(f_partners)

        f_price = filters['price']
        f_rating_low, f_rating_high = filters['rating']
        f_cuisines = filters['competitors']
        count_competitors(f_cuisines, f_price, f_rating_low, f_rating_high)

    def calculate_weights(data):
        priorities = {}
        rankings = data['rankings']
        keys = rankings.keys()
        ranks = [rankings[key] for key in rankings.keys()]
        p = float(data['power'])
        num_priorities = float(sum([rank > 0.0 for rank in rankings.values()]))
        numerator = [(num_priorities - rank + 1) ** p if rank > 0 else 0 for rank in ranks]
        weights = [num / sum(numerator) for num in numerator]
        for i in range(len(keys)):
            priorities[keys[i]] = weights[i]
        return priorities

    def score(weights):
        def calculate_max_min(attribute_name, eval_pts):
            max_val = eval_pts.aggregate(Max(attribute_name)).get(attribute_name + '__max')
            min_val = eval_pts.aggregate(Min(attribute_name)).get(attribute_name + '__min')
            return max_val, min_val

        def get_parameters():
            eval_pts = EvaluationPoint.objects.all()
            parameters = dict()
            parameters['range'] = dict()
            parameters['min'] = dict()

            for attribute in ['income', 'population', 'crime_count_local', 'crime_count_neighborhood',
                              'competitor_restaurant_count', 'partner_restaurant_count']:
                max_val, min_val = calculate_max_min(attribute, eval_pts)
                parameters['range'][attribute] = float(max_val - min_val)
                parameters['min'][attribute] = min_val
            return parameters

        def calculate_score(weights, parameters):
            def normalize(attribute_name):
                if parameters['range'][attribute_name] == 0:
                    return 0.0
                else:
                    return (F(attribute_name) - parameters['min'][attribute_name]) / parameters['range'][attribute_name]

            w1, w2, w3, w4, w5, w6 = weights
            income_norm = normalize('income')
            population_norm = normalize('population')
            local_cr_norm = normalize('crime_count_local')
            nbhd_cr_norm = normalize('crime_count_neighborhood')
            competitor_norm = normalize('competitor_restaurant_count')
            partner_norm = normalize('partner_restaurant_count')

            score_val = w1 * income_norm + w2 * population_norm + w3 * local_cr_norm + \
                        w4 * nbhd_cr_norm + w5 * competitor_norm + w6 * partner_norm
            return score_val

        def scale_scores_for_display():
            eval_pts = EvaluationPoint.objects.all()
            max_sc, min_sc = calculate_max_min('favorability_score', eval_pts)
            EvaluationPoint.objects.update(favorability_score=
                                           (F('favorability_score') - min_sc) / float((max_sc - min_sc)) * 100)

        def calculate_percentiles():
            ordered_pts = EvaluationPoint.objects.all().order_by('favorability_score')
            no_pts = ordered_pts.count()
            for num, point in enumerate(ordered_pts):
                point.favorability_percentile = num / no_pts * 100
                point.save()

        p_partner = float(weights['partner'])
        p_income = float(weights['income'])
        p_crime = float(weights['crime'])
        p_population = float(weights['population'])

        parameters = get_parameters()

        EvaluationPoint.objects.update(favorability_score=calculate_score([
            p_income, p_population, p_crime, p_crime, p_partner, p_partner], parameters))

        scale_scores_for_display()
        calculate_percentiles()

    data = eval(request.body)
    count_partners_and_competitors(filters=data['filter'])
    score(weights=calculate_weights(data))
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
        ],
        "All Categories": [
            "all",
        ],
    }
    return HttpResponse(json.dumps(categories), content_type='application/json')
