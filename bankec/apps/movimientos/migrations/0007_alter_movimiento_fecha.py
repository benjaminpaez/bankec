# Generated by Django 5.1.3 on 2024-11-27 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0006_movimiento_comprobante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
