from django.shortcuts import render, redirect
from .forms import ReservationForm


def booking_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReservationForm()

    return render(request, 'booking.html', {'form': form})