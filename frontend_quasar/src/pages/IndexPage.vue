<template>
  <q-page class="q-pa-md">
    <!-- Header del Dashboard -->
    <div class="q-mb-xl">
      <h3 class="q-ma-none text-primary">Dashboard - Ambiente SENA</h3>
      <p class="text-grey-6 q-mt-sm">
        Panel de control principal del sistema de gestión académica
      </p>
    </div>

    <!-- Loading inicial -->
    <div v-if="loading" class="text-center q-py-xl">
      <q-spinner color="primary" size="3em" />
      <p class="q-mt-md">Cargando datos del dashboard...</p>
    </div>

    <!-- Contenido del Dashboard -->
    <div v-else>
      <!-- Estadísticas principales -->
      <div class="row q-gutter-lg q-mb-xl">
        <!-- Estadística de Cursos -->
        <div class="col-12 col-md-6 col-lg-3">
          <q-card class="dashboard-card bg-gradient-blue">
            <q-card-section class="text-white">
              <div class="row items-center">
                <div class="col">
                  <div class="text-h4 text-weight-bold">{{ stats.cursos.total }}</div>
                  <div class="text-subtitle1">Cursos Totales</div>
                  <div class="text-caption">
                    {{ stats.cursos.activos }} activos
                  </div>
                </div>
                <div class="col-auto">
                  <q-icon name="school" size="3rem" class="opacity-60" />
                </div>
              </div>
            </q-card-section>
            <q-card-section class="bg-white bg-opacity-10">
              <q-btn 
                flat 
                color="white" 
                label="Ver cursos" 
                icon-right="arrow_forward"
                to="/cursos"
                class="full-width"
              />
            </q-card-section>
          </q-card>
        </div>

        <!-- Estadística de Horarios -->
        <div class="col-12 col-md-6 col-lg-3">
          <q-card class="dashboard-card bg-gradient-green">
            <q-card-section class="text-white">
              <div class="row items-center">
                <div class="col">
                  <div class="text-h4 text-weight-bold">{{ stats.horarios.total }}</div>
                  <div class="text-subtitle1">Horarios</div>
                  <div class="text-caption">
                    {{ stats.horarios.esta_semana }} esta semana
                  </div>
                </div>
                <div class="col-auto">
                  <q-icon name="schedule" size="3rem" class="opacity-60" />
                </div>
              </div>
            </q-card-section>
            <q-card-section class="bg-white bg-opacity-10">
              <q-btn 
                flat 
                color="white" 
                label="Ver horarios" 
                icon-right="arrow_forward"
                to="/horarios"
                class="full-width"
              />
            </q-card-section>
          </q-card>
        </div>

        <!-- Estadística de Materiales -->
        <div class="col-12 col-md-6 col-lg-3">
          <q-card class="dashboard-card bg-gradient-orange">
            <q-card-section class="text-white">
              <div class="row items-center">
                <div class="col">
                  <div class="text-h4 text-weight-bold">{{ stats.materiales.total }}</div>
                  <div class="text-subtitle1">Materiales</div>
                  <div class="text-caption">
                    {{ stats.materiales.documentos }} documentos
                  </div>
                </div>
                <div class="col-auto">
                  <q-icon name="folder" size="3rem" class="opacity-60" />
                </div>
              </div>
            </q-card-section>
            <q-card-section class="bg-white bg-opacity-10">
              <q-btn 
                flat 
                color="white" 
                label="Ver materiales" 
                icon-right="arrow_forward"
                to="/materiales"
                class="full-width"
              />
            </q-card-section>
          </q-card>
        </div>

        <!-- Estadística de Usuarios -->
        <div class="col-12 col-md-6 col-lg-3">
          <q-card class="dashboard-card bg-gradient-purple">
            <q-card-section class="text-white">
              <div class="row items-center">
                <div class="col">
                  <div class="text-h4 text-weight-bold">{{ stats.usuarios.total }}</div>
                  <div class="text-subtitle1">Usuarios</div>
                  <div class="text-caption">
                    {{ stats.usuarios.activos }} activos
                  </div>
                </div>
                <div class="col-auto">
                  <q-icon name="people" size="3rem" class="opacity-60" />
                </div>
              </div>
            </q-card-section>
            <q-card-section class="bg-white bg-opacity-10">
              <q-btn 
                flat 
                color="white" 
                label="Ver usuarios" 
                icon-right="arrow_forward"
                to="/usuarios"
                class="full-width"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Gráficos y información adicional -->
      <div class="row q-gutter-md">
        <!-- Actividad reciente -->
        <div class="col-12 col-lg-8">
          <q-card class="dashboard-card">
            <q-card-section>
              <div class="text-h6 q-mb-md">
                <q-icon name="timeline" class="q-mr-sm" />
                Actividad Reciente
              </div>
              
              <q-list separator>
                <q-item v-for="(actividad, index) in actividadReciente" :key="index">
                  <q-item-section avatar>
                    <q-avatar :color="actividad.color" text-color="white" size="md">
                      <q-icon :name="actividad.icon" />
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ actividad.titulo }}</q-item-label>
                    <q-item-label caption>{{ actividad.descripcion }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-item-label caption>{{ actividad.tiempo }}</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>

              <div v-if="actividadReciente.length === 0" class="text-center q-py-lg">
                <q-icon name="timeline" size="3em" color="grey-4" />
                <p class="text-grey-5 q-mt-md">No hay actividad reciente</p>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Accesos rápidos -->
        <div class="col-12 col-lg-4">
          <q-card class="dashboard-card">
            <q-card-section>
              <div class="text-h6 q-mb-md">
                <q-icon name="flash_on" class="q-mr-sm" />
                Accesos Rápidos
              </div>
              
              <div class="column q-gutter-sm">
                <q-btn 
                  color="primary" 
                  icon="add" 
                  label="Nuevo Curso"
                  to="/cursos"
                  class="justify-start"
                />
                <q-btn 
                  color="blue" 
                  icon="schedule" 
                  label="Programar Horario"
                  to="/horarios"
                  class="justify-start"
                />
                <q-btn 
                  color="orange" 
                  icon="upload" 
                  label="Subir Material"
                  to="/materiales"
                  class="justify-start"
                />
                <q-btn 
                  color="green" 
                  icon="person_add" 
                  label="Registrar Usuario"
                  to="/usuarios"
                  class="justify-start"
                />
              </div>
            </q-card-section>
          </q-card>

          <!-- Estado del sistema -->
          <q-card class="dashboard-card q-mt-md">
            <q-card-section>
              <div class="text-h6 q-mb-md">
                <q-icon name="settings" class="q-mr-sm" />
                Estado del Sistema
              </div>
              
              <div class="column q-gutter-sm">
                <div class="row items-center">
                  <div class="col">
                    <div class="text-body2">Conexión Django</div>
                  </div>
                  <div class="col-auto">
                    <q-chip color="green" text-color="white" size="sm" icon="check">
                      Conectado
                    </q-chip>
                  </div>
                </div>
                
                <div class="row items-center">
                  <div class="col">
                    <div class="text-body2">Base de Datos</div>
                  </div>
                  <div class="col-auto">
                    <q-chip color="green" text-color="white" size="sm" icon="storage">
                      MySQL
                    </q-chip>
                  </div>
                </div>
                
                <div class="row items-center">
                  <div class="col">
                    <div class="text-body2">Última actualización</div>
                  </div>
                  <div class="col-auto">
                    <div class="text-caption text-grey-6">
                      {{ ultimaActualizacion }}
                    </div>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Distribución por modalidad (gráfico simple) -->
      <div class="row q-gutter-md q-mt-md">
        <div class="col-12">
          <q-card class="dashboard-card">
            <q-card-section>
              <div class="text-h6 q-mb-md">
                <q-icon name="pie_chart" class="q-mr-sm" />
                Distribución de Cursos por Modalidad
              </div>
              
              <div class="row q-gutter-md">
                <div v-for="modalidad in distribucionModalidades" :key="modalidad.nombre" class="col-12 col-md-4">
                  <div class="text-center">
                    <q-circular-progress
                      :value="modalidad.porcentaje"
                      size="100px"
                      :thickness="0.15"
                      :color="modalidad.color"
                      track-color="grey-3"
                      show-value
                      class="q-ma-md"
                    >
                      {{ modalidad.porcentaje }}%
                    </q-circular-progress>
                    <div class="text-subtitle2 text-weight-medium">{{ modalidad.nombre }}</div>
                    <div class="text-caption text-grey-6">{{ modalidad.cantidad }} cursos</div>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { date } from 'quasar'

export default {
  name: 'IndexPage',
  setup() {
    // Estados reactivos
    const loading = ref(true)
    const stats = ref({
      cursos: { total: 0, activos: 0 },
      horarios: { total: 0, esta_semana: 0 },
      materiales: { total: 0, documentos: 0 },
      usuarios: { total: 0, activos: 0 }
    })
    
    const actividadReciente = ref([])
    const distribucionModalidades = ref([])
    const ultimaActualizacion = ref('')

    // Cargar estadísticas desde las APIs
    const loadDashboardData = async () => {
      loading.value = true
      
      try {
        // Cargar estadísticas en paralelo
        const [cursosRes, horariosRes, materialesRes] = await Promise.all([
          api.get('cursos/').catch(() => ({ data: [] })),
          api.get('horarios/').catch(() => ({ data: [] })),
          api.get('materiales/').catch(() => ({ data: [] }))
        ])

        // Procesar datos de cursos
        const cursos = cursosRes.data.results || cursosRes.data || []
        stats.value.cursos = {
          total: cursos.length,
          activos: cursos.filter(c => c.activo).length
        }

        // Calcular distribución por modalidad
        const modalidades = {}
        cursos.forEach(curso => {
          modalidades[curso.modalidad] = (modalidades[curso.modalidad] || 0) + 1
        })

        const colores = { presencial: 'blue', virtual: 'green', mixta: 'orange' }
        const total = cursos.length || 1
        
        distribucionModalidades.value = Object.entries(modalidades).map(([nombre, cantidad]) => ({
          nombre: nombre.charAt(0).toUpperCase() + nombre.slice(1),
          cantidad,
          porcentaje: Math.round((cantidad / total) * 100),
          color: colores[nombre] || 'grey'
        }))

        // Procesar datos de horarios
        const horarios = horariosRes.data.results || horariosRes.data || []
        stats.value.horarios = {
          total: horarios.length,
          esta_semana: horarios.length // Simplificado - podrías filtrar por fecha real
        }

        // Procesar datos de materiales
        const materiales = materialesRes.data.results || materialesRes.data || []
        stats.value.materiales = {
          total: materiales.length,
          documentos: materiales.filter(m => m.tipo_material === 'documento').length
        }

        // Simular datos de usuarios (puedes conectar con la API real)
        stats.value.usuarios = {
          total: 25, // Placeholder
          activos: 23 // Placeholder
        }

        // Simular actividad reciente
        actividadReciente.value = [
          {
            titulo: 'Nuevo curso creado',
            descripcion: cursos.length > 0 ? `Curso "${cursos[0]?.nombre}" agregado` : 'Curso agregado al sistema',
            tiempo: 'Hace 2 horas',
            icon: 'school',
            color: 'blue'
          },
          {
            titulo: 'Material subido',
            descripcion: materiales.length > 0 ? `Material "${materiales[0]?.nombre}" disponible` : 'Nuevo material disponible',
            tiempo: 'Hace 4 horas',
            icon: 'upload',
            color: 'orange'
          },
          {
            titulo: 'Horario programado',
            descripcion: 'Nuevo horario para el curso ADSO',
            tiempo: 'Hace 1 día',
            icon: 'schedule',
            color: 'green'
          }
        ].slice(0, Math.min(3, cursos.length + materiales.length)) // Solo mostrar si hay datos

        ultimaActualizacion.value = date.formatDate(new Date(), 'DD/MM/YYYY HH:mm')

      } catch (error) {
        console.error('Error al cargar datos del dashboard:', error)
      } finally {
        loading.value = false
      }
    }

    // Inicialización
    onMounted(() => {
      console.log('Dashboard montado, cargando datos...')
      loadDashboardData()
    })

    return {
      loading,
      stats,
      actividadReciente,
      distribucionModalidades,
      ultimaActualizacion
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-card {
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.bg-gradient-blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.bg-gradient-green {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.bg-gradient-orange {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.bg-gradient-purple {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.opacity-60 {
  opacity: 0.6;
}

.bg-opacity-10 {
  background-color: rgba(255, 255, 255, 0.1) !important;
}
</style>