from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    profileImage = models.ImageField()

    def __str__(self) -> str:
        return self.email
    
class Team(models.Model):
    nome = models.CharField(max_length=200)
    data_fundacao = models.DateField()
    cores = models.CharField(max_length=200)
    localizacao = models.CharField(max_length=100)
    isOnSerieA= models.BooleanField()

    def __str__(self) -> str:
        return self.nome
