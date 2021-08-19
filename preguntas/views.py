from django import forms
from django.shortcuts import redirect, render
from .forms import RegistroFormulario

# Create your views here.

def Inicio(request):

    return render(request,'Inicio.html', context=None)

def registro(request):
    titulo = 'Crear Usuario'
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = RegistroFormulario()
    context = {
        'form' : form,
        'titulo': titulo,
    }
    
    return render(request, 'Usuario/registro.html', context)