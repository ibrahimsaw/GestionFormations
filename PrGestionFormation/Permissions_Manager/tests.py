from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from Utilisateur.models import Utilisateur

class MetaPermission(models.Model):
    """
    Extension des permissions standard pour y ajouter des métadonnées
    """
    permission = models.OneToOneField(
        Permission,
        on_delete=models.CASCADE,
        related_name='meta'
    )
    description = models.TextField(blank=True)
    roles_autorises = models.CharField(max_length=200)
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MetaPermission pour {self.permission.name}"

    class Meta:
        verbose_name = "Métadonnée de permission"
        verbose_name_plural = "Métadonnées de permissions"