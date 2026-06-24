from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'guests', 'booking_date', 'booking_time', 'created_at')
    list_filter = ('booking_date', 'booking_time', 'created_at')
    search_fields = ('name', 'phone')
    ordering = ('-created_at',)