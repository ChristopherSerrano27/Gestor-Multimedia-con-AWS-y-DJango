from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views

urlpatterns = [
    # tus otras URLs
    path('subir/', views.subir_archivo, name='subir_archivo'),
    path('exito/', views.archivo_subido_exito, name='archivo_subido_exito'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
