from django import forms
#from django.forms import forms
from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas


class ElegirInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInlineFormset, self).clean()

        respuesta_correcta = 0
        for formulario in self.forms:
            if not formulario.is_valid():
                return
            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1
        try:
            assert respuesta_correcta == Pregunta.numero_de_respuestas_permitidas
        
        except AssertionError:
            raise forms.ValidationError('Se espera una sola respuesta correcta')
            
            


    
