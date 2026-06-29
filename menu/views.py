from django.shortcuts import render, get_object_or_404
from .models import Dish, Category


def home(request):
    dishes = Dish.objects.filter(is_available=True)[:3]
    hero_dish = dishes[0] if dishes else None
    return render(request, 'home.html', {
        'dishes': dishes,
        'hero_dish': hero_dish,
    })


def menu(request):
    dishes = Dish.objects.filter(is_available=True).order_by('id')
    categories = Category.objects.all()
    return render(request, 'menu.html', {
        'dishes': dishes,
        'categories': categories,
    })


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, 'dish_detail.html', {
        'dish': dish,
    })