from django.shortcuts import render

from foodmap.models import Category
from foodmap.models import Restaurant
# Create your views here.


def index(request):
    restaurants = Restaurant.objects.all()
    categories = Category.objects.all()
    context = {
        'restaurant_list': restaurants,
        'category_list': categories,
    }
    return render(request, 'HelloLeaflet.html', context)
