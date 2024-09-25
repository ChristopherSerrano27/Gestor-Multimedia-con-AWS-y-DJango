from django.db import models
from django.contrib.auth.models import User

class Archivo(models.Model):
    nombre = models.CharField(max_length=50)
    archivo = models.FileField(upload_to='')  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.archivo.name = f'archivos_usuarios/{self.usuario.username}/{self.archivo.name}'
        super().save(*args, **kwargs)