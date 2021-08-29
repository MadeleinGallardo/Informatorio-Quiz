from django import forms
from django.contrib.auth import authenticate, login, user_logged_in, user_logged_out
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistroFormulario, IniciarSesionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PreguntasRespondidas, QuizUsuario, Pregunta, UserActivityLog
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.

def inicio(request):
    return render(request,'quiz/inicio.html', context=None)

def juego(request):
    return render(request,'quiz/juego.html', context=None)


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
    if request.user.is_active:
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

            return redirect('resultado',pregunta_respondida.pk )
        
        else:
            pregunta = QuizUser.obtener_nuevas_preguntas()
            if pregunta is not None:
                QuizUser.crear_intentos(pregunta)
            context ={
            'pregunta':pregunta
            }

        return render(request, 'quiz/jugar.html', context)

    return render(request, 'quiz/jugar.html', context=None)

def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(PreguntasRespondidas, pk = pregunta_respondida_pk)
    context = {
        'respondida': respondida
    }
    return render(request, 'quiz/resultados.html', context)

@login_required()
def ranking(request):
    usuarios_top = QuizUsuario.objects.order_by('-puntaje_total')[:500]
    contador_total = usuarios_top.count()
    context = {
        'usuarios_top': usuarios_top,
        'contador_total': contador_total,
        
    }
    print(usuarios_top)
    for x in usuarios_top:
       print( x.__dict__)
       #print( x.user.__dict__)

    return render(request, 'quiz/ranking.html', context)


@login_required()
def estadisticas(request):
    usuarios = UserActivityLog.objects.order_by('-login_date')[:20]
    contador = User.objects.count()
    context = {
        'usuarios': usuarios,
        'contador': contador,

    }

    return render(request, 'quiz/estadisticas.html', context)


@receiver(user_logged_in)
def register_user_login(sender, request, user, **kwargs):
    obj = UserActivityLog.objects.create(user = user, login_date = timezone.now())
    request.session['user_activity_log_id'] = obj.id

@receiver(user_logged_out)
def register_user_logout(sender, request, user, **kwargs):
    UserActivityLog.objects.filter(id = request.session['user_activity_log_id']).update(
        logout_date = timezone.now()
    )




