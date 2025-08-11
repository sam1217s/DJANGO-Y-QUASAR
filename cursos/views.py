from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny  # Temporal para pruebas
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Curso, Horario, Material
from .serializers import CursoSerializer, HorarioSerializer, MaterialSerializer

class CursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cursos
    Proporciona operaciones CRUD completas
    """
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [AllowAny]  # Temporal para pruebas
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['modalidad', 'activo']
    search_fields = ['nombre', 'codigo', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['-fecha_creacion']

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas de cursos
        URL: /api/cursos/estadisticas/
        """
        # Contadores básicos
        total_cursos = Curso.objects.count()
        cursos_activos = Curso.objects.filter(activo=True).count()
        cursos_inactivos = total_cursos - cursos_activos
        
        # Estadísticas por modalidad
        modalidades = Curso.objects.values('modalidad').annotate(
            count=Count('id')
        ).order_by('modalidad')
        
        # Horas totales
        total_horas = sum(curso.duracion_horas for curso in Curso.objects.all())
        
        # Cursos más recientes (últimos 5)
        cursos_recientes = Curso.objects.order_by('-fecha_creacion')[:5]
        cursos_recientes_data = CursoSerializer(cursos_recientes, many=True).data
        
        estadisticas = {
            'resumen': {
                'total_cursos': total_cursos,
                'cursos_activos': cursos_activos,
                'cursos_inactivos': cursos_inactivos,
                'total_horas_formacion': total_horas,
            },
            'por_modalidad': list(modalidades),
            'cursos_recientes': cursos_recientes_data,
        }
        
        return Response(estadisticas)

class HorarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar horarios de cursos
    """
    queryset = Horario.objects.select_related('curso')
    serializer_class = HorarioSerializer
    permission_classes = [AllowAny]  # Temporal para pruebas
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['curso', 'dia_semana']

class MaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar materiales de cursos
    """
    queryset = Material.objects.select_related('curso')
    serializer_class = MaterialSerializer
    permission_classes = [AllowAny]  # Temporal para pruebas
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['curso', 'tipo_material']