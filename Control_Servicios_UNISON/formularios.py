from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from Control_Servicios_UNISON.models import UsuarioBase


class FormularioRegistro(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'last_name', 'first_name']


class Fsi_02(forms.Form):
    res1 = forms.BooleanField()
    res2 = forms.BooleanField()
    res3 = forms.BooleanField()
    res4 = forms.BooleanField()
    res5 = forms.BooleanField()
    res6 = forms.BooleanField()


class EleccionRol(forms.ModelForm):
    class Meta:
        model = UsuarioBase
        fields = ('rol',)
