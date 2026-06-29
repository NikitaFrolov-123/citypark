from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Иван'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@mail.ru'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Бронирование стола'}),
            'message': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Напишите ваш вопрос...'}),
        }