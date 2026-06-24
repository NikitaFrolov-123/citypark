from django.contrib import admin
from .models import Category, Dish, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available', 'is_popular')
    list_filter = ('category', 'is_available', 'is_popular')
    search_fields = ('name', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('dish', 'author', 'rating', 'created_at')
    list_filter = ('dish', 'rating')
    search_fields = ('author', 'text')