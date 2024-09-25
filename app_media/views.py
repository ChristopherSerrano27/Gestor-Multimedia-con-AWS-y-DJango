from django.shortcuts import render, redirect
from .forms import ArchivoForm
from .models import Archivo
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.decorators import login_required

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
