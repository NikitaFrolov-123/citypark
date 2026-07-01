from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import RegisterForm, ProfileForm
from .models import Profile, Favorite, Order
from menu.models import Dish


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Аккаунт создан')
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or 'profile'
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    favorites = Favorite.objects.filter(user=request.user).select_related('dish')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders,
        'favorites': favorites,
    })


@login_required
@require_POST
def toggle_favorite_view(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    favorite = Favorite.objects.filter(user=request.user, dish=dish)

    if favorite.exists():
        favorite.delete()
        messages.info(request, 'Удалено из избранного')
    else:
        Favorite.objects.create(user=request.user, dish=dish)
        messages.success(request, 'Добавлено в избранное')

    return redirect(request.POST.get('next') or 'profile')


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('dish')
    return render(request, 'accounts/favorites.html', {
        'favorites': favorites,
    })