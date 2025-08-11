<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md">
      <h4>Gestión de Cursos</h4>
      <p class="text-grey-7">Conectado con Django REST API - Actualizaciones en tiempo real</p>
    </div>

    <!-- Loading inicial -->
    <div v-if="initialLoading" class="text-center q-py-xl">
      <q-spinner color="primary" size="3em" />
      <p class="q-mt-md">Cargando cursos...</p>
    </div>

    <!-- Error de conexión -->
    <q-banner v-if="connectionError" class="bg-red-1 text-red q-mb-md">
      <template v-slot:avatar>
        <q-icon name="error" color="red" />
      </template>
      {{ connectionError }}
      <template v-slot:action>
        <q-btn flat color="red" label="Reintentar" @click="initializeData" :loading="initialLoading" />
      </template>
    </q-banner>

    <!-- Contenido principal -->
    <div v-if="!initialLoading && !connectionError">
      <!-- Estadísticas en tiempo real -->
      <div class="row q-gutter-md q-mb-md">
        <div class="col-md col-sm-6 col-xs-12">
          <q-card class="text-center stats-card">
            <q-card-section>
              <q-icon name="school" size="2em" color="primary" class="q-mb-sm" />
              <div class="text-h4 text-primary">{{ statsComputed.total_cursos }}</div>
              <div class="text-grey-6">Total Cursos</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-md col-sm-6 col-xs-12">
          <q-card class="text-center stats-card">
            <q-card-section>
              <q-icon name="check_circle" size="2em" color="green" class="q-mb-sm" />
              <div class="text-h4 text-green">{{ statsComputed.cursos_activos }}</div>
              <div class="text-grey-6">Cursos Activos</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-md col-sm-6 col-xs-12">
          <q-card class="text-center stats-card">
            <q-card-section>
              <q-icon name="schedule" size="2em" color="orange" class="q-mb-sm" />
              <div class="text-h4 text-orange">{{ statsComputed.total_horas }}</div>
              <div class="text-grey-6">Horas Totales</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Barra de acciones -->
      <div class="row q-mb-md items-center">
        <div class="col">
          <q-btn 
            color="primary" 
            icon="add" 
            label="Nuevo Curso" 
            @click="openCreateDialog" 
            :disable="saving"
          />
        </div>
        <div class="col-auto">
          <q-chip color="info" text-color="white" icon="info">
            {{ cursos.length }} curso{{ cursos.length !== 1 ? 's' : '' }}
          </q-chip>
        </div>
      </div>

      <!-- Cards de cursos con loading individual -->
      <div class="row q-gutter-md">
        <div v-for="curso in cursos" :key="curso.id" class="col-12 col-md-6 col-lg-4">
          <q-card 
            class="curso-card" 
            :class="{ 'curso-updating': cursosUpdating.includes(curso.id) }"
          >
            <!-- Indicador de actualización -->
            <q-linear-progress 
              v-if="cursosUpdating.includes(curso.id)" 
              indeterminate 
              color="primary" 
            />

            <q-card-section class="bg-primary text-white">
              <div class="text-h6">{{ curso.nombre }}</div>
              <div class="text-subtitle2">{{ curso.codigo }}</div>
            </q-card-section>

            <q-card-section>
              <p class="text-grey-7 ellipsis-2-lines">
                {{ curso.descripcion || 'Sin descripción' }}
              </p>
              <div class="text-caption q-mt-md">
                <div class="row q-gutter-x-md">
                  <div class="col">
                    <q-icon name="schedule" class="q-mr-xs" />
                    <strong>{{ curso.duracion_horas }}h</strong>
                  </div>
                  <div class="col">
                    <q-icon name="location_on" class="q-mr-xs" />
                    <strong>{{ curso.modalidad }}</strong>
                  </div>
                </div>
                <div class="q-mt-sm">
                  <q-chip 
                    :color="curso.activo ? 'green' : 'grey'" 
                    text-color="white" 
                    size="sm"
                    :icon="curso.activo ? 'check' : 'pause'"
                  >
                    {{ curso.activo ? 'Activo' : 'Inactivo' }}
                  </q-chip>
                </div>
              </div>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn 
                flat 
                round 
                color="blue" 
                icon="edit" 
                @click="editCurso(curso)"
                :disable="cursosUpdating.includes(curso.id) || saving"
              >
                <q-tooltip>Editar curso</q-tooltip>
              </q-btn>
              <q-btn 
                flat 
                round 
                color="red" 
                icon="delete" 
                @click="confirmDelete(curso)"
                :disable="cursosUpdating.includes(curso.id) || saving"
              >
                <q-tooltip>Eliminar curso</q-tooltip>
              </q-btn>
            </q-card-actions>
          </q-card>
        </div>
      </div>

      <!-- Estado vacío -->
      <div v-if="cursos.length === 0 && !initialLoading" class="text-center q-py-xl">
        <q-icon name="school" size="6em" color="grey-4" />
        <p class="text-h5 text-grey-5 q-mt-md">No hay cursos registrados</p>
        <p class="text-grey-6">¡Crea tu primer curso para comenzar!</p>
        <q-btn 
          color="primary" 
          label="Crear primer curso" 
          icon="add"
          @click="openCreateDialog" 
          class="q-mt-md"
        />
      </div>
    </div>

    <!-- Dialog para crear/editar curso -->
    <q-dialog 
      v-model="showCreateDialog" 
      persistent 
      :maximized="$q.screen.xs"
    >
      <q-card style="min-width: 500px; max-width: 600px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">
            <q-icon :name="editingCurso ? 'edit' : 'add'" class="q-mr-sm" />
            {{ editingCurso ? 'Editar Curso' : 'Nuevo Curso' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveCurso" ref="cursoFormRef" greedy>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="cursoForm.nombre"
                  label="Nombre del curso *"
                  outlined
                  :rules="[val => !!val?.trim() || 'El nombre es obligatorio']"
                  :error="!!formErrors.nombre"
                  :error-message="formErrors.nombre"
                  @input="formErrors.nombre = ''"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="cursoForm.codigo"
                  label="Código único *"
                  outlined
                  :rules="[val => !!val?.trim() || 'El código es obligatorio']"
                  :error="!!formErrors.codigo"
                  :error-message="formErrors.codigo"
                  @input="formErrors.codigo = ''"
                />
              </div>
            </div>

            <q-input
              v-model="cursoForm.descripcion"
              label="Descripción del curso"
              outlined
              type="textarea"
              rows="3"
              class="q-mt-md"
              counter
              maxlength="500"
            />

            <div class="row q-gutter-md q-mt-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="cursoForm.duracion_horas"
                  label="Duración en horas *"
                  outlined
                  type="number"
                  min="1"
                  max="1000"
                  :rules="[
                    val => !!val || 'La duración es obligatoria',
                    val => val > 0 || 'Debe ser mayor a 0',
                    val => val <= 1000 || 'Máximo 1000 horas'
                  ]"
                  :error="!!formErrors.duracion_horas"
                  :error-message="formErrors.duracion_horas"
                  @input="formErrors.duracion_horas = ''"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-select
                  v-model="cursoForm.modalidad"
                  :options="modalidadOptions"
                  label="Modalidad *"
                  outlined
                  emit-value
                  map-options
                  :rules="[val => !!val || 'La modalidad es obligatoria']"
                />
              </div>
            </div>

            <div class="q-mt-md">
              <q-toggle
                v-model="cursoForm.activo"
                label="Curso activo"
                color="green"
                checked-icon="check"
                unchecked-icon="clear"
              />
            </div>
          </q-form>
        </q-card-section>

        <q-card-actions align="right" class="q-pa-md">
          <q-btn 
            flat 
            label="Cancelar" 
            color="grey" 
            @click="closeDialog"
            :disable="saving"
          />
          <q-btn 
            :label="editingCurso ? 'Actualizar' : 'Crear'" 
            color="primary" 
            @click="saveCurso"
            :loading="saving"
            :disable="saving"
            icon-right="save"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from 'boot/axios'
import { Notify, Dialog } from 'quasar'

export default {
  name: 'CursosPage',
  setup() {
    // Estados reactivos
    const cursos = ref([])
    const initialLoading = ref(true)
    const saving = ref(false)
    const connectionError = ref(null)
    const showCreateDialog = ref(false)
    const editingCurso = ref(null)
    const formErrors = ref({})
    const cursosUpdating = ref([]) // IDs de cursos que se están actualizando
    const cursoFormRef = ref(null)
    
    // Formulario reactivo
    const cursoForm = ref({
      nombre: '',
      codigo: '',
      descripcion: '',
      duracion_horas: null,
      modalidad: 'presencial',
      activo: true
    })

    const modalidadOptions = [
      { label: 'Presencial', value: 'presencial' },
      { label: 'Virtual', value: 'virtual' },
      { label: 'Mixta', value: 'mixta' }
    ]

    // Estadísticas computadas en tiempo real
    const statsComputed = computed(() => {
      const total = cursos.value.length
      const activos = cursos.value.filter(c => c.activo).length
      const horas = cursos.value.reduce((sum, c) => sum + (c.duracion_horas || 0), 0)
      
      return {
        total_cursos: total,
        cursos_activos: activos,
        total_horas: horas
      }
    })

    // Métodos principales
    const loadCursos = async () => {
      try {
        console.log('Cargando cursos...')
        const response = await api.get('cursos/')
        const data = response.data.results || response.data
        
        // Actualización reactiva inmediata
        cursos.value = Array.isArray(data) ? data : []
        console.log(`Cursos cargados: ${cursos.value.length}`)
        
        connectionError.value = null
        return cursos.value
      } catch (error) {
        console.error('Error al cargar cursos:', error)
        connectionError.value = 'Error de conexión. Verifica que Django esté ejecutándose en http://127.0.0.1:8000'
        throw error
      }
    }

    const initializeData = async () => {
      initialLoading.value = true
      connectionError.value = null
      
      try {
        await loadCursos()
      } catch {
        // Error ya manejado en loadCursos
      } finally {
        initialLoading.value = false
      }
    }

    const openCreateDialog = () => {
      editingCurso.value = null
      cursoForm.value = {
        nombre: '',
        codigo: '',
        descripcion: '',
        duracion_horas: null,
        modalidad: 'presencial',
        activo: true
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const editCurso = (curso) => {
      editingCurso.value = curso
      cursoForm.value = {
        nombre: curso.nombre,
        codigo: curso.codigo,
        descripcion: curso.descripcion,
        duracion_horas: curso.duracion_horas,
        modalidad: curso.modalidad,
        activo: curso.activo
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const saveCurso = async () => {
      // Validar formulario
      if (cursoFormRef.value) {
        const isValid = await cursoFormRef.value.validate()
        if (!isValid) {
          Notify.create({
            type: 'negative',
            message: 'Por favor corrige los errores en el formulario',
            position: 'top'
          })
          return
        }
      }

      // Limpiar errores previos
      formErrors.value = {}
      saving.value = true

      try {
        console.log('Guardando curso:', cursoForm.value)

        let savedCurso
        if (editingCurso.value) {
          // Actualización
          const cursoId = editingCurso.value.id
          cursosUpdating.value.push(cursoId)
          
          const response = await api.put(`cursos/${cursoId}/`, cursoForm.value)
          savedCurso = response.data
          
          // Actualización reactiva inmediata
          const index = cursos.value.findIndex(c => c.id === cursoId)
          if (index !== -1) {
            cursos.value[index] = savedCurso
          }
          
          cursosUpdating.value = cursosUpdating.value.filter(id => id !== cursoId)
          
          Notify.create({
            type: 'positive',
            message: `Curso "${savedCurso.nombre}" actualizado exitosamente`,
            position: 'top',
            actions: [{ icon: 'close', color: 'white' }]
          })
        } else {
          // Creación
          const response = await api.post('cursos/', cursoForm.value)
          savedCurso = response.data
          
          // Agregar inmediatamente a la lista
          cursos.value.unshift(savedCurso)
          
          Notify.create({
            type: 'positive',
            message: `Curso "${savedCurso.nombre}" creado exitosamente`,
            position: 'top',
            actions: [{ icon: 'close', color: 'white' }]
          })
        }

        closeDialog()
        console.log('Curso guardado:', savedCurso)
        
      } catch (error) {
        console.error('Error al guardar curso:', error)
        
        // Remover del estado de actualización si hubo error
        if (editingCurso.value) {
          cursosUpdating.value = cursosUpdating.value.filter(id => id !== editingCurso.value.id)
        }
        
        if (error.response?.data) {
          const backendErrors = error.response.data
          
          if (typeof backendErrors === 'object' && !Array.isArray(backendErrors)) {
            // Errores de validación por campo
            formErrors.value = {}
            Object.entries(backendErrors).forEach(([field, messages]) => {
              const messageText = Array.isArray(messages) ? messages.join(', ') : messages
              formErrors.value[field] = messageText
            })
            
            Notify.create({
              type: 'negative',
              message: 'Errores de validación en el formulario',
              caption: 'Revisa los campos marcados en rojo',
              position: 'top'
            })
          } else {
            Notify.create({
              type: 'negative',
              message: `Error del servidor: ${JSON.stringify(backendErrors)}`,
              position: 'top'
            })
          }
        } else {
          Notify.create({
            type: 'negative',
            message: 'Error de conexión. Verifica que Django esté funcionando.',
            position: 'top'
          })
        }
      } finally {
        saving.value = false
      }
    }

    const confirmDelete = (curso) => {
      Dialog.create({
        title: 'Confirmar eliminación',
        message: `¿Estás seguro de que quieres eliminar el curso "${curso.nombre}"?`,
        html: true,
        ok: {
          label: 'Sí, eliminar',
          color: 'negative',
          icon: 'delete'
        },
        cancel: {
          label: 'Cancelar',
          color: 'grey',
          flat: true
        },
        persistent: true
      }).onOk(async () => {
        await deleteCurso(curso)
      })
    }

    const deleteCurso = async (curso) => {
      const cursoId = curso.id
      cursosUpdating.value.push(cursoId)
      
      try {
        await api.delete(`cursos/${cursoId}/`)
        
        // Remover inmediatamente de la lista
        cursos.value = cursos.value.filter(c => c.id !== cursoId)
        
        Notify.create({
          type: 'positive',
          message: `Curso "${curso.nombre}" eliminado exitosamente`,
          position: 'top',
          actions: [{ icon: 'close', color: 'white' }]
        })
        
        console.log('Curso eliminado:', curso.nombre)
        
      } catch (error) {
        console.error('Error al eliminar curso:', error)
        
        Notify.create({
          type: 'negative',
          message: `Error al eliminar el curso "${curso.nombre}"`,
          caption: error.response?.data?.detail || 'Verifica la conexión con el servidor',
          position: 'top'
        })
      } finally {
        cursosUpdating.value = cursosUpdating.value.filter(id => id !== cursoId)
      }
    }

    const closeDialog = () => {
      showCreateDialog.value = false
      editingCurso.value = null
      formErrors.value = {}
    }

    // Inicialización
    onMounted(() => {
      console.log('CursosPage montado, inicializando datos...')
      initializeData()
    })

    return {
      // Estados
      cursos,
      initialLoading,
      saving,
      connectionError,
      showCreateDialog,
      editingCurso,
      cursoForm,
      formErrors,
      cursosUpdating,
      cursoFormRef,
      
      // Opciones
      modalidadOptions,
      
      // Computadas
      statsComputed,
      
      // Métodos
      initializeData,
      openCreateDialog,
      editCurso,
      saveCurso,
      confirmDelete,
      closeDialog
    }
  }
}
</script>

<style lang="scss" scoped>
.curso-card {
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  
  &.curso-updating {
    opacity: 0.7;
  }
}

.stats-card {
  transition: transform 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
  }
}

.ellipsis-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.4em;
}
</style>