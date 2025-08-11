from django.contrib import admin
from .models import Curso, Horario, Material

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'modalidad', 'duracion_horas', 'activo', 'fecha_creacion']
    list_filter = ['modalidad', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'codigo', 'descripcion']
    list_editable = ['activo']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('modalidad', 'duracion_horas', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['curso', 'dia_semana', 'hora_inicio', 'hora_fin', 'aula', 'instructor']
    list_filter = ['dia_semana', 'curso']
    search_fields = ['curso__nombre', 'curso__codigo', 'aula', 'instructor']
    ordering = ['curso', 'dia_semana', 'hora_inicio']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'curso', 'tipo_material', 'fecha_creacion']
    list_filter = ['tipo_material', 'curso', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'curso__nombre']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion']