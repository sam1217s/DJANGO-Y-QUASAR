import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Configuración de la URL base del backend Django
const api = axios.create({ 
  baseURL: 'http://127.0.0.1:8000/api/',  // URL de tu Django REST API
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para requests - agregar token de autenticación si existe
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para responses - manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      // Redirigir al login si es necesario
    }
    return Promise.reject(error)
  }
)

export default boot(({ app }) => {
  // Para usar como this.$axios y this.$api
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }