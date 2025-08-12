const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      // Dashboard principal
      {
        path: '',
        name: 'dashboard',
        component: () => import('pages/IndexPage.vue'),
        meta: { 
          title: 'Dashboard',
          icon: 'dashboard',
          requiresAuth: false // Cambiar a true cuando tengas autenticación
        }
      },
      
      // Gestión de Cursos
      {
        path: '/cursos',
        name: 'cursos',
        component: () => import('pages/CursosPage.vue'),
        meta: { 
          title: 'Cursos',
          icon: 'school',
          requiresAuth: false
        }
      },
      
      // Gestión de Horarios
      {
        path: '/horarios',
        name: 'horarios',
        component: () => import('pages/HorariosPage.vue'),
        meta: { 
          title: 'Horarios',
          icon: 'schedule',
          requiresAuth: false
        }
      },
      
      // Gestión de Materiales
      {
        path: '/materiales',
        name: 'materiales',
        component: () => import('pages/MaterialesPage.vue'),
        meta: { 
          title: 'Materiales',
          icon: 'folder',
          requiresAuth: false
        }
      },
      
      // Gestión de Usuarios
      {
        path: '/usuarios',
        name: 'usuarios',
        component: () => import('pages/UsuariosPage.vue'),
        meta: { 
          title: 'Usuarios',
          icon: 'people',
          requiresAuth: false // Cambiar a true y verificar permisos de admin
        }
      },
      
      // Páginas existentes (si las tienes)
      {
        path: '/asesoria',
        name: 'asesoria',
        component: () => import('pages/AsesoriaPage.vue'),
        meta: { 
          title: 'Asesoría',
          icon: 'support',
          requiresAuth: false
        }
      },
      
      {
        path: '/capacitacion',
        name: 'capacitacion',
        component: () => import('pages/CapacitacionPage.vue'),
        meta: { 
          title: 'Capacitación',
          icon: 'training',
          requiresAuth: false
        }
      }
    ]
  },

  // Página de error 404 - Siempre debe ir al final
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes