from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArchivoForm
import boto3
from .models import Archivo, CompartirArchivo
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import FileResponse, Http404
from django.core.files import File

@login_required
def subir_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.usuario = request.user
            archivo.save()
            return redirect('archivo_subido_exito')
    else:
        form = ArchivoForm()
    
    return render(request, 'subir_archivo.html', {'form': form})

def archivo_subido_exito(request):
    return render(request, 'archivo_subido_exito.html')

@login_required
def listar_archivos(request):
    archivos = Archivo.objects.filter(usuario=request.user)

    for archivo in archivos:
        archivo.url = f'https://{archivo.archivo.storage.bucket_name}.s3.us-east-2.amazonaws.com/{archivo.archivo.name}'

        archivo.es_imagen = False
        archivo.es_pdf = False
        archivo.es_video = False
        archivo.es_audio = False
        archivo.es_documento = False
        archivo.es_excel = False
        archivo.es_ppt = False
        archivo.es_txt = False
        archivo.es_zip = False

        if archivo.archivo.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            archivo.es_imagen = True
        elif archivo.archivo.url.endswith('.pdf'):
            archivo.es_pdf = True
        elif archivo.archivo.url.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            archivo.es_video = True
        elif archivo.archivo.url.endswith(('.mp3', '.wav', '.ogg', '.flac')):
            archivo.es_audio = True
        elif archivo.archivo.url.endswith(('.doc', '.docx')):
            archivo.es_documento = True
        elif archivo.archivo.url.endswith(('.xls', '.xlsx')):
            archivo.es_excel = True
        elif archivo.archivo.url.endswith(('.ppt', '.pptx')):
            archivo.es_ppt = True
        elif archivo.archivo.url.endswith('.txt'):
            archivo.es_txt = True
        elif archivo.archivo.url.endswith(('.zip', '.rar', '.tar', '.gz')):
            archivo.es_zip = True

    return render(request, 'listar_archivos.html', {'archivos': archivos})

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})

@login_required
def compartir_archivo(request):
    if request.method == 'POST':
        archivos_id = request.POST.getlist('archivos')
        destinatario_id = request.POST.get('destinatario')
        destinatario = User.objects.get(id=destinatario_id)

        for archivo_id in archivos_id:
            archivo = Archivo.objects.get(id=archivo_id)

            CompartirArchivo.objects.create(
                archivo=archivo, 
                remitente=request.user, 
                destinatario=destinatario
            )

        return redirect('listar_archivos')

    archivos = Archivo.objects.filter(usuario=request.user)
    usuarios = User.objects.exclude(id=request.user.id)
    return render(request, 'compartir_archivo.html', {'archivos': archivos, 'usuarios': usuarios})

@login_required
def recibir_archivos(request):
    archivos_recibidos = CompartirArchivo.objects.filter(destinatario=request.user, aceptado=False, rechazado=False)

    if request.method == 'POST':
        decision = request.POST.get('decision')
        archivo_id = request.POST.get('archivo_id')
        archivo_compartido = get_object_or_404(CompartirArchivo, id=archivo_id)

        if decision == 'aceptar':
            archivo_compartido.aceptado = True
            archivo_compartido.save()

            archivo_original = archivo_compartido.archivo
            nombre_archivo = archivo_original.archivo.name.split('/')[-1]
            nuevo_nombre_archivo = f'archivos_usuarios/{request.user.username}/{nombre_archivo}'

            try:
                s3_client = boto3.client('s3')
                copy_source = {
                    'Bucket': 'multimediabucket',
                    'Key': archivo_original.archivo.name
                }

                s3_client.copy(copy_source, 'multimediabucket', nuevo_nombre_archivo)

                nuevo_archivo = Archivo.objects.create(
                    nombre=archivo_original.nombre,
                    archivo=nuevo_nombre_archivo,
                    usuario=request.user
                )                
                nuevo_archivo.save()

            except Exception as e:
                print(f"Error al copiar el archivo a S3: {e}")

        elif decision == 'rechazar':
            archivo_compartido.rechazado = True
            archivo_compartido.save()

        return redirect('recibir_archivos')

    return render(request, 'recibir_archivos.html', {'archivos_recibidos': archivos_recibidos})


@login_required
def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)

    if archivo.usuario == request.user:
        try:
            s3_client = boto3.client('s3')
            file_key = archivo.archivo.name
            response = s3_client.delete_object(Bucket='multimediabucket', Key=file_key)
        except s3_client.exceptions.NoSuchKey:
            print(f"El archivo {file_key} no existe en S3.")
        except Exception as e:
            print(f"Error al eliminar el archivo de S3: {e}")

        archivo.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def descargar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)
    return HttpResponseRedirect(archivo.archivo.url)