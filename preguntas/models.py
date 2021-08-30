from django.db import models
from django.db.models.base import Model
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import random


 
# Create your models here.


class Pregunta(models.Model):
    numero_de_respuestas_permitidas = 1
    texto = models.TextField(verbose_name= 'Texto de la pregunta')
    max_puntaje = models.DecimalField(verbose_name= 'Maximo puntaje', default= 3, decimal_places= 2, max_digits= 6)
    def __str__(self):
        return self.texto

class ElegirRespuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name= 'opciones', on_delete= models.CASCADE)
    correcta = models.BooleanField(verbose_name='¿ Es esta la pregunta correcta?', default= False, null= False)
    texto = models.TextField(verbose_name= 'texto de la respuesta')

    def __str__(self):
        return self.texto

class QuizUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete= models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name= 'Puntaje Total', default= 0, decimal_places= 2, max_digits= 10)

    def partidas_jugadas(self):
        pass


    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, quizUser = self)
        intento.save()

    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(quizUser = self).values_list('pregunta__pk', flat = True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in = respondidas)
        if not preguntas_restantes.exists():
            return None
        

        return random.choice(preguntas_restantes)

        

    
    def validar_intento(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return 
        
        pregunta_respondida.repuesta_seleccionada = respuesta_seleccionada
        
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_seleccionada
        else: 
            pregunta_respondida.respuesta = respuesta_seleccionada
        

       
       
        pregunta_respondida.save()
        self.actualizar_puntaje()
    
    def actualizar_puntaje(self):
        puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(
            models.Sum('puntaje_obtenido')) ['puntaje_obtenido__sum']
        self.puntaje_total = puntaje_actualizado or 0
        self.save()
        



class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete= models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete= models.CASCADE, null = True )
    correcta = models.BooleanField(verbose_name= '¿Es esta la respuesta correcta?', default= False, null= False)
    puntaje_obtenido = models.DecimalField(verbose_name= 'Puntaje Obtenido ', default= 0,decimal_places= 3, max_digits = 6)


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    login_date = models.DateTimeField(null = True)
    logout_date = models.DateTimeField(null = True)
    created = models.DateTimeField(auto_now_add = True, editable = False)

    
    class Meta:
        ordering = ['user', 'created']

    
    
    