<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md">
      <h4>Gestión de Materiales</h4>
      <p class="text-grey-7">Administra los materiales de estudio de los cursos</p>
    </div>

    <!-- Loading inicial -->
    <div v-if="initialLoading" class="text-center q-py-xl">
      <q-spinner color="primary" size="3em" />
      <p class="q-mt-md">Cargando materiales...</p>
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
      <!-- Filtros y estadísticas -->
      <div class="row q-gutter-md q-mb-md">
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
        <div class="col-12 col-md-3">
          <q-select
            v-model="tipoSeleccionado"
            :options="tiposOptions"
            label="Filtrar por tipo"
            outlined
            dense
            clearable
            emit-value
            map-options
            @update:model-value="aplicarFiltros"
          />
        </div>
        <div class="col-12 col-md-3 text-right">
          <q-chip color="info" text-color="white" icon="folder">
            {{ materialesFiltrados.length }} material{{ materialesFiltrados.length !== 1 ? 'es' : '' }}
          </q-chip>
        </div>
        <div class="col-12 col-md-2 text-right">
          <q-btn 
            color="primary" 
            icon="add" 
            label="Nuevo Material" 
            @click="openCreateDialog" 
            :disable="saving"
          />
        </div>
      </div>

      <!-- Grid de materiales -->
      <div class="row q-gutter-md">
        <div v-for="material in materialesFiltrados" :key="material.id" class="col-12 col-md-6 col-lg-4">
          <q-card class="material-card" style="height: 100%">
            <q-card-section class="bg-indigo text-white">
              <div class="row items-center">
                <div class="col">
                  <div class="text-h6">{{ material.nombre }}</div>
                  <div class="text-subtitle2">{{ material.curso_nombre }}</div>
                </div>
                <div class="col-auto">
                  <q-icon :name="getTipoIcon(material.tipo_material)" size="md" />
                </div>
              </div>
            </q-card-section>

            <q-card-section style="flex-grow: 1;">
              <p class="text-grey-7 ellipsis-3-lines">
                {{ material.descripcion || 'Sin descripción' }}
              </p>
              
              <div class="text-caption q-mt-md">
                <q-chip 
                  :color="getTipoColor(material.tipo_material)" 
                  text-color="white" 
                  size="sm"
                  :icon="getTipoIcon(material.tipo_material)"
                >
                  {{ getTipoDisplay(material.tipo_material) }}
                </q-chip>
              </div>

              <!-- Enlaces y archivos -->
              <div class="q-mt-md">
                <div v-if="material.archivo" class="q-mb-sm">
                  <q-btn 
                    flat 
                    color="blue" 
                    icon="download" 
                    label="Descargar archivo"
                    size="sm"
                    @click="downloadFile(material.archivo)"
                  />
                </div>
                <div v-if="material.enlace_externo">
                  <q-btn 
                    flat 
                    color="green" 
                    icon="link" 
                    label="Abrir enlace"
                    size="sm"
                    @click="openLink(material.enlace_externo)"
                  />
                </div>
              </div>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn 
                flat 
                round 
                color="blue" 
                icon="edit" 
                @click="editMaterial(material)"
                :disable="saving"
                size="sm"
              >
                <q-tooltip>Editar material</q-tooltip>
              </q-btn>
              <q-btn 
                flat 
                round 
                color="red" 
                icon="delete" 
                @click="confirmDelete(material)"
                :disable="saving"
                size="sm"
              >
                <q-tooltip>Eliminar material</q-tooltip>
              </q-btn>
            </q-card-actions>
          </q-card>
        </div>
      </div>

      <!-- Estado vacío -->
      <div v-if="materiales.length === 0 && !initialLoading" class="text-center q-py-xl">
        <q-icon name="folder_open" size="6em" color="grey-4" />
        <p class="text-h5 text-grey-5 q-mt-md">No hay materiales registrados</p>
        <p class="text-grey-6">¡Agrega el primer material para comenzar!</p>
        <q-btn 
          color="primary" 
          label="Crear primer material" 
          icon="add"
          @click="openCreateDialog" 
          class="q-mt-md"
        />
      </div>
    </div>

    <!-- Dialog para crear/editar material -->
    <q-dialog 
      v-model="showCreateDialog" 
      persistent 
      :maximized="$q.screen.xs"
    >
      <q-card style="min-width: 600px; max-width: 800px">
        <q-card-section class="bg-indigo text-white">
          <div class="text-h6">
            <q-icon :name="editingMaterial ? 'edit' : 'add'" class="q-mr-sm" />
            {{ editingMaterial ? 'Editar Material' : 'Nuevo Material' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveMaterial" ref="materialFormRef" greedy>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-select
                  v-model="materialForm.curso"
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
              <div class="col-12 col-md-6">
                <q-select
                  v-model="materialForm.tipo_material"
                  :options="tiposOptions"
                  label="Tipo de material *"
                  outlined
                  emit-value
                  map-options
                  :rules="[val => !!val || 'El tipo es obligatorio']"
                  :error="!!formErrors.tipo_material"
                  :error-message="formErrors.tipo_material"
                  @update:model-value="formErrors.tipo_material = ''"
                />
              </div>
            </div>

            <q-input
              v-model="materialForm.nombre"
              label="Nombre del material *"
              outlined
              class="q-mt-md"
              :rules="[val => !!val?.trim() || 'El nombre es obligatorio']"
              :error="!!formErrors.nombre"
              :error-message="formErrors.nombre"
              @input="formErrors.nombre = ''"
            />

            <q-input
              v-model="materialForm.descripcion"
              label="Descripción"
              outlined
              type="textarea"
              rows="3"
              class="q-mt-md"
              counter
              maxlength="500"
            />

            <q-separator class="q-my-md" />
            
            <div class="text-subtitle2 q-mb-md">Contenido del material</div>
            <p class="text-caption text-grey-6 q-mb-md">
              Puedes subir un archivo O proporcionar un enlace externo (o ambos)
            </p>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-file
                  v-model="materialForm.archivo"
                  label="Subir archivo"
                  outlined
                  accept=".pdf,.doc,.docx,.ppt,.pptx,.xlsx,.txt,.zip,.rar"
                  max-file-size="10000000"
                  @rejected="onFileRejected"
                >
                  <template v-slot:prepend>
                    <q-icon name="attach_file" />
                  </template>
                </q-file>
                <div class="text-caption text-grey-6 q-mt-xs">
                  Máximo 10MB. Formatos: PDF, DOC, PPT, Excel, ZIP, etc.
                </div>
              </div>
              
              <div class="col-12 col-md-6">
                <q-input
                  v-model="materialForm.enlace_externo"
                  label="Enlace externo"
                  outlined
                  placeholder="https://ejemplo.com/recurso"
                  type="url"
                  :error="!!formErrors.enlace_externo"
                  :error-message="formErrors.enlace_externo"
                  @input="formErrors.enlace_externo = ''"
                >
                  <template v-slot:prepend>
                    <q-icon name="link" />
                  </template>
                </q-input>
                <div class="text-caption text-grey-6 q-mt-xs">
                  YouTube, Google Drive, sitios web, etc.
                </div>
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
            :label="editingMaterial ? 'Actualizar' : 'Crear'" 
            color="primary" 
            @click="saveMaterial"
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
  name: 'MaterialesPage',
  setup() {
    // Estados reactivos
    const materiales = ref([])
    const cursos = ref([])
    const initialLoading = ref(true)
    const saving = ref(false)
    const connectionError = ref(null)
    const showCreateDialog = ref(false)
    const editingMaterial = ref(null)
    const formErrors = ref({})
    const materialFormRef = ref(null)
    const filtroSeleccionado = ref(null)
    const tipoSeleccionado = ref(null)
    
    // Formulario reactivo
    const materialForm = ref({
      curso: null,
      nombre: '',
      descripcion: '',
      tipo_material: 'documento',
      archivo: null,
      enlace_externo: ''
    })

    const tiposOptions = [
      { label: 'Documento', value: 'documento', icon: 'description', color: 'blue' },
      { label: 'Video', value: 'video', icon: 'play_circle', color: 'red' },
      { label: 'Presentación', value: 'presentacion', icon: 'slideshow', color: 'orange' },
      { label: 'Enlace', value: 'enlace', icon: 'link', color: 'green' },
      { label: 'Imagen', value: 'imagen', icon: 'image', color: 'purple' },
      { label: 'Otro', value: 'otro', icon: 'folder', color: 'grey' }
    ]

    // Opciones computadas
    const cursosOptions = computed(() => {
      return cursos.value.map(curso => ({
        label: `${curso.codigo} - ${curso.nombre}`,
        value: curso.id
      }))
    })

    const materialesFiltrados = computed(() => {
      let filtrados = materiales.value

      if (filtroSeleccionado.value) {
        filtrados = filtrados.filter(m => m.curso === filtroSeleccionado.value)
      }

      if (tipoSeleccionado.value) {
        filtrados = filtrados.filter(m => m.tipo_material === tipoSeleccionado.value)
      }

      return filtrados
    })

    // Métodos principales
    const loadMateriales = async () => {
      try {
        const response = await api.get('materiales/')
        materiales.value = response.data.results || response.data
        console.log(`Materiales cargados: ${materiales.value.length}`)
        connectionError.value = null
      } catch (error) {
        console.error('Error al cargar materiales:', error)
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
        await Promise.all([loadMateriales(), loadCursos()])
      } catch {
        // Errores ya manejados en las funciones individuales
      } finally {
        initialLoading.value = false
      }
    }

    const openCreateDialog = () => {
      editingMaterial.value = null
      materialForm.value = {
        curso: null,
        nombre: '',
        descripcion: '',
        tipo_material: 'documento',
        archivo: null,
        enlace_externo: ''
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const editMaterial = (material) => {
      editingMaterial.value = material
      materialForm.value = {
        curso: material.curso,
        nombre: material.nombre,
        descripcion: material.descripcion,
        tipo_material: material.tipo_material,
        archivo: null, // No pre-cargar archivo existente
        enlace_externo: material.enlace_externo || ''
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const saveMaterial = async () => {
      // Validar formulario
      if (materialFormRef.value) {
        const isValid = await materialFormRef.value.validate()
        if (!isValid) {
          Notify.create({
            type: 'negative',
            message: 'Por favor corrige los errores en el formulario',
            position: 'top'
          })
          return
        }
      }

      // Validar que tenga archivo O enlace
      if (!materialForm.value.archivo && !materialForm.value.enlace_externo?.trim()) {
        Notify.create({
          type: 'negative',
          message: 'Debes proporcionar un archivo o un enlace externo',
          position: 'top'
        })
        return
      }

      formErrors.value = {}
      saving.value = true

      try {
        console.log('Guardando material:', materialForm.value)

        // Preparar FormData para archivos
        const formData = new FormData()
        formData.append('curso', materialForm.value.curso)
        formData.append('nombre', materialForm.value.nombre)
        formData.append('descripcion', materialForm.value.descripcion)
        formData.append('tipo_material', materialForm.value.tipo_material)
        formData.append('enlace_externo', materialForm.value.enlace_externo)
        
        if (materialForm.value.archivo) {
          formData.append('archivo', materialForm.value.archivo)
        }

        let savedMaterial
        if (editingMaterial.value) {
          // Actualización
          const response = await api.put(`materiales/${editingMaterial.value.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          savedMaterial = response.data
          
          // Actualización reactiva inmediata
          const index = materiales.value.findIndex(m => m.id === editingMaterial.value.id)
          if (index !== -1) {
            materiales.value[index] = savedMaterial
          }
          
          closeDialog()
          
          Notify.create({
            type: 'positive',
            message: `Material "${savedMaterial.nombre}" actualizado exitosamente`,
            position: 'top'
          })
        } else {
          // Creación
          const response = await api.post('materiales/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          savedMaterial = response.data
          
          // Agregar inmediatamente a la lista
          materiales.value.unshift(savedMaterial)
          
          closeDialog()
          
          Notify.create({
            type: 'positive',
            message: `Material "${savedMaterial.nombre}" creado exitosamente`,
            position: 'top'
          })
        }

        console.log('Material guardado:', savedMaterial)
        
      } catch (error) {
        console.error('Error al guardar material:', error)
        
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

    const confirmDelete = (material) => {
      Dialog.create({
        title: 'Confirmar eliminación',
        message: `¿Estás seguro de eliminar el material "${material.nombre}"?`,
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
        await deleteMaterial(material)
      })
    }

    const deleteMaterial = async (material) => {
      try {
        await api.delete(`materiales/${material.id}/`)
        
        // Remover inmediatamente de la lista
        materiales.value = materiales.value.filter(m => m.id !== material.id)
        
        Notify.create({
          type: 'positive',
          message: `Material "${material.nombre}" eliminado exitosamente`,
          position: 'top'
        })
        
      } catch (error) {
        console.error('Error al eliminar material:', error)
        
        Notify.create({
          type: 'negative',
          message: 'Error al eliminar el material',
          position: 'top'
        })
      }
    }

    const closeDialog = () => {
      showCreateDialog.value = false
      editingMaterial.value = null
      formErrors.value = {}
    }

    const aplicarFiltros = () => {
      // Los filtros se aplican automáticamente a través de materialesFiltrados computed
    }

    // Funciones auxiliares
    const getTipoIcon = (tipo) => {
      const tipoObj = tiposOptions.find(t => t.value === tipo)
      return tipoObj ? tipoObj.icon : 'folder'
    }

    const getTipoColor = (tipo) => {
      const tipoObj = tiposOptions.find(t => t.value === tipo)
      return tipoObj ? tipoObj.color : 'grey'
    }

    const getTipoDisplay = (tipo) => {
      const tipoObj = tiposOptions.find(t => t.value === tipo)
      return tipoObj ? tipoObj.label : tipo
    }

    const downloadFile = (fileUrl) => {
      window.open(fileUrl, '_blank')
    }

    const openLink = (url) => {
      window.open(url, '_blank')
    }

    const onFileRejected = (rejectedEntries) => {
      Notify.create({
        type: 'negative',
        message: `Archivo rechazado: ${rejectedEntries[0].failedPropValidation}`,
        position: 'top'
      })
    }

    // Inicialización
    onMounted(() => {
      console.log('MaterialesPage montado, inicializando datos...')
      initializeData()
    })

    return {
      // Estados
      materiales,
      cursos,
      initialLoading,
      saving,
      connectionError,
      showCreateDialog,
      editingMaterial,
      materialForm,
      formErrors,
      materialFormRef,
      filtroSeleccionado,
      tipoSeleccionado,
      
      // Opciones
      tiposOptions,
      
      // Computadas
      cursosOptions,
      materialesFiltrados,
      
      // Métodos
      initializeData,
      openCreateDialog,
      editMaterial,
      saveMaterial,
      confirmDelete,
      closeDialog,
      aplicarFiltros,
      getTipoIcon,
      getTipoColor,
      getTipoDisplay,
      downloadFile,
      openLink,
      onFileRejected
    }
  }
}
</script>

<style lang="scss" scoped>
.material-card {
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.ellipsis-3-lines {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 3.6em;
}
</style>