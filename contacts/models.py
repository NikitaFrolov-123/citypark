from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон', default='')
    email = models.EmailField(verbose_name='Email', default='')
    subject = models.CharField(max_length=150, verbose_name='Тема', default='')
    message = models.TextField(verbose_name='Сообщение', default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.name} — {self.subject}'

    class Meta:
        verbose_name = 'Сообщение из формы'
        verbose_name_plural = 'Сообщения из формы'