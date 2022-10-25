from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    image = models.ImageField(null=True, blank=True)


class Category(models.Model):
    category = models.CharField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.category


class Note(models.Model):
    title = models.CharField(max_length=800)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cate')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.title


