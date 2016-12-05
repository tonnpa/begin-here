from __future__ import division  # fix division by integer errors

import json

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
            categories = [Category.objects.get(id=cat_id) for cat_id in partner_categories]
            partners = Restaurant.objects.filter(categories__in=categories)
            for restaurant in partners:
                EvaluationPoint.objects.filter(id=restaurant.eval_pt_id).update(
                    partner_restaurant_count=F('partner_restaurant_count') + 1)

        def count_competitors(f_cuisines, f_price, rating_low, rating_high):
            categories = [Category.objects.get(id=cuisine_id) for cuisine_id in f_cuisines]
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

        crime_region_weight = [16 / 17., 1 / 17.]  # So that local crimes are weighted 2x as much as neighborhood crime

        p_competitor = float(weights['competitor'])
        p_partner = float(weights['partner'])
        p_income = float(weights['income'])
        p_crime_local = float(weights['crime']) * crime_region_weight[0]
        p_crime_nbhd = float(weights['crime']) * crime_region_weight[1]
        p_population = float(weights['population'])

        parameters = get_parameters()

        EvaluationPoint.objects.update(favorability_score=calculate_score([
            p_income, p_population, p_crime_local, p_crime_nbhd, p_competitor, p_partner], parameters))

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
    categories = {'All Categories': [[191, 'all']],
                  'African': [[140, 'senegalese'],
                              [40, 'southafrican']],
                  'Asian': [[165, 'bangladeshi'],
                            [112, 'burmese'],
                            [49, 'cantonese'],
                            [175, 'chinese'],
                            [86, 'dimsum'],
                            [32, 'himalayan'],
                            [136, 'indonesian'],
                            [162, 'indpak'],
                            [65, 'japanese'],
                            [114, 'korean'],
                            [150, 'laotian'],
                            [173, 'malaysian'],
                            [62, 'mediterranean'],
                            [38, 'mongolian'],
                            [41, 'noodles'],
                            [75, 'pakistani'],
                            [30, 'ramen'],
                            [141, 'sushi'],
                            [42, 'szechuan'],
                            [88, 'taiwanese'],
                            [185, 'vietnamese']],
                  'European': [[90, 'belgian'],
                               [163, 'british'],
                               [16, 'creperies'],
                               [174, 'ethiopian'],
                               [166, 'french'],
                               [44, 'german'],
                               [128, 'greek'],
                               [2, 'hungarian'],
                               [67, 'irish'],
                               [12, 'italian'],
                               [79, 'russian'],
                               [23, 'scandinavian'],
                               [138, 'spanish'],
                               [36, 'tapas']],
                  'Fast Food': [[17, 'burgers'],
                                [35, 'cafes'],
                                [52, 'chicken_wings'],
                                [134, 'donuts'],
                                [123, 'falafel'],
                                [117, 'hotdog'],
                                [51, 'hotdogs'],
                                [69, 'pizza'],
                                [101, 'sandwiches'],
                                [99, 'tacos'],
                                [137, 'waffles']],
                  'Latin American': [[70, 'caribbean'],
                                     [130, 'cuban'],
                                     [106, 'dominican'],
                                     [6, 'hawaiian'],
                                     [33, 'latin'],
                                     [29, 'mexican'],
                                     [105, 'puertorican']],
                  'Middle-East': [[60, 'lebanese'],
                                  [147, 'moroccan'],
                                  [71, 'persian'],
                                  [115, 'turkish']],
                  'South American': [[1, 'brazilian'],
                                     [145, 'colombian'],
                                     [164, 'peruvian'],
                                     [57, 'southern'],
                                     [97, 'venezuelan']]
                  }
    return HttpResponse(json.dumps(categories), content_type='application/json')
