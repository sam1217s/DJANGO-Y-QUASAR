from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para ViewSets de DRF
router = DefaultRouter()
router.register(r'cursos', views.CursoViewSet, basename='curso')
router.register(r'horarios', views.HorarioViewSet, basename='horario')  
router.register(r'materiales', views.MaterialViewSet, basename='material')
router.register(r'auth/users', views.UserViewSet, basename='user')  # Nuevo endpoint para usuarios

urlpatterns = [
    path('', include(router.urls)),
]

# Esto creará automáticamente estas URLs:
# /api/cursos/ - GET (listar), POST (crear)
# /api/cursos/{id}/ - GET (detalle), PUT (actualizar), DELETE (eliminar)
# /api/cursos/estadisticas/ - GET (estadísticas)
# /api/horarios/ - GET, POST  
# /api/horarios/{id}/ - GET, PUT, DELETE
# /api/materiales/ - GET, POST
# /api/materiales/{id}/ - GET, PUT, DELETE
# /api/auth/users/ - GET, POST (usuarios)
# /api/auth/users/{id}/ - GET, PUT, DELETE (usuario específico)
# /api/auth/users/estadisticas/ - GET (estadísticas de usuarios)