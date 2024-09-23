from django.shortcuts import render, redirect
from .forms import ArchivoForm
from .models import Archivo

def subir_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('archivo_subido_exito')
    else:
        form = ArchivoForm()
    
    return render(request, 'subir_archivo.html', {'form': form})


def archivo_subido_exito(request):
    return render(request, 'archivo_subido_exito.html')


def listar_archivos(request):
    archivos = Archivo.objects.all()
    return render(request, 'listar_archivos.html', {'archivos': archivos})