# Generated by Django 3.1.3 on 2020-11-26 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Control_Servicios_UNISON', '0003_auto_20201117_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariobase',
            name='rol',
            field=models.CharField(choices=[('NA', 'No elegido'), ('BR', 'Brigadista'), ('JD', 'Jefe de departamento'), ('RA', 'Responsable'), ('IN', 'Investigador'), ('AL', 'Alumno'), ('EM', 'Empleado'), ('QU', 'Químico')], default='NA', max_length=2),
        ),
    ]
