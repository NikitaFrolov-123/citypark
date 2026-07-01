import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from menu.models import Dish
from .cart import Cart


def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        dish_id = data.get('dish_id')
        quantity = int(data.get('quantity', 1))

        if quantity < 1:
            quantity = 1

        dish = get_object_or_404(Dish, id=dish_id)
        cart = Cart(request)
        cart.add(dish=dish, quantity=quantity)

        return JsonResponse({
            'success': True,
            'message': 'Блюдо добавлено в корзину',
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def cart(request):
    cart_obj = Cart(request)
    dishes = list(cart_obj)

    return render(request, 'cart_detail.html', {
        'dishes': dishes,
        'total': cart_obj.get_total_price(),
    })


def remove_from_cart(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        dish_id = data.get('dish_id')
        dish = get_object_or_404(Dish, id=dish_id)

        cart = Cart(request)
        cart.remove(dish)

        return JsonResponse({
            'success': True,
            'message': 'Блюдо удалено из корзины',
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def update_quantity(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        dish_id = data.get('dish_id')
        quantity = int(data.get('quantity', 1))

        if quantity < 1:
            quantity = 1

        dish = get_object_or_404(Dish, id=dish_id)
        cart = Cart(request)
        cart.add(dish=dish, quantity=quantity, override_quantity=True)

        return JsonResponse({
            'success': True,
            'message': 'Количество обновлено',
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def clear_cart(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'}, status=400)

    cart = Cart(request)
    cart.clear()

    return JsonResponse({
        'success': True,
        'message': 'Корзина очищена',
        'cart_count': 0,
        'cart_total': '0',
    })