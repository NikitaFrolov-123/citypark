from django.shortcuts import render
from django.http import JsonResponse
from menu.models import Dish
import json


def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        dish_id = data.get('dish_id')
        quantity = int(data.get('quantity', 1))

        dish = Dish.objects.get(id=dish_id)
        cart = request.session.get('cart', {})

        if str(dish_id) in cart:
            cart[str(dish_id)]['quantity'] += quantity
        else:
            cart[str(dish_id)] = {
                'dish_id': dish_id,
                'name': dish.name,
                'price': int(dish.price),
                'quantity': quantity
            }

        request.session['cart'] = cart
        request.session.modified = True

        cart_count = sum(item['quantity'] for item in cart.values())

        return JsonResponse({
            'success': True,
            'message': 'Блюдо добавлено в корзину',
            'cart_count': cart_count
        })

    except Dish.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Блюдо не найдено'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def cart(request):
    cart_data = request.session.get('cart', {})
    dishes = []
    total = 0

    for item in cart_data.values():
        try:
            dish = Dish.objects.get(id=item['dish_id'])
            quantity = int(item['quantity'])
            price = int(item['price'])
            item_total = price * quantity
            dishes.append({
                'dish': dish,
                'quantity': quantity,
                'price': price,
                'total': item_total
            })
            total += item_total
        except Dish.DoesNotExist:
            continue

    return render(request, 'cart.html', {
        'dishes': dishes,
        'total': total
    })


def remove_from_cart(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        dish_id = str(data.get('dish_id'))

        cart = request.session.get('cart', {})

        if dish_id in cart:
            del cart[dish_id]
            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({'success': True, 'message': 'Блюдо удалено из корзины'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def update_quantity(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        dish_id = str(data.get('dish_id'))
        quantity = int(data.get('quantity', 1))

        cart = request.session.get('cart', {})

        if dish_id in cart:
            cart[dish_id]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({'success': True, 'message': 'Количество обновлено'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)