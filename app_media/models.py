from django.db import models

class Archivo(models.Model):
    nombre = models.CharField(max_length=50)
    archivo = models.FileField(upload_to = '')