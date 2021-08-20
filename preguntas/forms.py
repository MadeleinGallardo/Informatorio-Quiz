from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import fields
#from django.forms import forms
from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas
from django.contrib.auth import authenticate, get_user_model

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
            
#registrarse
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


# Intento de login


class IniciarSesionForm(forms.Form):
    usuario = forms.CharField()
    contraseña = forms.CharField(widget= forms.PasswordInput)

    def clean(self, *args, **kwargs):
        usuario = self.cleaned_data.get("usuario")
        contraseña = self.cleaned_data.get("contraseña")

        if usuario and contraseña:
            user = authenticate(usuario=usuario, contraseña=contraseña)
            if not user:
                raise forms.ValidationError("Este nombre de usuario no existe")

            if not user.check_password(contraseña):
                raise forms.ValidationError("Contraseña incorrecta, intentelo nuevamente")

        return super(IniciarSesionForm,self).clean(*args, **kwargs)

