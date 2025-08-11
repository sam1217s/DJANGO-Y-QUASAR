from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para ViewSets de DRF
router = DefaultRouter()
router.register(r'cursos', views.CursoViewSet, basename='curso')
router.register(r'horarios', views.HorarioViewSet, basename='horario')  
router.register(r'materiales', views.MaterialViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
]

# Esto creará automáticamente estas URLs:
# /api/cursos/ - GET (listar), POST (crear)
# /api/cursos/{id}/ - GET (detalle), PUT (actualizar), DELETE (eliminar)
# /api/horarios/ - GET, POST  
# /api/horarios/{id}/ - GET, PUT, DELETE
# /api/materiales/ - GET, POST
# /api/materiales/{id}/ - GET, PUT, DELETE