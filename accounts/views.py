from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from main.models import ImageRestoration
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# def profile_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     return render(request, 'accounts/profile.html', {'user': request.user})
#

@login_required
def profile_view(request):
    if request.method == 'POST' and 'delete_id' in request.POST:
        # Обработка удаления изображения
        try:
            image = ImageRestoration.objects.get(id=request.POST['delete_id'], user=request.user)
            image.delete()
        except ImageRestoration.DoesNotExist:
            pass
        return redirect('profile')

    # Получаем все изображения пользователя
    user_images = ImageRestoration.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'user_images': user_images
    })