from django.contrib import admin
from preguntas.models import Pregunta, ElegirRespuesta
# Register your models here.

admin.site.register(Pregunta)
admin.site.register(ElegirRespuesta)