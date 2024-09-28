from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return f'archivos_usuarios/{instance.usuario.username}/{filename}'

class Archivo(models.Model):
    nombre = models.CharField(max_length=50)
    archivo = models.FileField(upload_to=user_directory_path) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.archivo:
            self.archivo.name = f'{self.archivo.name}'
        super().save(*args, **kwargs)

class CompartirArchivo(models.Model):
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enviado_por')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recibido_por')
    aceptado = models.BooleanField(default=False)
    rechazado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.remitente.username} compartió {self.archivo.nombre} con {self.destinatario.username}"
