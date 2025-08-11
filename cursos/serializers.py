from rest_framework import serializers
from .models import Curso, Horario, Material

class CursoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Curso
    Convierte entre objetos Python y JSON
    """
    # Campos calculados (solo lectura)
    total_horarios = serializers.SerializerMethodField()
    total_materiales = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = [
            'id',
            'nombre',
            'codigo',
            'descripcion',
            'duracion_horas',
            'modalidad',
            'activo',
            'fecha_creacion',
            'fecha_actualizacion',
            'total_horarios',
            'total_materiales'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_total_horarios(self, obj):
        """Obtener número total de horarios del curso"""
        return obj.horarios.count()
    
    def get_total_materiales(self, obj):
        """Obtener número total de materiales del curso"""
        return obj.materiales.count()
    
    def validate_codigo(self, value):
        """Validar que el código sea único"""
        if self.instance:
            # Actualización: excluir la instancia actual
            if Curso.objects.exclude(id=self.instance.id).filter(codigo=value).exists():
                raise serializers.ValidationError("Ya existe un curso con este código.")
        else:
            # Creación: verificar que no exista
            if Curso.objects.filter(codigo=value).exists():
                raise serializers.ValidationError("Ya existe un curso con este código.")
        return value
    
    def validate_duracion_horas(self, value):
        """Validar que la duración sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0 horas.")
        return value

class HorarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Horario
    """
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    
    class Meta:
        model = Horario
        fields = [
            'id',
            'curso',
            'curso_nombre',
            'dia_semana',
            'hora_inicio',
            'hora_fin',
            'aula',
            'instructor',
            'fecha_creacion'
        ]
        read_only_fields = ['fecha_creacion']
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')
        
        if hora_inicio and hora_fin:
            if hora_inicio >= hora_fin:
                raise serializers.ValidationError(
                    "La hora de inicio debe ser anterior a la hora de fin."
                )
        
        return data

class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Material
    """
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    archivo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Material
        fields = [
            'id',
            'curso',
            'curso_nombre',
            'nombre',
            'descripcion',
            'tipo_material',
            'archivo',
            'archivo_url',
            'enlace_externo',
            'fecha_creacion'
        ]
        read_only_fields = ['fecha_creacion']
    
    def get_archivo_url(self, obj):
        """Obtener URL completa del archivo"""
        if obj.archivo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.archivo.url)
            return obj.archivo.url
        return None
    
    def validate(self, data):
        """Validar que tenga archivo o enlace externo"""
        archivo = data.get('archivo')
        enlace_externo = data.get('enlace_externo')
        
        if not archivo and not enlace_externo:
            raise serializers.ValidationError(
                "Debe proporcionar un archivo o un enlace externo."
            )
        
        return data

# Serializers adicionales para casos específicos

class CursoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar cursos
    Más eficiente para listas grandes
    """
    class Meta:
        model = Curso
        fields = [
            'id',
            'nombre',
            'codigo',
            'modalidad',
            'duracion_horas',
            'activo',
            'fecha_creacion'
        ]

class CursoDetailSerializer(CursoSerializer):
    """
    Serializer detallado para curso individual
    Incluye horarios y materiales relacionados
    """
    horarios = HorarioSerializer(many=True, read_only=True)
    materiales = MaterialSerializer(many=True, read_only=True)
    
    class Meta(CursoSerializer.Meta):
        fields = CursoSerializer.Meta.fields + ['horarios', 'materiales']