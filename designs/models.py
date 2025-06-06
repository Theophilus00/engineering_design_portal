from django.db import models
from django.conf import settings

# Create your models here.

class Design(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='designs')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    design_file = models.FileField(upload_to='designs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
