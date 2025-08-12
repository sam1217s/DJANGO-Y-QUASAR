<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="bg-primary text-white">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title class="text-weight-bold">
          <q-icon name="school" class="q-mr-sm" />
          Ambiente SENA
        </q-toolbar-title>

        <!-- Información del usuario -->
        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn flat round dense icon="notifications">
            <q-badge color="red" floating>2</q-badge>
            <q-tooltip>Notificaciones</q-tooltip>
          </q-btn>
          
          <q-btn flat round dense>
            <q-avatar size="32px">
              <img src="https://cdn.quasar.dev/img/avatar2.jpg" />
            </q-avatar>
            
            <q-menu>
              <q-list style="min-width: 200px">
                <q-item clickable>
                  <q-item-section avatar>
                    <q-icon name="person" />
                  </q-item-section>
                  <q-item-section>Mi Perfil</q-item-section>
                </q-item>
                
                <q-item clickable>
                  <q-item-section avatar>
                    <q-icon name="settings" />
                  </q-item-section>
                  <q-item-section>Configuración</q-item-section>
                </q-item>
                
                <q-separator />
                
                <q-item clickable @click="logout">
                  <q-item-section avatar>
                    <q-icon name="logout" />
                  </q-item-section>
                  <q-item-section>Cerrar Sesión</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-1"
      :width="280"
    >
      <q-scroll-area class="fit">
        <!-- Logo/Header del drawer -->
        <div class="q-pa-md text-center bg-primary text-white">
          <q-icon name="school" size="2em" class="q-mb-sm" />
          <div class="text-h6 text-weight-bold">SENA</div>
          <div class="text-caption">Sistema Académico</div>
        </div>

        <!-- Lista de navegación -->
        <q-list padding>
          <!-- Dashboard -->
          <q-item 
            clickable 
            v-ripple 
            :to="{ name: 'dashboard' }"
            exact-active-class="bg-blue-1 text-primary"
          >
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Dashboard</q-item-label>
              <q-item-label caption>Panel principal</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Separador -->
          <q-separator class="q-my-md" />
          
          <!-- Sección: Gestión Académica -->
          <q-item-label header class="text-weight-bold text-primary">
            <q-icon name="school" class="q-mr-sm" />
            Gestión Académica
          </q-item-label>

          <!-- Cursos -->
          <q-item 
            clickable 
            v-ripple 
            :to="{ name: 'cursos' }"
            active-class="bg-blue-1 text-primary"
          >
            <q-item-section avatar>
              <q-icon name="school" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Cursos</q-item-label>
              <q-item-label caption>Gestionar programas formativos</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-badge color="primary" :label="stats.cursos" />
            </q-item-section>
          </q-item>

          <!-- Horarios -->
          <q-item 
            clickable 
            v-ripple 
            :to="{ name: 'horarios' }"
            active-class="bg-green-1 text-primary"
          >
            <q-item-section avatar>
              <q-icon name="schedule" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Horarios</q-item-label>
              <q-item-label caption>Programación de clases</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-badge color="green" :label="stats.horarios" />
            </q-item-section>
          </q-item>

          <!-- Materiales -->
          <q-item 
            clickable 
            v-ripple 
            :to="{ name: 'materiales' }"
            active-class="bg-orange-1 text-primary"
          >
            <q-item-section avatar>
              <q-icon name="folder" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Materiales</q-item-label>
              <q-item-label caption>Recursos de estudio</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-badge color="orange" :label="stats.materiales" />
            </q-item-section>
          </q-item>

          <!-- Separador -->
          <q-separator class="q-my-md" />
          
          <!-- Sección: Administración -->
          <q-item-label header class="text-weight-bold text-primary">
            <q-icon name="admin_panel_settings" class="q-mr-sm" />
            Administración
          </q-item-label>

          <!-- Usuarios -->
          <q-item 
            clickable 
            v-ripple 
            :to="{ name: 'usuarios' }"
            active-class="bg-purple-1 text-primary"
          >
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Usuarios</q-item-label>
              <q-item-label caption>Estudiantes e instructores</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-badge color="purple" :label="stats.usuarios" />
            </q-item-section>
          </q-item>

          <!-- Separador -->
          <q-separator class="q-my-md" />
          
          <!-- Sección: Servicios (si existen otras páginas) -->
          <q-item-label header class="text-weight-bold text-primary">
            <q-icon name="business" class="q-mr-sm" />
            Servicios
          </q-item-label>

          <!-- Asesoría -->
          <q-item 
            clickable 
            v-ripple 
            :to="{ name: 'asesoria' }"
            active-class="bg-cyan-1 text-primary"
            v-if="$route.matched.some(route => route.name === 'asesoria')"
          >
            <q-item-section avatar>
              <q-icon name="support" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Asesoría</q-item-label>
              <q-item-label caption>Apoyo académico</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Capacitación -->
          <q-item 
            clickable 
            v-ripple 
            :to="{ name: 'capacitacion' }"
            active-class="bg-pink-1 text-primary"
            v-if="$route.matched.some(route => route.name === 'capacitacion')"
          >
            <q-item-section avatar>
              <q-icon name="trending_up" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Capacitación</q-item-label>
              <q-item-label caption>Formación continua</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Separador final -->
          <q-separator class="q-my-md" />
          
          <!-- Enlaces adicionales -->
          <q-item 
            clickable 
            v-ripple 
            @click="openExternalLink('https://www.sena.edu.co')"
          >
            <q-item-section avatar>
              <q-icon name="open_in_new" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Portal SENA</q-item-label>
              <q-item-label caption>Sitio web oficial</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Acerca de -->
          <q-item 
            clickable 
            v-ripple 
            @click="showAbout"
          >
            <q-item-section avatar>
              <q-icon name="info" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Acerca de</q-item-label>
              <q-item-label caption>Información del sistema</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer opcional -->
    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title class="text-center">
          <div class="text-caption">
            © 2025 SENA - Sistema de Gestión Académica | 
            <a href="#" class="text-white">Soporte Técnico</a>
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { Dialog, Notify } from 'quasar'

export default defineComponent({
  name: 'MainLayout',
  setup() {
    const leftDrawerOpen = ref(false)
    const stats = ref({
      cursos: 0,
      horarios: 0,
      materiales: 0,
      usuarios: 0
    })

    // Métodos
    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }

    const logout = () => {
      Dialog.create({
        title: 'Cerrar Sesión',
        message: '¿Estás seguro de que quieres cerrar sesión?',
        cancel: true,
        persistent: true
      }).onOk(() => {
        // Limpiar tokens de autenticación
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        
        Notify.create({
          type: 'positive',
          message: 'Sesión cerrada exitosamente',
          position: 'top'
        })
        
        // Redirigir al login (cuando lo implementes)
        // this.$router.push('/login')
      })
    }

    const openExternalLink = (url) => {
      window.open(url, '_blank')
    }

    const showAbout = () => {
      Dialog.create({
        title: 'Acerca del Sistema',
        message: `
          <div class="q-pa-md">
            <h6 class="q-ma-none q-mb-sm">Sistema de Gestión Académica SENA</h6>
            <p><strong>Versión:</strong> 1.0.0</p>
            <p><strong>Tecnologías:</strong></p>
            <ul>
              <li>Frontend: Vue.js 3 + Quasar Framework</li>
              <li>Backend: Django + Django REST Framework</li>
              <li>Base de datos: MySQL</li>
            </ul>
            <p><strong>Desarrollado para:</strong> Gestión integral de cursos, horarios, materiales y usuarios del ambiente SENA.</p>
          </div>
        `,
        html: true,
        ok: {
          label: 'Entendido',
          color: 'primary'
        }
      })
    }

    // Cargar estadísticas para los badges del menú
    const loadMenuStats = async () => {
      try {
        const [cursosRes, horariosRes, materialesRes] = await Promise.all([
          api.get('cursos/').catch(() => ({ data: [] })),
          api.get('horarios/').catch(() => ({ data: [] })),
          api.get('materiales/').catch(() => ({ data: [] }))
        ])

        stats.value = {
          cursos: (cursosRes.data.results || cursosRes.data || []).length,
          horarios: (horariosRes.data.results || horariosRes.data || []).length,
          materiales: (materialesRes.data.results || materialesRes.data || []).length,
          usuarios: 25 // Placeholder - conectar con API real cuando esté disponible
        }
      } catch (error) {
        console.error('Error al cargar estadísticas del menú:', error)
      }
    }

    // Inicialización
    onMounted(() => {
      loadMenuStats()
    })

    return {
      leftDrawerOpen,
      stats,
      toggleLeftDrawer,
      logout,
      openExternalLink,
      showAbout
    }
  }
})
</script>

<style lang="scss" scoped>
.q-item {
  border-radius: 8px;
  margin: 2px 8px;
  
  &:hover {
    background-color: rgba(25, 118, 210, 0.04);
  }
}

.q-drawer {
  .q-item--active {
    color: var(--q-primary);
    font-weight: 600;
  }
}

.q-footer {
  .text-caption a {
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>