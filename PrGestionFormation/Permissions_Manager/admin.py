from django.contrib import admin
from .models import *
from Utilisateur.models import FonctionAgent

# Register your models here.
@admin.register(MetaPermission)
class MetaPermissionAdmin(admin.ModelAdmin):
    list_display = ('date_creation','date_modification','permission', 'description', 'roles_autorises')

# @admin.register(FonctionAgent)
# class PermissionFonctionAgent(admin.ModelAdmin):
#     list_display = ('code', 'nom', 'description', 'responsabilites', 'controles', 'protocoles', 'permissions')

# @admin.register(FonctionAgent)
# class FonctionAgentAdmin(admin.ModelAdmin):
#     list_display = ('code', 'nom', 'description', 'responsabilites', 'controles', 'protocoles', 'permissions')
#     filter_horizontal = ('permissions',)