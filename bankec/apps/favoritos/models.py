from django.db import models
from apps.usuario.models import Usuario


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos')
    favorito = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='es_favorito')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'favorito')

    def __str__(self):
        return f'{self.usuario} -> {self.favorito}'
