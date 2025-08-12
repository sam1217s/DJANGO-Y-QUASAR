<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Header con gradiente profesional -->
    <q-header elevated class="header-gradient">
      <q-toolbar class="text-white q-px-lg" style="height: 70px;">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          class="menu-toggle-btn"
          size="md"
        />

        <q-toolbar-title class="text-weight-bold q-ml-md">
          <div class="flex items-center">
            <q-icon name="school" class="q-mr-sm" size="28px" />
            <div>
              <div class="text-h5 text-weight-bold">Ambiente SENA</div>
              <div class="text-caption opacity-80">Sistema de Gestión Académica</div>
            </div>
          </div>
        </q-toolbar-title>

        <!-- Barra de búsqueda -->
        <div class="q-mx-lg" style="max-width: 300px; min-width: 200px;">
          <q-input
            v-model="searchText"
            outlined
            dense
            placeholder="Buscar..."
            bg-color="white"
            class="search-input"
          >
            <template v-slot:prepend>
              <q-icon name="search" color="grey-6" />
            </template>
          </q-input>
        </div>

        <!-- Información del usuario -->
        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn flat round dense icon="notifications" class="notification-btn">
            <q-badge color="red" floating rounded>2</q-badge>
            <q-tooltip class="text-body2">Notificaciones</q-tooltip>
          </q-btn>
          
          <q-btn flat round dense class="profile-btn">
            <q-avatar size="40px" class="profile-avatar">
              <img src="https://cdn.quasar.dev/img/avatar2.jpg" />
            </q-avatar>
            
            <q-menu class="profile-menu" transition-show="fade" transition-hide="fade">
              <q-list style="min-width: 220px" class="q-pa-sm">
                <q-item class="profile-header q-pa-md text-center">
                  <q-item-section>
                    <q-avatar size="50px" class="q-mb-sm">
                      <img src="https://cdn.quasar.dev/img/avatar2.jpg" />
                    </q-avatar>
                    <div class="text-weight-bold">Juan Pérez</div>
                    <div class="text-caption text-grey-6">Instructor</div>
                  </q-item-section>
                </q-item>
                
                <q-separator class="q-my-sm" />
                
                <q-item clickable v-ripple class="menu-item">
                  <q-item-section avatar>
                    <q-icon name="person" color="primary" />
                  </q-item-section>
                  <q-item-section>Mi Perfil</q-item-section>
                </q-item>
                
                <q-item clickable v-ripple class="menu-item">
                  <q-item-section avatar>
                    <q-icon name="settings" color="primary" />
                  </q-item-section>
                  <q-item-section>Configuración</q-item-section>
                </q-item>
                
                <q-separator class="q-my-sm" />
                
                <q-item clickable v-ripple @click="logout" class="menu-item logout-item">
                  <q-item-section avatar>
                    <q-icon name="logout" color="red-6" />
                  </q-item-section>
                  <q-item-section>Cerrar Sesión</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Área de hover para activar el sidebar -->
    <div 
      class="sidebar-hover-trigger"
      @mouseenter="openDrawerOnHover"
      @mouseleave="startCloseTimer"
      v-if="!leftDrawerOpen"
    ></div>

    <!-- Sidebar profesional con hover -->
    <q-drawer
      v-model="leftDrawerOpen"
      :show-if-above="false"
      :mini="false"
      bordered
      class="sidebar-drawer"
      :width="300"
      :breakpoint="500"
      behavior="desktop"
      @mouseenter="cancelCloseTimer"
      @mouseleave="closeDrawerOnLeave"
    >
      <q-scroll-area class="fit">
        <!-- Header del sidebar -->
        <div class="sidebar-header">
          <div class="logo-container">
            <q-icon name="school" size="3em" class="logo-icon" />
            <div class="text-h5 text-weight-bold text-white">SENA</div>
            <div class="text-caption text-white opacity-80">Sistema Académico</div>
          </div>
        </div>

        <!-- Navigation Menu -->
        <div class="navigation-container" style="padding: 16px;">
          <!-- Dashboard -->
          <div 
            class="nav-item nav-dashboard" 
            @click="navigateTo('dashboard')"
          >
            <q-icon name="dashboard" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Dashboard</div>
              <div class="nav-subtitle">Panel principal</div>
            </div>
            <q-icon name="chevron_right" class="nav-arrow" />
          </div>

          <!-- Separador -->
          <div class="nav-section">
            <q-icon name="school" />
            <span>Gestión Académica</span>
          </div>

          <!-- Cursos -->
          <div 
            class="nav-item nav-cursos" 
            @click="navigateTo('cursos')"
          >
            <q-icon name="school" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Cursos</div>
              <div class="nav-subtitle">Gestionar programas formativos</div>
            </div>
            <q-badge color="blue" :label="stats.cursos" class="nav-badge" />
          </div>

          <!-- Horarios -->
          <div 
            class="nav-item nav-horarios" 
            @click="navigateTo('horarios')"
          >
            <q-icon name="schedule" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Horarios</div>
              <div class="nav-subtitle">Programación de clases</div>
            </div>
            <q-badge color="green" :label="stats.horarios" class="nav-badge" />
          </div>

          <!-- Materiales -->
          <div 
            class="nav-item nav-materiales" 
            @click="navigateTo('materiales')"
          >
            <q-icon name="folder" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Materiales</div>
              <div class="nav-subtitle">Recursos de estudio</div>
            </div>
            <q-badge color="orange" :label="stats.materiales" class="nav-badge" />
          </div>

          <!-- Separador -->
          <div class="nav-section">
            <q-icon name="admin_panel_settings" />
            <span>Administración</span>
          </div>

          <!-- Usuarios -->
          <div 
            class="nav-item nav-usuarios" 
            @click="navigateTo('usuarios')"
          >
            <q-icon name="people" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Usuarios</div>
              <div class="nav-subtitle">Estudiantes e instructores</div>
            </div>
            <q-badge color="purple" :label="stats.usuarios" class="nav-badge" />
          </div>

          <!-- Separador -->
          <div class="nav-section">
            <q-icon name="business" />
            <span>Servicios</span>
          </div>

          <!-- Asesoría -->
          <div 
            class="nav-item nav-servicios" 
            @click="navigateTo('asesoria')"
            v-if="$route.matched.some(route => route.name === 'asesoria')"
          >
            <q-icon name="support" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Asesoría</div>
              <div class="nav-subtitle">Apoyo académico</div>
            </div>
          </div>

          <!-- Capacitación -->
          <div 
            class="nav-item nav-servicios" 
            @click="navigateTo('capacitacion')"
            v-if="$route.matched.some(route => route.name === 'capacitacion')"
          >
            <q-icon name="trending_up" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Capacitación</div>
              <div class="nav-subtitle">Formación continua</div>
            </div>
          </div>

          <!-- Separador -->
          <div class="nav-section">
            <q-icon name="link" />
            <span>Enlaces</span>
          </div>

          <!-- Portal SENA -->
          <div 
            class="nav-item nav-enlaces" 
            @click="openExternalLink('https://www.sena.edu.co')"
          >
            <q-icon name="open_in_new" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Portal SENA</div>
              <div class="nav-subtitle">Sitio web oficial</div>
            </div>
          </div>

          <!-- Acerca de -->
          <div 
            class="nav-item nav-enlaces" 
            @click="showAbout"
          >
            <q-icon name="info" class="nav-icon" />
            <div class="nav-content">
              <div class="nav-title">Acerca de</div>
              <div class="nav-subtitle">Información del sistema</div>
            </div>
          </div>
        </div>
      </q-scroll-area>
    </q-drawer>

    <!-- Overlay difuminado cuando el drawer está abierto (solo cubre el contenido) -->
    <transition name="fade">
      <div 
        v-if="leftDrawerOpen"
        class="content-overlay"
        @click="leftDrawerOpen = false"
      ></div>
    </transition>

    <q-page-container :class="{ 'content-blurred': leftDrawerOpen }">
      <router-view />
    </q-page-container>

    <!-- Footer profesional -->
    <q-footer class="footer-gradient text-white" :class="{ 'content-blurred': leftDrawerOpen }">
      <q-toolbar class="q-px-lg">
        <q-toolbar-title class="text-center">
          <div class="footer-content">
            <span class="text-body2">© 2025 SENA - Sistema de Gestión Académica</span>
            <span class="footer-separator">|</span>
            <a href="#" class="footer-link">Soporte Técnico</a>
            <span class="footer-separator">|</span>
            <a href="#" class="footer-link">Política de Privacidad</a>
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'
import { api } from 'boot/axios'
import { Dialog, Notify } from 'quasar'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'MainLayout',
  setup() {
    const router = useRouter()
    const leftDrawerOpen = ref(false)
    const searchText = ref('')
    const closeTimer = ref(null)
    const openTimer = ref(null)
    const drawerBehavior = ref('desktop')
    
    const stats = ref({
      cursos: 12,
      horarios: 8,
      materiales: 24,
      usuarios: 156
    })

    // Control del drawer con hover
    const openDrawerOnHover = () => {
      // Cancelar cualquier timer de cierre existente
      if (closeTimer.value) {
        clearTimeout(closeTimer.value)
        closeTimer.value = null
      }
      
      // Abrir el drawer inmediatamente con un pequeño delay
      openTimer.value = setTimeout(() => {
        leftDrawerOpen.value = true
      }, 100) // Reducido para una respuesta más rápida
    }

    const closeDrawerOnLeave = () => {
      // Cancelar cualquier timer de apertura
      if (openTimer.value) {
        clearTimeout(openTimer.value)
        openTimer.value = null
      }
      
      // Cerrar el drawer con un delay para permitir mover el cursor
      closeTimer.value = setTimeout(() => {
        leftDrawerOpen.value = false
      }, 400)
    }

    const startCloseTimer = () => {
      // Cancelar timer de apertura si existe
      if (openTimer.value) {
        clearTimeout(openTimer.value)
        openTimer.value = null
      }
      
      // Iniciar timer de cierre con más delay
      closeTimer.value = setTimeout(() => {
        leftDrawerOpen.value = false
      }, 600)
    }

    const cancelCloseTimer = () => {
      if (closeTimer.value) {
        clearTimeout(closeTimer.value)
        closeTimer.value = null
      }
    }

    // Toggle manual del drawer
    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }

    // Navegación
    const navigateTo = (routeName) => {
      router.push({ name: routeName })
      // Cerrar el drawer después de navegar
      setTimeout(() => {
        leftDrawerOpen.value = false
      }, 100)
    }

    // Logout
    const logout = () => {
      Dialog.create({
        title: 'Cerrar Sesión',
        message: '¿Estás seguro de que quieres cerrar sesión?',
        cancel: {
          label: 'Cancelar',
          color: 'grey',
          flat: true
        },
        ok: {
          label: 'Sí, cerrar sesión',
          color: 'negative'
        },
        persistent: true
      }).onOk(() => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        
        Notify.create({
          type: 'positive',
          message: 'Sesión cerrada exitosamente',
          position: 'top-right',
          timeout: 3000,
          actions: [
            { icon: 'close', color: 'white', round: true }
          ]
        })
        
        // router.push('/login')
      })
    }

    const openExternalLink = (url) => {
      window.open(url, '_blank')
      leftDrawerOpen.value = false
    }

    const showAbout = () => {
      leftDrawerOpen.value = false
      Dialog.create({
        title: 'Acerca del Sistema',
        message: `
          <div class="q-pa-md">
            <div class="text-center q-mb-md">
              <q-icon name="school" size="64px" color="primary" />
            </div>
            <h6 class="q-ma-none q-mb-sm text-center">Sistema de Gestión Académica SENA</h6>
            <div class="q-mb-md">
              <p><strong>Versión:</strong> 1.0.0</p>
              <p><strong>Última actualización:</strong> Agosto 2025</p>
            </div>
            <p><strong>Tecnologías utilizadas:</strong></p>
            <ul class="q-pl-md">
              <li>Frontend: Vue.js 3 + Quasar Framework</li>
              <li>Backend: Django + Django REST Framework</li>
              <li>Base de datos: MySQL</li>
              <li>Autenticación: JWT</li>
            </ul>
            <p><strong>Características:</strong></p>
            <ul class="q-pl-md">
              <li>Gestión integral de cursos y programas formativos</li>
              <li>Administración de horarios y recursos</li>
              <li>Sistema de usuarios con roles diferenciados</li>
              <li>Interfaz responsiva y moderna</li>
            </ul>
            <div class="text-center q-mt-md">
              <p class="text-caption text-grey-6">Desarrollado para optimizar la gestión académica del SENA</p>
            </div>
          </div>
        `,
        html: true,
        ok: {
          label: 'Entendido',
          color: 'primary'
        }
      })
    }

    // Cargar estadísticas
    const loadMenuStats = async () => {
      try {
        const [cursosRes, horariosRes, materialesRes] = await Promise.all([
          api.get('cursos/').catch(() => ({ data: [] })),
          api.get('horarios/').catch(() => ({ data: [] })),
          api.get('materiales/').catch(() => ({ data: [] }))
        ])

        stats.value = {
          cursos: (cursosRes.data.results || cursosRes.data || []).length || 12,
          horarios: (horariosRes.data.results || horariosRes.data || []).length || 8,
          materiales: (materialesRes.data.results || materialesRes.data || []).length || 24,
          usuarios: 156
        }
      } catch (error) {
        console.error('Error al cargar estadísticas del menú:', error)
      }
    }

    // Limpiar timers al destruir el componente
    onUnmounted(() => {
      if (closeTimer.value) clearTimeout(closeTimer.value)
      if (openTimer.value) clearTimeout(openTimer.value)
    })

    onMounted(() => {
      loadMenuStats()
    })

    return {
      leftDrawerOpen,
      searchText,
      stats,
      drawerBehavior,
      toggleLeftDrawer,
      openDrawerOnHover,
      closeDrawerOnLeave,
      startCloseTimer,
      cancelCloseTimer,
      navigateTo,
      logout,
      openExternalLink,
      showAbout
    }
  }
})
</script>

<style lang="scss" scoped>
// Área de hover para activar el sidebar
.sidebar-hover-trigger {
  position: fixed;
  top: 70px; // Debajo del header
  left: 0;
  width: 15px; // Área estrecha para detectar hover
  height: calc(100vh - 70px); // Alto completo menos header
  z-index: 1999; // Debajo del drawer pero encima del contenido
  cursor: pointer;
  background: transparent;
  transition: all 0.3s ease;
  
  &:hover {
    background: linear-gradient(90deg, rgba(25, 118, 210, 0.2) 0%, transparent 100%);
    width: 25px;
  }
}

// Overlay difuminado
.content-overlay {
  position: fixed;
  top: 70px;
  left: 300px; // Empieza donde termina el sidebar
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  z-index: 1998;
  animation: fadeIn 0.3s ease;
  cursor: pointer;
  transition: all 0.3s ease;
}

// Contenido difuminado
.content-blurred {
  filter: blur(2px) brightness(0.9);
  transition: all 0.3s ease;
  pointer-events: none;
  user-select: none;
  opacity: 0.8;
}

// Animaciones
@keyframes fadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(3px);
  }
}

// Transición fade para el overlay
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

// Gradientes profesionales
.header-gradient {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 50%, #0d47a1 100%);
  box-shadow: 0 4px 20px rgba(25, 118, 210, 0.3);
  z-index: 3000; // Asegurar que el header esté siempre encima
}

.footer-gradient {
  background: linear-gradient(135deg, #37474f 0%, #263238 100%);
}

.sidebar-drawer {
  background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
  border-right: 1px solid #e0e0e0;
  z-index: 2000 !important;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
  
  ::v-deep(.q-drawer__content) {
    background: transparent;
  }
}

// Header styles
.menu-toggle-btn {
  transition: all 0.3s ease;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transform: scale(1.05);
  }
}

.search-input {
  border-radius: 25px;
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
  }
  
  &:focus-within {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3);
  }
  
  ::v-deep(.q-field__control) {
    border-radius: 25px;
    height: 40px;
  }
}

.notification-btn, .profile-btn {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 50%;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.15);
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  }
  
  &:active {
    transform: scale(0.95);
  }
}

.profile-avatar {
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  
  &:hover {
    border-color: rgba(255, 255, 255, 0.8);
  }
}

// Sidebar header
.sidebar-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 50%, #0d47a1 100%);
  padding: 2rem 1.5rem;
  text-align: center;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  
  &:hover {
    background: linear-gradient(135deg, #2196f3 0%, #1976d2 50%, #1565c0 100%);
  }
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  }
}

.logo-container {
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.05);
    
    .logo-icon {
      transform: scale(1.1) rotate(10deg);
      background: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.4);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
  }
  
  .logo-icon {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    padding: 12px;
    margin-bottom: 8px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    color: white;
  }
}

// Navegación mejorada
.navigation-container {
  padding: 16px;
  background: white;
  min-height: calc(100vh - 200px);
  
  .nav-item {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    margin: 4px 0;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent;
    border-left: 4px solid transparent;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(25, 118, 210, 0.08), transparent);
      transition: left 0.5s ease;
    }
    
    .nav-icon {
      font-size: 24px;
      color: #546e7a;
      margin-right: 16px;
      transition: all 0.3s ease;
    }
    
    .nav-content {
      flex: 1;
      
      .nav-title {
        font-size: 15px;
        font-weight: 500;
        color: #37474f;
        transition: all 0.3s ease;
      }
      
      .nav-subtitle {
        font-size: 12px;
        color: #78909c;
        margin-top: 2px;
        transition: all 0.3s ease;
      }
    }
    
    .nav-arrow {
      font-size: 18px;
      color: #b0bec5;
      opacity: 0.6;
      transition: all 0.3s ease;
    }
    
    .nav-badge {
      transition: all 0.3s ease;
      font-weight: 600;
    }
    
    &:hover {
      background-color: #f0f7ff;
      transform: translateX(8px);
      box-shadow: 0 4px 12px rgba(25, 118, 210, 0.15);
      
      &::before {
        left: 100%;
      }
      
      .nav-icon {
        color: #1976d2;
        transform: scale(1.1) rotate(5deg);
      }
      
      .nav-title {
        color: #1976d2;
        font-weight: 600;
      }
      
      .nav-subtitle {
        color: #1976d2;
      }
      
      .nav-arrow {
        color: #1976d2;
        opacity: 1;
        transform: translateX(4px);
      }
      
      .nav-badge {
        transform: scale(1.1);
      }
    }
    
    // Colores específicos por sección
    &.nav-dashboard:hover {
      border-left-color: #1976d2;
      background-color: #e3f2fd;
      
      .nav-icon, .nav-title, .nav-subtitle {
        color: #1976d2;
      }
    }
    
    &.nav-cursos:hover {
      border-left-color: #2196f3;
      background-color: #e1f5fe;
      
      .nav-icon, .nav-title, .nav-subtitle {
        color: #2196f3;
      }
    }
    
    &.nav-horarios:hover {
      border-left-color: #4caf50;
      background-color: #e8f5e9;
      
      .nav-icon, .nav-title, .nav-subtitle {
        color: #4caf50;
      }
    }
    
    &.nav-materiales:hover {
      border-left-color: #ff9800;
      background-color: #fff3e0;
      
      .nav-icon, .nav-title, .nav-subtitle {
        color: #ff9800;
      }
    }
    
    &.nav-usuarios:hover {
      border-left-color: #9c27b0;
      background-color: #f3e5f5;
      
      .nav-icon, .nav-title, .nav-subtitle {
        color: #9c27b0;
      }
    }
    
    &.nav-servicios:hover {
      border-left-color: #607d8b;
      background-color: #eceff1;
      
      .nav-icon, .nav-title, .nav-subtitle {
        color: #607d8b;
      }
    }
    
    &.nav-enlaces:hover {
      border-left-color: #795548;
      background-color: #efebe9;
      
      .nav-icon, .nav-title, .nav-subtitle {
        color: #795548;
      }
    }
  }
  
  .nav-section {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    margin: 20px 0 12px 0;
    font-size: 12px;
    font-weight: 700;
    color: #1976d2;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.9;
    transition: all 0.3s ease;
    border-bottom: 1px solid rgba(25, 118, 210, 0.1);
    padding-bottom: 8px;
    
    &:hover {
      opacity: 1;
      transform: translateX(4px);
    }
    
    .q-icon {
      margin-right: 8px;
      font-size: 16px;
      color: #1976d2;
    }
  }
}

// Profile menu
.profile-menu {
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(0, 0, 0, 0.05);
  
  .profile-header {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 8px;
    margin-bottom: 8px;
    transition: all 0.3s ease;
    cursor: pointer;
    
    &:hover {
      background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
      transform: scale(1.02);
    }
  }
  
  .menu-item {
    border-radius: 8px;
    margin: 2px 4px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    
    &:hover {
      background-color: rgba(25, 118, 210, 0.12);
      transform: translateX(8px) scale(1.02);
      box-shadow: 0 4px 12px rgba(25, 118, 210, 0.15);
      
      .q-icon {
        transform: scale(1.2) rotate(10deg);
      }
      
      ::v-deep(.q-item__section) {
        color: #1976d2;
        font-weight: 600;
      }
    }
    
    &.logout-item:hover {
      background-color: rgba(244, 67, 54, 0.12);
      
      .q-icon {
        color: #f44336;
        transform: scale(1.2) rotate(-10deg);
      }
      
      ::v-deep(.q-item__section) {
        color: #f44336;
      }
    }
  }
}

// Footer
.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  
  .footer-separator {
    opacity: 0.6;
  }
  
  .footer-link {
    color: white;
    text-decoration: none;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 4px 8px;
    border-radius: 4px;
    
    &:hover {
      color: #64b5f6;
      text-decoration: underline;
      background-color: rgba(255, 255, 255, 0.1);
      transform: scale(1.05) translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
  }
}

// Responsive
@media (max-width: 768px) {
  .sidebar-hover-trigger {
    display: none;
  }
  
  .search-input {
    display: none;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 8px;
    
    .footer-separator {
      display: none;
    }
  }
}
</style>