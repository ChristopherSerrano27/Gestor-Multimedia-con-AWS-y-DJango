from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView, compartir_archivo, recibir_archivos, eliminar_archivo, descargar_archivo


urlpatterns = [
    path('subir/', views.subir_archivo, name='subir_archivo'),
    path('exito/', views.archivo_subido_exito, name='archivo_subido_exito'),
    path('', views.listar_archivos, name='listar_archivos'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('compartir/', compartir_archivo, name='compartir_archivo'),
    path('recibir/', recibir_archivos, name='recibir_archivos'),
    path('eliminar_archivo/<int:archivo_id>/', eliminar_archivo, name='eliminar_archivo'),
    path('descargar_archivo/<int:archivo_id>/', descargar_archivo, name='descargar_archivo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
