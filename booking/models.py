from django.db import models


class Reservation(models.Model):
    name = models.CharField(max_length=120, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    guests = models.PositiveIntegerField(verbose_name='Гостей')
    booking_date = models.DateField(verbose_name='Дата')
    booking_time = models.TimeField(verbose_name='Время')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.booking_date} {self.booking_time}'