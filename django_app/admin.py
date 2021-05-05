from django.contrib import admin

from .models import *


# from import_export.admin import ImportExportModelAdmin


# Register your models here.
admin.site.register(Classroom)
admin.site.register(Evenement)
admin.site.register(Matiere)

# class MatiereResource(ImportExportModelAdmin):

#     class Meta:
#         model = Matiere
#         fields = ('id', 'name', 'price',)


# admin.site.register(Matiere,MatiereResource)
admin.site.register(SupportDeCours)
admin.site.register(TypeNote)
admin.site.register(Note)