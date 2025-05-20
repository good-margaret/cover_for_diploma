from PIL import Image, ImageEnhance
import os

from django.conf import settings
from ..models import ImageRestoration
from datetime import datetime

def process_image(image_restoration):
    try:
        if not image_restoration.original_image:
            raise ValueError("No image file attached")

        original_path = image_restoration.original_image.path
        img = Image.open(original_path)

        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)

        # Сохранение обработанного изображения
        processed_filename = f"processed_{os.path.basename(original_path)}"
        processed_path = os.path.join(settings.MEDIA_ROOT, 'processed', processed_filename)

        img.save(processed_path)

        # Обновление модели
        image_restoration.processed_image = f"processed/{processed_filename}"
        image_restoration.processed_at = datetime.now()
        image_restoration.save()
    except Exception as e:
        # Логируем ошибку
        print(f"Image processing failed: {e}")
        raise