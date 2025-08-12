<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md">
      <h4>Gestión de Usuarios</h4>
      <p class="text-grey-7">Administra estudiantes, instructores y personal administrativo</p>
    </div>

    <!-- Loading inicial -->
    <div v-if="initialLoading" class="text-center q-py-xl">
      <q-spinner color="primary" size="3em" />
      <p class="q-mt-md">Cargando usuarios...</p>
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
      <!-- Estadísticas rápidas -->
      <div class="row q-gutter-md q-mb-md">
        <div class="col-md col-sm-6 col-xs-12">
          <q-card class="text-center stats-card">
            <q-card-section>
              <q-icon name="people" size="2em" color="primary" class="q-mb-sm" />
              <div class="text-h4 text-primary">{{ statsComputed.total_usuarios }}</div>
              <div class="text-grey-6">Total Usuarios</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-md col-sm-6 col-xs-12">
          <q-card class="text-center stats-card">
            <q-card-section>
              <q-icon name="check_circle" size="2em" color="green" class="q-mb-sm" />
              <div class="text-h4 text-green">{{ statsComputed.usuarios_activos }}</div>
              <div class="text-grey-6">Usuarios Activos</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-md col-sm-6 col-xs-12">
          <q-card class="text-center stats-card">
            <q-card-section>
              <q-icon name="admin_panel_settings" size="2em" color="orange" class="q-mb-sm" />
              <div class="text-h4 text-orange">{{ statsComputed.administradores }}</div>
              <div class="text-grey-6">Administradores</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Filtros y acciones -->
      <div class="row q-mb-md items-end">
        <div class="col-12 col-md-3">
          <q-input
            v-model="busqueda"
            label="Buscar usuarios"
            outlined
            dense
            clearable
            @input="aplicarFiltros"
            debounce="500"
          >
            <template v-slot:prepend>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
        <div class="col-12 col-md-2 q-px-md">
          <q-select
            v-model="filtroActivo"
            :options="[
              { label: 'Todos', value: null },
              { label: 'Activos', value: true },
              { label: 'Inactivos', value: false }
            ]"
            label="Estado"
            outlined
            dense
            emit-value
            map-options
            @update:model-value="aplicarFiltros"
          />
        </div>
        <div class="col-12 col-md-2">
          <q-select
            v-model="filtroStaff"
            :options="[
              { label: 'Todos', value: null },
              { label: 'Staff', value: true },
              { label: 'Estudiantes', value: false }
            ]"
            label="Tipo"
            outlined
            dense
            emit-value
            map-options
            @update:model-value="aplicarFiltros"
          />
        </div>
        <div class="col-12 col-md-3 text-right">
          <q-chip color="info" text-color="white" icon="info">
            {{ usuariosFiltrados.length }} usuario{{ usuariosFiltrados.length !== 1 ? 's' : '' }}
          </q-chip>
        </div>
        <div class="col-12 col-md-2 text-right">
          <q-btn 
            color="primary" 
            icon="add" 
            label="Nuevo Usuario" 
            @click="openCreateDialog" 
            :disable="saving"
          />
        </div>
      </div>

      <!-- Tabla de usuarios -->
      <q-card>
        <q-card-section>
          <q-table
            :rows="usuariosFiltrados"
            :columns="columns"
            row-key="id"
            :pagination="{ rowsPerPage: 15 }"
            binary-state-sort
          >
            <template v-slot:body-cell-avatar="props">
              <q-td :props="props">
                <q-avatar color="primary" text-color="white" size="md">
                  {{ getInitials(props.row.first_name, props.row.last_name) }}
                </q-avatar>
              </q-td>
            </template>

            <template v-slot:body-cell-nombre_completo="props">
              <q-td :props="props">
                <div class="text-weight-medium">
                  {{ props.row.first_name }} {{ props.row.last_name }}
                </div>
                <div class="text-caption text-grey-6">
                  @{{ props.row.username }}
                </div>
              </q-td>
            </template>

            <template v-slot:body-cell-tipo="props">
              <q-td :props="props">
                <q-chip 
                  :color="props.row.is_superuser ? 'red' : (props.row.is_staff ? 'orange' : 'blue')" 
                  text-color="white" 
                  size="sm"
                >
                  {{ getUserType(props.row) }}
                </q-chip>
              </q-td>
            </template>

            <template v-slot:body-cell-estado="props">
              <q-td :props="props">
                <q-chip 
                  :color="props.row.is_active ? 'green' : 'grey'" 
                  text-color="white" 
                  size="sm"
                  :icon="props.row.is_active ? 'check' : 'pause'"
                >
                  {{ props.row.is_active ? 'Activo' : 'Inactivo' }}
                </q-chip>
              </q-td>
            </template>

            <template v-slot:body-cell-ultimo_acceso="props">
              <q-td :props="props">
                <div v-if="props.row.last_login">
                  {{ formatDate(props.row.last_login) }}
                </div>
                <div v-else class="text-grey-5">
                  Nunca
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
                  @click="editUsuario(props.row)"
                  :disable="saving"
                  size="sm"
                >
                  <q-tooltip>Editar usuario</q-tooltip>
                </q-btn>
                <q-btn 
                  flat 
                  round 
                  :color="props.row.is_active ? 'orange' : 'green'" 
                  :icon="props.row.is_active ? 'pause' : 'play_arrow'"
                  @click="toggleUsuarioEstado(props.row)"
                  :disable="saving"
                  size="sm"
                >
                  <q-tooltip>{{ props.row.is_active ? 'Desactivar' : 'Activar' }}</q-tooltip>
                </q-btn>
                <q-btn 
                  flat 
                  round 
                  color="red" 
                  icon="delete" 
                  @click="confirmDelete(props.row)"
                  :disable="saving || props.row.is_superuser"
                  size="sm"
                >
                  <q-tooltip>{{ props.row.is_superuser ? 'No se puede eliminar superusuario' : 'Eliminar usuario' }}</q-tooltip>
                </q-btn>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>

      <!-- Estado vacío -->
      <div v-if="usuarios.length === 0 && !initialLoading" class="text-center q-py-xl">
        <q-icon name="people_outline" size="6em" color="grey-4" />
        <p class="text-h5 text-grey-5 q-mt-md">No hay usuarios registrados</p>
        <p class="text-grey-6">¡Crea el primer usuario para comenzar!</p>
        <q-btn 
          color="primary" 
          label="Crear primer usuario" 
          icon="add"
          @click="openCreateDialog" 
          class="q-mt-md"
        />
      </div>
    </div>

    <!-- Dialog para crear/editar usuario -->
    <q-dialog 
      v-model="showCreateDialog" 
      persistent 
      :maximized="$q.screen.xs"
    >
      <q-card style="min-width: 600px; max-width: 700px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">
            <q-icon :name="editingUsuario ? 'edit' : 'add'" class="q-mr-sm" />
            {{ editingUsuario ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveUsuario" ref="usuarioFormRef" greedy>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="usuarioForm.username"
                  label="Nombre de usuario *"
                  outlined
                  :rules="[val => !!val?.trim() || 'El nombre de usuario es obligatorio']"
                  :error="!!formErrors.username"
                  :error-message="formErrors.username"
                  @input="formErrors.username = ''"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="usuarioForm.email"
                  label="Correo electrónico *"
                  outlined
                  type="email"
                  :rules="[
                    val => !!val?.trim() || 'El email es obligatorio',
                    val => /.+@.+\..+/.test(val) || 'Email inválido'
                  ]"
                  :error="!!formErrors.email"
                  :error-message="formErrors.email"
                  @input="formErrors.email = ''"
                />
              </div>
            </div>

            <div class="row q-gutter-md q-mt-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="usuarioForm.first_name"
                  label="Nombres *"
                  outlined
                  :rules="[val => !!val?.trim() || 'Los nombres son obligatorios']"
                  :error="!!formErrors.first_name"
                  :error-message="formErrors.first_name"
                  @input="formErrors.first_name = ''"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="usuarioForm.last_name"
                  label="Apellidos *"
                  outlined
                  :rules="[val => !!val?.trim() || 'Los apellidos son obligatorios']"
                  :error="!!formErrors.last_name"
                  :error-message="formErrors.last_name"
                  @input="formErrors.last_name = ''"
                />
              </div>
            </div>

            <q-input
              v-model="usuarioForm.password"
              :label="editingUsuario ? 'Nueva contraseña (dejar vacío para mantener)' : 'Contraseña *'"
              outlined
              type="password"
              class="q-mt-md"
              :rules="editingUsuario ? [] : [val => !!val || 'La contraseña es obligatoria']"
              :error="!!formErrors.password"
              :error-message="formErrors.password"
              @input="formErrors.password = ''"
            />

            <q-separator class="q-my-md" />
            
            <div class="text-subtitle2 q-mb-md">Permisos y estado</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-4">
                <q-toggle
                  v-model="usuarioForm.is_active"
                  label="Usuario activo"
                  color="green"
                />
              </div>
              <div class="col-12 col-md-4">
                <q-toggle
                  v-model="usuarioForm.is_staff"
                  label="Personal (staff)"
                  color="orange"
                />
              </div>
              <div class="col-12 col-md-4">
                <q-toggle
                  v-model="usuarioForm.is_superuser"
                  label="Superusuario"
                  color="red"
                />
              </div>
            </div>

            <div class="text-caption text-grey-6 q-mt-sm">
              <strong>Usuario activo:</strong> Puede acceder al sistema<br>
              <strong>Personal:</strong> Puede acceder al panel de administración<br>
              <strong>Superusuario:</strong> Acceso completo a todo el sistema
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
            :label="editingUsuario ? 'Actualizar' : 'Crear'" 
            color="primary" 
            @click="saveUsuario"
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
import { date } from 'quasar'

export default {
  name: 'UsuariosPage',
  setup() {
    // Estados reactivos
    const usuarios = ref([])
    const initialLoading = ref(true)
    const saving = ref(false)
    const connectionError = ref(null)
    const showCreateDialog = ref(false)
    const editingUsuario = ref(null)
    const formErrors = ref({})
    const usuarioFormRef = ref(null)
    const busqueda = ref('')
    const filtroActivo = ref(null)
    const filtroStaff = ref(null)
    
    // Formulario reactivo
    const usuarioForm = ref({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
      is_active: true,
      is_staff: false,
      is_superuser: false
    })

    // Configuración de la tabla
    const columns = [
      { name: 'avatar', align: 'center', label: '', sortable: false },
      { name: 'nombre_completo', align: 'left', label: 'Usuario', sortable: true },
      { name: 'email', align: 'left', label: 'Email', field: 'email', sortable: true },
      { name: 'tipo', align: 'center', label: 'Tipo', sortable: false },
      { name: 'estado', align: 'center', label: 'Estado', sortable: false },
      { name: 'ultimo_acceso', align: 'center', label: 'Último acceso', field: 'last_login', sortable: true },
      { name: 'acciones', align: 'center', label: 'Acciones', sortable: false }
    ]

    // Estadísticas computadas
    const statsComputed = computed(() => {
      const total = usuarios.value.length
      const activos = usuarios.value.filter(u => u.is_active).length
      const admins = usuarios.value.filter(u => u.is_superuser).length
      
      return {
        total_usuarios: total,
        usuarios_activos: activos,
        administradores: admins
      }
    })

    // Usuarios filtrados
    const usuariosFiltrados = computed(() => {
      let filtrados = usuarios.value

      if (busqueda.value?.trim()) {
        const busq = busqueda.value.toLowerCase()
        filtrados = filtrados.filter(u => 
          u.username.toLowerCase().includes(busq) ||
          u.first_name.toLowerCase().includes(busq) ||
          u.last_name.toLowerCase().includes(busq) ||
          u.email.toLowerCase().includes(busq)
        )
      }

      if (filtroActivo.value !== null) {
        filtrados = filtrados.filter(u => u.is_active === filtroActivo.value)
      }

      if (filtroStaff.value !== null) {
        filtrados = filtrados.filter(u => u.is_staff === filtroStaff.value)
      }

      return filtrados
    })

    // Métodos principales
    const loadUsuarios = async () => {
      try {
        // Usamos el endpoint de usuarios de Django Admin
        const response = await api.get('auth/users/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        usuarios.value = response.data.results || response.data
        console.log(`Usuarios cargados: ${usuarios.value.length}`)
        connectionError.value = null
      } catch (error) {
        console.error('Error al cargar usuarios:', error)
        if (error.response?.status === 401) {
          connectionError.value = 'No tienes permisos para ver usuarios. Inicia sesión como administrador.'
        } else {
          connectionError.value = 'Error de conexión. Verifica que Django esté ejecutándose'
        }
        throw error
      }
    }

    const initializeData = async () => {
      initialLoading.value = true
      connectionError.value = null
      
      try {
        await loadUsuarios()
      } catch {
        // Error ya manejado en loadUsuarios
      } finally {
        initialLoading.value = false
      }
    }

    const openCreateDialog = () => {
      editingUsuario.value = null
      usuarioForm.value = {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        is_active: true,
        is_staff: false,
        is_superuser: false
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const editUsuario = (usuario) => {
      editingUsuario.value = usuario
      usuarioForm.value = {
        username: usuario.username,
        email: usuario.email,
        first_name: usuario.first_name,
        last_name: usuario.last_name,
        password: '', // No pre-llenar contraseña
        is_active: usuario.is_active,
        is_staff: usuario.is_staff,
        is_superuser: usuario.is_superuser
      }
      formErrors.value = {}
      showCreateDialog.value = true
    }

    const saveUsuario = async () => {
      // Validar formulario
      if (usuarioFormRef.value) {
        const isValid = await usuarioFormRef.value.validate()
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
        console.log('Guardando usuario:', usuarioForm.value)

        // Preparar datos (no enviar password vacío en edición)
        const userData = { ...usuarioForm.value }
        if (editingUsuario.value && !userData.password) {
          delete userData.password
        }

        let savedUsuario
        if (editingUsuario.value) {
          // Actualización
          const response = await api.put(`auth/users/${editingUsuario.value.id}/`, userData)
          savedUsuario = response.data
          
          // Actualización reactiva inmediata
          const index = usuarios.value.findIndex(u => u.id === editingUsuario.value.id)
          if (index !== -1) {
            usuarios.value[index] = savedUsuario
          }
          
          closeDialog()
          
          Notify.create({
            type: 'positive',
            message: `Usuario "${savedUsuario.username}" actualizado exitosamente`,
            position: 'top'
          })
        } else {
          // Creación
          const response = await api.post('auth/users/', userData)
          savedUsuario = response.data
          
          // Agregar inmediatamente a la lista
          usuarios.value.unshift(savedUsuario)
          
          closeDialog()
          
          Notify.create({
            type: 'positive',
            message: `Usuario "${savedUsuario.username}" creado exitosamente`,
            position: 'top'
          })
        }

        console.log('Usuario guardado:', savedUsuario)
        
      } catch (error) {
        console.error('Error al guardar usuario:', error)
        
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

    const toggleUsuarioEstado = async (usuario) => {
      try {
        const nuevoEstado = !usuario.is_active
        const response = await api.patch(`auth/users/${usuario.id}/`, {
          is_active: nuevoEstado
        })
        
        // Actualización reactiva inmediata
        const index = usuarios.value.findIndex(u => u.id === usuario.id)
        if (index !== -1) {
          usuarios.value[index] = response.data
        }
        
        Notify.create({
          type: 'positive',
          message: `Usuario ${nuevoEstado ? 'activado' : 'desactivado'} exitosamente`,
          position: 'top'
        })
        
      } catch (error) {
        console.error('Error al cambiar estado:', error)
        Notify.create({
          type: 'negative',
          message: 'Error al cambiar el estado del usuario',
          position: 'top'
        })
      }
    }

    const confirmDelete = (usuario) => {
      Dialog.create({
        title: 'Confirmar eliminación',
        message: `¿Estás seguro de eliminar el usuario "${usuario.username}"? Esta acción no se puede deshacer.`,
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
        await deleteUsuario(usuario)
      })
    }

    const deleteUsuario = async (usuario) => {
      try {
        await api.delete(`auth/users/${usuario.id}/`)
        
        // Remover inmediatamente de la lista
        usuarios.value = usuarios.value.filter(u => u.id !== usuario.id)
        
        Notify.create({
          type: 'positive',
          message: `Usuario "${usuario.username}" eliminado exitosamente`,
          position: 'top'
        })
        
      } catch (error) {
        console.error('Error al eliminar usuario:', error)
        
        Notify.create({
          type: 'negative',
          message: 'Error al eliminar el usuario',
          position: 'top'
        })
      }
    }

    const closeDialog = () => {
      showCreateDialog.value = false
      editingUsuario.value = null
      formErrors.value = {}
    }

    const aplicarFiltros = () => {
      // Los filtros se aplican automáticamente a través de usuariosFiltrados computed
    }

    // Funciones auxiliares
    const getInitials = (firstName, lastName) => {
      const first = firstName?.charAt(0)?.toUpperCase() || ''
      const last = lastName?.charAt(0)?.toUpperCase() || ''
      return first + last || '?'
    }

    const getUserType = (usuario) => {
      if (usuario.is_superuser) return 'Superusuario'
      if (usuario.is_staff) return 'Staff'
      return 'Estudiante'
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return date.formatDate(dateString, 'DD/MM/YYYY HH:mm')
    }

    // Inicialización
    onMounted(() => {
      console.log('UsuariosPage montado, inicializando datos...')
      initializeData()
    })

    return {
      // Estados
      usuarios,
      initialLoading,
      saving,
      connectionError,
      showCreateDialog,
      editingUsuario,
      usuarioForm,
      formErrors,
      usuarioFormRef,
      busqueda,
      filtroActivo,
      filtroStaff,
      
      // Configuración
      columns,
      
      // Computadas
      statsComputed,
      usuariosFiltrados,
      
      // Métodos
      initializeData,
      openCreateDialog,
      editUsuario,
      saveUsuario,
      toggleUsuarioEstado,
      confirmDelete,
      closeDialog,
      aplicarFiltros,
      getInitials,
      getUserType,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.stats-card {
  transition: transform 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
  }
}
</style>