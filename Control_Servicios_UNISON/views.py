from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .decorators import para_no_autenticados, usuarios_admitidos
from .formularios import *


# Create your views here.
def inicio(request):
    if request.user.is_authenticated:
        # Todos tienen un grupo por defecto al crearse
        grupo = request.user.groups.all()[0].name
        if grupo == 'Entrenamiento':
            incumbencia = 'capacitarse'

        elif grupo == 'Jefes de Departamento':
            incumbencia = 'registro-departamento'

        elif grupo == 'Responsables':
            incumbencia = 'administrar-area'

        elif grupo == 'Brigada':
            incumbencia = 'brigada'

        elif grupo == 'Comisión':
            incumbencia = 'seguimiento'

        # Aquí actúa el grupo Capacitados
        else:
            if request.user.usuariobase.rol != 'SIN_ELEGIR':
                incumbencia = 'turno'
            else:
                incumbencia = 'solicitar-acceso'

    else:
        incumbencia = 'iniciar-sesion'

    return redirect(incumbencia)


@para_no_autenticados
def registrarse(request):
    formulario = FormularioRegistro(request.POST)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, 'Su cuenta se ha creado, complete los cursos y elija un rol.')

        return redirect('iniciar-sesion')

    context = {'formulario': formulario}
    return render(request, 'registrarse.html', context)


@para_no_autenticados
def iniciar_sesion(request):
    if request.method == 'POST':
        expediente = request.POST.get('expediente')
        contrasena = request.POST.get('contrasena')
        usuario = authenticate(request, username=expediente, password=contrasena)

        if usuario is not None:
            login(request, usuario)
            return redirect('inicio')
        else:
            messages.info(request, 'Esa combinación de expediente y contraseña no está en el sistema.')

    context = {}

    return render(request, 'iniciar-sesion.html', context)


def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar-sesion')


@usuarios_admitidos(roles_admitidos=['Responsables'])
def administrar_area(request):
    context = {'solicitudes': SolicitudTurno.objects.filter(area_solici=request.user.responsabilidadarea.area_trabajo),
               'turnos': request.user.responsabilidadarea.area_trabajo.turnoasignado_set.all(),
               'area': request.user.responsabilidadarea.area_trabajo}
    return render(request, 'administrar-area.html', context)


@usuarios_admitidos(roles_admitidos=['Brigada'])
def brigada(request):
    division = request.user.asignacionbrigada.division
    areas = []

    for departamento in division.departamento_set.all():
        for area in departamento.areatrabajo_set.all():
            if area.autorizada:
                areas.append(area)

    context = {'division': division, 'areas': areas}
    return render(request, 'brigada.html', context)


@usuarios_admitidos(roles_admitidos=['Brigada'])
def inspeccion_sanitaria(request, pk):
    formulario = ReportarArea(request.POST)
    inspector = request.user
    area = AreaTrabajo.objects.get(id=pk)

    if request.method == 'POST':
        if formulario.is_valid():
            puntos_riesgo = 0
            if formulario.cleaned_data['limite_usuarios'] == 'False':
                puntos_riesgo += 1
            if not formulario.cleaned_data['higiene'] == 'False':
                puntos_riesgo += 1
            if not formulario.cleaned_data['gel_antibacterial'] == 'False':
                puntos_riesgo += 1
            if not formulario.cleaned_data['sanitizante'] == 'False':
                puntos_riesgo += 1
            if not formulario.cleaned_data['tapete'] == 'False':
                puntos_riesgo += 1
            if not formulario.cleaned_data['cubrebocas'] == 'False':
                puntos_riesgo += 1

            if puntos_riesgo != 0 or formulario.cleaned_data['comentarios'] != '':
                inspeccion = InspeccionSanitaria.objects.create(
                    limite_usuarios=formulario.cleaned_data['limite_usuarios'],
                    higiene=formulario.cleaned_data['higiene'],
                    gel_antibacterial=formulario.cleaned_data['gel_antibacterial'],
                    sanitizante=formulario.cleaned_data['sanitizante'],
                    tapete=formulario.cleaned_data['tapete'],
                    cubrebocas=formulario.cleaned_data['cubrebocas'],
                    comentarios=formulario.cleaned_data['comentarios'],
                    brigadista=inspector,
                    area_revisada=area,
                    fecha=datetime.now(),
                    riesgo=puntos_riesgo
                    )

                inspeccion.save()
            area.ultima_rev = datetime.now()
            area.save()
            return redirect(brigada)

    context = {'formulario': formulario, 'area': area}
    return render(request, 'inspeccion-sanitaria.html', context)


@usuarios_admitidos(roles_admitidos=['Jefes de Departamento'])
def registro_departamento(request):
    formulario = RegistrarArea(request.POST)
    departamento = request.user.jefaturadepartamento.departamento

    if request.method == 'POST':
        if formulario.is_valid():
            if formulario.cleaned_data['espacio_m2'] < 9:
                capacidad = 1
            else:
                capacidad = formulario.cleaned_data['espacio_m2'] / 1.8

            nueva_area = AreaTrabajo.objects.create(nombre=formulario.cleaned_data['nombre'], departamento=departamento,
                                                    direccion=formulario.cleaned_data['direccion'],
                                                    espacio_m2=formulario.cleaned_data['espacio_m2'],
                                                    capacidad=capacidad)
            nueva_area.save()
            return redirect('registro-departamento')

    context = {'nombre_depto': departamento.nombre, 'division': departamento.division.nombre,
               'areas': departamento.areatrabajo_set.all(), 'formulario': formulario}
    return render(request, 'registro-departamento.html', context)


@usuarios_admitidos(roles_admitidos=['Capacitados'])
def turno(request):
    return render(request, 'turno.html')


@usuarios_admitidos(roles_admitidos=['Capacitados'])
def solicitar_acceso(request):
    # Jefes de departamento
    if request.user.usuariobase.rol == 'JD':
        formulario = SolicitarJefatura(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                nueva_jefatura = SolicitudJefatura.objects.create(jefe=request.user,
                                                                  division=formulario.cleaned_data['division'],
                                                                  nombre_depto=formulario.cleaned_data['nombre_depto'])
                nueva_jefatura.save()
                return redirect('inicio')

    # Responsables de área
    elif request.user.usuariobase.rol == 'RA':
        formulario = SolicitarApertura(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                nueva_responsabilidad = SolicitudApertura.objects.create(responsable=request.user,
                                                                         area_solici=formulario.cleaned_data[
                                                                             'area_solici'])
                nueva_responsabilidad.save()
                return redirect('inicio')

    # Usuarios que piden acceso
    elif request.user.usuariobase.rol == 'IN' or request.user.usuariobase.rol == 'AL' or request.user.usuariobase.rol == 'EM':
        formulario = SolicitarTurno(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                nuevo_turno = SolicitudTurno.objects.create(usuario=request.user,
                                                            area_solici=formulario.cleaned_data['area_solici'])
                nuevo_turno.save()
                return redirect('inicio')


    # Brigadistas (no requieren solicitud)
    elif request.user.usuariobase.rol == 'BR':
        return redirect('inicio')

    # Usuario aún sin rol definido
    else:
        formulario = EleccionRol(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                request.user.usuariobase.rol = formulario.cleaned_data['rol']
                request.user.usuariobase.save()
                return redirect('solicitar-acceso')

    return render(request, 'solicitar-acceso.html', {'formulario': formulario})


@usuarios_admitidos(roles_admitidos=['Comisión'])
def seguimiento(request):
    context = {'divisiones': Division.objects.all(),
               'solic_jefaturas': SolicitudJefatura.objects.all(),
               'solic_aperturas': SolicitudApertura.objects.all(),
               'inspecciones': InspeccionSanitaria.objects.all(),
               }
    return render(request, 'seguimiento.html', context)


@usuarios_admitidos(roles_admitidos=['Entrenamiento'])
def responder_fsi_02(request):
    formulario = Fsi_02(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            for respuesta in formulario:
                if respuesta.value() == 'False':
                    messages.info(request, 'Lamentablemente, no cumple con los requisitos para volver en esta etapa.')
                    return redirect('capacitarse')

            request.user.usuariobase.fsi_02 = True
            request.user.usuariobase.save()
            messages.success(request, 'Ha completado el formato FSI-02.')

            return redirect('capacitarse')

    context = {'formulario': formulario}
    return render(request, 'responder-FSI-02.html', context)


@usuarios_admitidos(roles_admitidos=['Entrenamiento'])
def responder_fsi_04(request):
    formulario = Fsi_04(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            puntaje = 0
            for respuesta in formulario:
                puntaje += int(respuesta.value())

            print(puntaje)
            if puntaje >= 80:
                request.user.usuariobase.fsi_04 = True
                request.user.usuariobase.save()
                messages.success(request, 'Ha completado el formato FSI-04.')

            else:
                messages.info(request, 'Lamentablemente, no cumple con los requisitos para volver en esta etapa.')

            return redirect('capacitarse')


    context = {'formulario': formulario}
    return render(request, 'responder-FSI-04.html', context)


@usuarios_admitidos(roles_admitidos=['Entrenamiento'])
def capacitarse(request):
    if request.user.usuariobase.fsi_02 and request.user.usuariobase.fsi_04:
        grupo = Group.objects.get(name='Entrenamiento')
        request.user.groups.remove(grupo)
        grupo = Group.objects.get(name='Capacitados')
        request.user.groups.add(grupo)
        return redirect('solicitar-acceso')

    return render(request, 'capacitarse.html', {'fsi_02': request.user.usuariobase.fsi_02, 'fsi_04': request.user.usuariobase.fsi_04 })


@usuarios_admitidos(roles_admitidos=['Comisión'])
def divisiones(request, pk):
    division = Division.objects.get(id=pk)
    brigada = AsignacionBrigada.objects.filter(division=division)
    brigadistas = UsuarioBase.objects.filter(rol='BR')
    brigadistas_disp = []
    for brigadista in brigadistas:
        if brigadista.usuario.groups.all()[0].name != 'Brigada':
            brigadistas_disp.append(brigadista.usuario)

    context = {'division': division, 'brigada': brigada, 'brigadistas_disp': brigadistas_disp}

    return render(request, 'divisiones.html', context)


@usuarios_admitidos(roles_admitidos=['Comisión'])
def aceptar_jefatura(request, pk):
    solicitud = SolicitudJefatura.objects.get(id=pk)

    nuevo_depto = Departamento.objects.create(nombre=solicitud.nombre_depto, division=solicitud.division)
    nuevo_depto.save()
    nueva_jefatura = JefaturaDepartamento.objects.create(usuario=solicitud.jefe, departamento=nuevo_depto)
    nueva_jefatura.save()

    solicitud.jefe.groups.add(Group.objects.get(name='Jefes de Departamento'))
    solicitud.jefe.groups.remove(Group.objects.get(name='Capacitados'))

    solicitud.delete()

    return render(request, 'aceptar-jefatura.html')


@usuarios_admitidos(roles_admitidos=['Comisión'])
def aceptar_apertura(request, pk):
    solicitud = SolicitudApertura.objects.get(id=pk)

    nueva_responsabilidad = ResponsabilidadArea.objects.create(usuario=solicitud.responsable,
                                                               area_trabajo=solicitud.area_solici)
    nueva_responsabilidad.save()

    solicitud.responsable.groups.add(Group.objects.get(name='Responsables'))
    solicitud.responsable.groups.remove(Group.objects.get(name="Capacitados"))
    solicitud.area_solici.autorizada = True
    if solicitud.area_solici.capacidad == 1:
        solicitud.area_solici.disponibles = False

    solicitud.area_solici.ultima_rev = datetime.now()
    solicitud.area_solici.save()
    solicitud.delete()

    return redirect(seguimiento)


@usuarios_admitidos(roles_admitidos=['Comisión'])
def clausurar_area(request, pk):
    area = AreaTrabajo.objects.get(id=pk)

    for turno in area.turnoasignado_set.all():
        turno.delete()

    area.responsabilidadarea_set.all()[0].usuario.groups.remove(Group.objects.get(name='Responsables'))
    area.responsabilidadarea_set.all()[0].usuario.groups.add(Group.objects.get(name='Capacitados'))
    area.responsabilidadarea_set.all()[0].delete()
    area.autorizada = False
    area.disponibles = True
    area.save()

    return redirect(seguimiento)


@usuarios_admitidos(roles_admitidos=['Responsables'])
def aceptar_turno(request, pk):
    solicitud = SolicitudTurno.objects.get(id=pk)

    nuevo_turno = TurnoAsignado.objects.create(usuario=solicitud.usuario, area_trabajo=solicitud.area_solici)
    nuevo_turno.save()

    if solicitud.area_solici.turnoasignado_set.count() + 1 >= solicitud.area_solici.capacidad:
        solicitud.area_solici.disponibles = False

    solicitud.area_solici.save()
    solicitud.delete()

    return redirect(administrar_area)


@usuarios_admitidos(roles_admitidos=['Responsables'])
def revocar_turno(request, pk):
    turno = TurnoAsignado.objects.get(id=pk)
    turno.delete()

    return redirect(administrar_area)


@usuarios_admitidos(roles_admitidos=['Comisión'])
def asignar_brigadista(request, usuario, division):
    brigadista = User.objects.get(id=usuario)
    divisi_asig = Division.objects.get(id=division)

    nueva_asignacion = AsignacionBrigada.objects.create(division=divisi_asig, usuario=brigadista)
    nueva_asignacion.save()
    brigadista.groups.add(Group.objects.get(name="Brigada"))
    brigadista.groups.remove(Group.objects.get(name="Capacitados"))

    return redirect(divisiones, divisi_asig.id)


@usuarios_admitidos(roles_admitidos=['Comisión'])
def desasignar_brigadista(request, usuario, division):
    brigadista = User.objects.get(id=usuario)
    asignacion = AsignacionBrigada.objects.get(usuario=brigadista)
    asignacion.delete()
    brigadista.groups.remove(Group.objects.get(name="Brigada"))
    brigadista.groups.add(Group.objects.get(name="Capacitados"))

    return redirect(divisiones, division)
