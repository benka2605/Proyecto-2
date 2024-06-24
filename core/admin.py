from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from admin_confirm import AdminConfirmMixin


# Register your models here.

class PeriodistaAdmin(AdminConfirmMixin,admin.ModelAdmin):
    confirm_change=True
    confirmation_fields = ['usuario','nombre','apellido','genero','plan']

class NoticiaAdmin(AdminConfirmMixin,admin.ModelAdmin):
    confirm_change=True
    confirmation_fields = ['titulo','descripcion','periodista','fecha_noticia','ubicacion']

class GeneroAdmin(AdminConfirmMixin,admin.ModelAdmin):
    confirm_change=True
    confirmation_fields = ['descripcion']

class CategoriaAdmin(AdminConfirmMixin,admin.ModelAdmin):
    confirm_change=True
    confirmation_fields = ['name']

admin.site.register(Periodista,PeriodistaAdmin)
admin.site.register(Genero,GeneroAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Noticia,NoticiaAdmin)
admin.site.register(Imagen)
admin.site.register(Plan)
admin.site.register(Voucher)
