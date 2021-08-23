from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import RegistroFormulario, IniciarSesionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def inicio(request):
    return render(request,'quiz/inicio.html', context=None)


def registro(request):
    
    data = {
        "form" : RegistroFormulario()
    }

    if request.method == 'POST':
        form = RegistroFormulario(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to='inicio')
        data["form"] = form

    return render(request, 'registration/registro.html', data)


def jugar(request):

    return render(request, 'quiz/jugar.html', context=None)


@login_required()
def ranking(request):

    return render(request, 'quiz/ranking.html',context=None)

@login_required()
def estadisticas(request):
    return render(request, 'quiz/estadisticas.html',context=None)





