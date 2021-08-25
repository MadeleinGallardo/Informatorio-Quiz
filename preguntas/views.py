from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import RegistroFormulario, IniciarSesionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PreguntasRespondidas, QuizUsuario, Pregunta

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

@login_required()
def jugar(request):
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario = request.user)
    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk= pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')
    else:
        respondidas = PreguntasRespondidas.objects.filter(quizUser = QuizUser).values_list('pregunta__pk', flat = True)
        pregunta = Pregunta.objects.exclude(pk__in = respondidas)
        context ={
           'pregunta':pregunta
        }
    

    return render(request, 'quiz/jugar.html', context)


@login_required()
def ranking(request):
    usuarios_top = QuizUsuario.objects.order_by('-puntaje_total')[:500]
    contador_total = usuarios_top.count()
    context = {
        'Usuarios_ranking': usuarios_top,
        'contador_total': contador_total,
    }

    return render(request, 'quiz/ranking.html', context)


@login_required()
def estats_usuario(request):

    return render(request, 'quiz/estadisticas.html',context=None)





