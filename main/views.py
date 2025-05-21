from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ImageRestoration
from .utils.image_processor import process_image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import ImageRestoration
from .utils.image_processor import process_image
from django.contrib.auth.decorators import login_required

def home(request):
    # Инициализация формы и данных
    form = ImageUploadForm()
    restored_images = []

    if request.user.is_authenticated:
        restored_images = ImageRestoration.objects.filter(user=request.user).order_by('-uploaded_at')[:5]

    # Обработка POST-запроса (загрузка изображения)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image_restoration = form.save(commit=False)
                image_restoration.user = request.user
                image_restoration.save()

                process_image(image_restoration)

                return redirect('home')
            except Exception as e:
                # Логирование ошибки
                print(f"Error processing image: {e}")
                messages.error(request, "Ошибка при обработке изображения")

    return render(request, 'main/index.html', {
        'form': form,
        'restored_images': restored_images
    })


def about(request):
    return render(request, 'main/about.html')

