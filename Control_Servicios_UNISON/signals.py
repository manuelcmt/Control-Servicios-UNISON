from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import UsuarioBase, AsignacionBrigada, QuimicoActivo, ResponsabilidadArea, JefaturaDepartamento, \
    TurnoAsignado


def nuevo_registro(sender, instance, created, **kwargs):
    if created:
        UsuarioBase.objects.create(usuario=instance, rol='SIN_ELEGIR', fsi_02=False, fsi_04=False, capacitacion=False)
        group = Group.objects.get(name='Entrenamiento')
        instance.groups.add(group)


post_save.connect(nuevo_registro, sender=User)
