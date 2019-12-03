from django.db import models

# Create your models here.

class Report(models.Model):
    description = models.TextField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    ANOMALY_CHOICE = {
        (1, '낙석'), (2, '추돌 사고'), (3, '전복 사고'), (4, '야생 동물')
    }
    DIVISION_CHOICE = {
        (1, '서울/경기'), (2, '전라도'), (3, '충청도'), (4, '경상북도'), (5, '강원도'), (6, '경상남도')
    }
    anomaly_division = models.IntegerField(choices=ANOMALY_CHOICE)
    area_division = models.IntegerField(choices=DIVISION_CHOICE)
    video = models.FileField(upload_to="", null=True)
