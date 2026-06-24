from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_quantity, name='update_quantity'),
]