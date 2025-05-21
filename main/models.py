from django.db import models
from accounts.models import CustomUser


class ImageRestoration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='uploads/')
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Удаляем файлы изображений при удалении записи
        self.original_image.delete(save=False)
        if self.processed_image:
            self.processed_image.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Image {self.id} by {self.user.username}"

# Create your models here.
