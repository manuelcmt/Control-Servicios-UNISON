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
    res1 = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    res2 = forms.ChoiceField(choices=((True, "Sí"), (False, "No"), (False, "No aplica")), widget=forms.RadioSelect)
    res3 = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    res4 = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    res5 = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)
    res6 = forms.ChoiceField(choices=((True, "Sí"), (False, "No")), widget=forms.RadioSelect)


class Fsi_04(forms.Form):
    res1 = forms.ChoiceField(choices=((5, "Fiebre, dolor de cabeza y tos seca."),
                                      (0, "Mareos, dolor de cabeza y oídos."),
                                      (0, "Tos seca, cansancio y dolor de oídos."),
                                      (0, "Fiebre, dolor muscular y moretones.")), widget=forms.RadioSelect)

    res2 = forms.ChoiceField(choices=((5, "Cubrebocas y careta."),
                                      (0, "Cubrebocas y lentes."),
                                      (0, "Bata y guantes."),
                                      (0, "Lentes y guantes.")), widget=forms.RadioSelect)

    res3 = forms.ChoiceField(choices=((0, "12 metros cuadrados."),
                                      (5, "9 metros cuadrados."),
                                      (0, "8 metros cuadrados"),
                                      (0, "5 metros cuadrados")), widget=forms.RadioSelect)

    res4 = forms.ChoiceField(choices=((0, "Evitar usar el agua por riesgo de contaminación."),
                                      (0, "Utilizar guantes en todo momento."),
                                      (0, "Lavarse las manos una vez al día."),
                                      (5, "Lavarse las manos constantemente o usar de la misma forma el alcohol con gel.")), widget=forms.RadioSelect)

    res5 =forms.ChoiceField(choices=((5, "La Comisión de Seguimiento para el regreso a las actividades."),
                                     (0, "Los Usuarios."),
                                     (0, "Los Responsables."),
                                     (0, "La Brigada de Inspección.")), widget=forms.RadioSelect)

    res6 = forms.ChoiceField(choices=((0, "Sí."),
                                      (5, "No.")), widget=forms.RadioSelect)

    res7 = forms.ChoiceField(choices=((0, "0.1%"),
                                      (0, "0.5%"),
                                      (5, "4-5%"),
                                      (0, "3-4%")), widget=forms.RadioSelect)

    res8 = forms.ChoiceField(choices=((5, "No he viajado a zonas gravemente afectadas por COVID-19 o zonas en semáforo rojo en los últimos 15 días."),
                                      (0, "No tengo ni he tenido contacto directo o indirecto, durante los últimos 15 días con alguna persona que haya sido diagnosticada con COVID-19, ni en mi domicilio ni en mi lugar de trabajo."),
                                      (0, "Me comprometo a atender el llamado de la Comisión de Seguimiento para realizarme la toma de muestra para el diagnóstico COVID-19, en caso de salir sorteado dentro del 5% de personal activo en el campus."),
                                      (0, "Me comprometo a no emplear el transporte público para trasladarme a las instalaciones universitarias.")), widget=forms.RadioSelect)

    res9_1 = forms.ChoiceField(choices=((0, "1"),
                                        (0, "2"),
                                        (1, "3"),
                                        (0, "4")), widget=forms.RadioSelect)

    res9_2 = forms.ChoiceField(choices=((0, "1"),
                                        (1, "2"),
                                        (0, "3"),
                                        (0, "4")), widget=forms.RadioSelect)

    res9_3 = forms.ChoiceField(choices=((0, "1"),
                                        (0, "2"),
                                        (0, "3"),
                                        (1, "4")), widget=forms.RadioSelect)

    res9_4 = forms.ChoiceField(choices=((1, "1"),
                                        (0, "2"),
                                        (0, "3"),
                                        (0, "4")), widget=forms.RadioSelect)

    res10 = forms.ChoiceField(choices=((0, "1.50 metros"),
                                        (5, "1.80 metros"),
                                        (0, "1.20 metros"),
                                        (0, "0.50 metros")), widget=forms.RadioSelect)

    res11 = forms.ChoiceField(choices=((0, "Los Responsables"),
                                       (5, "Los Usuarios"),
                                       (0, "La Comisión de Seguimiento para el regreso a las actividades"),
                                       (0, "La Brigada de Inspección")), widget=forms.RadioSelect)

    res12 = forms.ChoiceField(choices=((0, "Los Responsables"),
                                       (5, "Los Usuarios"),
                                       (0, "La Comisión de Seguimiento para el regreso a las actividades"),
                                       (0, "La Brigada de Inspección")), widget=forms.RadioSelect)

    res13 = forms.ChoiceField(choices=((0, "Corroborar que el personal tome los cursos de capacitación y llevar el control de esta capacitación por medio de las constacias de acreditación."),
                                       (0, "Establecer protocolo de limpieza de equipos y espacios al inicio y final de cada jornada."),
                                       (5, "Identificar el personal que debe retornar con base a la priorización de actividades, excluyendo personal que se encuentre dentro de los grupos de riesgo."),
                                       (0, "Poner a disposición de los usuarios material y sustancias para limpieza y desinfección.")), widget=forms.RadioSelect)

    res14 = forms.ChoiceField(choices=((0, "Falso."),
                                      (5, "Verdadero.")), widget=forms.RadioSelect)

    res15 = forms.ChoiceField(choices=((0, "Falso."),
                                      (5, "Verdadero.")), widget=forms.RadioSelect)

    res16 = forms.ChoiceField(choices=((0, "Falso."),
                                      (5, "Verdadero.")), widget=forms.RadioSelect)

    res17 = forms.ChoiceField(choices=((5, "Verde"),
                                        (0, "Amarillo"),
                                        (0, "Rojo"),
                                        (0, "Naranja")), widget=forms.RadioSelect)

    res18 = forms.ChoiceField(choices=((0, "Los Usuarios."),
                                        (5, "La Comisión de Seguimiento para el regreso a las actividades."),
                                        (0, "La Brigada de Inspección."),
                                        (0, "Los Responsables.")), widget=forms.RadioSelect)

    res19 = forms.ChoiceField(choices=((0, "Falso."),
                                       (5, "Verdadero.")), widget=forms.RadioSelect)

    res20 = forms.ChoiceField(choices=((5, "Sí."),
                                       (0, "No.")), widget=forms.RadioSelect)




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
