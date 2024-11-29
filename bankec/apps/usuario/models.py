from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    dni = models.IntegerField(null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    avatar = models.ImageField(upload_to='avatars/',default='avatars/avatar_default.jpeg', blank=True )

    def __str__(self):
        return f'{self.username}'
