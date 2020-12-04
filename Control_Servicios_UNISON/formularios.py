from django.contrib.auth.forms import UserCreationForm
from django import forms

from Control_Servicios_UNISON.models import *


# Formularios de registro
class FormularioRegistro(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'last_name', 'first_name']

# EleccionRol
class EleccionRol(forms.ModelForm):
    class Meta:
        model = UsuarioBase
        fields = ('rol',)


# Formulario de registro de área para el jefe de departamento
class RegistrarArea(forms.ModelForm):
    class Meta:
        model = AreaTrabajo
        fields = ('nombre', 'direccion', 'espacio_m2',)

# Formularios de capacitación
class Fsi_02(forms.Form):
    res1 = forms.BooleanField()
    res2 = forms.BooleanField()
    res3 = forms.BooleanField()
    res4 = forms.BooleanField()
    res5 = forms.BooleanField()
    res6 = forms.BooleanField()


# Formularios de acceso
class SolicitarJefatura(forms.Form):
    division = forms.ModelChoiceField(label='División', queryset=Division.objects.order_by("nombre").all())
    nombre_depto = forms.CharField(max_length=50)



class SolicitarApertura(forms.Form):
    area_solici = forms.ModelChoiceField(label='Área', queryset=AreaTrabajo.objects.order_by("nombre").exclude(autorizada=True))


class SolicitarTurno(forms.Form):
    area_solici = forms.ModelChoiceField(label="Área", queryset=AreaTrabajo.objects.order_by("nombre").exclude(autorizada=False).exclude(disponibles=False))


class ReportarArea(forms.Form):
    # Indicadores de salubridad
    # No se sobrepasa el límite de usuarios indicado para el área en cuestión
    limite_usuarios = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    # El lugar presenta, en general una buena higiene
    higiene = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    # Hay gel antibacterial disponible
    gel_antibacterial = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    # Hay sanitizante para superficies y otros objetos
    sanitizante = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    # Hay tapete desinfectante en la entrada
    tapete = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    # Todos los presentes tienen cubrebocas
    cubrebocas = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)

    # Cualquier observación personalizada del brigadista
    comentarios = forms.CharField(widget=forms.Textarea, required=False)
