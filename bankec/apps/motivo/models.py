from django.db import models

class MotivoTransferencia(models.Model):
    titulo = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo
