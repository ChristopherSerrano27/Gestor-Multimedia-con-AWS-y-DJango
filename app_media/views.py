from django.shortcuts import render, redirect
from .forms import ArchivoForm

def subir_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('archivo_subido_exito')  # Redirigir a una página de éxito
    else:
        form = ArchivoForm()
    
    return render(request, 'subir_archivo.html', {'form': form})


def archivo_subido_exito(request):
    return render(request, 'archivo_subido_exito.html')