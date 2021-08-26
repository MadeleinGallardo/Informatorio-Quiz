from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
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

        try:
            opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(pk = respuesta_pk)
        except ObjectDoesNotExist:
            raise Http404
        
        #Validar el intento
        QuizUser.validar_intento(pregunta_respondida, opcion_seleccionada)

        return redirect(pregunta_respondida)
    
    else:
        pregunta = QuizUser.obtener_nuevas_preguntas()
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)
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





