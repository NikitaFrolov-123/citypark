from datetime import time
from django import forms
from django.utils import timezone
from .models import Reservation


def hour_choices():
    return [(f'{h:02d}:00', f'{h:02d}:00') for h in range(10, 23)]


class ReservationForm(forms.ModelForm):
    booking_time = forms.ChoiceField(choices=hour_choices(), label='Время')

    class Meta:
        model = Reservation
        fields = ['name', 'phone', 'guests', 'booking_date', 'booking_time']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
            'guests': forms.NumberInput(attrs={'min': '1', 'max': '20'}),
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        today = timezone.localdate()
        if booking_date < today:
            raise forms.ValidationError('Нельзя бронировать на прошедшую дату.')
        return booking_date

    def clean_booking_time(self):
        booking_time = self.cleaned_data['booking_time']
        hours, minutes = map(int, booking_time.split(':'))
        return time(hours, minutes)