<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md">
      <h4>Gestión de Horarios</h4>
      <p class="text-grey-7">Administra los horarios de los cursos</p>
    </div>

    <!-- Loading inicial -->
    <div v-if="initialLoading" class="text-center q-py-xl">
      <q-spinner color="primary" size="3em" />
      <p class="q-mt-md">Cargando horarios...</p>
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
      <!-- Filtros y acciones -->
      <div class="row q-mb-md items-center">
        <div class="col-12 col-md-4">
          <q-select
            v-model="filtroSeleccionado"
            :options="cursosOptions"
            label="Filtrar por curso"
            outlined
            dense
            clearable
            emit-value
            map-options
            @update:model-value="aplicarFiltros"
          />
        </div>
        <div class="col-12 col-md-4 q-px-md">
          <q-select
            v-model="diaSeleccionado"
            :options="diasOptions"
            label="Filtrar por día"
            outlined
            dense
            clearable
            emit-value
            map-options
            @update:model-value="aplicarFiltros"
          />
        </div>
        <div class="col-12 col-md-4 text-right">
          <q-btn 
            color="primary" 
            icon="add" 
            label="Nuevo Horario" 
            @click="openCreateDialog" 
            :disable="saving"
          />
        </div>
      </div>

      <!-- Tabla de horarios -->
      <q-card>
        <q-card-section>
          <q-table
            :rows="horariosFiltrados"
            :columns="columns"
            row-key="id"
            :loading="initialLoading"
            :pagination="{ rowsPerPage: 10 }"
            binary-state-sort
          >
            <template v-slot:body-cell-curso="props">
              <q-td :props="props">
                <q-chip color="primary" text-color="white" size="sm">
                  {{ props.row.curso_nombre }}
                </q-chip>
              </q-td>
            </template>

            <template v-slot:body-cell-dia_semana="props">
              <q-td :props="props">
                <q-chip color="blue" text-color="white" size="sm">
                  {{ getDiaDisplay(props.row.dia_semana) }}
                </q-chip>
              </q-td>
            </template>

            <template v-slot:body-cell-horario="props">
              <q-td :props="props">
                <div class="text-weight-medium">
                  {{ formatTime(props.row.hora_inicio) }} - {{ formatTime(props.row.hora_fin) }}
                </div>
              </q-td>
            </template>

            <template v-slot:body-cell-acciones="props">
              <q-td :props="props">
                <q-btn 
                  flat 
                  round 
                  color="blue" 
                  icon="edit" 
                  @click="editHorario(props.row)"
                  :disable="saving"
                  size="sm"
                >
                  <q-tooltip>Editar horario</q-tooltip>
                </q-btn>
                <q-btn 
                  flat 
                  round 
                  color="red" 
                  icon="delete" 
                  @click="confirmDelete(props.row)"
                  :disable="saving"
                  size="sm"
                >
                  <q-tooltip>Eliminar horario</q-tooltip>
                </q-btn>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>

      <!-- Estado vacío -->
      <div v-if="horarios.length === 0 && !initialLoading" class="text-center q-py-xl">
        <q-icon name="schedule" size="6em" color="grey-4" />
        <p class="text-h5 text-grey-5 q-mt-md">No hay horarios registrados</p>
        <p class="text-grey-6">¡Crea el primer horario para comenzar!</p>
        <q-btn 
          color="primary" 
          label="Crear primer horario" 
          icon="add"
          @click="openCreateDialog" 
          class="q-mt-md"
        />
      </div>
    </div>

    <!-- Dialog para crear/editar horario -->
    <q-dialog 
      v-model="showCreateDialog" 
      persistent 
      :maximized="$q.screen.xs"
    >
      <q-card style="min-width: 500px; max-width: 600px">
        <q-card-section class="bg-blue text-white">
          <div class="text-h6">
            <q-icon :name="editingHorario ? 'edit' : 'add'" class="q-mr-sm" />
            {{ editingHorario ? 'Editar Horario' : 'Nuevo Horario' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveHorario" ref="horarioFormRef" greedy>
            <div class="row q-gutter-md">
              <div class="col-12">
                <q-select
                  v-model="horarioForm.curso"
                  :options="cursosOptions"
                  label="Curso *"
                  outlined
                  emit-value
                  map-options
                  :rules="[val => !!val || 'El curso es obligatorio']"
                  :error="!!formErrors.curso"
                  :error-message="formErrors.curso"
                  @update:model-value="formErrors.curso = ''"
                />
              </div>
            </div>

            <div class="row q-gutter-md q-mt-md">
              <div class="col-12 col-md-6">
                <q-select
                  v-model="horarioForm.dia_semana"
                  :options="diasOptions"
                  label="Día de la semana *"
                  outlined
                  emit-value
                  map-options
                  :rules="[val => !!val || 'El día es obligatorio']"
                  :error="!!formErrors.dia_semana"
                  :error-message="formErrors.dia_semana"
                  @update:model-value="formErrors.dia_semana = ''"
                />
              </div>
            </div>

            <div class="row q-gutter-md q-mt-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="horarioForm.hora_inicio"
                  label="Hora de inicio *"
                  outlined
                  type="time"
                  :rules="[val => !!val || 'La hora de inicio es obligatoria']"
                  :error="!!formErrors.hora_inicio"
                  :error-message="formErrors.hora_inicio"
                  @input="formErrors.hora_inicio = ''"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="horarioForm.hora_fin"
                  label="Hora de fin *"
                  outlined
                  type="time"
                  :rules="[
                    val => !!val || 'La hora de fin es obligatoria',
                    val => !horarioForm.hora_inicio || val > horarioForm.hora_inicio || 'Debe ser posterior a la hora de inicio'
                  ]"
                  :error="!!formErrors.hora_fin"
                  :error-message="formErrors.hora_fin"
                  @input="formErrors.hora_fin = ''"
                />
              </div>
            </div>

            <div class="row q-gutter-md q-mt-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="horarioForm.aula"
                  label="Aula"
                  outlined
                  placeholder="Ej: Aula 101, Lab A"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="horarioForm.instructor"
                  label="Instructor"
                  outlined
                  placeholder="Nombre del instructor"
                />
              </div>
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
            :label="editingHorario ? 'Actualizar' : 'Crear'" 
            color="primary" 
            @click="saveHorario"
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
  name: 'HorariosPage',
  setup() {
    // Estados reactivos
    const horarios = ref([])
    const cursos = ref([])
    const initialLoading = ref(true)
    const saving = ref(false)
    const connectionError = ref(null)
    const showCreateDialog = ref(false)
    const editingHorario = ref(null)
    const formErrors = ref({})
    const horarioFormRef = ref(null)
    const filtroSeleccionado = ref(null)
    const diaSeleccionado = ref(null)
    
    // Formulario reactivo
    const horarioForm = ref({
      curso: null,
      dia_semana: '',
      hora_inicio: '',
      hora_fin: '',
      aula: '',
      instructor: ''
    })

    const diasOptions = [
      { label: 'Lunes', value: 'lunes' },
      { label: 'Martes', value: 'martes' },
      { label: 'Miércoles', value: 'miercoles' },
      { label: 'Jueves', value: 'jueves' },
      { label: 'Viernes', value: 'viernes' },
      { label: 'Sábado', value: 'sabado' },
      { label: 'Domingo', value: 'domingo' }
    ]

    // Configuración de la tabla
    const columns = [
      { name: 'curso', align: 'left', label: 'Curso', field: 'curso_nombre', sortable: true },
      { name: 'dia_semana', align: 'center', label: 'Día', field: 'dia_semana', sortable: true },
      { name: 'horario', align: 'center', label: 'Horario', sortable: false },
      { name: 'aula', align: 'center', label: 'Aula', field: 'aula', sortable: true },
      { name: 'instructor', align: 'center', label: 'Instructor', field: 'instructor', sortable: true },
      { name: 'acciones', align: 'center', label: 'Acciones', sortable: false }
    ]

    // Opciones computadas
    const cursosOptions = computed(() => {
      return cursos.value.map(curso => ({
        label: `${curso.codigo} - ${curso.nombre}`,
        value: curso.id
      }))
    })

    const horariosFiltrados = computed(() => {
      let filtrados = horarios.value

      if (filtroSeleccionado.value) {
        filtrados = filtrados.filter(h => h.curso === filtroSeleccionado.value)
      }

      if (diaSeleccionado.value) {
        filtrados = filtrados.filter(h => h.dia_semana === diaSeleccionado.value)
      }

      return filtrados
    })

    // Métodos principales
    const loadHorarios = async () => {
      try {
        const response = await api.get('horarios/')
        horarios.value = response.data.results || response.data
        console.log(`Horarios cargados: ${horarios.value.length}`)
        connectionError.value = null
      } catch (error) {
        console.error('Error al cargar horarios:', error)
        connectionError.value = 'Error de conexión. Verifica que Django esté ejecutándose'
        throw error
      }
    }

    const loadCursos = async () => {
      try {
        const response = await api.get('cursos/')
        cursos.value = response.data.results || response.data
        console.log(`Cursos cargados: ${cursos.value.length}`)
      } catch (error) {
        console.error('Error al cargar cursos:', error)
      }
    }

    const initializeData = async () => {
      initialLoading.value = true
      connectionError.value = null
      
      try {
        await Promise.all([loadHorarios(), loadCursos()])
      } catch {
        // Errores ya manejados en las funciones individuales
      } finally {
        initialLoading.value = false
      }
    }

    const openCreateDialog = () => {
      editingHorario.value = null
      horarioForm.value = {
        curso: null,
        dia_semana: '',
        hora_inicio: '',
        hora_fin: '',
        aula: '',
        instructor: ''
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const editHorario = (horario) => {
      editingHorario.value = horario
      horarioForm.value = {
        curso: horario.curso,
        dia_semana: horario.dia_semana,
        hora_inicio: horario.hora_inicio,
        hora_fin: horario.hora_fin,
        aula: horario.aula || '',
        instructor: horario.instructor || ''
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const saveHorario = async () => {
      // Validar formulario
      if (horarioFormRef.value) {
        const isValid = await horarioFormRef.value.validate()
        if (!isValid) {
          Notify.create({
            type: 'negative',
            message: 'Por favor corrige los errores en el formulario',
            position: 'top'
          })
          return
        }
      }

      formErrors.value = {}
      saving.value = true

      try {
        console.log('Guardando horario:', horarioForm.value)

        let savedHorario
        if (editingHorario.value) {
          // Actualización
          const response = await api.put(`horarios/${editingHorario.value.id}/`, horarioForm.value)
          savedHorario = response.data
          
          // Actualización reactiva inmediata
          const index = horarios.value.findIndex(h => h.id === editingHorario.value.id)
          if (index !== -1) {
            horarios.value[index] = savedHorario
          }
          
          closeDialog()
          
          Notify.create({
            type: 'positive',
            message: 'Horario actualizado exitosamente',
            position: 'top'
          })
        } else {
          // Creación
          const response = await api.post('horarios/', horarioForm.value)
          savedHorario = response.data
          
          // Agregar inmediatamente a la lista
          horarios.value.unshift(savedHorario)
          
          closeDialog()
          
          Notify.create({
            type: 'positive',
            message: 'Horario creado exitosamente',
            position: 'top'
          })
        }

        console.log('Horario guardado:', savedHorario)
        
      } catch (error) {
        console.error('Error al guardar horario:', error)
        
        if (error.response?.data) {
          const backendErrors = error.response.data
          
          if (typeof backendErrors === 'object' && !Array.isArray(backendErrors)) {
            formErrors.value = {}
            Object.entries(backendErrors).forEach(([field, messages]) => {
              const messageText = Array.isArray(messages) ? messages.join(', ') : messages
              formErrors.value[field] = messageText
            })
            
            Notify.create({
              type: 'negative',
              message: 'Errores de validación en el formulario',
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

    const confirmDelete = (horario) => {
      Dialog.create({
        title: 'Confirmar eliminación',
        message: `¿Estás seguro de eliminar el horario del ${getDiaDisplay(horario.dia_semana)}?`,
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
        await deleteHorario(horario)
      })
    }

    const deleteHorario = async (horario) => {
      try {
        await api.delete(`horarios/${horario.id}/`)
        
        // Remover inmediatamente de la lista
        horarios.value = horarios.value.filter(h => h.id !== horario.id)
        
        Notify.create({
          type: 'positive',
          message: 'Horario eliminado exitosamente',
          position: 'top'
        })
        
      } catch (error) {
        console.error('Error al eliminar horario:', error)
        
        Notify.create({
          type: 'negative',
          message: 'Error al eliminar el horario',
          position: 'top'
        })
      }
    }

    const closeDialog = () => {
      showCreateDialog.value = false
      editingHorario.value = null
      formErrors.value = {}
    }

    const aplicarFiltros = () => {
      // Los filtros se aplican automáticamente a través de horariosFiltrados computed
    }

    // Funciones auxiliares
    const getDiaDisplay = (dia) => {
      const diaObj = diasOptions.find(d => d.value === dia)
      return diaObj ? diaObj.label : dia
    }

    const formatTime = (time) => {
      if (!time) return ''
      return time.slice(0, 5) // Formato HH:MM
    }

    // Inicialización
    onMounted(() => {
      console.log('HorariosPage montado, inicializando datos...')
      initializeData()
    })

    return {
      // Estados
      horarios,
      cursos,
      initialLoading,
      saving,
      connectionError,
      showCreateDialog,
      editingHorario,
      horarioForm,
      formErrors,
      horarioFormRef,
      filtroSeleccionado,
      diaSeleccionado,
      
      // Opciones
      diasOptions,
      columns,
      
      // Computadas
      cursosOptions,
      horariosFiltrados,
      
      // Métodos
      initializeData,
      openCreateDialog,
      editHorario,
      saveHorario,
      confirmDelete,
      closeDialog,
      aplicarFiltros,
      getDiaDisplay,
      formatTime
    }
  }
}
</script>

<style lang="scss" scoped>
.q-table {
  th {
    font-weight: bold;
  }
}
</style>