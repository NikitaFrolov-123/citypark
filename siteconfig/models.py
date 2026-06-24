from django.db import models


class SiteSettings(models.Model):
    title = models.CharField(max_length=120, default='CityPark')
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    work_time = models.CharField(max_length=120)

    class Meta:
        verbose_name = 'Настройка сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.title