from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Curso, Horario, Material

class CursoSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para debugging
    """
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
            'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def validate_codigo(self, value):
        """Validar que el código sea único"""
        print(f"Validando código: {value}")  # Debug
        
        if self.instance:
            # Actualización: excluir la instancia actual
            exists = Curso.objects.exclude(id=self.instance.id).filter(codigo=value).exists()
            print(f"Código existe en actualización: {exists}")
            if exists:
                raise serializers.ValidationError("Ya existe un curso con este código.")
        else:
            # Creación: verificar que no exista
            exists = Curso.objects.filter(codigo=value).exists()
            print(f"Código existe en creación: {exists}")
            if exists:
                raise serializers.ValidationError("Ya existe un curso con este código.")
        return value
    
    def validate_duracion_horas(self, value):
        """Validar que la duración sea positiva"""
        print(f"Validando duración: {value}")  # Debug
        if value is None or value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0 horas.")
        return value

    def validate(self, data):
        """Validación general"""
        print(f"Datos recibidos: {data}")  # Debug
        return data

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

class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Material
    """
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    
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
            'enlace_externo',
            'fecha_creacion'
        ]
        read_only_fields = ['fecha_creacion']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User de Django
    """
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login'
        ]
        read_only_fields = ['date_joined', 'last_login']
    
    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Actualizar usuario, encriptando contraseña si se proporciona"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance