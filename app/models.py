from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CovidUserModel(models.Model):
    gender_type = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    age = models.CharField(max_length=3, blank=False, null=False)
    gender = models.CharField(choices=gender_type, max_length=100, blank=False, null=False)
    image = models.FileField(upload_to='to_predict', blank=False, null=False)
    phone = models.CharField(max_length=100, blank=False, null=False)
