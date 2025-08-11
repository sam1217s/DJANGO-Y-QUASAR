from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Curso(models.Model):
    """
    Modelo para representar un curso del SENA
    """
    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('mixta', 'Mixta'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre del curso")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código del curso")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    duracion_horas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Duración en horas"
    )
    modalidad = models.CharField(
        max_length=20,
        choices=MODALIDAD_CHOICES,
        default='presencial',
        verbose_name="Modalidad"
    )
    activo = models.BooleanField(default=True, verbose_name="Curso activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Horario(models.Model):
    """
    Modelo para representar horarios de cursos
    """
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    curso = models.ForeignKey(
        Curso, 
        on_delete=models.CASCADE, 
        related_name='horarios',
        verbose_name="Curso"
    )
    dia_semana = models.CharField(
        max_length=10,
        choices=DIAS_SEMANA,
        verbose_name="Día de la semana"
    )
    hora_inicio = models.TimeField(verbose_name="Hora de inicio")
    hora_fin = models.TimeField(verbose_name="Hora de fin")
    aula = models.CharField(max_length=50, blank=True, null=True, verbose_name="Aula")
    instructor = models.CharField(max_length=100, blank=True, null=True, verbose_name="Instructor")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        unique_together = ['curso', 'dia_semana', 'hora_inicio']
        ordering = ['dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.curso.codigo} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"

class Material(models.Model):
    """
    Modelo para representar materiales de estudio de cursos
    """
    TIPO_MATERIAL_CHOICES = [
        ('documento', 'Documento'),
        ('video', 'Video'),
        ('presentacion', 'Presentación'),
        ('enlace', 'Enlace'),
        ('imagen', 'Imagen'),
        ('otro', 'Otro'),
    ]
    
    curso = models.ForeignKey(
        Curso, 
        on_delete=models.CASCADE, 
        related_name='materiales',
        verbose_name="Curso"
    )
    nombre = models.CharField(max_length=200, verbose_name="Nombre del material")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    tipo_material = models.CharField(
        max_length=20,
        choices=TIPO_MATERIAL_CHOICES,
        default='documento',
        verbose_name="Tipo de material"
    )
    archivo = models.FileField(
        upload_to='materiales/',
        blank=True,
        null=True,
        verbose_name="Archivo"
    )
    enlace_externo = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enlace externo"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.curso.codigo} - {self.nombre}"