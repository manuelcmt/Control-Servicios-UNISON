# Generated by Django 3.1.3 on 2020-12-04 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Control_Servicios_UNISON', '0007_auto_20201203_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areatrabajo',
            name='usuarios',
        ),
        migrations.AddField(
            model_name='inspeccionsanitaria',
            name='comentarios',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='inspeccionsanitaria',
            name='cubrebocas',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='inspeccionsanitaria',
            name='gel_antibacterial',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='inspeccionsanitaria',
            name='higiene',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='inspeccionsanitaria',
            name='limite_usuarios',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='inspeccionsanitaria',
            name='sanitizante',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='inspeccionsanitaria',
            name='tapete',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='inspeccionsanitaria',
            name='brigadista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
