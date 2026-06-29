from decimal import Decimal
from menu.models import Dish


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, dish, quantity=1, override_quantity=False):
        dish_id = str(dish.id)

        if dish_id not in self.cart:
            self.cart[dish_id] = {
                'dish_id': dish.id,
                'name': dish.name,
                'price': str(dish.price),
                'quantity': 0,
                'image': dish.image.url if dish.image else '',
            }

        if override_quantity:
            self.cart[dish_id]['quantity'] = quantity
        else:
            self.cart[dish_id]['quantity'] += quantity

        self.save()

    def remove(self, dish):
        dish_id = str(dish.id)
        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        self.cart = {}

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        dish_ids = self.cart.keys()
        dishes = Dish.objects.filter(id__in=dish_ids)
        cart = self.cart.copy()

        for dish in dishes:
            cart[str(dish.id)]['dish'] = dish

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())