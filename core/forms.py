from  django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField

class RegistroUsuarioForm(UserCreationForm):
    #captcha = ReCaptchaField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Correo electrónico', max_length=254)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class NoticiaForm(forms.ModelForm):
    #captcha = ReCaptchaField()
    class Meta:
        model = Noticia
        fields = ['titulo', 'descripcion', 'ubicacion', 'categoria']


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['image']

class CrearPeriodistaForm(forms.ModelForm):
    #captcha = CaptchaField()
    captcha = ReCaptchaField()
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Periodista
        fields = ['nombre', 'apellido', 'genero', 'usuario','plan']



