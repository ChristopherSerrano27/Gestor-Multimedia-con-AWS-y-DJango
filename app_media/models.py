from django.db import models

class Archivo(models.Model):
    archivo = models.FileField(upload_to = '')