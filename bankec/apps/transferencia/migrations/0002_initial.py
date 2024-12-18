# Generated by Django 5.1.3 on 2024-11-22 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('motivo', '0001_initial'),
        ('transferencia', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='transferencia',
            name='emisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_enviadas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transferencia',
            name='motivo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='motivo.razontransferencia'),
        ),
        migrations.AddField(
            model_name='transferencia',
            name='receptor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_recibidas', to=settings.AUTH_USER_MODEL),
        ),
    ]
