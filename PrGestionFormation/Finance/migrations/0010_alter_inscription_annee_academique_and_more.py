# Generated by Django 5.2.1 on 2025-07-15 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0009_alter_inscription_date_evenement'),
        ('Formation', '0002_alter_formation_duree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscription',
            name='annee_academique',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='Formation.anneeacademique'),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='classe',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='Formation.classe'),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='parcours',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='Formation.parcours'),
        ),
    ]
