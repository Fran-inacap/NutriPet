from django.contrib import admin
from .models import Registro

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista principal
    list_display = ('nombre', 'especie', 'edad', 'alergeno', 'resultado', 'fecha', 'eliminado')
    
    # Filtros laterales
    list_filter = ('especie', 'eliminado', 'fecha')
    
    # Buscador por nombre de mascota
    search_fields = ('nombre',)
    
    # Campos que solo se pueden leer (para no alterar la fecha de borrado a mano)
    readonly_fields = ('fecha_eliminacion',)