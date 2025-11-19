from django.db import migrations, models
from Formation.models import AnneeAcademique

def remplir_fk_annee_academique(apps, schema_editor):
    Enseignement = apps.get_model('Cours', 'Enseignement')
    AnneeAcademique = apps.get_model('Formation', 'AnneeAcademique')

    for ens in Enseignement.objects.all():
        aa, created = AnneeAcademique.objects.get_or_create(nom=ens.annee_academique)
        ens.annee_academique_id = aa.id
        ens.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Cours', '0005_alter_evaluation_enseignement_and_more'),
    ]

    operations = [
        migrations.RunPython(remplir_fk_annee_academique),
    ]
