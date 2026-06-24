from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название блюда')
    description = models.TextField(verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name='Изображение')
    is_available = models.BooleanField(default=True, verbose_name='Доступно')
    is_popular = models.BooleanField(default=False, verbose_name='Популярное')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['id']

    def __str__(self):
        return self.name


class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews', verbose_name='Блюдо')
    author = models.CharField(max_length=100, verbose_name='Автор')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5, verbose_name='Рейтинг')
    text = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author} - {self.rating}⭐'