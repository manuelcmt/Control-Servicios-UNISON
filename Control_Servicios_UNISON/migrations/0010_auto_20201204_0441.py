# Generated by Django 3.1.3 on 2020-12-04 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Control_Servicios_UNISON', '0009_auto_20201204_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspeccionsanitaria',
            name='comentarios',
            field=models.TextField(null=True),
        ),
    ]
