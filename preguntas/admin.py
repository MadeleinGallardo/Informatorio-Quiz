from django.contrib import admin
from django.db import models
from preguntas.models import Pregunta, ElegirRespuesta, PreguntasRespondidas
from .forms import ElegirInlineFormset

# Register your models here.
# instancia los modelos
class ElegirRespuestaInline(admin.TabularInline):
    model = ElegirRespuesta
    formset = ElegirInlineFormset


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestaInline, )
    list_display = ['texto',]
    seach_fields = ['texto', 'preguntas__texto']

class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']
    class Meta:
        model = PreguntasRespondidas


admin.site.register(PreguntasRespondidas, PreguntasRespondidasAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)