from django.db import models

# Create your models here.

class Report(models.Model):
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to="video/%Y/%m/%d", null=True)
