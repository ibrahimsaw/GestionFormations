from django.contrib import admin
from .models import (
    Parcours,Formation,AnneeAcademique,Specification,Classe,TypeFormation
)
from .forms import (
    ParcoursForm,FormationForm,AnneeAcademiqueForm,SpecificationForm ,ClasseForm,TypeFormationForm
)


class SpecificationAdmin(admin.ModelAdmin):
    form = SpecificationForm
    list_display = ('nom',)
    search_fields = ('nom',)

class TypeFormationAdmin(admin.ModelAdmin):
    form = TypeFormationForm
    list_display = ('code','nom',)
    search_fields = ('code','nom',)


class ParcoursAdmin(admin.ModelAdmin):
    form = ParcoursForm
    list_display = ('nom', 'type_formation', 'specification')
    list_filter = ('type_formation', 'specification')
    search_fields = ('nom', 'code_serie')
    ordering = ('type_formation', 'nom')



class FormationAdmin(admin.ModelAdmin):
    form = FormationForm
    list_display = ('nom', 'parcours', 'duree', 'est_professionnelle', 'avec_classes')
    list_filter = ('parcours__type_formation', 'est_professionnelle')
    search_fields = ('nom', 'parcours__nom')
    raw_id_fields = ('parcours',)
    actions = ['creer_classes']

    @admin.action(description="Créer classes pour année sélectionnée")
    def creer_classes(self, request, queryset):
        annee = AnneeAcademique.objects.filter(classes_standards_creees=False).first()
        if annee:
            for formation in queryset:
                formation.creer_classes(annee)
            self.message_user(request, f"Classes créées pour {annee.nom}")
        else:
            self.message_user(request, "Aucune année académique disponible", level='error')


class AnneeAcademiqueAdmin(admin.ModelAdmin):
    form = AnneeAcademiqueForm
    list_display = ('nom', 'date_debut', 'date_fin', 'classes_standards_creees')
    list_editable = ('classes_standards_creees',)
    ordering = ('-date_debut',)
    actions = ['creer_classes_standards']

    @admin.action(description="Créer classes standards")
    def creer_classes_standards(self, request, queryset):
        for annee in queryset:
            annee.creer_classes_standards()
        self.message_user(request, "Classes standards créées")


class ClasseAdmin(admin.ModelAdmin):
    form = ClasseForm
    list_display = ('nom', 'formation', 'annee_academique', 'ordre')
    list_filter = ('formation__parcours__type_formation', 'annee_academique')
    search_fields = ('nom', 'formation__nom')
    raw_id_fields = ('formation', 'annee_academique')


admin.site.register(Specification, SpecificationAdmin)
admin.site.register(TypeFormation, TypeFormationAdmin)
admin.site.register(Parcours, ParcoursAdmin)
admin.site.register(Formation, FormationAdmin)
admin.site.register(AnneeAcademique, AnneeAcademiqueAdmin)
admin.site.register(Classe, ClasseAdmin)
# Register your models here.
