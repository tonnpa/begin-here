from foodmap.models import Category
from foodmap.models import Restaurant
from django.shortcuts import render
from .models import EvaluationPoint

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
    return render(request,'Heatmap.html',context)
