from django.contrib import admin

# Register your models here.
from Control_Servicios_UNISON.models import *

admin.site.register(UsuarioBase)
admin.site.register(Division)
admin.site.register(Departamento)
admin.site.register(AreaTrabajo)

admin.site.register(QuimicoActivo)
admin.site.register(AsignacionBrigada)
admin.site.register(ResponsabilidadArea)
admin.site.register(JefaturaDepartamento)
admin.site.register(TurnoAsignado)

admin.site.register(InspeccionSanitaria)
admin.site.register(PruebaCovidPositivo)

admin.site.register(SolicitudJefatura)
admin.site.register(SolicitudApertura)
admin.site.register(SolicitudTurno)
