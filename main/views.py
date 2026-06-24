from django.shortcuts import render
from menu.models import Dish


def home(request):
    dishes = Dish.objects.all().order_by('?')[:6]
    hero_dish = Dish.objects.order_by('?').first()

    return render(request, 'home.html', {
        'dishes': dishes,
        'hero_dish': hero_dish,
    })