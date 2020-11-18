from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .decorators import para_no_autenticados, usuarios_admitidos
from .formularios import *


# Create your views here.
def inicio(request):
    if request.user.is_authenticated is False:
        return redirect('iniciar-sesion')

    return render(request, 'inicio.html')


@para_no_autenticados
def registrarse(request):
    formulario = FormularioRegistro(request.POST)
    messages.success(request, 'Su cuenta se ha creado, complete los cursos y elija un rol.')
    if formulario.is_valid():
        formulario.save()

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
    return render(request, 'administrar-area.html')


@usuarios_admitidos(roles_admitidos=['Brigada'])
def brigada(request):
    return render(request, 'brigada.html')


@usuarios_admitidos(roles_admitidos=['Jefes de Departamento'])
def registro_departamento(request):
    return render(request, 'registro-departamento.html')


@usuarios_admitidos(roles_admitidos=['Capacitados'])
def turno(request):
    return render(request, 'turno.html')


@usuarios_admitidos(roles_admitidos=['Capacitados'])
def reservar_turno(request):
    return render(request, 'reservar-turno.html')


@usuarios_admitidos(roles_admitidos=['Comisión'])
def seguimiento(request):
    return render(request, 'seguimiento.html')


@usuarios_admitidos(roles_admitidos=['Entrenamiento'])
def responder_fsi_02(request):
    formulario = Fsi_02(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            for respuesta in formulario:
                if respuesta is False:
                    messages.info(request, 'Lamentablemente, no cumple con los requisitos para volver en esta etapa.')
                    return redirect('inicio')

            request.user.usuariobase.fsi_02 = True
            request.user.usuariobase.save()
            messages.success(request, 'Ha completado el formato FSI-02.')

            return redirect('capacitarse')

    context = {'formulario': formulario}
    return render(request, 'responder-FSI-02.html', context)


@usuarios_admitidos(roles_admitidos=['Entrenamiento'])
def responder_fsi_04(request):
    return None


@usuarios_admitidos(roles_admitidos=['Entrenamiento'])
def capacitarse(request):
    formulario = EleccionRol(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            request.user.usuariobase.rol = formulario.cleaned_data['rol']
            request.user.usuariobase.save()

    if request.user.usuariobase.fsi_02:
        grupo = Group.objects.get(name='Entrenamiento')
        request.user.groups.remove(grupo)
        grupo = Group.objects.get(name='Capacitados')
        request.user.groups.add(grupo)

    return render(request, 'capacitarse.html', {'formulario': formulario, 'rol_actual': request.user.usuariobase.rol})


@usuarios_admitidos(roles_admitidos=['Comisión'])
def divisiones(request):
    return None
