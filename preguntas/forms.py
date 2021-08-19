from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
#from django.forms import forms
from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas
from django.contrib.auth import get_user_model
User = get_user_model()


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
            
            
class RegistroFormulario(UserCreationForm):
    email = forms.EmailField(required= True)
    nombre = forms.CharField( max_length= 30, required=True)
    apellido = forms.CharField(max_length= 30, required= True)
        
    class Meta: 
        model = User
            
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            ]


    
