# Generated by Django 5.1.3 on 2024-11-26 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motivo', '0001_initial'),
        ('transferencia', '0004_rename_timestamp_transferencia_fecha_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RazonTransferencia',
            new_name='MotivoTransferencia',
        ),
    ]