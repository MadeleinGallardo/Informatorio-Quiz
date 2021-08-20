from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import RegistroFormulario, IniciarSesionForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):
    return render(request,'quiz/inicio.html', context=None)



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


def jugar(request):

    return render(request, 'quiz/jugar.html', context=None)

# Intento de inicio de sesion

def vista_login(request):
    title = "Iniciar Sesion"
    form = IniciarSesionForm(request.POST or None)
    if form.is_valid():
        usuario = form.cleaned_data.get("Nombre de usuario")
        contraseña = form.cleaned_data.get("contraseña")
        user = authenticate(username=usuario, password=contraseña)
        login(request,user)
        return redirect('')

    return render(request, 'Usuario/login.html',{"form":form, "titulo":title})


