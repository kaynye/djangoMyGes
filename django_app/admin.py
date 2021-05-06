from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .models import *


# from import_export.admin import ImportExportModelAdmin


# Register your models here.
admin.site.register(Classroom)
admin.site.register(Evenement)
admin.site.register(Matiere)
admin.site.register(ProfileUser)

# class MatiereResource(ImportExportModelAdmin):

#     class Meta:
#         model = Matiere
#         fields = ('id', 'name', 'price',)


# admin.site.register(Matiere,MatiereResource)
admin.site.register(SupportDeCours)
admin.site.register(TypeNote)
admin.site.register(Note)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id','username','first_name', 'last_name', 'email')

# class UserAdmin(ExportMixin, UserAdmin):
#     resource_class = UserResource
#     pass

class UserAdmin(ImportExportModelAdmin):
    list_display = ('id','username','first_name', 'last_name', 'email')
    list_filter = ('groups',)
    resource_class = UserResource
    pass



admin.site.unregister(User)
admin.site.register(User, UserAdmin)